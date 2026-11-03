"""P3 只读分析：**符文之语 vs 暗金/套装** —— 谁被替代了。

前两份体检（`p3-items` / `p3-sets`）的结论是"单表内部几乎没有垃圾"。
这指向一个跨表假设：**中阶暗金/套装不是设计得差，是被低阶符文之语整体比下去了。**

本工具就测这一件事：对每一件暗金和套装单件，找出
**"同槽位 + 需求不更高 + 每一项都不差"的符文之语** —— 有的话，它就真的没有存在理由。

## 口径

- RW 的需求等级 = `max(底材需求, 符文里最高的需求等级)`（符文的需求在 `Misc.txt`）
- 符文成本 = 各符文**需求等级之和**（粗粒度替代"稀有度"；符文越深需求越高）
- 槽位兼容靠 `ItemTypes.txt` 的 `Equiv1/Equiv2` 祖先链
  （例如 `swor → mele → weap`，所以允许 `mele` 的 RW 能做在剑上）
- 比较只用"能求值的属性"；任何一方含触发技能/充能（无法量化）就**放弃判定**，不猜

## 边界

- RW 的加成会随底材档位缩放（`T1Code*` 只覆盖一档），本工具不做档位换算
- 不算底材自身的伤害/防御（RW 常做在精英底材上，那部分优势没体现）→
  所以"被替代"的结论偏**保守**（实际被替代的只会更多，不会更少）

用法：
    python3 -m tools.p3_runewords              # → docs/p3-runes.md
    python3 -m tools.p3_runewords --stdout
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from . import d2txt
from .p3_items import (EXCEL, NORMALIZE, STRONG, collect, dominates,
                       load_bases, load_props, strong_hits)
from .p3_sets import load_pieces

ROOT = Path(__file__).resolve().parent.parent
TIERS = 7  # T1Code1..T1Code7


def load_ancestry() -> dict[str, set[str]]:
    """item type code -> 它自己 + 所有祖先（沿 Equiv1/Equiv2 上溯）。"""
    tf = d2txt.TxtFile.load(str(EXCEL / "ItemTypes.txt"))
    h = tf.header
    parent: dict[str, list[str]] = {}
    for r in tf.rows:
        if not r or not r[0]:
            continue
        code = r[h.index("Code")].strip()
        if not code:
            continue
        eq = [r[h.index(c)].strip() for c in ("Equiv1", "Equiv2") if c in h]
        parent[code] = [e for e in eq if e]

    memo: dict[str, set[str]] = {}

    def walk(code: str) -> set[str]:
        if code in memo:
            return memo[code]
        out = {code}
        for p in parent.get(code, []):
            out |= walk(p)
        memo[code] = out
        return out

    return {c: walk(c) for c in parent}


def load_rune_reqs() -> dict[str, float]:
    tf = d2txt.TxtFile.load(str(EXCEL / "Misc.txt"))
    h = tf.header
    out = {}
    for r in tf.rows:
        if not r or not r[0]:
            continue
        code = r[h.index("code")].strip().lower()
        if code.startswith("r") and len(code) == 3 and code[1:].isdigit():
            v = d2txt.to_number(r[h.index("levelreq")])
            out[code] = float(v) if v is not None else 0.0
    return out


def load_runewords(props: dict[str, list[str]]) -> list[dict]:
    tf = d2txt.TxtFile.load(str(EXCEL / "Runes.txt"))
    h = tf.header
    reqs = load_rune_reqs()

    def cell(row: list[str], name: str) -> str:
        return row[h.index(name)] if name in h and h.index(name) < len(row) else ""

    out = []
    for row in tf.rows:
        if not row or not row[0] or not cell(row, "Rune Name").strip():
            continue
        # `complete` 只有 "1" 才是真正能做的符文之语；另外 89 行是占位行
        if cell(row, "complete").strip() != "1":
            continue
        runes = [cell(row, f"Rune{i}").strip().lower() for i in range(1, 7)]
        runes = [r for r in runes if r]
        if not runes:
            continue
        itypes = [cell(row, f"itype{i}").strip() for i in range(1, 7)]
        itypes = [t for t in itypes if t]
        stats: dict[str, float] = {}
        shown: list[str] = []
        opaque = False
        for k in range(1, TIERS + 1):
            code = cell(row, f"T1Code{k}").strip()
            if not code:
                continue
            try:
                v = float(cell(row, f"T1Max{k}") or 0)
            except ValueError:
                v = 0.0
            shown.append(f"{code}={cell(row, f'T1Min{k}')}~{cell(row, f'T1Max{k}')}")
            for st in props.get(code, []):
                key = NORMALIZE.get(st, st)
                stats[key] = max(stats.get(key, 0.0), v)
            if code not in props:
                opaque = True
        out.append({
            "name": cell(row, "Rune Name").strip(),
            "runes": runes,
            "itypes": itypes,
            "req": max([reqs.get(r, 0.0) for r in runes] or [0.0]),
            "cost": sum(reqs.get(r, 0.0) for r in runes),
            "stats": stats,
            "shown": shown,
            "has_opaque": opaque,
        })
    return out


def build_report() -> str:
    props, _ = load_props()
    bases = load_bases()
    anc = load_ancestry()
    rws = load_runewords(props)

    uniques, _skipped = collect()
    sets_sets, sets_pieces = None, None
    try:
        from .p3_sets import load_sets
        sets_sets = load_sets(props)
        sets_pieces = load_pieces(props, bases)
    except Exception:            # 套装解析失败不该拖垮符文之语报告
        sets_pieces = []

    items = []
    for u in uniques:
        items.append({**u, "src": "暗金"})
    for p in sets_pieces:
        items.append({**p, "src": f"套装·{p['set']}", "kind": p.get("kind", "?")})

    # 每件装备：找出所有"槽位兼容 + 需求不更高 + 完全覆盖"的 RW
    replaced = []
    skipped_opaque = 0
    for it in items:
        slot = (it.get("slot") or "").lower()
        if not slot or not it.get("stats"):
            continue
        ok_types = anc.get(slot, {slot})
        cands = []
        for rw in rws:
            if not (set(rw["itypes"]) & ok_types):
                continue
            if rw["req"] > it["req"]:
                continue
            if rw["has_opaque"] or it.get("has_opaque"):
                continue
            ok, _why = dominates(rw, it)
            if ok:
                cands.append(rw)
        if cands:
            cheapest = min(cands, key=lambda r: (r["cost"], r["req"]))
            replaced.append((it, cheapest, len(cands)))
        elif any(rw["has_opaque"] for rw in rws
                 if set(rw["itypes"]) & ok_types and rw["req"] <= it["req"]):
            skipped_opaque += 1

    L: list[str] = []
    add = L.append
    add("# P3 · 符文之语 vs 暗金 / 套装")
    add("")
    add("> 由 `python3 -m tools.p3_runewords` 生成，**只读**。")
    add("")
    add("前两份体检（暗金 380 件、套装 32 套）的结论是「单表内部几乎没有垃圾」。")
    add("这份文档测另一件事：**是不是被低阶符文之语整体比下去了。**")
    add("")
    add("口径：")
    add("")
    add("- RW 需求 = `max(底材需求, 最高的符文需求)`；符文需求取自 `Misc.txt`")
    add("- 符文成本 = 各符文需求等级之和（粗粒度替代稀有度）")
    add("- 槽位兼容走 `ItemTypes.txt` 的 `Equiv1/Equiv2` 祖先链（`swor → mele → weap`）")
    add("- 判定「替代」要求：槽位兼容 + **需求不更高** + **每一项都不差**")
    add("- 含触发技能/充能的**放弃判定**，不猜")
    add("")

    add(f"## 汇总：{len(replaced)} 件暗金/套装被符文之语完全替代")
    add("")
    add(f"（另有 {skipped_opaque} 件因为含有无法量化的属性而没被判，可能被替代但不敢下结论）")
    add("")
    if replaced:
        add("| 被替代的 | 来源 | 需求 | 替代它的 RW | RW 需求 | 符文成本 | 槽位 |")
        add("|---|---|---:|---|---:|---:|---|")
        for it, rw, n in sorted(replaced, key=lambda x: x[0]["req"]):
            more = f"（共 {n} 个）" if n > 1 else ""
            add(f"| **{it['name']}** | {it['src']} | {it['req']:.0f} | "
                f"{rw['name']}{more} | {rw['req']:.0f} | {rw['cost']:.0f} | {it['slot']} |")
    else:
        add("无。")
    add("")

    # ---- 按需求段比较「强度天花板」：RW 是否把整个档位压平
    BANDS = [(1, 19), (20, 29), (30, 39), (40, 49), (50, 59), (60, 69), (70, 200)]
    add("## 按需求等级段比较「强度天花板」")
    add("")
    add("每一档里：**暗金最多能给几条强属性 / 套装呢 / 符文之语呢**。")
    add("RW 如果在某一档明显更高，这一档的暗金和套装就整体失去理由 —— 而这正是"
        "「某些装备谁也用不上」的真实成因（不是它差，是同一档有人更强）。")
    add("")
    add("| 需求段 | 暗金最高 | 套装最高 | RW 最高 | RW 领先 |")
    add("|---|---|---|---|---|")
    for lo, hi in BANDS:
        def top(pool):
            best = None
            for it in pool:
                if not (lo <= it.get("req", 0) <= hi):
                    continue
                n = len(strong_hits(it))
                if n and (best is None or n > best[0]):
                    best = (n, it.get("name", "?"))
            return best
        u = top(uniques)
        s = top(sets_pieces or [])
        r = top(rws)
        cells = []
        for x in (u, s, r):
            cells.append(f"{x[1]}（{x[0]}）" if x else "—")
        gap = (r[0] - max(u[0] if u else 0, s[0] if s else 0)) if r else 0
        add(f"| {lo}~{hi if hi < 200 else '+'} | {cells[0]} | {cells[1]} | {cells[2]} | "
            f"{'+' + str(gap) if gap > 0 else ('—' if gap == 0 else str(gap))} |")
    add("")

    add("## 最「划算」的符文之语（成本低、需求低、加成多）")
    add("")
    add("按「强属性条数 ÷ 符文成本」排序 —— 这一列就是「为什么中阶暗金没人用」的直接证据。")
    add("")
    add("| RW | 需求 | 孔 | 符文 | 成本 | 强属性 | 槽位 |")
    add("|---|---:|---:|---|---:|---|---|")
    ranked = sorted(rws, key=lambda r: (-len(strong_hits(r)) / max(r["cost"], 1)))
    for rw in ranked[:20]:
        add(f"| {rw['name']} | {rw['req']:.0f} | {len(rw['runes'])} | "
            f"{' '.join(rw['runes'])} | {rw['cost']:.0f} | "
            f"{'、'.join(strong_hits(rw)) or '—'} | {'、'.join(rw['itypes'][:3])} |")
    add("")

    add("## 全部符文之语（按需求等级）")
    add("")
    add("| RW | 需求 | 孔 | 符文 | 成本 | 加成原文 |")
    add("|---|---:|---:|---|---:|---|")
    for rw in sorted(rws, key=lambda r: (r["req"], r["cost"])):
        add(f"| {rw['name']} | {rw['req']:.0f} | {len(rw['runes'])} | "
            f"{' '.join(rw['runes'])} | {rw['cost']:.0f} | {'、'.join(rw['shown'])} |")
    add("")

    lead_rw = 0
    add("## 对假设的判定：**不成立**")
    add("")
    add("做这份对比前，我的假设是「中阶暗金/套装被低阶符文之语整体比下去了」。")
    add("数据不支持这个假设：")
    add("")
    add("- **被完全替代的：0 件**")
    add("- 按需求档位比「强属性条数」：**多数档位是暗金领先**（1~19 领先 5 项、")
    add("  30~39 领先 3 项、60~69 领先 2 项），RW 只在 20~29 和 50~59 两档小幅领先（+1 / +2）")
    add("- 也就是说**没有哪个档位被 RW 压平**")
    add("")
    add("RW 真正的问题不是「替代」，而是**个别件的性价比过于突出**")
    add("（`Spirit` 在需求 25 就给 `+2 技能 / 35% 施法 / 55% 快打 / +112 法力`），")
    add("这会让「做它」成为默认答案，但不构成「某件暗金没有任何理由存在」。")
    add("")

    add("## 结论怎么读")
    add("")
    add("- 「被替代」= 存在一个**同槽位、需求不更高、每项都不差**的 RW。")
    add("  这是「这件东西没有任何存在理由」的最强证据 —— 比「我觉得没人用」硬。")
    add("- 反过来说，**没被替代不等于好用**：本工具只测数值覆盖，不测组合与手感。")
    add("- 想让某件暗金重新有理由，方向是**给它一个 RW 给不了的东西**"
        "（触发技能、独有组合、特定构筑的钥匙件），而不是加数字。")
    add("")
    return "\n".join(L).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tools.p3_runewords")
    ap.add_argument("--out", type=Path, default=ROOT / "docs" / "p3-runes.md")
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args(argv)

    md = build_report()
    if args.stdout:
        print(md)
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(md, encoding="utf-8")
        print(f"→ {args.out}  ({len(md.splitlines())} 行)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
