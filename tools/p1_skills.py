"""P1 只读分析：技能本体伤害曲线。

回答的问题：**在 skills.txt 里，哪些技能天生就是废的？**

方法和边界（很重要，别把结论当成游戏内实际 DPS）：
  包含：技能本体的基础伤害 + 等级分段增幅（Lev1~Lev5）+ HitShift 定点缩放。
  不包含：
    - **技能协同加成**（1.13c 的协同是硬编码在 Dll 里的，txt 里没有对应列！
      已核对：Skills.txt / SkillDesc.txt 都没有任何 syn*/ergy 列，passivestat 只用于掌握类技能）
    - 掌握/降抗/装备/护身符等外部加成
    - 施法速度、命中、NextHitDelay、弹道数量（多段命中技能会被显著低估）

公式（已验证）：
    damage = (base + Σ 分段增量) × 2^HitShift / 256
    分段增量：L2-8 用 Lev1，L9-16 用 Lev2，L17-22 用 Lev3，L23-28 用 Lev4，L29+ 用 Lev5

对照游戏内已知值（L1）：
    火弹 3-6 ✓  冰弹 3-5 ✓  火球 6-14 ✓  充能弹(每颗) 2-4 ✓  牙齿 2-4 ✓

用法：
    python3 -m tools.p1_skills                 # → docs/p1-skills.md
    python3 -m tools.p1_skills --class sor
"""

from __future__ import annotations

import argparse
from pathlib import Path

from . import d2txt
from .d2patch import Ctx

ROOT = Path(__file__).resolve().parent.parent

# 元素 -> (掌握 stat, 降抗 stat)。`itemstatcost.txt` 里八个 stat 全都存在。
ELEM_STATS = {
    "火": ("passive_fire_mastery", "passive_fire_pierce"),
    "冰": ("passive_cold_mastery", "passive_cold_pierce"),
    "电": ("passive_ltng_mastery", "passive_ltng_pierce"),
    "毒": ("passive_pois_mastery", "passive_pois_pierce"),
}

# D2 的抗性下限是 -100%，所以降抗超过 100 点之后收益归零。
RES_FLOOR = -100

CLASSES = {
    "ama": "亚马逊", "sor": "法师", "nec": "死灵法师", "pal": "圣骑士",
    "bar": "野蛮人", "dru": "德鲁伊", "ass": "刺客",
}

# 分段起点：第 i 段从 slvl = start[i] 之后开始累加
STARTS = {1: 1, 2: 8, 3: 16, 4: 22, 5: 28}
LEVELS = (1, 10, 20, 30)

# 这些技能的伤害数字**不能按单次命中读**，否则会得出完全错误的结论。
# 名单是人工整理的（不是从数据推出的），按原因分组。
READ_CAREFULLY = {
    "每帧判定（数字是每帧伤害，实际要乘命中帧数）": [
        "Fire Wall", "Inferno", "Blaze", "Arctic Blast",
    ],
    "毒素速率（EMin/EMax 是伤害速率，ELen 才是持续时间，不是单次总伤害）": [
        "Poison Dagger", "Poison Explosion", "Poison Nova", "Venom", "Poison Javelin",
    ],
    "光环脉冲（数字是每次脉冲伤害，不是每秒）": [
        "Holy Fire", "Holy Freeze", "Holy Shock", "Sanctuary",
    ],
    "多发射物（数字是单颗伤害，实际随等级增加数量）": [
        "Charged Bolt", "Teeth", "Multiple Shot", "Strafe",
    ],
}


def num(tf: d2txt.TxtFile, row: list[str], col: str) -> float:
    ci = tf.find(col)
    if ci is None:
        return 0.0
    v = d2txt.to_number(tf.get(row, ci))
    return float(v) if v is not None else 0.0


def lev_bonus(base: float, levs: list[float], slvl: int) -> float:
    v = base
    for i, inc in enumerate(levs, start=1):
        if slvl > STARTS[i]:
            v += (slvl - STARTS[i]) * inc
    return v


def skill_damage(tf: d2txt.TxtFile, row: list[str], slvl: int) -> tuple[float, float]:
    hs = num(tf, row, "HitShift")
    scale = (2 ** hs) / 256 if hs else 1.0
    e_min = [num(tf, row, f"EMinLev{i}") for i in range(1, 6)]
    e_max = [num(tf, row, f"EMaxLev{i}") for i in range(1, 6)]
    p_min = [num(tf, row, f"MinLevDam{i}") for i in range(1, 6)]
    p_max = [num(tf, row, f"MaxLevDam{i}") for i in range(1, 6)]
    lo = lev_bonus(num(tf, row, "EMin"), e_min, slvl) + lev_bonus(num(tf, row, "MinDam"), p_min, slvl)
    hi = lev_bonus(num(tf, row, "EMax"), e_max, slvl) + lev_bonus(num(tf, row, "MaxDam"), p_max, slvl)
    return lo * scale, hi * scale


def scan(ctx: Ctx) -> tuple[list[dict], list[dict], list[dict]]:
    tf = ctx.load("skills.txt")
    i_skill = tf.find("skill")
    i_class = tf.find("charclass")

    rows, weapon, no_damage = [], [], []
    for row in tf.rows:
        name = tf.get(row, i_skill).strip()
        cls = tf.get(row, i_class).strip().lower() if i_class is not None else ""
        if not name or cls not in CLASSES:
            continue
        dmg = {lvl: skill_damage(tf, row, lvl) for lvl in LEVELS}
        rec = {
            "skill": name,
            "class": cls,
            "req": num(tf, row, "reqlevel"),
            "max": num(tf, row, "maxlvl"),
            "mana": num(tf, row, "mana"),
            "srcdam": num(tf, row, "SrcDam"),
            "dmg": dmg,
        }
        if dmg[20][1] > 0:
            rows.append(rec)
        elif num(tf, row, "SrcDam") > 0:
            # 武器百分比技能：真伤害 = 武器伤害 × SrcDam%，txt 里没有武器伤害
            weapon.append(rec)
        else:
            no_damage.append(rec)
    return rows, weapon, no_damage


# 地狱里「能不能打」的真正瓶颈不是伤害数字，而是这两个变量：
#   1. 该元素有多少怪免疫（`MonStats.txt` 的 ResXX(H)）
#   2. 你自带的降抗够不够（降抗是稀缺资源，见下）
RES_STAT_TO_ELEM = {
    "fireresist": "火", "coldresist": "冰", "lightresist": "电", "poisonresist": "毒",
    # 掌握类技能用的是另一套 stat（只作用于自己的元素）
    "passive_fire_pierce": "火", "passive_cold_pierce": "冰",
    "passive_ltng_pierce": "电", "passive_pois_pierce": "毒",
}


def _eval_calc(calc: str, p: list[str], maxlvl: int) -> tuple[float, float] | None:
    """只解 txt 里真实出现过的几种公式，其余返回 None（标 `—`，不猜）。"""
    calc = calc.strip().strip('"')  # 含逗号的公式在 txt 里被引号包住，见文末说明

    def num(i: int) -> float:
        try:
            return float(p[i - 1] or 0)
        except (ValueError, IndexError):
            return 0.0
    try:
        if calc == "-dm56":
            return -num(5), -num(6)
        if calc == "-min(ln34,150)":
            return -min(num(3), 150), -min(num(3) + num(4) * (maxlvl - 1), 150)
        if calc == "ln12":
            return num(1), num(1) + num(2) * (maxlvl - 1)
        if calc == "-ln12":
            return -num(1), -(num(1) + num(2) * (maxlvl - 1))
        if calc == "dm12":
            return num(1), num(2)
        if calc == "-par5":
            return -num(5), -num(5)
    except (ValueError, IndexError):
        return None
    return None


def resistance_audit(ctx: Ctx) -> list[str]:
    """审计「谁能让怪物抗性下降」。

    这是 1.13c 里决定职业强弱的第一变量：免疫只能被降抗破，
    而全游戏只有三个技能在降低**敌人**抗性。
    """
    f = ctx.load("skills.txt")
    c = {n: f.need(n) for n in
         ["charclass", "reqlevel", "maxlvl"] +
         [f"Param{i}" for i in range(1, 9)] +
         [f"aurastat{i}" for i in range(1, 7)] + [f"aurastatcalc{i}" for i in range(1, 7)] +
         [f"passivestat{i}" for i in range(1, 4)] + [f"passivecalc{i}" for i in range(1, 4)]}

    found: list[dict] = []
    for r in f.rows:
        if not r or not r[0]:
            continue
        params = [f.get(r, c[f"Param{i}"]) for i in range(1, 9)]
        maxlvl = int(float(f.get(r, c["maxlvl"]) or 1))
        for kind, n in (("aura", 6), ("passive", 3)):
            for i in range(1, n + 1):
                scol = f"aurastat{i}" if kind == "aura" else f"passivestat{i}"
                ccol = f"aurastatcalc{i}" if kind == "aura" else f"passivecalc{i}"
                stat = f.get(r, c[scol])
                calc = f.get(r, c[ccol])
                elem = RES_STAT_TO_ELEM.get(stat)
                if not elem or not calc:
                    continue
                vals = _eval_calc(calc, params, maxlvl)
                if stat.endswith("_pierce") and vals:
                    # 掌握类的 pierce stat 是「正数表示降抗」，统一成负号再比较
                    vals = (-vals[0], -vals[1])
                if not vals or vals[1] >= 0:
                    continue
                found.append({
                    "skill": r[0], "class": f.get(r, c["charclass"]),
                    "req": f.get(r, c["reqlevel"]), "elem": elem,
                    "calc": calc, "l1": vals[0], "l20": vals[1],
                })

    L = ["## 降抗审计：全游戏只有三个技能能降低「敌人」的抗性", ""]
    L += [
        "免疫（抗性 ≥100）只能靠降抗打破，而且对免疫怪只按 1/5 生效。",
        "所以「自带降抗」是 1.13c 里最稀缺的资源——把 txt 里所有降抗技能列出来：",
        "",
        "| 技能 | 职业 | 需等级 | 作用元素 | 公式 | L1 | L20 | 破免疫上限(≈L20/5) |",
        "|---|---|---|---|---|---:|---:|---:|",
    ]
    for d in sorted(found, key=lambda x: (x["l20"], x["skill"])):
        L.append(f"| {d['skill']} | {CLASSES.get(d['class'], d['class'] or '—')} | "
                 f"{d['req']} | {d['elem']} | `{d['calc']}` | "
                 f"{d['l1']:+.0f}% | **{d['l20']:+.0f}%** | "
                 f"{100 + abs(d['l20']) / 5:.0f}% 抗性 |")
    L += [
        "",
        "**竖着读这一列「作用元素」**：火、电、毒 的降抗都不在法师手里，",
        "只存在于死灵的诅咒和圣骑士的光环里。**法师自己只有冰系能降抗。**",
        "",
        "> ⚠ 冰掌握能不能破免疫，社区有争议（普遍认为不能，只有信念/降抗可以）。",
        "> 上表的「破免疫上限」是按 txt 数值 + 1/5 规则算的理论值，进游戏要验。",
        "",
        "> 📌 解析坑：含逗号的公式在 txt 里被**双引号包住**（如 "
        "`\"-min(ln34,150)\"`，因为文件是 CSV 风格）。读的时候要 strip 掉引号，",
        "否则字符串比较永远不匹配。",
        "",
    ]
    return L


def _ln12(param: list[str], slvl: int) -> float:
    """`ln12` 公式：L1 取 Param1，之后每级累加 Param2。"""
    try:
        p1 = float(param[0] or 0)
        p2 = float(param[1] or 0)
    except ValueError:
        return 0.0
    return p1 + p2 * (slvl - 1)


def mastery_audit(ctx: Ctx) -> tuple[list[str], dict[str, dict[str, float]]]:
    """审计「谁在发放 passive_* stat」。

    这是 1.13c 里一个真实且纯 txt 可查的不对称：八个 stat 引擎全都支持，
    但只有冰系的降抗真的被某个技能发出来了。
    """
    f = ctx.load("skills.txt")
    ci = {n: f.need(n) for n in
          ["Param1", "Param2", "reqlevel", "skilldesc"] +
          [f"passivestat{i}" for i in range(1, 6)] +
          [f"passivecalc{i}" for i in range(1, 6)]}
    grants: dict[str, list[tuple[str, str, list[str], float]]] = {}
    for r in f.rows:
        if not r or not r[0]:
            continue
        for i in range(1, 6):
            stat = f.get(r, ci[f"passivestat{i}"])
            if not stat.startswith("passive"):
                continue
            grants.setdefault(stat, []).append(
                (r[0], f.get(r, ci[f"passivecalc{i}"]),
                 [f.get(r, ci["Param1"]), f.get(r, ci["Param2"])],
                 float(f.get(r, ci["reqlevel"]) or 0))
            )

    L: list[str] = []
    add = L.append
    add("## 掌握结构审计：谁在给「降抗」，谁只给「加伤害」")
    add("")
    add("`itemstatcost.txt` 里八个 `passive_*` stat 全都存在，`skills.txt` 通过 "
        "`passivestat1..5` + `passivecalc1..5` 发放。把发放者列出来，问题一目了然：")
    add("")
    add("| stat | 发放它的技能 | 公式 | L20 数值 |")
    add("|---|---|---|---:|")
    for elem, (m_stat, p_stat) in ELEM_STATS.items():
        for stat in (m_stat, p_stat):
            gs = grants.get(stat, [])
            if gs:
                names = "、".join(f"`{n}`" for n, *_ in gs)
                calc = gs[0][1]
                val = _ln12(gs[0][2], 20) if calc == "ln12" else None
                shown = "—" if val is None else f"{val:+.0f}%"
                add(f"| `{stat}` | {names} | `{calc}` | {shown} |")
            else:
                add(f"| `{stat}` | **无人发放** | — | — |")
    add("")

    vals: dict[str, dict[str, float]] = {}
    for elem, (m_stat, p_stat) in ELEM_STATS.items():
        dmg = pierce = 0.0
        for stat, key in ((m_stat, "dmg"), (p_stat, "pierce")):
            gs = grants.get(stat, [])
            if gs and gs[0][1] == "ln12":
                v = _ln12(gs[0][2], 20)
                if key == "dmg":
                    dmg = v
                else:
                    pierce = v
        vals[elem] = {"dmg": dmg, "pierce": pierce}

    add("### 对高抗性怪的**实际**伤害倍率（掌握满级 20 级）")
    add("")
    add("倍率 = `(1 + 伤害加成%) × (1 - 最终抗性/100)`，最终抗性下限 -100%。")
    add("")
    add("| 怪物抗性 | " + " | ".join(f"{e}系" for e in ELEM_STATS) + " |")
    add("|---|" + "---:|" * len(ELEM_STATS))
    for res in (0, 50, 75, 90, 99):
        cells = []
        for elem in ELEM_STATS:
            v = vals[elem]
            final = max(RES_FLOOR, res - v["pierce"])
            cells.append(f"{(1 + v['dmg'] / 100) * (1 - final / 100):.2f}×")
        add(f"| {res}% | " + " | ".join(cells) + " |")
    add("")
    add("**读法**：抗性 0% 时火/电靠「加伤害」是赢的；一旦怪物抗性上到 75% 以上，")
    add("只剩冰系靠降抗还能维持输出。抗性越高差距越大——这就是「地狱里火系打不动」的数学原因。")
    add("")
    return L, vals



def build_report(ctx: Ctx, only_class: str | None) -> str:
    rows, weapon, no_damage = scan(ctx)
    L: list[str] = []
    add = L.append

    add("# P1 · 技能本体伤害曲线")
    add("")
    add("> 由 `tools/p1_skills.py` 从 `vanilla/` 生成。只读分析。")
    add("")
    add("**边界**：这里只有 `skills.txt` 里的本体伤害 + 等级增幅，**不含协同加成**")
    add("（1.13c 的协同硬编码在 Dll 里，txt 没有任何 syn 列，已核对）、不含掌握/装备、")
    add("不含施法速度与多段命中。多段技能（充能弹、多重箭等）会严重低估，请看单位伤害而非总和。")
    add("")
    add("公式：`(base + Σ分段增量) × 2^HitShift / 256`；")
    add("已验证对照：火弹 3-6、冰弹 3-5、火球 6-14、充能弹 2-4、牙齿 2-4（均为 1 级）。")
    add("")
    add("### 读表须知：这些技能的伤害列不能直接比大小")
    add("")
    for reason, names in READ_CAREFULLY.items():
        add(f"- **{reason}**：{'、'.join(names)}")
    add("")
    add("另外，武器系技能（战吼/攻击类）显示的是固定加成部分，实际伤害要乘武器伤害，")
    add("见下面单独的表。")
    add("")

    for cls, cname in CLASSES.items():
        if only_class and cls != only_class:
            continue
        pool = [r for r in rows if r["class"] == cls]
        if not pool:
            continue
        add(f"## {cname}（`{cls}`，{len(pool)} 个有伤害的技能）")
        add("")
        add("| 技能 | 需等级 | L1 | L10 | L20 | L30 | 法力 | 伤害/法力(L20) |")
        add("|---|---:|---:|---:|---:|---:|---:|---:|")
        for r in sorted(pool, key=lambda x: -x["dmg"][20][1]):
            d = r["dmg"]
            per_mana = (d[20][0] + d[20][1]) / 2 / r["mana"] if r["mana"] else 0
            add(
                f"| {r['skill']} | {r['req']:.0f} | "
                f"{d[1][0]:.0f}-{d[1][1]:.0f} | {d[10][0]:.0f}-{d[10][1]:.0f} | "
                f"{d[20][0]:.0f}-{d[20][1]:.0f} | {d[30][0]:.0f}-{d[30][1]:.0f} | "
                f"{r['mana']:.0f} | {per_mana:.1f} |"
            )
        add("")

        # 自动结论：20 级伤害最低的几个 + 每级增幅
        worst = sorted(pool, key=lambda x: x["dmg"][20][1])[:5]
        add("20 级伤害最低的 5 个：")
        for r in worst:
            add(f"- `{r['skill']}`：{r['dmg'][20][0]:.0f}-{r['dmg'][20][1]:.0f}，"
                f"需等级 {r['req']:.0f}，法力 {r['mana']:.0f}")
        add("")

    audit, _ = mastery_audit(ctx)
    L += audit
    L += resistance_audit(ctx)

    if weapon:
        add("## 武器百分比技能（伤害取决于武器，`skills.txt` 只有百分比）")
        add("")
        add("`SrcDam` = 使用的武器伤害百分比。这些技能的实际伤害 = 武器伤害 × SrcDam%")
        add("（+ 少量固定附加）。所以改它们的伤害要改 `weapons.txt` 或 `SrcDam`，")
        add("不能只改 `skills.txt` 的 MinDam/MaxDam。")
        add("")
        add("| 技能 | 职业 | 需等级 | SrcDam% | 法力 |")
        add("|---|---|---:|---:|---:|")
        for r in sorted(weapon, key=lambda x: (x["class"], x["skill"])):
            add(f"| {r['skill']} | {CLASSES.get(r['class'], r['class'])} | {r['req']:.0f} | "
                f"{r['srcdam']:.0f} | {r['mana']:.0f} |")
        add("")

    if no_damage:
        add("## 伤害不在 `skills.txt` 里的技能")
        add("")
        add("这些技能在 `skills.txt` 的伤害列是空的 —— 真实伤害来自 `Missiles.txt`")
        add("（弹道伤害）或纯硬编码，改 `skills.txt` 对它们无效，需要去改 `missiles.txt`。")
        add("")
        by_class: dict[str, list[str]] = {}
        for r in no_damage:
            by_class.setdefault(r["class"], []).append(r["skill"])
        for cls, names in by_class.items():
            add(f"- **{CLASSES.get(cls, cls)}**：{'、'.join(names)}")
        add("")

    return "\n".join(L).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tools.p1_skills")
    ap.add_argument("--vanilla", type=Path, default=ROOT / "vanilla")
    ap.add_argument("--out", type=Path, default=ROOT / "docs" / "p1-skills.md")
    ap.add_argument("--class", dest="only_class", default=None)
    ap.add_argument("--overlay", type=Path, default=None,
                    help="叠加层目录（如 mod/）：用于量化「打上补丁之后会变成什么样」")
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args(argv)

    ctx = Ctx(vanilla=args.vanilla, out=ROOT / "mod", overlay=args.overlay)
    report = build_report(ctx, args.only_class)
    if args.stdout:
        print(report)
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report, encoding="utf-8")
        print(f"→ {args.out}  ({len(report.splitlines())} 行)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
