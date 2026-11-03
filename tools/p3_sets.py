"""P3 只读分析：**套装体检** —— 单件和"穿到第 N 件"分别值不值。

套装和暗金的判据不一样，这一点必须先说清楚：

- 暗金：**单件**要有一个身份（E1）
- 套装：身份可以来自**单件**，也可以来自**"凑到 N 件"的加成**（`Sets.txt` 里的
  `PCode2a/3a/4a/5a` 与 `FCode1` 就是这些）
- 所以套装的问题不是"这件垃圾"，而是**"这套能不能凑、凑到 2 件有没有意义"**

D2 里最常见的"结构性垃圾"就是：**单件弱、2 件加成也弱、还必须凑 4~6 件才像样** ——
那种套装在单机开荒里等于不存在。

## 边界

- `SetItems.txt` 的 `add func` 是"套装加成随件数增长"的函数**编号**，它在硬编码里，
  本工具**不猜**它的具体行为，只在表里标出来
- 触发技能 / 充能 / 光环仍然列为「未量化」
- 单件强度沿用 `tools/p3_items.py` 的 STRONG 阈值（同一把尺子，避免两套标准）

用法：
    python3 -m tools.p3_sets                # → docs/p3-sets.md
    python3 -m tools.p3_sets --stdout
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from . import d2txt
from .p3_items import (EXCEL, NORMALIZE, STRONG, load_bases, load_props,
                       strong_hits)

# 套装"加成"用的是**更严的**尺子：凑 2 件要有真东西，而不是 +75 命中这种填充。
# 收进来的只有：抗性 / 技能 / 吸血吸蓝 / 攻速施法 / 压碎致命撕开 / 生命法力 / 元素穿透 / MF
PARTIAL_REAL = {
    "res": 10, "res-fire": 20, "res-cold": 20, "res-ltng": 20, "res-pois": 20,
    "skills": 1, "skill": 1, "skilltab": 1, "oskill": 1, "free_skill": 1,
    "lifesteal": 3, "manasteal": 3, "ias": 10, "fcr": 10, "fhr": 10,
    "cb": 10, "ds": 10, "ow": 10, "hp": 30, "mana": 50,
    "elem_pierce": 5, "item_magicbonus": 30, "dr": 10,
}
# 只算"纯数值填充"，凑它基本不划算
FILLER = {"ac", "att", "str", "dex", "vit", "enr", "def", "ed_def", "ar",
          "thorns", "regen-mana", "regen", "move2", "move3", "att%",
          "item_goldbonus", "add_dmg", "elem_dmg"}


def partial_hits(stats: dict) -> list[str]:
    return [f"{k}={v:.0f}" for k, v in stats.items()
            if k in PARTIAL_REAL and v >= PARTIAL_REAL[k]]

ROOT = Path(__file__).resolve().parent.parent

# `Sets.txt` 里混着非套装行（Expansion 是版本标记）
NOT_A_SET = {"Expansion"}

# Sets.txt 里的阈位：2/3/4/5 件分别有一到两条 bonus，最后 FCode* 是全套加成
PARTIAL_KEYS = [(n, f"PCode{n}{s}", f"PMin{n}{s}", f"PMax{n}{s}")
                for n in (2, 3, 4, 5) for s in ("a", "b")]
FULL_KEYS = [(1, f"FCode{i}", f"FMin{i}", f"FMax{i}") for i in range(1, 9)]


def resolve(props: dict[str, list[str]], code: str, mx: float) -> list[str]:
    return props.get(code, []) if mx or True else []


def load_sets(props: dict[str, list[str]]) -> dict[str, dict]:
    tf = d2txt.TxtFile.load(str(EXCEL / "Sets.txt"))
    h = tf.header

    def cell(row: list[str], name: str) -> str:
        return row[h.index(name)] if name in h and h.index(name) < len(row) else ""

    def to_float(v: str) -> float:
        n = d2txt.to_number(v)
        return float(n) if n is not None else 0.0

    out: dict[str, dict] = {}
    for row in tf.rows:
        if not row or not row[0]:
            continue
        name = cell(row, "index").strip()
        if name in NOT_A_SET:
            continue
        tiers: dict[int, dict[str, float]] = defaultdict(dict)
        shown: dict[int, list[str]] = defaultdict(list)
        opaque: set[int] = set()
        for n, ccol, cmin, cmax in PARTIAL_KEYS:
            code = cell(row, ccol).strip()
            if not code:
                continue
            v = to_float(cell(row, cmax))
            shown[n].append(f"{code}={cell(row, cmin)}~{cell(row, cmax)}")
            for st in resolve(props, code, v):
                key = NORMALIZE.get(st, st)
                tiers[n][key] = max(tiers[n].get(key, 0.0), v)
            if not props.get(code):
                opaque.add(n)
        for _n, ccol, cmin, cmax in FULL_KEYS:
            code = cell(row, ccol).strip()
            if not code:
                continue
            v = to_float(cell(row, cmax))
            shown[99].append(f"{code}={cell(row, cmin)}~{cell(row, cmax)}")
            for st in resolve(props, code, v):
                key = NORMALIZE.get(st, st)
                tiers[99][key] = max(tiers[99].get(key, 0.0), v)
            if not props.get(code):
                opaque.add(99)
        out[name] = {
            "name": name,
            "level": to_float(cell(row, "level")),
            "tiers": dict(tiers),
            "shown": dict(shown),
            "opaque_tiers": opaque,
            "pieces": [],
        }
    return out


def load_pieces(props: dict[str, list[str]], bases: dict[str, dict]) -> list[dict]:
    tf = d2txt.TxtFile.load(str(EXCEL / "SetItems.txt"))
    h = tf.header

    def cell(row: list[str], name: str) -> str:
        return row[h.index(name)] if name in h and h.index(name) < len(row) else ""

    out = []
    for row in tf.rows:
        if not row or not row[0]:
            continue
        if not cell(row, "set").strip():
            continue                     # 没有归属套装的空行
        code = cell(row, "item").strip().lower()
        base = bases.get(code, {})
        stats: dict[str, float] = {}
        shown: list[str] = []
        opaque = False
        for k in range(1, 10):
            pcode = cell(row, f"prop{k}").strip()
            if not pcode:
                continue
            try:
                v = float(cell(row, f"max{k}") or 0)
            except ValueError:
                v = 0.0
            shown.append(f"{pcode}={cell(row, f'min{k}')}~{cell(row, f'max{k}')}")
            for st in props.get(pcode, []):
                key = NORMALIZE.get(st, st)
                stats[key] = max(stats.get(key, 0.0), v)
            if pcode not in props:
                opaque = True
        out.append({
            "name": cell(row, "index").strip(),
            "set": cell(row, "set").strip(),
            "slot": base.get("type", code or "?"),
            "kind": base.get("kind", "?"),
            "req": float(cell(row, "lvl req") or 0),
            "add_func": cell(row, "add func").strip(),
            "stats": stats,
            "shown": shown,
            "has_opaque": opaque,
            "base_req": base.get("levelreq", 0.0),
        })
    return out


def build_report(sets: dict[str, dict], pieces: list[dict]) -> str:
    by_set: dict[str, list[dict]] = defaultdict(list)
    for p in pieces:
        by_set[p["set"]].append(p)

    L: list[str] = []
    add = L.append
    add("# P3 · 套装体检表")
    add("")
    add("> 由 `python3 -m tools.p3_sets` 生成，**只读**。单件强度沿用 `p3_items` 的同一把尺子。")
    add("")
    add("判据（E1 的套装版）：**每一套要能回答「几件之后值得穿」**。")
    add("三种情况：")
    add("")
    add("- ✅ **单件就有身份**：某件单穿就够强")
    add("- ✅ **凑到 2~3 件有身份**：加成够强，且件数门槛低 —— 这是套装最健康的设计")
    add("- ⚠️ **只有全套才有意义**：单件弱、2/3 件加成也弱 —— 单机开荒里基本等于不存在")
    add("")
    add("> `add func` 是「套装加成随件数增长」的函数编号，行为在硬编码里，本工具不猜。")
    add("")

    rows = []
    for name, st in sorted(sets.items(), key=lambda kv: kv[1]["level"]):
        plist = by_set.get(name, [])
        if not plist:
            continue
        reqs = [p["req"] for p in plist]
        # 单件里最强的
        best_piece = max(plist, key=lambda p: len(strong_hits(p)))
        tier_hits = {n: partial_hits(st["tiers"].get(n, {})) for n in (2, 3, 4, 5, 99)}
        low_tier = bool(tier_hits.get(2) or tier_hits.get(3))
        full = tier_hits.get(99, [])
        piece_ok = bool(strong_hits(best_piece))
        filler = bool(st["tiers"].get(2) or st["tiers"].get(3))

        if piece_ok and low_tier:
            verdict = "✅ 单件够强，凑 2~3 件还有真加成"
        elif piece_ok:
            verdict = "✅ 单件有身份；凑套加成偏低"
        elif low_tier:
            verdict = "✅ 靠 2~3 件加成"
        elif full:
            verdict = "⚠️ 只有全套有意义"
        elif filler:
            verdict = "⚠️ 2~5 件加成全是数值填充"
        else:
            verdict = "⚠️ 加成未量化（触发技能/光环）"

        rows.append((name, st, plist, reqs, best_piece, tier_hits, verdict))

    add("## 总表（按套装等级）")
    add("")
    add("| 套装 | 件数 | 需求 | 部位 | 最强单件 | 2/3 件加成 | 全套加成 | 判定 |")
    add("|---|---:|---:|---|---|---|---|---|")
    for name, st, plist, reqs, best_piece, tier_hits, verdict in rows:
        slots = "、".join(sorted({p["slot"] for p in plist}))
        lo = "/".join(f"{n}件:{'、'.join(tier_hits[n])}" for n in (2, 3) if tier_hits.get(n)) or "—"
        hi = f"{len(tier_hits.get(99, []))}项" if tier_hits.get(99) else "—"
        add(f"| {name} | {len(plist)} | {min(reqs):.0f}~{max(reqs):.0f} | {slots} | "
            f"{best_piece['name']}（{len(strong_hits(best_piece))} 项） | {lo} | {hi} | {verdict} |")
    add("")

    bad = [r for r in rows if r[6].startswith("⚠️")]
    add("## 候选：只有全套才有意义 / 全套也弱")
    add("")
    if bad:
        add("| 套装 | 件数 | 需求 | 2~5 件加成原文 | 为什么可疑 |")
        add("|---|---:|---:|---|---|")
        for name, st, plist, reqs, best_piece, tier_hits, verdict in bad:
            raw = "；".join(f"{n}件: {'、'.join(st['shown'].get(n, []))}"
                           for n in (2, 3, 4, 5) if st["shown"].get(n))
            add(f"| {name} | {len(plist)} | {min(reqs):.0f}~{max(reqs):.0f} | {raw or '—'} | {verdict} |")
    else:
        add("无。")
    add("")

    add("## 单件表（按套装 → 需求等级）")
    add("")
    add("| 件 | 套装 | 部位 | 需求 | 强属性 | 未量化 | 单穿值得吗？ |")
    add("|---|---|---|---:|---|---|---|")
    for name, st, plist, reqs, best_piece, tier_hits, verdict in rows:
        for p in sorted(plist, key=lambda x: x["req"]):
            hits = strong_hits(p)
            add(f"| {p['name']} | {name} | {p['slot']} | {p['req']:.0f} | "
                f"{'、'.join(hits) if hits else '—'} | "
                f"{'是（含触发技能/充能）' if p['has_opaque'] and not hits else '—'} |  |")
    add("")
    return "\n".join(L).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tools.p3_sets")
    ap.add_argument("--out", type=Path, default=ROOT / "docs" / "p3-sets.md")
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args(argv)

    props, _opaque = load_props()
    bases = load_bases()
    sets = load_sets(props)
    pieces = load_pieces(props, bases)
    md = build_report(sets, pieces)
    if args.stdout:
        print(md)
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(md, encoding="utf-8")
        print(f"→ {args.out}  ({len(md.splitlines())} 行)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
