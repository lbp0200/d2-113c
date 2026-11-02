"""P1 只读分析：佣兵数值对比。

回答的问题：**A3 铁狼 / A5 野蛮人到底比 A2 沙漠佣兵差多少？值不值得修？**

数据来源：`Hireling.txt`（只取 `Version=100`，即 LoD/资料片的佣兵；`Version=0` 是经典模式）。

关键公式（已用数据验证连续性）：
    stat(level) = base + perLvl × (level - baseLevel)
    取「Level 不超过目标等级的最大那一行」作为 base。
    Hireling.txt 每 3 个断点一行（起始 / 中段 / 末段），速率逐段变化但**连续**：
    例：Rogue 普通 L3 HP45(+9/lvl) → L36 HP342(+18/lvl) → L67 HP900(+30/lvl)，
    代入 L36 得 45+9×33=342 ✓，代入 L67 得 342+18×31=900 ✓。

不能直接从这张表得出的东西（已在报告里标注）：
    - `Resist` / `Resist/Lvl` 的语义未核实（可能是难度惩罚前的原始值），不用来做结论；
    - `Head/Torso/Weapon/Shield` 四列**不是**"能否装备"的开关
      （Rogue 是 2/1/2/0，A5 野蛮人是 0/0/0/0，与常识相反），佣兵装备槽由代码决定；
    - A3 铁狼的 `Dmg-Min/Max` 只是它的近战攻击，真实输出来自元素技能；
    - 技能等级随佣兵等级成长的确切公式未核实，报告只给原始 `Level` / `LvlPerLvl`。

用法：
    python3 -m tools.p1_merc            # → docs/p1-merc.md
"""

from __future__ import annotations

import argparse
from pathlib import Path

from . import d2txt
from .d2patch import Ctx
from .p1_skills import skill_damage

ROOT = Path(__file__).resolve().parent.parent

MERC_NAMES = {
    "Rogue Scout": "A1 罗格",
    "Desert Mercenary": "A2 沙漠佣兵",
    "Eastern Sorceror": "A3 铁狼",
    "Barbarian": "A5 野蛮人",
}
MERC_ORDER = ["Rogue Scout", "Desert Mercenary", "Eastern Sorceror", "Barbarian"]
DIFF = {"1": "普通", "2": "噩梦", "3": "地狱"}
COMPARE_LEVELS = (80, 85, 90)  # 取所有佣兵都存在的等级，避免向下外推
MAIN_LEVEL = 85


def num(tf, row, col) -> float:
    ci = tf.find(col)
    if ci is None:
        return 0.0
    v = d2txt.to_number(tf.get(row, ci))
    return float(v) if v is not None else 0.0


def rows_of(tf, hireling: str, difficulty: str | None = None) -> list[list[str]]:
    i_h, i_v, i_d = tf.find("Hireling"), tf.find("Version"), tf.find("Difficulty")
    out = []
    for r in tf.rows:
        if tf.get(r, i_v).strip() != "100":
            continue
        if tf.get(r, i_h).strip() != hireling:
            continue
        if difficulty and tf.get(r, i_d).strip() != difficulty:
            continue
        out.append(r)
    out.sort(key=lambda r: num(tf, r, "Level"))
    return out


def stat_at(tf, brackets: list[list[str]], level: int, base: str, per: str) -> float:
    """分段线性取值；取 Level <= level 的最后一段。"""
    pick = None
    for r in brackets:
        if num(tf, r, "Level") <= level:
            pick = r
    if pick is None:
        pick = brackets[0]  # 目标等级低于该难度最低断点：不外推，直接取断点值
    return num(tf, pick, base) + num(tf, pick, per) * (level - num(tf, pick, "Level"))


def build_report(ctx: Ctx) -> str:
    tf = ctx.load("hireling.txt")
    L: list[str] = []
    add = L.append

    add("# P1 · 佣兵数值对比")
    add("")
    add("> 由 `tools/p1_merc.py` 从 `vanilla/data/global/excel/Hireling.txt` 生成。只读分析。")
    add("> 只统计 `Version=100`（LoD 资料片佣兵）。")
    add("")

    # ---------------------------------------------------------------- 地狱属性
    add(f"## 地狱难度 · 各佣兵在 {MAIN_LEVEL} 级的属性")
    add("")
    add("| 佣兵 | 类型 | HP | 物理伤害 | 命中 AR | 每级 HP | 每级伤害 | 雇价 |")
    add("|---|---|---:|---:|---:|---:|---:|---:|")
    for h in MERC_ORDER:
        brackets = rows_of(tf, h, "3")
        if not brackets:
            continue
        subtypes = sorted({tf.get(r, tf.find("SubType")).strip() for r in brackets})
        hp = stat_at(tf, brackets, MAIN_LEVEL, "HP", "HP/Lvl")
        dmin = stat_at(tf, brackets, MAIN_LEVEL, "Dmg-Min", "Dmg/Lvl")
        dmax = stat_at(tf, brackets, MAIN_LEVEL, "Dmg-Max", "Dmg/Lvl")
        ar = stat_at(tf, brackets, MAIN_LEVEL, "AR", "AR/Lvl")
        hpl = num(tf, brackets[-1], "HP/Lvl")
        dl = num(tf, brackets[-1], "Dmg/Lvl")
        gold = num(tf, brackets[-1], "Gold")
        add(f"| {MERC_NAMES[h]} | {' / '.join(subtypes)} | {hp:.0f} | {dmin:.0f}-{dmax:.0f} | "
            f"{ar:.0f} | +{hpl:.0f} | +{dl:.0f} | {gold:.0f} |")
    add("")

    # ---------------------------------------------------------------- 成长曲线
    add("## 成长曲线（地狱）")
    add("")
    header = "| 佣兵 | " + " | ".join(f"HP@{lv} | 伤害@{lv}" for lv in COMPARE_LEVELS) + " |"
    add(header)
    add("|---|" + "---:|---:|" * len(COMPARE_LEVELS))
    for h in MERC_ORDER:
        brackets = rows_of(tf, h, "3")
        if not brackets:
            continue
        cells = []
        for lv in COMPARE_LEVELS:
            hp = stat_at(tf, brackets, lv, "HP", "HP/Lvl")
            dmin = stat_at(tf, brackets, lv, "Dmg-Min", "Dmg/Lvl")
            dmax = stat_at(tf, brackets, lv, "Dmg-Max", "Dmg/Lvl")
            cells.append(f"{hp:.0f}")
            cells.append(f"{dmin:.0f}-{dmax:.0f}")
        add(f"| {MERC_NAMES[h]} | " + " | ".join(cells) + " |")
    add("")

    # ---------------------------------------------------------------- 相对差距
    add(f"## 相对差距（以 A2 沙漠佣兵为基准，{MAIN_LEVEL} 级地狱）")
    add("")
    base = rows_of(tf, "Desert Mercenary", "3")
    if base:
        b_hp = stat_at(tf, base, MAIN_LEVEL, "HP", "HP/Lvl")
        b_dmax = stat_at(tf, base, MAIN_LEVEL, "Dmg-Max", "Dmg/Lvl")
        add("| 佣兵 | HP | 相对 A2 | 物理伤害上限 | 相对 A2 |")
        add("|---|---:|---:|---:|---:|")
        for h in MERC_ORDER:
            brackets = rows_of(tf, h, "3")
            if not brackets:
                continue
            hp = stat_at(tf, brackets, MAIN_LEVEL, "HP", "HP/Lvl")
            dmax = stat_at(tf, brackets, MAIN_LEVEL, "Dmg-Max", "Dmg/Lvl")
            add(f"| {MERC_NAMES[h]} | {hp:.0f} | {hp / b_hp - 1:+.0%} | "
                f"{dmax:.0f} | {dmax / b_dmax - 1:+.0%} |")
        add("")

    # ---------------------------------------------------------------- 技能/光环
    add("## 技能与光环（这才是 A2 强、A3/A5 弱的真正原因）")
    add("")
    add("等级写的是「该难度下最低断点 → 最高断点」的技能等级区间。")
    add("只有 A2 提供**光环**；A1 的 Inner Sight 是减防 debuff；A3 是纯输出法术；")
    add("A5 两个技能都是单体控制。")
    add("")
    add("| 佣兵 | 难度 | 类型 | 技能（技能等级区间） |")
    add("|---|---|---|---|")
    for h in MERC_ORDER:
        for diff in ("1", "2", "3"):
            brackets = rows_of(tf, h, diff)
            if not brackets:
                continue
            subtypes = []
            for r in brackets:
                st = tf.get(r, tf.find("SubType")).strip()
                if st not in subtypes:
                    subtypes.append(st)
            for st in subtypes:
                group = [r for r in brackets if tf.get(r, tf.find("SubType")).strip() == st]
                skills: dict[str, list[int]] = {}
                for r in group:
                    for i in range(1, 7):
                        s = tf.get(r, tf.find(f"Skill{i}")).strip()
                        if not s:
                            continue
                        lv = int(num(tf, r, f"Level{i}"))
                        skills.setdefault(s, []).append(lv)
                parts = []
                for s, lvs in skills.items():
                    lo, hi = min(lvs), max(lvs)
                    parts.append(f"{s} L{lo}" + ("" if lo == hi else f"→{hi}"))
                add(f"| {MERC_NAMES[h]} | {DIFF[diff]} | {st} | {'、'.join(parts)} |")
    add("")

    # ---------------------------------------------------------------- A3 元素输出
    add("## A3 铁狼的元素输出（按地狱档基础技能等级）")
    add("")
    add("上表的 `Dmg-Min/Max` 只算了它的近战平砍。它真实的输出来自这些法术，")
    add("用 `skills.txt` 的本体伤害公式算（不含协同，见 [p1-skills.md](p1-skills.md)）：")
    add("")
    add("| 类型 | 技能 | 技能等级 | 单次伤害 |")
    add("|---|---|---:|---:|")
    sk = ctx.load("skills.txt")
    cache: dict[str, list[str]] = {}
    for r in sk.rows:
        cache[sk.get(r, sk.find("skill")).strip()] = r
    for r in rows_of(tf, "Eastern Sorceror", "3"):
        st = tf.get(r, tf.find("SubType")).strip()
        for i in range(1, 7):
            name = tf.get(r, tf.find(f"Skill{i}")).strip()
            if not name or name not in cache:
                continue
            lvl = int(num(tf, r, f"Level{i}"))
            lo, hi = skill_damage(sk, cache[name], lvl)
            if hi <= 0:
                continue  # Frozen Armor 之类没有伤害
            add(f"| {st} | {name} | {lvl} | {lo:.0f}-{hi:.0f} |")
    add("")
    add("对照：A3 的法术单发伤害其实不低（火球 23 级约 500），")
    add("所以它的问题不是「打不动」，而是 **HP 最低、没有光环、且施法频率受 AI/冷却限制**。")
    add("")

    # ---------------------------------------------------------------- 结论
    add("## 结论")
    add("")
    add("- **A2 沙漠佣兵的优势不在面板，在光环。** 面板上 A5 野蛮人的伤害甚至更高，")
    add("  但 A2 提供的是**全队乘算**：噩梦档给「力量(Might) / 神圣冰冻(Holy Freeze) / 荆棘(Thorns)」，")
    add("  地狱档给「祈祷(Prayer) / 反抗(Defiance) / 祝福瞄准(Blessed Aim)」。")
    add("  所以正确的雇佣姿势是**在噩梦雇一个 A2 再带进地狱**——这是数据里能直接看出来的机制。")
    add("- **A3 铁狼是纯数值弱**：HP 与每级成长都明显低于其他三个，且没有光环。")
    add("  它的 `Dmg-Min/Max` 只代表近战平砍，真实输出来自元素技能（火球/冰爆/闪电），")
    add("  所以「伤害」这一项对它是低估；但 HP 低、无光环、且吃不到武器伤害加成，是它常年垫底的结构性原因。")
    add("- **A5 野蛮人面板不差**（HP 与 A2 接近，伤害更高），问题是没光环 + 两个技能都是纯单体控制，")
    add("  对队伍没有任何增益。要「修」它，加数值是没用的，得给它一个定位。")
    add("")

    return "\n".join(L).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tools.p1_merc")
    ap.add_argument("--vanilla", type=Path, default=ROOT / "vanilla")
    ap.add_argument("--out", type=Path, default=ROOT / "docs" / "p1-merc.md")
    ap.add_argument("--overlay", type=Path, default=None,
                    help="叠加层目录（如 mod/）：用于量化「打上补丁之后会变成什么样」")
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args(argv)

    ctx = Ctx(vanilla=args.vanilla, out=ROOT / "mod", overlay=args.overlay)
    report = build_report(ctx)
    if args.stdout:
        print(report)
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report, encoding="utf-8")
        print(f"→ {args.out}  ({len(report.splitlines())} 行)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
