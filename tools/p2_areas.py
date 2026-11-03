"""P2 只读分析：**区域元素适配度**（"这一系在多少地方打得动"）。

之前这份数据是手算的、只存在于文档里的几个数字，没有工具、算不回去 —— 这是个错误。
本文件把它变成可重跑的东西，并且把**免疫规则**明确写死在代码里。

## 免疫规则（关键，之前算错过）

`passive_*_pierce`（冰掌握/火掌握/电掌握、装备上的"−X% 敌人抗性"）
**不能打破免疫**。1.13 里只有 `Conviction`（信念光环）和 `Lower Resist`（降抗诅咒）
可以，而且对免疫怪只按 1/5 生效。

所以默认规则 `strict`：
    抗性 < 100  → 有效抗性 = 抗性 - 穿透（下限 -100）
    抗性 >= 100 → **保持免疫，伤害为 0**（穿透无效）

`--rule breaking` 是"如果穿透能破免疫"的乐观假设，只用于对比，**不作为结论依据**
（本仓库 `docs/p2-skills-classes.md` 已经写明"冰掌握能否破免疫有争议，普遍认为不能"）。

## 两个指标

- **单点倍率** = `(1 + 伤害%) × (1 - 最终抗性/100)`：跟区域无关，纯数学，任何时候都对
- **区域平均系数** = 区域内所有怪物的单点倍率取平均：回答"这一系在这个区域 handic 多重"

"归零区域"= 平均系数为 0 的区域，也就是**进去就是完全打不动**。

用法：
    python3 -m tools.p2_areas                 # → docs/p2-areas.md（默认 strict 规则）
    python3 -m tools.p2_areas --rule breaking # 对照用
    python3 -m tools.p2_areas --stdout
"""

from __future__ import annotations

import argparse
from pathlib import Path
from statistics import mean

from .d2patch import Ctx
from .p1_immunity import ELEMS, areas, monster_resists

ROOT = Path(__file__).resolve().parent.parent

RES_FLOOR = -100.0
PIERCE = ("strict", "breaking")

# (标签, 元素, 伤害加成%, 穿透%)。数字必须来自 patches/ 里的实际改动，
# 改完补丁要同步这里 —— 这是本文件唯一的"输入"，其余全是算出来的。
PROFILES = [
    ("冰 · 裸抗性（无掌握）", "冰", 0, 0),
    ("冰 · 冰掌握满级", "冰", 0, 115),
    ("火 · 裸抗性（无掌握）", "火", 0, 0),
    ("火 · 无掌握 + 穿透 craft（10/10）", "火", 10, 10),
    ("火 · 无掌握 + 穿透 craft（15/20）", "火", 15, 20),
    ("火 · 法师火掌握（修后）", "火", 100, 45),
    ("电 · 法师电掌握（修前）", "电", 278, 0),
    ("电 · 法师电掌握（修后）", "电", 200, 25),
    ("毒 · 裸抗性（无掌握）", "毒", 0, 0),
    ("毒 · 毒死灵（Lower Resist −70）", "毒", 0, 70),
    ("物理 · 裸抗性", "物理", 0, 0),
    ("魔法 · 祝福之锤", "魔法", 0, 0),
]

RES_POINTS = (0, 50, 75, 90, 99)


def factor(res: float, pierce: float, rule: str = "strict") -> float:
    """一只怪、一个配置的伤害系数。0 = 完全打不动。"""
    if res >= 100:
        if rule == "strict":
            return 0.0
        if pierce >= 5 * (res - 100):
            res = res - pierce / 5
        else:
            return 0.0
    else:
        res = res - pierce
    return 1 - max(RES_FLOOR, res) / 100


def point_mult(dmg: float, pierce: float, res: float, rule: str = "strict") -> float:
    return (1 + dmg / 100) * factor(res, pierce, rule)


def area_stats(ids: list[str], res: dict, elem: str, dmg: float,
               pierce: float, rule: str) -> tuple[float, int] | None:
    """-> (区域平均系数, 该区域内**打不动的怪物个数**)。

    注意第二个值不是"归零区域数"：一个区域只要平均系数 > 0 就不是归零区域。
    之前把这两个概念混用过，所以这里写死在 docstring 里。
    """
    vals = [factor(res[i][elem], pierce, rule) * (1 + dmg / 100)
            for i in ids if i in res]
    if not vals:
        return None
    return mean(vals), sum(1 for v in vals if v == 0)


def _fmt_row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def build_report(rule: str, rules_note: str) -> str:
    base = Ctx(vanilla=ROOT / "vanilla", out=ROOT / "mod")
    patched = Ctx(vanilla=ROOT / "vanilla", out=ROOT / "mod", overlay=ROOT / "mod")

    L: list[str] = []
    add = L.append
    add("# P2 · 区域元素适配度")
    add("")
    add("> 由 `python3 -m tools.p2_areas` 生成。**这是所有「区域平均系数」数字的唯一来源**，")
    add("> 文档里引用这些数字时必须指向本文件，不要再手算。")
    add("")
    add(f"**本次规则：`{rule}`** —— {rules_note}")
    add("")
    add("计算口径：")
    add("")
    add("- 区域来自 `levels.txt`（只算挂了怪的区域），怪物抗性来自 `MonStats.txt` 的地狱列")
    add("- 单点倍率 = `(1 + 伤害%) × (1 - 最终抗性/100)`，抗性下限 −100%")
    add("- 区域平均系数 = 该区域内所有怪物单点倍率的平均；**0 表示进去完全打不动**")
    add("")

    # ---- 表 A：单点倍率（跟规则基本无关，纯数学）
    add("## A · 单点抗性倍率（与区域无关）")
    add("")
    add(_fmt_row(["配置"] + [f"{r}%" for r in RES_POINTS]))
    add("|" + "---|" * (len(RES_POINTS) + 1))
    for label, elem, dmg, pierce in PROFILES:
        add(_fmt_row([label] + [f"{point_mult(dmg, pierce, r, rule):.2f}×"
                                for r in RES_POINTS]))
    add("")

    # ---- 表 B：裸抗性（各元素在怪物抗性分布下的天然表现）
    for ctx, title in ((patched, "打上补丁后"),):
        ms, lv = ctx.load("monstats.txt"), ctx.load("levels.txt")
        res = monster_resists(ms)
        ars = areas(lv)
        add(f"## B · 元素本身的环境系数（{title}，无掌握、无穿透）")
        add("")
        add("| 元素 | 区域平均 | 归零区域 | 最差区域 |")
        add("|---|---:|---:|---|")
        for elem in ("火", "冰", "电", "毒", "物理", "魔法"):
            vals = []
            for _a, name, _l, ids in ars:
                s = area_stats(ids, res, elem, 0, 0, rule)
                if s:
                    vals.append((name, s[0]))
            avg = mean(v for _n, v in vals)
            zero = [n for n, v in vals if v == 0]
            worst = min(vals, key=lambda x: x[1])
            add(f"| {elem} | {avg:.2f} | {len(zero)}/{len(vals)} | "
                f"{worst[0]}（{worst[1]:.2f}） |")
        add("")

        # ---- 表 C：每个配置的区域表现
        add("## C · 各配置的区域平均系数（含穿透）")
        add("")
        add("| 配置 | 区域平均 | 归零区域 |")
        add("|---|---:|---:|")
        for label, elem, dmg, pierce in PROFILES:
            vals = []
            for _a, name, _l, ids in ars:
                s = area_stats(ids, res, elem, dmg, pierce, rule)
                if s:
                    vals.append(s[0])
            add(f"| {label} | {mean(vals):.2f} | {sum(1 for v in vals if v == 0)}/{len(vals)} |")
        add("")

        # ---- 表 D：归零区域清单（透明化）
        add("## D · 完全打不动的区域（按元素）")
        add("")
        add("这些区域里**每一只怪的该元素抗性都 ≥100**，靠 `passive_*_pierce` 破不开，")
        add("只能靠 `Conviction` / `Lower Resist`（且对免疫怪只按 1/5 生效）。")
        add("")
        for elem in ("火", "冰", "电", "毒"):
            zero = []
            for _a, name, _l, ids in ars:
                s = area_stats(ids, res, elem, 0, 0, rule)
                if s and s[0] == 0:
                    zero.append(name)
            add(f"- **{elem}**：{len(zero)} 个 —— " + ("、".join(zero) if zero else "无"))
        add("")

    add("## 结论怎么用")
    add("")
    add("- **`strict` 规则下，穿透类改动永远无法把归零区域变成非零** —— 所以「消除归零区域」")
    add("  这句话只有在 `breaking` 假设下才成立，不能拿来当改动的理由。")
    add("- 穿透的真实价值在 **50~99% 抗性**那一段：把 0.38 拉回 1.05 是实的，")
    add("  把「打不动」变「能打」是虚的（免疫不动）。")
    add("- 想解决归零区域，唯一的杠杆是 `Conviction` / `Lower Resist`（技能层）")
    add("  或降低怪物抗性（但那是提高/降低难度，属于别的议题）。")
    add("")
    return "\n".join(L).rstrip() + "\n"


RULES_NOTE = {
    "strict": "`passive_*_pierce` **不能破免疫**（1.13 只有 Conviction / Lower Resist 可以，"
              "且对免疫怪按 1/5 生效）。这是默认规则，也是结论所依赖的规则。",
    "breaking": "⚠️ 反事实假设：假装 `passive_*_pierce` 能按 1/5 破免疫。"
                "**仅用于对照，不作为任何结论的依据** —— 仓库里的分析认为这个假设不成立。",
}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tools.p2_areas")
    ap.add_argument("--vanilla", type=Path, default=ROOT / "vanilla")
    ap.add_argument("--out", type=Path, default=ROOT / "docs" / "p2-areas.md")
    ap.add_argument("--rule", choices=PIERCE, default="strict")
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args(argv)

    md = build_report(args.rule, RULES_NOTE[args.rule])
    if args.stdout:
        print(md)
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(md, encoding="utf-8")
        print(f"→ {args.out}  ({len(md.splitlines())} 行, rule={args.rule})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
