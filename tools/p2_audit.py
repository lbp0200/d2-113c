"""P2 审计：**本轮到底改了哪些数字，有没有"没给补偿的削弱"**。

判据 T3 说的是「只加不改，或拿走 A 换给 B」。话说起来容易，做起来容易忘 ——
尤其是"为了平衡"顺手把某个数字调低的时候。

所以这里把 `vanilla/` 和 `mod/` 逐单元格对一遍，把所有**数值下降**单独列出来，
逼着每个下降都能指认出对应的上升（等价交换）。

用法：
    python3 -m tools.p2_audit                # → docs/p2-audit.md
    python3 -m tools.p2_audit --stdout
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from . import d2txt
from .d2patch import KEY_COLS

ROOT = Path(__file__).resolve().parent.parent
EXCEL = Path("data/global/excel")


def as_num(v: str) -> float | None:
    if v is None:
        return None
    v = v.strip()
    if not v:
        return None
    try:
        return float(v)
    except ValueError:
        return None


def keyed(tf: d2txt.TxtFile, key_col: str | None):
    """-> {行键: 行}。没有 key 列就把行号当键。"""
    ci = tf.find(key_col) if key_col else None
    out = {}
    for i, row in enumerate(tf.rows):
        if not row or not any(c.strip() for c in row):
            continue
        k = tf.get(row, ci).strip() if ci is not None else f"#{i + 1}"
        out[k or f"#{i + 1}"] = row
    return out


def audit(vanilla: Path, mod: Path) -> dict:
    files = sorted({p.name for p in (mod / EXCEL).glob("*.txt")})
    tables = {}
    for name in files:
        a = d2txt.TxtFile.load(vanilla / EXCEL / name)
        b = d2txt.TxtFile.load(mod / EXCEL / name)
        if a.header != b.header:
            tables[name] = {"error": "表头不一致"}
            continue
        key_col = KEY_COLS.get(name.lower())
        ra, rb = keyed(a, key_col), keyed(b, key_col)

        up, down, set_changed = [], [], []
        for k, rowb in rb.items():
            rowa = ra.get(k)
            if rowa is None:
                tables.setdefault(name, {}).setdefault("added", []).append(k)
                continue
            for i, col in enumerate(b.header):
                va = a.get(rowa, i)
                vb = b.get(rowb, i)
                if va == vb or col.startswith("*"):
                    continue
                na, nb = as_num(va), as_num(vb)
                if na is not None and nb is not None:
                    (up if nb > na else down).append((k, col, va, vb))
                else:
                    set_changed.append((k, col, va, vb))
        for k in ra:
            if k not in rb:
                tables.setdefault(name, {}).setdefault("removed", []).append(k)

        if up or down or set_changed or name in tables:
            t = tables.setdefault(name, {})
            t["up"] = up
            t["down"] = down
            t["set"] = set_changed
    return tables


def build_report(tables: dict) -> str:
    L: list[str] = []
    add = L.append
    add("# P2 审计：改了哪些数字，有没有没补偿的削弱")
    add("")
    add("> 由 `python3 -m tools.p2_audit` 生成：`vanilla/` 与 `mod/` 逐单元格对比。")
    add("> 判据 T3 要求「只加不改，或拿走 A 换给 B」——所以每一个**数值下降**")
    add("> 都必须能指认出对应的上升/新增。")
    add("")

    total_up = total_down = total_set = total_added = 0
    add("## 总览")
    add("")
    add("| 表 | 数值上升 | 数值下降 | 非数值改动 | 新增行 |")
    add("|---|---:|---:|---:|---:|")
    for name, t in sorted(tables.items()):
        if "error" in t:
            add(f"| {name} | ⚠️ {t['error']} | | | |")
            continue
        up, down = len(t.get("up", [])), len(t.get("down", []))
        st, ad = len(t.get("set", [])), len(t.get("added", []))
        total_up += up
        total_down += down
        total_set += st
        total_added += ad
        add(f"| {name} | {up} | {down} | {st} | {ad} |")
    add(f"| **合计** | **{total_up}** | **{total_down}** | **{total_set}** | **{total_added}** |")
    add("")

    add("## 所有「数值下降」（必须能被解释）")
    add("")
    if total_down == 0:
        add("无。")
    else:
        add("| 表 | 行 | 列 | 前 | 后 |")
        add("|---|---|---|---:|---:|")
        for name, t in sorted(tables.items()):
            for k, col, va, vb in t.get("down", []):
                add(f"| {name} | `{k}` | {col} | {va} | **{vb}** |")
    add("")

    add("## 所有非数值改动（改名/换引用/加行）")
    add("")
    if total_set == 0:
        add("无。")
    else:
        add("| 表 | 行 | 列 | 前 | 后 |")
        add("|---|---|---|---|---|")
        for name, t in sorted(tables.items()):
            for k, col, va, vb in t.get("set", [])[:40]:
                add(f"| {name} | `{k}` | {col} | `{va}` | `{vb}` |")
            n = len(t.get("set", []))
            if n > 40:
                add(f"| {name} | … | 其余 {n - 40} 处 | | |")
    add("")
    if total_added:
        add("新增行：")
        for name, t in sorted(tables.items()):
            for k in t.get("added", []):
                add(f"- {name}：`{k}`")
        add("")
    return "\n".join(L).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tools.p2_audit")
    ap.add_argument("--vanilla", type=Path, default=ROOT / "vanilla")
    ap.add_argument("--mod", type=Path, default=ROOT / "mod")
    ap.add_argument("--out", type=Path, default=ROOT / "docs" / "p2-audit.md")
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args(argv)

    md = build_report(audit(args.vanilla, args.mod))
    if args.stdout:
        print(md)
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(md, encoding="utf-8")
        print(f"→ {args.out}  ({len(md.splitlines())} 行)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
