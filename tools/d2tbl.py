"""D2 字符串表（.tbl）读取器。

格式（1.13c）：
    uint16  两个字节的标记
    uint32  条目数
    uint32  索引表起始偏移
    uint32  字符串区起始偏移
  之后：条目数 × (uint16 序号, uint32 偏移)  —— 偏移相对字符串区
  字符串区：NUL 结尾的字节串

编码不确定（整合版可能是 Big5 / GBK），所以两种都试，取能正常解码的那个。
"""

from __future__ import annotations

import struct
from pathlib import Path

ENCODINGS = ("big5", "gbk", "cp950", "utf-8")


def _decode(raw: bytes) -> str:
    for enc in ENCODINGS:
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1")


def load(path: str | Path) -> dict[str, str]:
    data = Path(path).read_bytes()
    if len(data) < 14:
        return {}
    _mark, count, idx_start, str_start = struct.unpack_from("<HIII", data, 0)
    out: dict[str, str] = {}
    for i in range(count):
        off = idx_start + i * 6
        if off + 6 > len(data):
            break
        _num, s_off = struct.unpack_from("<HI", data, off)
        start = str_start + s_off
        end = data.find(b"\x00", start)
        if end < 0:
            end = len(data)
        key = _decode(data[start:end])
        out[key] = key          # 键就是字符串本身；值留给调用方按序号取
    return out


def entries(path: str | Path) -> list[str]:
    """按序号返回所有字符串（D2 的 tbl 就是"序号 → 字符串"）。"""
    data = Path(path).read_bytes()
    if len(data) < 14:
        return []
    _mark, count, idx_start, str_start = struct.unpack_from("<HIII", data, 0)
    out = []
    for i in range(count):
        off = idx_start + i * 6
        if off + 6 > len(data):
            break
        _num, s_off = struct.unpack_from("<HI", data, off)
        start = str_start + s_off
        end = data.find(b"\x00", start)
        if end < 0:
            end = len(data)
        out.append(_decode(data[start:end]))
    return out
