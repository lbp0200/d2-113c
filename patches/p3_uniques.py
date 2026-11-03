"""P3 · 重做 7 件「数据确认确实弱」的暗金/套装单件。

来源：用户提供的社区名单 → 逐件用数据核对（`docs/p3-junk-list.md`）后**筛掉了 5 件**
数据不支持的（Guillaume's Face / IK 碎石锤 / Natalya's Shadow / Arm of King Leoric /
Skullder's Ire）。剩下的这 7 件是真的有问题。

方法统一：**给每件一个明确身份（E1），不造成新 BiS（E2），只换/补、不凭空加（E3）**。

| 装备 | 身份 | 改动 |
|---|---|---|
| `Steelpillar`（req 69，力需 **165**） | 高 CB 双手矛 | 加 `ease -25`（力需 165 → 124） |
| `Venomsward`（req 20） | 毒环境续航甲 | 加 `hp 50` + `regen 15` |
| `Heavenly Garb`（req 29） | **打恶魔**甲（原来只打不死） | 对不死 → 对恶魔 + 加 `hp 30` |
| `Gravepalm`（req 32 手套） | 低阶 **CB 手套** | 加 `crush 10` |
| `Hawkmail`（req 15） | 冰抗 + 跑速甲 | 冰抗 15→**30**、跑速 10→**25** |
| `Razortine`（req 12） | 开荒减速矛 | 伤害 30-50%→**60-80%**、加 `ease -20` |
| `Magnus' Skin`（套装手套 req 37） | 攻速 + 生存手套 | 加 `balance2 20`（20% FHR）+ `hp 30` |

为什么要这么做（不这么做的后果）：

- `Steelpillar` 的问题不是数值：260% 伤害 + 25% CB + 25% 攻速是够的，
  但**双手矛要 165 力量**，实战根本举不起来。`ease` 是专门修这个的属性。
- `Heavenly Garb` / `Gravepalm` 的「对不死 +50~200%」在 1.13c 地狱几乎无用
  —— 地狱里成规模的不死怪集中在少数区域，而**恶魔**（混沌避难所、Act 4/5、巴尔）到处都是。
  所以把 `Heavenly Garb` 改成对恶魔，`Gravepalm` 保留对不死但补一条 CB 让它有活儿干。
- `Venomsward` 是「只有毒抗」，`Hawkmail` 是「只有防冰冻」，`Razortine` 是「低阶过渡」——
  这三件都是**数值太低**而不是设计错，所以走"补强"而不是"换方向"。

刻意**没动**的：底材（`code` 列）。换底材会让名字和物品对不上（"剃刀之锋"变成斧），
而且会影响掉落表的观感；先只做属性层。如果之后还嫌弱，再考虑换底材。
"""

from tools.d2patch import eq, patch


def u(name: str, why: str):
    return patch("uniqueitems.txt", why=why).where("index", eq(name))


# ---------------------------------------------------------------- Steelpillar
# 力需 165（War Pike）→ ease -25% → 约 124。数值本身不动。
_s = u("Steelpillar", "P3 Steelpillar：力需 165 举不起来 → ease -25%")
_s.set("prop7", "ease")
_s.set("min7", -25)
_s.set("max7", -25)

# ---------------------------------------------------------------- Venomsward
# 只有毒抗（90）没有续航 → 补生命与回血，成为「毒环境续航甲」。
_v = u("Venomsward", "P3 Venomsward：只有毒抗 → 补 hp 50 + regen 15")
_v.set("prop6", "hp")
_v.set("min6", 40)
_v.set("max6", 60)
_v.set("prop7", "regen")
_v.set("min7", 15)
_v.set("max7", 15)

# ------------------------------------------------------------- Heavenly Garb
# 对不死（地狱几乎用不上）→ 对恶魔（混沌/Act4-5/巴尔遍地），并补 hp。
_h = u("Heavenly Garb", "P3 Heavenly Garb：对不死 → 对恶魔 + hp 30")
_h.set("prop5", "dmg-demon")
_h.set("min5", 50)
_h.set("max5", 50)
_h.set("prop6", "att-demon")
_h.set("min6", 100)
_h.set("max6", 100)
_h.set("prop7", "hp")
_h.set("min7", 30)
_h.set("max7", 30)

# ------------------------------------------------------------------ Gravepalm
# 保留对不死，补一条低阶 CB —— 32 级手套此前没有任何 CB 选项。
_g = u("Gravepalm", "P3 Gravepalm：补 crush 10（低阶 CB 手套）")
_g.set("prop6", "crush")
_g.set("min6", 10)
_g.set("max6", 10)

# ------------------------------------------------------------------- Hawkmail
# 冰抗 15 → 30、跑速 10 → 25。设计方向没问题，纯粹是数值太低。
_k = u("Hawkmail", "P3 Hawkmail：冰抗 15→30、跑速 10→25")
_k.set("min3", 30)
_k.set("max3", 30)
_k.set("min5", 25)
_k.set("max5", 25)

# ------------------------------------------------------------------ Razortine
# 伤害 30-50% → 60-80%，另加 ease -20%（力量 38 → 约 30）。
_r = u("Razortine", "P3 Razortine：伤害 30-50→60-80、ease -20%")
_r.set("min6", 60)
_r.set("max6", 80)
_r.set("prop7", "ease")
_r.set("min7", -20)
_r.set("max7", -20)

# --------------------------------------------------------------- Magnus' Skin
# 套装手套，只有攻速与命中 → 补 20% FHR 与 30 生命，成为「攻速+生存」手套。
# 注意：它在 setitems.txt 而不是 uniqueitems.txt。
_m = patch("setitems.txt", why="P3 Magnus' Skin：补 20% FHR + hp 30").where(
    "index", eq("Magnus' Skin"))
_m.set("prop6", "balance2")
_m.set("min6", 20)
_m.set("max6", 20)
_m.set("prop7", "hp")
_m.set("min7", 30)
_m.set("max7", 30)


# ============================================================================
# 元素强化：把「4 条 craft 配方」换成「4 件有主题的中阶暗金」
# ============================================================================
# 背景：原版的「元素强化」装备**全部在 req 66~82 的终局段**
# （Griffon's 76 / Nightwing's 67 / Ravenlore 74 / Fathom 73 / Death's Web 66 …），
# req 20~50 之间一件都没有 —— 而**没有任何装备给「毒系技能伤害」**。
#
# 原本这个空档由 `patches/_disabled_cubemain_crafts.py` 的 4 条合成配方填补，
# 但那个整合版不能碰 `CubeMain.txt`（会毁掉人家 75 条自定义公式）。
# 所以改成给 4 件**主题契合、目前没人用**的中阶暗金各加一条，
# 这也是原版自己的做法（Ravenlore / Griffon's / Nightwing's 就是这个套路）。
#
# 槽位刻意分散（靴 / 甲 / 头 / 头），每件只强化**一个**元素 → 可以叠，但不会一件通吃。
# 验收：火系配 `Radiance`（信念 L3）后环境系数 1.18 = 冰法的 86%。

# 火 · 地狱阔步（req 29 靴子，原版就是"走过留火"的主题）
_inf = u("Infernostride", "P3 火系中阶：Infernostride 补 extra-fire 10~15 + pierce-fire 15")
_inf.set("prop10", "extra-fire")
_inf.set("min10", 10)
_inf.set("max10", 15)
_inf.set("prop11", "pierce-fire")
_inf.set("min11", 15)
_inf.set("max11", 15)

# 冰 · 鹰甲（req 15，冰抗/防冰冻主题）—— 冰系本来就强，只给伤害%，不给穿透
_hk = u("Hawkmail", "P3 冰系中阶：Hawkmail 补 extra-cold 10~15")
_hk.set("prop6", "extra-cold")
_hk.set("min6", 10)
_hk.set("max6", 15)

# 电 · 黑角之脸（req 41 头盔，电吸收/电反伤主题）
_bh = u("Blackhorn's Face", "P3 电系中阶：Blackhorn's Face 补 pierce-ltng 15 + extra-ltng 10")
_bh.set("prop7", "pierce-ltng")
_bh.set("min7", 15)
_bh.set("max7", 15)
_bh.set("prop8", "extra-ltng")
_bh.set("min8", 10)
_bh.set("max8", 10)

# 毒 · 虫颅（req 21 头盔，本来就有毒伤）—— 填「全游戏没有 extra-pois」的空白
_ws = u("Wormskull", "P3 毒系中阶：Wormskull 补 extra-pois 20（原版没有任何 extra-pois 装备）")
_ws.set("prop6", "extra-pois")
_ws.set("min6", 20)
_ws.set("max6", 20)
