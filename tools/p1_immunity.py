"""P1 只读分析：地狱难度的"免疫墙"。

不修改任何数据，只回答一个问题：**单元素 build 在地狱里有多少地方是死路。**

用法：
    python3 -m tools.p1_immunity                # 输出到 docs/p1-immunity.md
    python3 -m tools.p1_immunity --act 5        # 只看第 5 幕
"""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path

from . import d2txt
from .d2patch import Ctx

ROOT = Path(__file__).resolve().parent.parent

# 元素 -> MonStats 的地狱抗性列
ELEMS = {
    "火": "ResFi(H)",
    "冰": "ResCo(H)",
    "电": "ResLi(H)",
    "毒": "ResPo(H)",
    "物理": "ResDm(H)",
    "魔法": "ResMa(H)",
}

# 抗性 R 要降到 100 以下，需要 -res >= R-100；而对免疫怪 -res 只按 1/5 生效，
# 所以实际需要 5*(R-100) 点降抗。这才是「能不能打」的真正判据。
# 分档按「需要多少点降抗」：50 点 = 单靠信念/无限；100 点 = 信念+降抗诅咒；200 点 = 叠满装备也很勉强。
REQ_TIERS = [(0, "0（本来不免疫）"), (50, "1~50"), (100, "51~100"), (200, "101~200"), (10**9, ">200")]


def req_res(v: float) -> float:
    """把抗性 R 折算成「需要多少点降抗才能破」。"""
    return max(0.0, 5 * (v - 100))


def load(ctx: Ctx):
    ms = ctx.load("monstats.txt")
    lv = ctx.load("levels.txt")
    return ms, lv


def monster_resists(ms: d2txt.TxtFile) -> dict[str, dict[str, float]]:
    i_id = ms.find("Id")
    idx = {e: ms.find(c) for e, c in ELEMS.items()}
    out: dict[str, dict[str, float]] = {}
    for row in ms.rows:
        mid = ms.get(row, i_id).strip()
        if not mid:
            continue
        res = {}
        for e, ci in idx.items():
            v = d2txt.to_number(ms.get(row, ci)) if ci is not None else None
            res[e] = float(v) if v is not None else 0.0
        out[mid] = res
    return out


def areas(lv: d2txt.TxtFile) -> list[tuple[str, str, str, list[str]]]:
    """-> [(act, name, hell_level, [monster ids])]"""
    i_name = lv.find("Name")
    i_act = lv.find("Act")
    i_lvl = lv.find("MonLvl3Ex") or lv.find("MonLvl3")
    mon_cols = [lv.find(f"mon{i}") for i in range(1, 26)]
    mon_cols = [c for c in mon_cols if c is not None]

    out = []
    for row in lv.rows:
        name = lv.get(row, i_name).strip() if i_name is not None else ""
        if not name:
            continue
        # levels.txt 的 Act 列大面积为空且编号不可靠（Barricade 归在 Act 4 下但名字是 Act 5），
        # 所以幕号从 Name 的 "Act N - " 前缀取，这是 1.13c 里最稳的判据。
        m = re.match(r"Act (\d+) - ", name)
        act = m.group(1) if m else (lv.get(row, i_act).strip() if i_act is not None else "")
        if not act:
            continue
        ids = []
        for ci in mon_cols:
            mid = lv.get(row, ci).strip()
            if mid and mid not in ids:
                ids.append(mid)
        if not ids:
            continue
        out.append((act, name, lv.get(row, i_lvl).strip() if i_lvl is not None else "", ids))
    return out


def build_report(ctx: Ctx, act_filter: str | None, budget: float = 100.0) -> str:
    ms, lv = load(ctx)
    res = monster_resists(ms)
    area_list = areas(lv)
    threshold = 100 + budget / 5

    L: list[str] = []
    add = L.append

    add("# P1 · 地狱免疫墙报告")
    add("")
    add("> 由 `tools/p1_immunity.py` 从 `vanilla/` 自动生成。只读分析，不代表任何改动。")
    add("")

    total = len(res)
    add(f"## 总览（{total} 个怪物条目）")
    add("")
    add("| 元素 | 免疫数(>=100) | 占比 | 其中 >100 | 其中 >=200 | 绝对(>=1000) |")
    add("|---|---:|---:|---:|---:|---:|")
    for e in ELEMS:
        vals = [r[e] for r in res.values()]
        imm = sum(1 for v in vals if v >= 100)
        over = sum(1 for v in vals if v > 100)
        hard = sum(1 for v in vals if v >= 200)
        absn = sum(1 for v in vals if v >= 1000)
        add(f"| {e} | {imm} | {imm / total:.0%} | {over} | {hard} | {absn} |")
    add("")

    del L[-1]
    add("")

    add("### 可破性（关键：免疫 ≠ 无解）")
    add("")
    add(f"假设你能凑到 **{budget}** 点降抗（信念/无限 + 降抗诅咒 + 装备），")
    add("对免疫怪按 1/5 生效 → 实际可破上限 = **抗性 " + f"{100 + budget / 5:.0f}" + "**。")
    add("超过这条线的怪，免疫数量再多也不是「难」，而是「无解」。")
    add("")
    add("| 元素 | 免疫(>=100) | 无解(>阈值) | 最高抗性 |")
    add("|---|---:|---:|---:|")
    for e in ELEMS:
        vals = [r[e] for r in res.values()]
        imm = sum(1 for v in vals if v >= 100)
        dead = sum(1 for v in vals if v > threshold)
        add(f"| {e} | {imm} | **{dead}** | {max(vals):.0f} |")
    add("")

    # ------------------------------------------------------------------ 抗性分布
    add("## 抗性值分布")
    add("")
    add("抗性 R 降到 100 以下需要 `-res >= R-100`；对免疫怪降抗只按 1/5 生效，")
    add("所以真正需要的是 `5*(R-100)` 点降抗。这就是「某些免疫打不穿」的数学原因。")
    add("")
    add("| 需要的降抗量 | 火 | 冰 | 电 | 毒 | 物理 | 魔法 |")
    add("|---|---:|---:|---:|---:|---:|---:|")
    for i, (lo, label) in enumerate(REQ_TIERS):
        hi = REQ_TIERS[i + 1][0] if i + 1 < len(REQ_TIERS) else 10**9
        row = [label]
        for e in ELEMS:
            n = sum(1 for r in res.values() if lo <= req_res(r[e]) < hi)
            row.append(str(n))
        add("| " + " | ".join(row) + " |")
    add("")

    # ------------------------------------------------------------------ 区域
    add("## 区域：单元素 build 的死路")
    add("")
    add(f"按幕列出「该区域里**免疫且破不开**（抗性 > {threshold:.0f}）的怪物占比」。")
    add("100% = 纯该元素的 build 在该区域完全无解。")
    add("（只统计 `levels.txt` 里挂在该区域下的怪物，不含随机刷新的精英词缀与特殊事件。）")
    add("")

    acts = sorted({a[0] for a in area_list}, key=lambda x: (len(x), x))
    for act in acts:
        if act_filter and act != act_filter:
            continue
        add(f"### 第 {act} 幕")
        add("")
        add("| 区域 | 地狱等级 | 怪物数 | 火 | 冰 | 电 | 毒 | 物理 | 魔法 |")
        add("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
        for a, name, hlvl, ids in area_list:
            if a != act:
                continue
            pool = [res[m] for m in ids if m in res]
            if not pool:
                continue
            cells = []
            for e in ELEMS:
                n = sum(1 for r in pool if r[e] > threshold)
                pct = n / len(pool)
                cells.append("**100%**" if pct == 1 else (f"{pct:.0%}" if n else "–"))
            add(f"| {name} | {hlvl} | {len(pool)} | " + " | ".join(cells) + " |")
        add("")

    # ------------------------------------------------------------------ 死角汇总
    add(f"## 无解死角（某元素全部怪抗性都 > {threshold:.0f} 的区域）")
    add("")
    for e in ELEMS:
        dead = []
        for a, name, hlvl, ids in area_list:
            pool = [res[m] for m in ids if m in res]
            if pool and all(r[e] > threshold for r in pool):
                dead.append(f"A{a} {name}")
        add(f"- **{e}**：{len(dead)} 个区域 → " + ("、".join(dead) if dead else "无"))
    add("")

    # ------------------------------------------------------------------ 绝对免疫名单
    add(f"## 抗性 > {threshold:.0f} 的怪物（按当前降抗预算 = 无解）")
    add("")
    names = Counter()
    for mid, r in res.items():
        for e in ELEMS:
            if r[e] > threshold:
                names[(mid, e, int(r[e]))] += 1
    for (mid, e, v), _ in sorted(names.items(), key=lambda kv: (-kv[0][2], kv[0][0])):
        add(f"- `{mid}` {e}抗性 {v}")
    add("")

    return "\n".join(L).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tools.p1_immunity")
    ap.add_argument("--vanilla", type=Path, default=ROOT / "vanilla")
    ap.add_argument("--out", type=Path, default=ROOT / "docs" / "p1-immunity.md")
    ap.add_argument("--act", default=None, help="只看某一幕（1-5）")
    ap.add_argument("--res-budget", type=float, default=100.0,
                    help="假设能凑到的降抗点数（默认 100；对免疫怪按 1/5 生效）")
    ap.add_argument("--overlay", type=Path, default=None,
                    help="叠加层目录（如 mod/）：用于量化「打上补丁之后会变成什么样」")
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args(argv)

    ctx = Ctx(vanilla=args.vanilla, out=ROOT / "mod", overlay=args.overlay)
    report = build_report(ctx, args.act, args.res_budget)
    if args.stdout:
        print(report)
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report, encoding="utf-8")
        print(f"→ {args.out}  ({len(report.splitlines())} 行)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
