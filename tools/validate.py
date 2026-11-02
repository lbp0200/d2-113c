"""校验 mod/ 输出（或 vanilla 基线）的结构完整性。

    python3 -m tools.validate            # 校验 mod/
    python3 -m tools.validate --dir vanilla

设计原则：**只报确定的问题**。D2 的 txt 有很多历史怪癖（重名列、行尾缺列、'-' 当空值），
把怪癖报成错误会让人忽略真正的错误。

检查项：
  1. 表头与基线一致（列名/列数被改动 = 高危，通常是编辑器把表改了）
  2. 行的列数不多于表头（多出来的列几乎一定是编辑事故）
  3. 主键列不重复、不为空
  4. 声明的数值列可以解析成数字
  5. 单元格里出现 Excel 错误值 / 全角空格 / 首尾空白
  6. 换行符与基线一致
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import d2txt
from .d2patch import KEY_COLS

ROOT = Path(__file__).resolve().parent.parent

# 逐表声明"应该是数字"的列；先留空，P1 分析时按需补充。
# 例：NUMERIC_COLS = {"monstats.txt": ["ResFi(H)", "Level", "MinHP"]}
NUMERIC_COLS: dict[str, list[str]] = {}

BAD_TOKENS = ("#REF!", "#N/A", "#VALUE!", "#DIV/0!", "NULL", "None")


def excel_dir(root: Path) -> Path:
    p = root / "data" / "global" / "excel"
    return p if p.is_dir() else root


def validate(target: Path, baseline: Path | None) -> tuple[int, int]:
    errors = 0
    warns = 0
    files = sorted(excel_dir(target).glob("*.txt"))
    if not files:
        print(f"[错误] {target} 下没有 .txt")
        return 1, 0

    def err(msg: str) -> None:
        nonlocal errors
        errors += 1
        print(f"  ✗ {msg}")

    def warn(msg: str) -> None:
        nonlocal warns
        warns += 1
        print(f"  ! {msg}")

    for p in files:
        data = p.read_bytes()
        tf = d2txt.TxtFile.loads(data)
        name = p.name
        label = f"{name}"

        print(f"{label}: {len(tf.rows)} 行 × {len(tf.header)} 列")

        # 1. 表头 vs 基线
        if baseline is not None:
            bp = excel_dir(baseline) / name
            if not bp.exists():
                err(f"{name}: 基线里没有这张表（新增表需要同步更新基线）")
            else:
                base_tf = d2txt.TxtFile.load(bp)
                if base_tf.header != tf.header:
                    err(f"{name}: 表头与基线不一致"
                        f"（基线 {len(base_tf.header)} 列，当前 {len(tf.header)} 列）")
                if len(base_tf.seps) and len(tf.seps):
                    if base_tf.default_sep != tf.default_sep:
                        err(f"{name}: 换行符与基线不一致 {base_tf.default_sep!r} → {tf.default_sep!r}")

        # 2. 超长行
        if (n := tf.long_rows()):
            err(f"{name}: {n} 行的列数多于表头")

        # 3. 主键
        kc = KEY_COLS.get(name)
        if kc:
            ci = tf.find(kc)
            if ci is None:
                warn(f"{name}: 找不到主键列 {kc!r}")
            else:
                seen: dict[str, int] = {}
                for i, row in enumerate(tf.rows):
                    v = tf.get(row, ci)
                    if not v.strip():
                        warn(f"{name}: 第 {i + 2} 行主键为空")
                        continue
                    if v in seen:
                        err(f"{name}: 主键 {v!r} 重复（第 {seen[v] + 2} 行和第 {i + 2} 行）")
                    else:
                        seen[v] = i

        # 4. 数值列
        for col in NUMERIC_COLS.get(name, []):
            ci = tf.find(col)
            if ci is None:
                warn(f"{name}: 声明的数值列 {col!r} 不存在")
                continue
            for i, row in enumerate(tf.rows):
                v = tf.get(row, ci)
                if v.strip() == "" or v.strip() == "-":
                    continue
                if d2txt.to_number(v) is None:
                    err(f"{name}: 第 {i + 2} 行 {col} 不是数字：{v!r}")

        # 5. 脏值
        dirty_bad = dirty_ws = 0
        for row in tf.rows:
            for v in row:
                if any(t in v for t in BAD_TOKENS):
                    dirty_bad += 1
                if v != v.strip():
                    dirty_ws += 1
        if dirty_bad:
            err(f"{name}: {dirty_bad} 个单元格含 Excel 错误值/None")
        if dirty_ws:
            warn(f"{name}: {dirty_ws} 个单元格首尾有空白（D2 会当成不同字符串）")

    return errors, warns


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tools.validate")
    ap.add_argument("--dir", type=Path, default=ROOT / "mod", help="要校验的目录")
    ap.add_argument("--baseline", type=Path, default=ROOT / "vanilla", help="基线目录")
    ap.add_argument("--no-baseline", action="store_true", help="不与基线对比")
    args = ap.parse_args(argv)

    if not excel_dir(args.dir).is_dir():
        print(f"[错误] {args.dir} 不存在（先跑 tools.build）")
        return 1

    errors, warns = validate(args.dir, None if args.no_baseline else args.baseline)
    print(f"\n结果：{errors} 个错误，{warns} 个提醒")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
