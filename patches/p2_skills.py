"""P2 · 职业技能系平衡（逐系推进，一次只动一系）

## 判据（整套工作的验收标准）

- **T1 每系一个胜场**：每个技能系都必须至少有一个「选它最优」的具体场景。
  找不到胜场的系 = 死内容，必须修。
- **T2 没有全能系**：不能有一系在所有场景都最优（否则没有选择）。
- **T3 加法或等价交换**：只加不改、或"拿走 A 换给 B"，不凭空提高总量。
- **T4 数值可预演**：改动前先用 `(1+伤害加成)×(1-最终抗性/100)` 算出各抗性段的倍率，
  写进 changelog。不许"改完再说感觉"。

## 本次：法师火系（A2）

诊断见 `docs/p2-skills-classes.md`：火系伤害不低（掌握 +163%），
但**全程没有降抗**，抗性 90% 时实际倍率只有 0.26×，而冰系有 −115% 穿透、仍有 1.25×。

`passive_fire_pierce` 这个 stat 在 `itemstatcost.txt` 里是现成的（`Hydra` 甚至已经在读它），
只是原版没有任何技能发放它。所以这次改动**不引入任何新机制**，只是把口子填上。

| | 改动前 | 改动后 |
|---|---|---|
| 火掌握伤害 (`ln12`) | Param1=30, Param2=7 → **+163%** | Param1=24, Param2=4 → **+100%** |
| 火穿透 (`ln34`) | 无 | Param3=7, Param4=2 → **−45%** |

预期倍率（对照冰系）：

| 怪物抗性 | 火（前） | 火（后） | 冰（基准） |
|---|---:|---:|---:|
| 0% | 2.63× | **2.90×** | 2.00× |
| 50% | 1.31× | **1.90×** | 1.65× |
| 75% | 0.66× | **1.40×** | 1.40× |
| 90% | 0.26× | **1.10×** | 1.25× |
| 99% | 0.03× | **0.92×** | 1.16× |

→ 低抗段略强于冰、高抗段略弱，**75% 处正好相等**。T2 成立（两系各有场景），T3 成立（等价交换）。

## 已知代价：技能描述里看不到

火掌握的说明文字由 `SkillDesc.txt` 的 `descline1` 驱动（`desctexta1=StrSkill5`），
里面只有伤害那一行。要显示"降抗 −45%"必须**再加一行描述 + 一条字符串**，
而整合版的字符串表是 **Big5 繁体**，改 tbl 的风险（编码错→乱码/崩溃）远高于收益。

所以：**机制生效，描述不显示。** 这条记在 TODO 里，等能安全改 tbl 时再补。
（对照：装备上的 `passive_fire_pierce` 是 `descfunc=20`，会**自动**显示成
"−X% 敌人火抗"，这也是「选项 B（做成装备）」的一个隐性优势。）
"""

from tools.d2patch import matches, patch

# ------------------------------------------------------------------ 法师火系
_fm = patch(
    "skills.txt",
    why="P2-法师火系：火掌握 伤害163%→100%，并发放 -45% 火穿透（填 passive_fire_pierce 的空口）",
).where("skill", matches(r"^Fire Mastery$"))

_fm.set("Param1", 24)     # ln12：L1 = +24%
_fm.set("Param2", 4)      # ln12：每级 +4% → L20 = 24 + 76 = 100%
_fm.set("Param3", 7)      # ln34：L1 = -7%
_fm.set("Param4", 2)      # ln34：每级 +2% → L20 = 7 + 38 = 45%
_fm.set("passivestat2", "passive_fire_pierce")
_fm.set("passivecalc2", "ln34")

# 注释列（游戏不读，但要让下一个看文件的人知道这些参数是什么）
_fm.set("*Param1 Description", "Damage bonus")
_fm.set("*Param2 Description", "Damage bonus per level")
_fm.set("*Param3 Description", "Enemy fire resist reduction")
_fm.set("*Param4 Description", "Enemy fire resist reduction per level")


# --------------------------------------------------------------- 德鲁伊火系
# 诊断：火系不是"伤害低"，是**贵**。
#   Armageddon  L20 834-963 / 35 法力 = 25.7 伤害/法力
#   Volcano     L20 236-240 / 25 法力 =  9.5
#   Tornado(风) L20 425-451 / 10 法力 = 43.8   ← 对照组
# 单发伤害反而是 Armageddon 高（2 倍于 Tornado），但它烧不动：一发 35 点法力。
#
# 所以这里动的是"可持续性"而不是纯粹加伤害：
#   Armageddon：法力 35→25，伤害 ×1.25 → 约 44.8 伤害/法力（追平 Tornado）
#   Volcano   ：法力 25→16，伤害 ×1.30 → 约 20.0
#
# 为什么不去改 Armageddon 的"陨石乱落"：那是弹道/硬编码，txt 碰不到。
# 火德能拿到手的独有胜场因此定为 **M2 密集清场（边走边烧）**，而不是和风德拼单体。
_DRU_FIRE = [
    ("Armageddon", 25, 1.25, "法力 35→25、伤害 ×1.25"),
    ("Volcano", 16, 1.30, "法力 25→16、伤害 ×1.30"),
]

for _name, _mana, _factor, _why in _DRU_FIRE:
    _p = patch("skills.txt", why=f"P2-德鲁伊火系：{_name} {_why}").where(
        "skill", matches(rf"^{_name}$")
    )
    _p.set("mana", _mana)
    for _col in ["EMin", "EMax"] + [
        f"{pre}Lev{i}" for pre in ("EMin", "EMax") for i in range(1, 6)
    ]:
        _p.mul(_col, _factor, ndigits=0)


# --------------------------------------------------------------- 死灵毒系
# 诊断（详见 docs/p1-skills.md 的「毒系：EMin/EMax 是速率，不是总量」）：
#   毒系的伤害列是**每帧速率**，`ELen` 才是持续时间（25 帧 = 1 秒）。
#   所以 Poison Nova L20 的真实总量是 12.5-13.3/帧 × 50 帧 = 625-666，
#   不是主表上那个"12-13"。**按总量算，它和 Bone Spirit(600-645) 同档。**
#
# 那么毒系的真问题不是伤害，而是：
#   1. 摊在 2 秒里，打完不能立刻见效；2. 法力 20 偏高，密集清场时续不上。
#
# 毒的降抗本来就有，但在**另一个系**里：诅咒系的 Lower Resist −70%（含毒）。
# 这是"跨系依赖"，所以毒与骨这一格的自降抗看起来是空的。
#
# 定位因此定为 **M2 密集清场**：一次施法覆盖全屏、放完就走。
# 改动只动"可持续性"：法力 20→16、速率 ×1.25 → 总量约 780-830，约 50 总量/法力。
_pn = patch(
    "skills.txt",
    why="P2-死灵毒系：Poison Nova 法力 20→16、毒速率 ×1.25（定位 M2 全屏清场）",
).where("skill", matches(r"^Poison Nova$"))
_pn.set("mana", 16)
for _col in ["EMin", "EMax"] + [
    f"{pre}Lev{i}" for pre in ("EMin", "EMax") for i in range(1, 6)
]:
    _pn.mul(_col, 1.25, ndigits=0)
