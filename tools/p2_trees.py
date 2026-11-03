"""P2 只读分析：21 个职业/技能系的体检表。

回答的问题：**每一系到底赢在哪个场景？** 赢不了的系就是死内容。

## 边界（重要）

- 技能清单、伤害类型、场景胜场是**人工整理的元数据**（技能树归属在
  `skills.txt` 里没有列，它是硬编码的）。判断结论写在下面对应的常量里，
  有争议就改常量，不是从数据"推"出来的。
- 伤害数字来自 `skills.txt`（`EMin/EMax` + Lev1~5 分段 + `HitShift`），
  和 `docs/p1-skills.md` 完全同一套公式。
- **伤害/法力只作参考，不作判据**：它分不清"单体轰炸"和"持续覆盖"。
  真正的判据是场景矩阵（M1~M6），见 `docs/p2-balance-plan.md`。

用法：
    python3 -m tools.p2_trees                    # → docs/p2-trees.md
    python3 -m tools.p2_trees --overlay mod      # 同时给出「打上补丁后」的对照
"""

from __future__ import annotations

import argparse
from pathlib import Path

from . import d2txt
from .d2patch import Ctx
from .p1_skills import CLASSES, LEVELS, _eval_calc, scan

ROOT = Path(__file__).resolve().parent.parent

# 场景矩阵（"胜场"的定义）
SCENARIOS = {
    "M1": "开荒（零装备）",
    "M2": "密集清场",
    "M3": "单体攻坚",
    "M4": "高抗/免疫区",
    "M5": "安全/容错",
    "M6": "终局极限",
}

# 状态
DONE = "✅已改"
HEALTHY = "⚪体检通过"
T2 = "⚠️T2过强"
TODO = "⬜待修"
CANT = "❌修不了"

# 技能树归属（硬编码，人工整理）+ 伤害类型 + 当前判定的胜场
# 字段：class, 系名, 技能列表, 伤害类型, 胜场(M 编号), 状态, 一句话结论
TREES: list[dict] = [
    # ---------------------------------------------------------------- 亚马逊
    dict(cls="ama", tree="弓与弩", dmg="物理 + 火/冰",
         skills=["Magic Arrow", "Fire Arrow", "Cold Arrow", "Multiple Shot",
                 "Exploding Arrow", "Ice Arrow", "Guided Arrow", "Strafe",
                 "Immolation Arrow", "Freezing Arrow"],
         wins=["M2", "M6"], status=HEALTHY,
         note="物理免疫只 3%，弓马免疫压力最小；元素箭支线缺降抗（见 p2-items 的 craft）"),
    dict(cls="ama", tree="被动与魔法", dmg="—",
         skills=["Inner Sight", "Critical Strike", "Dodge", "Slow Missiles",
                 "Avoid", "Penetrate", "Dopplezon", "Evade", "Valkyrie", "Pierce"],
         wins=["M5"], status=HEALTHY,
         note="女武神肉盾 + 闪避三连 + 100% 穿刺，纯支援系，本身不产伤害"),
    dict(cls="ama", tree="标枪与长矛", dmg="电 + 毒",
         skills=["Jab", "Power Strike", "Poison Javelin", "Impale", "Lightning Bolt",
                 "Charged Strike", "Plague Javelin", "Fend", "Lightning Strike",
                 "Lightning Fury"],
         wins=["M2", "M3"], status=HEALTHY,
         note="闪电之怒是少数「一格打一群」的技能；电系无降抗，靠 craft 头盔补"),

    # ---------------------------------------------------------------- 法师
    dict(cls="sor", tree="火", dmg="火",
         skills=["Fire Bolt", "Warmth", "Inferno", "Blaze", "Fire Ball",
                 "Fire Wall", "Enchant", "Meteor", "Fire Mastery", "Hydra"],
         wins=["M3", "M4"], status=DONE,
         note="已修：火掌握 伤害 163%→100% + 穿透 −45%，75% 抗性处与冰系相等"),
    dict(cls="sor", tree="电", dmg="电",
         skills=["Charged Bolt", "Static Field", "Telekinesis", "Nova",
                 "Lightning", "Chain Lightning", "Teleport", "Thunder Storm",
                 "Energy Shield", "Lightning Mastery"],
         wins=["M2", "M6"], status=TODO,
         note="原始伤害全法师最高（掌握 +278%），但 M4 完全没有 → 见 TODO #sor-lightning"),
    dict(cls="sor", tree="冰", dmg="冰",
         skills=["Ice Bolt", "Frozen Armor", "Frost Nova", "Ice Blast",
                 "Shiver Armor", "Glacial Spike", "Blizzard", "Chilling Armor",
                 "Frozen Orb", "Cold Mastery"],
         wins=["M1", "M2", "M3", "M4"], status=T2,
         note="唯一同时赢 4 个场景的系：自带 −115% 降抗 + 大范围形态。不砍，靠抬高别人制衡"),

    # ---------------------------------------------------------------- 死灵
    dict(cls="nec", tree="召唤", dmg="物理",
         skills=["Skeleton Mastery", "Raise Skeleton", "Clay Golem", "Golem Mastery",
                 "Raise Skeletal Mage", "BloodGolem", "Summon Resist", "IronGolem",
                 "Revive", "FireGolem"],
         wins=["M1", "M5"], status=HEALTHY,
         note="零装备开荒最省心的路线；伤害不在 skills.txt（召唤物自带）"),
    dict(cls="nec", tree="毒与骨", dmg="魔法 + 毒",
         skills=["Teeth", "Bone Armor", "Poison Dagger", "Corpse Explosion",
                 "Bone Wall", "Poison Explosion", "Bone Spear", "Bone Prison",
                 "Poison Nova", "Bone Spirit"],
         wins=["M3"], status=TODO,
         note="骨系是魔法伤害（免疫 1%）很稳；**毒系是唯一没有任何掌握 stat 的伤害系**"),
    dict(cls="nec", tree="诅咒", dmg="—",
         skills=["Amplify Damage", "Dim Vision", "Weaken", "Iron Maiden", "Terror",
                 "Confuse", "Life Tap", "Attract", "Decrepify", "Lower Resist"],
         wins=["M5"], status=HEALTHY,
         note="降抗 −70%（四系）+ 伤害加深 + 衰老，全游戏最强的「让队友变强」体系"),

    # ---------------------------------------------------------------- 圣骑士
    dict(cls="pal", tree="战斗", dmg="魔法 + 物理 + 电",
         skills=["Sacrifice", "Smite", "Holy Bolt", "Zeal", "Charge", "Vengeance",
                 "Blessed Hammer", "Conversion", "Holy Shield", "Fist of the Heavens"],
         wins=["M1", "M2", "M3", "M4"], status=T2,
         note="锤子是魔法伤害（免疫 1%）+ 光环自带全部辅助。不砍，靠抬高别人制衡"),
    dict(cls="pal", tree="进攻光环", dmg="火/冰/电 + 支援",
         skills=["Might", "Holy Fire", "Thorns", "Blessed Aim", "Concentration",
                 "Holy Freeze", "Holy Shock", "Sanctuary", "Fanaticism", "Conviction"],
         wins=["M6"], status=HEALTHY,
         note="信念 −125% 是全游戏最强降抗；狂热是物理系的天花板"),
    dict(cls="pal", tree="防御光环", dmg="—",
         skills=["Prayer", "Resist Fire", "Defiance", "Resist Cold", "Cleansing",
                 "Resist Lightning", "Vigor", "Meditation", "Redemption", "Salvation"],
         wins=["M5"], status=HEALTHY,
         note="抗性/回血/回蓝/救赎，纯支援；也是佣兵光环的模板"),

    # ---------------------------------------------------------------- 野蛮人
    dict(cls="bar", tree="战斗", dmg="物理",
         skills=["Bash", "Leap", "Double Swing", "Stun", "Double Throw", "Leap Attack",
                 "Concentrate", "Frenzy", "Whirlwind", "Berserk"],
         wins=["M3", "M6"], status=CANT,
         note="免疫压力最小，但**缺 AoE**（旋风斩判定是硬编码），txt 修不了"),
    dict(cls="bar", tree="战斗精通", dmg="—",
         skills=["Sword Mastery", "Axe Mastery", "Mace Mastery", "Pole Arm Mastery",
                 "Throwing Mastery", "Spear Mastery", "Increased Stamina", "Iron Skin",
                 "Increased Speed", "Natural Resistance"],
         wins=[], status=HEALTHY,
         note="纯被动（武器伤害%/防御/抗性），本身不构成「系」，只放大战斗系"),
    dict(cls="bar", tree="战吼", dmg="物理 + 支援",
         skills=["Howl", "Find Potion", "Taunt", "Shout", "Find Item", "Battle Cry",
                 "Battle Orders", "Grim Ward", "War Cry", "Battle Command"],
         wins=["M5"], status=HEALTHY,
         note="战斗指挥/战斗体制是团队级 buff；War Cry 伤害不足以清场"),

    # ---------------------------------------------------------------- 德鲁伊
    dict(cls="dru", tree="元素", dmg="火 + 物理（风）",
         skills=["Firestorm", "Molten Boulder", "Arctic Blast", "Eruption",
                 "Cyclone Armor", "Twister", "Volcano", "Tornado", "Hurricane",
                 "Armageddon"],
         wins=["M2", "M3"], status=DONE,
         note="已修：Armageddon 法力 35→25、伤害 ×1.25，Volcano 法力 25→16、伤害 ×1.30；"
              "火半系赢 M2，风半系赢 M3"),
    dict(cls="dru", tree="变形", dmg="物理 + 火/毒",
         skills=["Wearwolf", "Shape Shifting", "Wearbear", "Feral Rage", "Maul",
                 "Rabies", "Fire Claws", "Hunger", "Shock Wave", "Fury"],
         wins=["M3"], status=HEALTHY,
         note="Fire Claws 伤害/法力 99.4（全德鲁伊最高）但走武器；内容健康"),
    dict(cls="dru", tree="召唤", dmg="物理",
         skills=["Raven", "Plague Poppy", "Oak Sage", "Summon Spirit Wolf",
                 "Heart of Wolverine", "Summon Fenris", "Vines", "Spirit of Barbs",
                 "Cycle of Life", "Summon Grizzly"],
         wins=["M5"], status=HEALTHY,
         note="橡木贤者 + 灰熊，肉盾与续航；伤害不在 skills.txt"),

    # ---------------------------------------------------------------- 刺客
    dict(cls="ass", tree="陷阱", dmg="火 + 电",
         skills=["Fire Trauma", "Shock Field", "Blade Sentinel", "Charged Bolt Sentry",
                 "Wake of Fire Sentry", "Blade Fury", "Lightning Sentry",
                 "Inferno Sentry", "Death Sentry", "Blade Shield"],
         wins=["M2"], status=TODO,
         note="雷光守卫 + 亡者守卫（尸爆）撑起主线；**火陷阱半系是死内容**"),
    dict(cls="ass", tree="暗影", dmg="—",
         skills=["Claw Mastery", "Psychic Hammer", "Quickness", "Weapon Block",
                 "Cloak of Shadows", "Fade", "Shadow Warrior", "Mind Blast", "Venom",
                 "Shadow Master"],
         wins=["M5"], status=HEALTHY,
         note="消退 +75% 全抗 + 魔影斗篷 + 心灵爆震，全游戏最完整的自保体系"),
    dict(cls="ass", tree="武学", dmg="物理 + 元素",
         skills=["Tiger Strike", "Dragon Talon", "Fists of Fire", "Dragon Claw",
                 "Cobra Strike", "Claws of Thunder", "Dragon Tail", "Blades of Ice",
                 "Dragon Flight", "Royal Strike"],
         wins=["M3"], status=HEALTHY,
         note="蓄气/终结连段，靠武器；元素部分无降抗但物理主体免疫压力小"),
]

assert len(TREES) == 21, f"应该是 21 个技能系，现在 {len(TREES)}"


def pierce_grants(ctx: Ctx) -> dict[str, tuple[str, float]]:
    """-> {技能名: (pierce stat, L20 值)}。只有"发放" pasivestat 的技能才算。"""
    tf = ctx.load("skills.txt")
    c = {n: tf.need(n) for n in
         ["maxlvl"] + [f"Param{i}" for i in range(1, 9)] +
         [f"passivestat{i}" for i in range(1, 6)] + [f"passivecalc{i}" for i in range(1, 6)]}
    out: dict[str, tuple[str, float]] = {}
    for row in tf.rows:
        if not row or not row[0]:
            continue
        params = [tf.get(row, c[f"Param{i}"]) for i in range(1, 9)]
        maxlvl = int(float(tf.get(row, c["maxlvl"]) or 1))
        for i in range(1, 6):
            stat = tf.get(row, c[f"passivestat{i}"])
            if not stat.endswith("_pierce"):
                continue
            ev = _eval_calc(tf.get(row, c[f"passivecalc{i}"]), params, maxlvl)
            if ev is None:
                continue
            # 只认"跟着技能等级长"的发放；`stat(...accr)` 那种是读取，不是发放
            if tf.get(row, c[f"passivecalc{i}"]).strip('\'"').startswith("stat("):
                out.setdefault(row[0], (stat, 0.0))
                continue
            out[row[0]] = (stat, ev[1])
    return out


SKIP_DIFF = {"skill", "charclass", "*eol"}


def changed_columns(base: Ctx, overlay: Ctx, skills: list[str]) -> list[tuple[str, list[str]]]:
    """这个系的技能里，哪些列在补丁前后变了。"""
    a = base.load("skills.txt")
    b = overlay.load("skills.txt")
    idx_a = {a.get(r, 0).strip(): r for r in a.rows if r and r[0]}
    idx_b = {b.get(r, 0).strip(): r for r in b.rows if r and r[0]}
    out: list[tuple[str, list[str]]] = []
    for s in skills:
        ra, rb = idx_a.get(s), idx_b.get(s)
        if ra is None or rb is None:
            continue
        cols: list[str] = []
        for i, name in enumerate(a.header):
            if name in SKIP_DIFF or name.startswith("*"):
                continue
            if i >= len(b.header) or b.header[i] != name:
                continue
            if i < len(ra) and i < len(rb) and ra[i] != rb[i]:
                cols.append(name)
        if cols:
            out.append((s, cols))
    return out


def tree_stats(ctx: Ctx, tree: dict) -> dict:
    rows, weapon, _ = scan(ctx)
    by_skill = {r["skill"]: r for r in rows}
    weapon_set = {r["skill"] for r in weapon}
    present = [by_skill[s] for s in tree["skills"] if s in by_skill]
    weapon_present = [s for s in tree["skills"] if s in weapon_set]

    best = max(present, key=lambda r: (r["dmg"][20][0] + r["dmg"][20][1]) / 2 / r["mana"]
               if r["mana"] else 0, default=None)
    hardest = max(present, key=lambda r: r["dmg"][20][1], default=None)

    grants = pierce_grants(ctx)
    pierce = [(s, *grants[s]) for s in tree["skills"] if s in grants and grants[s][1] > 0]

    return {
        "n_dmg": len(present),
        "n_weapon": len(weapon_present),
        "n_total": len(tree["skills"]),
        "best": best,
        "hardest": hardest,
        "pierce": pierce,
    }


def caution(skill: str) -> str:
    """这个技能的伤害数字不能按"单次命中"读（每帧/速率/脉冲/多发射物）。"""
    from .p1_skills import READ_CAREFULLY
    for reason, names in READ_CAREFULLY.items():
        if skill in names:
            return "⚠"
    return ""


def _fmt_skill(r: dict | None) -> str:
    if r is None:
        return "—"
    avg = (r["dmg"][20][0] + r["dmg"][20][1]) / 2
    per = avg / r["mana"] if r["mana"] else 0
    return f"{r['skill']} {per:.1f}{caution(r['skill'])}"


def build_report(ctx: Ctx, overlay: Ctx | None) -> str:
    L: list[str] = []
    add = L.append
    add("# P2 · 21 个技能系体检表")
    add("")
    add("> 由 `tools/p2_trees.py` 生成。**技能树归属、伤害类型、场景胜场是人工整理的元数据**")
    add("> （技能树在 `skills.txt` 里没有列，是硬编码的）；伤害数字与 `docs/p1-skills.md` 同一套公式。")
    add("")
    add("判据见 [p2-balance-plan.md](p2-balance-plan.md)：")
    add("**T1 每系一个胜场**（赢 0 个场景 = 死内容）、**T2 没有全能系**（赢 ≥4 个 = 过强）、")
    add("**T3 等价交换**、**T4 数值可预演**。")
    add("")
    add("| | 场景 |")
    add("|---|---|")
    for k, v in SCENARIOS.items():
        add(f"| {k} | {v} |")
    add("")

    head = ("| 职业 | 系 | 伤害类型 | 技能数（伤害/武器/全部） | 胜场 | 自降抗 | "
            "主输出（伤害/法力@20） | 本轮改动 | 状态 |")
    rule = "|---|---|---|---:|---|---|---|---|---|"
    if overlay:
        add("## 总表（数值为**打上补丁后**的状态）")
    else:
        add("## 总表（数值为 `vanilla/` 状态）")
    add("")
    add(head)
    add(rule)

    active = overlay or ctx      # 表格显示的是「现在会进游戏的状态」
    detail: list[str] = []
    for t in TREES:
        st = tree_stats(active, t)
        pierce_txt = "、".join(
            f"{s} −{v:.0f}%" for s, _stat, v in st["pierce"]
        ) or "—"
        best_txt = _fmt_skill(st["best"])
        changed_txt = "—"
        if overlay:
            ch = changed_columns(ctx, overlay, t["skills"])
            if ch:
                parts = []
                for skill, cols in ch:
                    shown = "、".join(cols[:4]) + ("…" if len(cols) > 4 else "")
                    parts.append(f"`{skill}`（{shown}）")
                changed_txt = "<br>".join(parts)
        wins = " ".join(t["wins"]) or "**无**"
        add(f"| {CLASSES[t['cls']]} | {t['tree']} | {t['dmg']} | "
            f"{st['n_dmg']}/{st['n_weapon']}/{st['n_total']} | {wins} | {pierce_txt} | "
            f"{best_txt} | {changed_txt} | {t['status']} |")

        # 明细
        d = [f"### {CLASSES[t['cls']]} · {t['tree']}", ""]
        d.append(f"- 伤害类型：{t['dmg']}")
        d.append(f"- 胜场：{'、'.join(f'`{w}` {SCENARIOS[w]}' for w in t['wins']) or '**无**（死内容）'}")
        d.append(f"- 自降抗：{pierce_txt}")
        if st["best"]:
            b = st["best"]
            d.append(f"- 主输出：`{b['skill']}` — L20 {b['dmg'][20][0]:.0f}-{b['dmg'][20][1]:.0f}，"
                     f"法力 {b['mana']:.0f}，{_fmt_skill(b).split()[-1]} 伤害/法力")
        if st["hardest"] and st["hardest"] is not st["best"]:
            h = st["hardest"]
            d.append(f"- 最大单发：`{h['skill']}` — L20 {h['dmg'][20][0]:.0f}-{h['dmg'][20][1]:.0f}")
        if st["n_weapon"]:
            d.append(f"- 其中 {st['n_weapon']} 个是武器百分比技能（`SrcDam`，伤害取决于武器）")
        d.append(f"- 判定：**{t['status']}** — {t['note']}")
        d.append("")
        detail.extend(d)

    add("")
    add("## 明细")
    add("")
    L.extend(detail)

    # 统计
    from collections import Counter
    cnt = Counter(t["status"] for t in TREES)
    add("## 状态统计")
    add("")
    add("| 状态 | 数量 |")
    add("|---|---:|")
    for k in (DONE, HEALTHY, T2, TODO, CANT):
        add(f"| {k} | {cnt.get(k, 0)} |")
    add(f"| **合计** | **{len(TREES)}** |")
    add("")
    # 纯支援系（伤害类型为「—」）不参与"死内容"判定：它本来就不产伤害
    no_win = [f"{CLASSES[t['cls']]}·{t['tree']}" for t in TREES
              if not t["wins"] and t["dmg"] != "—"]
    add(f"- 死内容（胜场 = 0）：{'、'.join(no_win) if no_win else '无'}")
    over = [f"{CLASSES[t['cls']]}·{t['tree']}" for t in TREES if len(t["wins"]) >= 4]
    add(f"- T2 违规（胜场 ≥4）：{'、'.join(over) if over else '无'}")
    add("")
    return "\n".join(L).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tools.p2_trees")
    ap.add_argument("--vanilla", type=Path, default=ROOT / "vanilla")
    ap.add_argument("--out", type=Path, default=ROOT / "docs" / "p2-trees.md")
    ap.add_argument("--overlay", type=Path, default=None)
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args(argv)

    ctx = Ctx(vanilla=args.vanilla, out=ROOT / "mod")
    ov = args.overlay
    if ov is None and (ROOT / "mod" / "data" / "global" / "excel" / "Skills.txt").exists():
        ov = ROOT / "mod"      # 默认读 mod/：表格反映的是"当前会进游戏的状态"
    overlay = Ctx(vanilla=args.vanilla, out=ROOT / "mod", overlay=ov) if ov else None
    md = build_report(ctx, overlay)
    if args.stdout:
        print(md)
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(md, encoding="utf-8")
        print(f"→ {args.out}  ({len(md.splitlines())} 行)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
