"""声明式补丁层：vanilla/ 只读，patches/*.py 用一句话描述一处改动，构建产物落到 mod/。

为什么不用"手改 txt + git diff"：
  - 平衡性改动经常是"所有 >=100 的抗性封顶到 100"这类批量操作，手改必然漏行；
  - 联动改动（技能伤害 + 协同 + 描述）分散在 3 张表，手改难保证一致；
  - 一句 `mul("MinDamage", 1.15)` 比 300 行 txt diff 更容易 review 和回滚。

为什么不用"生成器从零生成 txt"：
  - 100+ 列的表，生成器少写一列就是静默丢数据；
  - 所以这里走 **应用补丁** 路线：从 vanilla 读进来，改单元格，原样写出去。

用法（patches/xxx.py）:
    from tools.d2patch import patch, gt

    patch("monstats.txt", why="地狱元素抗性封顶 100").where("ResFi(H)", gt(100)).clamp("ResFi(H)", hi=100)
    patch("runes.txt", why="单机可用天梯符文之语").all().set("server", "0")
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import wraps
from pathlib import Path
from typing import Callable, Iterable

from . import d2txt
from .d2txt import MissingColumn, format_number, to_number

# 各表的"主键"列，仅用于改动报告里的人类可读定位；找不到就退回行号。
KEY_COLS = {
    "skills.txt": "Skill",
    "skilldesc.txt": "skilldesc",
    "monstats.txt": "Id",
    "monstats2.txt": "Id",
    "monprop.txt": "Id",
    "missiles.txt": "Missile",
    "levels.txt": "Name",
    "uniqueitems.txt": "index",
    "setitems.txt": "index",
    "sets.txt": "index",
    "runes.txt": "Name",
    "treasureclassex.txt": "Treasure Class",
    "cubemain.txt": "description",
    "itemtypes.txt": "ItemType",
    "weapons.txt": "name",
    "armor.txt": "name",
    "misc.txt": "name",
    "properties.txt": "code",
    "itemstatcost.txt": "Stat",
    "charstats.txt": "class",
    "hireling.txt": "Id",
    "pettype.txt": "pet type",
    "difficultylevels.txt": "Name",
    "monlvl.txt": "Level",
    "experience.txt": "Level",
}


# --------------------------------------------------------------------- 谓词


def gt(n):
    def f(v):
        x = to_number(v)
        return x is not None and x > n

    return f


def ge(n):
    def f(v):
        x = to_number(v)
        return x is not None and x >= n

    return f


def lt(n):
    def f(v):
        x = to_number(v)
        return x is not None and x < n


def le(n):
    def f(v):
        x = to_number(v)
        return x is not None and x <= n


def num_eq(n):
    def f(v):
        x = to_number(v)
        return x is not None and x == n

    return f


def eq(s: str):
    return lambda v: v == s


def ne(s: str):
    return lambda v: v != s


def one_of(*vals: str):
    s = set(vals)
    return lambda v: v in s


def matches(pat: str):
    rx = re.compile(pat)
    return lambda v: rx.search(v) is not None


def blank():
    return lambda v: v.strip() == ""


def nonblank():
    return lambda v: v.strip() != ""


def isnum():
    return lambda v: to_number(v) is not None


def not_(p: Callable[[str], bool]):
    return lambda v: not p(v)


# --------------------------------------------------------------------- 上下文


@dataclass
class Change:
    file: str
    row: str
    col: str
    old: str
    new: str
    why: str = ""


@dataclass
class Ctx:
    vanilla: Path
    out: Path
    files: dict[str, d2txt.TxtFile] = field(default_factory=dict)
    original: dict[str, bytes] = field(default_factory=dict)
    changes: list[Change] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    skipped: list[tuple[str, str]] = field(default_factory=list)
    _warned: set[tuple[str, str]] = field(default_factory=set)

    @property
    def excel(self) -> Path:
        """基线 txt 所在目录。支持 vanilla/data/global/excel 与 vanilla 直放两种布局。"""
        p = self.vanilla / "data" / "global" / "excel"
        return p if p.is_dir() else self.vanilla

    @property
    def out_prefix(self) -> Path:
        return Path("data") / "global" / "excel" if self.excel != self.vanilla else Path()

    def out_path(self, name: str) -> Path:
        return self.out / self.out_prefix / name

    def load(self, name: str) -> d2txt.TxtFile:
        if name in self.files:
            return self.files[name]
        p = self.excel / name
        if not p.exists():
            raise SystemExit(
                f"[错误] 找不到 {p}\n"
                f"  → vanilla 基线还没抽取。见 PLAN.md 的 P0：先在 VM 里用 MPQ Editor\n"
                f"    把 data/global/excel/*.txt 抽到 {self.vanilla}/data/global/excel/ 下。"
            )
        data = p.read_bytes()
        tf = d2txt.TxtFile.loads(data)
        self.files[name] = tf
        self.original[name] = data
        return tf

    def warn_once(self, file: str, col: str, msg: str) -> None:
        k = (file, col)
        if k in self._warned:
            return
        self._warned.add(k)
        self.warnings.append(f"{file}:{col} — {msg}")

    def record(self, ch: Change) -> None:
        self.changes.append(ch)

    def changed_files(self) -> dict[str, bytes]:
        """只返回内容真的变了的表。"""
        out = {}
        for name, tf in self.files.items():
            data = tf.dumps()
            if data != self.original.get(name):
                out[name] = data
        return out


_CTX: Ctx | None = None


def use(ctx: Ctx) -> None:
    global _CTX
    _CTX = ctx


def patch(filename: str, why: str = "", *, key: str | None = None, soft: bool = False) -> "Patch":
    """声明一处补丁。

    soft=True：如果列名对不上（版本/拼写差异），只打警告并跳过，不让整个构建失败。
    """
    if _CTX is None:
        raise RuntimeError("patch() 之前必须先调用 use(ctx)")
    return Patch(_CTX, filename, why, key=key, soft=soft)


# --------------------------------------------------------------------- 行选择


def _guarded(fn):
    @wraps(fn)
    def wrapper(self, *a, **kw):
        if self.dead:
            return self
        try:
            return fn(self, *a, **kw)
        except MissingColumn as e:
            if self.patch.soft:
                self.dead = True
                self.patch.ctx.skipped.append((self.patch.filename, f"{self.patch.why} — {e}"))
                return self
            raise SystemExit(
                f"[错误] {self.patch.filename}: {e}\n"
                f"  → 补丁：{self.patch.why}\n"
                f"  → 列名可能拼错，或这个表的版本不是 1.13c。核对后改 patches/ 里的声明。"
            ) from e

    return wrapper


class Selection:
    def __init__(self, patch: "Patch", indices: list[int]):
        self.patch = patch
        self.tf = patch.tf
        self.indices = indices
        self.dead = False
        self.touched = 0

    # ----------------------------------------------------------- 内部工具

    def _key_of(self, i: int) -> str:
        kc = self.patch.key_col
        if kc:
            ci = self.tf.find(kc)
            if ci is not None:
                v = self.tf.get(self.tf.rows[i], ci)
                if v.strip():
                    return v
        return f"#{i + 1}"

    def _write(self, i: int, ci: int, col: str, new) -> None:
        row = self.tf.rows[i]
        old = self.tf.get(row, ci)
        if new is None:
            return
        new = new if isinstance(new, str) else format_number(new)
        if new == old:
            return
        self.tf.put(row, ci, new)
        self.touched += 1
        self.patch.ctx.record(
            Change(self.patch.filename, self._key_of(i), col, old, new, self.patch.why)
        )

    def _each_numeric(self, ci: int, col: str, fn) -> None:
        for i in self.indices:
            old = self.tf.get(self.tf.rows[i], ci)
            x = to_number(old)
            if x is None:
                self.patch.ctx.warn_once(
                    self.patch.filename, col, f"有非数字单元格（如 {old!r}），这些行已跳过"
                )
                continue
            self._write(i, ci, col, fn(x))

    # --------------------------------------------------------------- 操作

    @_guarded
    def set(self, col: str, value):
        """把列 set 成固定值，或者 set 成 old -> new 的函数（返回 None 表示跳过）。"""
        ci = self.tf.need(col)
        for i in self.indices:
            old = self.tf.get(self.tf.rows[i], ci)
            self._write(i, ci, col, value(old) if callable(value) else value)
        return self

    @_guarded
    def add(self, col: str, delta: float):
        ci = self.tf.need(col)
        self._each_numeric(ci, col, lambda x: x + delta)
        return self

    @_guarded
    def mul(self, col: str, factor: float):
        ci = self.tf.need(col)
        self._each_numeric(ci, col, lambda x: x * factor)
        return self

    @_guarded
    def clamp(self, col: str, lo: float | None = None, hi: float | None = None):
        ci = self.tf.need(col)

        def _clamp(x):
            if lo is not None and x < lo:
                return lo
            if hi is not None and x > hi:
                return hi
            return x

        self._each_numeric(ci, col, _clamp)
        return self

    @_guarded
    def swap(self, a: str, b: str):
        """两列互换（少数情况下有用）。"""
        ia, ib = self.tf.need(a), self.tf.need(b)
        for i in list(self.indices):
            va = self.tf.get(self.tf.rows[i], ia)
            vb = self.tf.get(self.tf.rows[i], ib)
            self._write(i, ia, a, vb)
            self._write(i, ib, b, va)
        return self

    def __len__(self) -> int:
        return 0 if self.dead else len(self.indices)


class Patch:
    def __init__(self, ctx: Ctx, filename: str, why: str = "",
                 *, key: str | None = None, soft: bool = False):
        self.ctx = ctx
        self.filename = filename
        self.why = why
        self.soft = soft
        self.tf = ctx.load(filename)
        self.key_col = key or KEY_COLS.get(filename)

    def _select(self, preds) -> Selection:
        rows = self.tf.rows
        idx = []
        for i, row in enumerate(rows):
            ok = True
            for col, cond in preds:
                ci = self.tf.find(col)
                if ci is None:
                    raise MissingColumn(f"没有列 {col!r}（表头末尾 {self.tf.header[-6:]}）")
                if not cond(self.tf.get(row, ci)):
                    ok = False
                    break
            if ok:
                idx.append(i)
        if not idx:
            self.ctx.warnings.append(
                f"{self.filename}: 选择器没匹配到任何行（why={self.why!r}）"
            )
        return Selection(self, idx)

    def all(self) -> Selection:
        return self._select([])

    def where(self, col: str, cond=None) -> Selection:
        """cond 可以是谓词函数，也可以是字符串等值匹配。"""
        if cond is None:
            cond = nonblank()
        elif not callable(cond):
            cond = eq(cond)
        try:
            return self._select([(col, cond)])
        except MissingColumn as e:
            if self.soft:
                self.ctx.skipped.append((self.filename, f"{self.why} — {e}"))
                return Selection(self, [])
            raise SystemExit(f"[错误] {self.filename}: {e}\n  → 补丁：{self.why}") from e

    def only(self, col: str, values: Iterable[str]) -> Selection:
        return self.where(col, one_of(*values))

    def where_all(self, **_) -> Selection:  # 占位：列名带空格/括号，不支持 kwargs
        raise TypeError("列名里常有空格和括号，请用 where(col, cond) / where_cols([...])")

    def where_cols(self, conds: Iterable[tuple[str, object]]) -> Selection:
        prepared = []
        for col, cond in conds:
            if cond is None:
                cond = nonblank()
            elif not callable(cond):
                cond = eq(cond)
            prepared.append((col, cond))
        try:
            return self._select(prepared)
        except MissingColumn as e:
            if self.soft:
                self.ctx.skipped.append((self.filename, f"{self.why} — {e}"))
                return Selection(self, [])
            raise SystemExit(f"[错误] {self.filename}: {e}\n  → 补丁：{self.why}") from e
