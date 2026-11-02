"""D2 1.13c excel .txt 的读写：未改动的字节必须原样回写。

三个必须保留的细节（每条都是踩坑点）：

1. **编码**：用 latin-1 做 bytes <-> str 的一一映射，绝不 strip、绝不规范化空白。
   D2 的解析器对 tab 数量敏感，空格也可能是数据的一部分（字符串键里就带空格）。
2. **列数**：每行的实际列数可以少于表头（D2 允许），必须原样保留，不能补齐。
   补一个空列看起来无害，但会让手工 diff 全部漂移，也掩盖真实错误。
3. **换行**：CRLF / LF 风格、以及"末行有没有换行"，都必须保留。

另外，表头里允许有重名列，所以按名取列时返回下标而不是值。
"""

from __future__ import annotations

import re
from pathlib import Path

_SEP = re.compile(rb"\r\n|\n|\r")


class MissingColumn(KeyError):
    """表里没有这一列（通常是列名拼错，或者版本对不上）。"""


def to_number(s: str):
    """'12' -> 12, '1.5' -> 1.5, ''/'-'/乱码 -> None。"""
    t = s.strip()
    if not t or t == "-":
        return None
    try:
        return int(t)
    except ValueError:
        pass
    try:
        return float(t)
    except ValueError:
        return None


def format_number(v) -> str:
    """把数字写回 txt，尽量不产生 '12.000000001' 这类噪音。"""
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        if v == int(v) and abs(v) < 1e15:
            return str(int(v))
        s = f"{v:.10f}".rstrip("0").rstrip(".")
        return s or "0"
    return str(v)


class TxtFile:
    """一张 D2 数据表。lines[0] 是表头，lines[1:] 是数据行。"""

    def __init__(self, lines: list[list[str]], seps: list[bytes], default_sep: bytes = b"\r\n"):
        self.lines = lines
        self.seps = list(seps)
        self.default_sep = default_sep

    # ------------------------------------------------------------------ 读

    @classmethod
    def loads(cls, data: bytes) -> "TxtFile":
        parts = _SEP.split(data)
        seps = _SEP.findall(data)
        if parts and parts[-1] == b"":
            parts.pop()  # 文件末尾的换行不算"一个空行"
        lines = [[f.decode("latin-1") for f in p.split(b"\t")] for p in parts]
        default = b"\r\n"
        if seps:
            default = max(set(seps), key=seps.count)
        return cls(lines, seps, default)

    @classmethod
    def load(cls, path: str | Path) -> "TxtFile":
        return cls.loads(Path(path).read_bytes())

    # ------------------------------------------------------------------ 写

    def dumps(self) -> bytes:
        n = len(self.lines)
        while len(self.seps) < n - 1:  # 有人直接 append 了 lines，自愈
            self.seps.append(self.default_sep)
        out = bytearray()
        for i, line in enumerate(self.lines):
            out += "\t".join(line).encode("latin-1")
            if i < len(self.seps):
                out += self.seps[i]
        return bytes(out)

    def save(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(self.dumps())

    # ------------------------------------------------------------ 表头访问

    @property
    def header(self) -> list[str]:
        return self.lines[0] if self.lines else []

    @property
    def rows(self) -> list[list[str]]:
        return self.lines[1:]

    def find(self, name: str) -> int | None:
        """按列名找下标。先精确匹配，再唯一的大小写不敏感匹配。"""
        h = self.header
        if name in h:
            return h.index(name)
        low = name.lower()
        cands = [i for i, x in enumerate(h) if x.lower() == low]
        if len(cands) == 1:
            return cands[0]
        return None

    def need(self, name: str) -> int:
        i = self.find(name)
        if i is None:
            raise MissingColumn(
                f"没有列 {name!r}；表头共 {len(self.header)} 列，末尾几列 = {self.header[-6:]}"
            )
        return i

    # ------------------------------------------------------------ 行/单元格

    @staticmethod
    def get(row: list[str], i: int) -> str:
        return row[i] if i < len(row) else ""

    @staticmethod
    def put(row: list[str], i: int, value: str) -> None:
        if i >= len(row):
            row.extend([""] * (i + 1 - len(row)))
        row[i] = value

    def append(self, row: list[str]) -> None:
        had_trailing_newline = len(self.seps) == len(self.lines)
        if not had_trailing_newline:
            self.seps.append(self.default_sep)
        self.lines.append(list(row))
        if had_trailing_newline:
            self.seps.append(self.default_sep)

    def cell(self, row_index: int, col: str) -> str:
        return self.get(self.rows[row_index], self.need(col))

    def short_rows(self) -> int:
        n = len(self.header)
        return sum(1 for r in self.rows if len(r) < n)

    def long_rows(self) -> int:
        n = len(self.header)
        return sum(1 for r in self.rows if len(r) > n)
