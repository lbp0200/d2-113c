# P1 · 技能本体伤害曲线

> 由 `tools/p1_skills.py` 从 `vanilla/` 生成。只读分析。

**边界**：这里只有 `skills.txt` 里的本体伤害 + 等级增幅，**不含协同加成**
（1.13c 的协同硬编码在 Dll 里，txt 没有任何 syn 列，已核对）、不含掌握/装备、
不含施法速度与多段命中。多段技能（充能弹、多重箭等）会严重低估，请看单位伤害而非总和。

公式：`(base + Σ分段增量) × 2^HitShift / 256`；
已验证对照：火弹 3-6、冰弹 3-5、火球 6-14、充能弹 2-4、牙齿 2-4（均为 1 级）。

### 读表须知：这些技能的伤害列不能直接比大小

- **每帧判定（数字是每帧伤害，实际要乘命中帧数）**：Fire Wall、Inferno、Blaze、Arctic Blast
- **毒素速率（EMin/EMax 是伤害速率，ELen 才是持续时间，不是单次总伤害）**：Poison Dagger、Poison Explosion、Poison Nova、Venom、Poison Javelin
- **光环脉冲（数字是每次脉冲伤害，不是每秒）**：Holy Fire、Holy Freeze、Holy Shock、Sanctuary
- **多发射物（数字是单颗伤害，实际随等级增加数量）**：Charged Bolt、Teeth、Multiple Shot、Strafe

另外，武器系技能（战吼/攻击类）显示的是固定加成部分，实际伤害要乘武器伤害，
见下面单独的表。

## 亚马逊（`ama`，14 个有伤害的技能）

| 技能 | 需等级 | L1 | L10 | L20 | L30 | 法力 | 伤害/法力(L20) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Power Strike | 6 | 1-16 | 1-250 | 1-1006 | 1-2842 | 8 | 62.9 |
| Poison Javelin | 6 | 32-48 | 240-264 | 912-992 | 2576-2744 | 16 | 59.5 |
| Lightning Fury | 30 | 1-40 | 1-280 | 1-940 | 1-2340 | 20 | 23.5 |
| Immolation Arrow | 24 | 12-23 | 166-177 | 652-663 | 1706-1717 | 12 | 54.8 |
| Lightning Bolt | 12 | 1-40 | 1-184 | 1-596 | 1-1736 | 24 | 12.4 |
| Charged Strike | 18 | 1-30 | 1-170 | 1-530 | 1-1258 | 16 | 16.6 |
| Freezing Arrow | 30 | 40-50 | 160-170 | 490-500 | 1164-1174 | 18 | 27.5 |
| Lightning Strike | 30 | 1-25 | 1-145 | 1-475 | 1-1185 | 9 | 26.4 |
| Ice Arrow | 18 | 6-10 | 84-90 | 336-356 | 976-1028 | 16 | 21.6 |
| Exploding Arrow | 12 | 2-6 | 61-67 | 217-241 | 563-639 | 10 | 22.9 |
| Fire Arrow | 1 | 1-4 | 25-28 | 99-106 | 353-392 | 24 | 4.3 |
| Cold Arrow | 6 | 3-4 | 26-27 | 87-90 | 278-292 | 28 | 3.2 |
| Magic Arrow | 1 | 1-1 | 12-12 | 36-36 | 76-76 | 12 | 3.0 |
| Plague Javelin | 18 | 0-0 | 3-3 | 11-11 | 36-37 | 14 | 0.8 |

20 级伤害最低的 5 个：
- `Plague Javelin`：11-11，需等级 18，法力 14
- `Magic Arrow`：36-36，需等级 1，法力 12
- `Cold Arrow`：87-90，需等级 6，法力 28
- `Fire Arrow`：99-106，需等级 1，法力 24
- `Exploding Arrow`：217-241，需等级 12，法力 10

## 法师（`sor`，22 个有伤害的技能）

| 技能 | 需等级 | L1 | L10 | L20 | L30 | 法力 | 伤害/法力(L20) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Meteor | 24 | 80-100 | 365-407 | 1301-1391 | 3525-3695 | 34 | 39.6 |
| Blizzard | 24 | 45-75 | 240-281 | 870-935 | 2340-2445 | 23 | 39.2 |
| Chain Lightning | 18 | 1-40 | 1-165 | 1-465 | 1-1005 | 9 | 25.9 |
| Thunder Storm | 24 | 1-100 | 111-210 | 355-454 | 775-874 | 19 | 21.3 |
| Frozen Orb | 30 | 40-45 | 154-164 | 430-452 | 936-978 | 50 | 8.8 |
| Lightning | 12 | 1-40 | 1-136 | 1-416 | 1-1112 | 16 | 13.0 |
| Ice Blast | 6 | 8-12 | 99-108 | 393-414 | 1107-1148 | 12 | 33.6 |
| Glacial Spike | 18 | 16-24 | 105-118 | 361-386 | 853-898 | 20 | 18.7 |
| Fire Ball | 12 | 6-14 | 88-106 | 324-366 | 814-896 | 10 | 34.5 |
| Nova | 12 | 1-20 | 69-110 | 231-320 | 533-702 | 15 | 18.4 |
| Hydra | 30 | 14-20 | 78-95 | 246-287 | 590-671 | 40 | 6.7 |
| Enchant | 18 | 8-10 | 28-42 | 100-138 | 284-362 | 25 | 4.8 |
| Shiver Armor | 12 | 6-8 | 30-38 | 96-116 | 238-278 | 11 | 9.6 |
| Frost Nova | 6 | 2-4 | 26-34 | 92-112 | 234-274 | 9 | 11.3 |
| Fire Bolt | 1 | 3-6 | 20-26 | 72-90 | 272-322 | 5 | 16.2 |
| Chilling Armor | 24 | 4-6 | 17-24 | 59-78 | 161-200 | 17 | 4.0 |
| Ice Bolt | 1 | 3-5 | 16-24 | 58-78 | 160-200 | 3 | 22.6 |
| Telekinesis | 6 | 1-2 | 12-13 | 36-37 | 76-77 | 7 | 5.2 |
| Fire Wall | 18 | 1-1 | 8-8 | 27-28 | 68-68 | 22 | 1.3 |
| Charged Bolt | 1 | 2-4 | 8-10 | 22-24 | 58-60 | 24 | 0.9 |
| Inferno | 6 | 0-1 | 5-5 | 14-15 | 32-33 | 36 | 0.4 |
| Blaze | 12 | 0-0 | 2-2 | 6-6 | 16-16 | 22 | 0.3 |

20 级伤害最低的 5 个：
- `Blaze`：6-6，需等级 12，法力 22
- `Inferno`：14-15，需等级 6，法力 36
- `Charged Bolt`：22-24，需等级 1，法力 24
- `Fire Wall`：27-28，需等级 18，法力 22
- `Telekinesis`：36-37，需等级 6，法力 7

## 死灵法师（`nec`，7 个有伤害的技能）

| 技能 | 需等级 | L1 | L10 | L20 | L30 | 法力 | 伤害/法力(L20) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Bone Spirit | 30 | 20-30 | 198-219 | 600-645 | 1302-1387 | 24 | 25.9 |
| FireGolem | 30 | 10-27 | 111-139 | 345-397 | 767-859 | 50 | 7.4 |
| Bone Spear | 18 | 16-24 | 106-114 | 324-336 | 806-838 | 28 | 11.8 |
| Teeth | 1 | 2-4 | 13-16 | 39-49 | 95-120 | 6 | 7.3 |
| Poison Nova | 30 | 1-2 | 4-5 | 12-13 | 33-34 | 20 | 0.6 |
| Poison Explosion | 18 | 0-2 | 2-3 | 7-8 | 20-21 | 8 | 1.0 |
| Poison Dagger | 6 | 0-0 | 1-1 | 4-4 | 9-9 | 12 | 0.3 |

20 级伤害最低的 5 个：
- `Poison Dagger`：4-4，需等级 6，法力 12
- `Poison Explosion`：7-8，需等级 18，法力 8
- `Poison Nova`：12-13，需等级 30，法力 20
- `Teeth`：39-49，需等级 1，法力 6
- `Bone Spear`：324-336，需等级 18，法力 28

## 圣骑士（`pal`，8 个有伤害的技能）

| 技能 | 需等级 | L1 | L10 | L20 | L30 | 法力 | 伤害/法力(L20) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fist of the Heavens | 30 | 150-200 | 345-395 | 975-1025 | 2445-2495 | 25 | 40.0 |
| Holy Bolt | 6 | 8-16 | 100-110 | 332-360 | 810-890 | 32 | 10.8 |
| Blessed Hammer | 18 | 12-16 | 104-108 | 332-336 | 764-768 | 20 | 16.7 |
| Holy Shock | 24 | 1-10 | 1-80 | 1-260 | 1-626 | 0 | 0.0 |
| Sanctuary | 24 | 8-16 | 52-62 | 152-176 | 334-388 | 1 | 164.0 |
| Holy Shield | 24 | 3-6 | 27-30 | 93-96 | 223-226 | 35 | 2.7 |
| Holy Freeze | 18 | 2-3 | 15-16 | 57-58 | 159-160 | 0 | 0.0 |
| Holy Fire | 6 | 1-3 | 8-10 | 28-30 | 86-88 | 0 | 0.0 |

20 级伤害最低的 5 个：
- `Holy Fire`：28-30，需等级 6，法力 0
- `Holy Freeze`：57-58，需等级 18，法力 0
- `Holy Shield`：93-96，需等级 24，法力 35
- `Sanctuary`：152-176，需等级 24，法力 1
- `Holy Shock`：1-260，需等级 24，法力 0

## 野蛮人（`bar`，1 个有伤害的技能）

| 技能 | 需等级 | L1 | L10 | L20 | L30 | 法力 | 伤害/法力(L20) |
|---|---:|---:|---:|---:|---:|---:|---:|
| War Cry | 30 | 20-30 | 88-98 | 250-260 | 552-562 | 10 | 25.5 |

20 级伤害最低的 5 个：
- `War Cry`：250-260，需等级 30，法力 10

## 德鲁伊（`dru`，17 个有伤害的技能）

| 技能 | 需等级 | L1 | L10 | L20 | L30 | 法力 | 伤害/法力(L20) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Armageddon | 30 | 29-91 | 252-329 | 834-963 | 2042-2289 | 35 | 25.7 |
| Summon Grizzly | 30 | 30-60 | 150-180 | 480-510 | 1198-1228 | 40 | 12.4 |
| Molten Boulder | 6 | 12-24 | 112-146 | 412-494 | 1104-1266 | 20 | 22.6 |
| Tornado | 24 | 25-35 | 125-137 | 425-451 | 1093-1149 | 10 | 43.8 |
| Fire Claws | 18 | 15-20 | 111-116 | 391-404 | 1043-1100 | 4 | 99.4 |
| Plague Poppy | 1 | 12-16 | 99-103 | 349-353 | 863-867 | 8 | 43.9 |
| Hurricane | 30 | 25-50 | 108-133 | 326-351 | 760-785 | 30 | 11.3 |
| Eruption | 12 | 15-25 | 93-103 | 337-347 | 865-885 | 15 | 22.8 |
| Volcano | 24 | 16-20 | 68-72 | 236-240 | 646-654 | 25 | 9.5 |
| Shock Wave | 24 | 10-20 | 47-57 | 155-165 | 375-385 | 7 | 22.9 |
| Summon Fenris | 18 | 7-12 | 31-36 | 105-110 | 301-318 | 20 | 5.4 |
| Twister | 18 | 6-8 | 31-33 | 106-110 | 279-293 | 7 | 15.4 |
| Summon Spirit Wolf | 6 | 2-6 | 15-19 | 61-65 | 187-191 | 15 | 4.2 |
| Raven | 1 | 2-4 | 13-15 | 37-39 | 77-79 | 6 | 6.3 |
| Arctic Blast | 6 | 0-1 | 3-3 | 10-10 | 22-23 | 24 | 0.4 |
| Rabies | 18 | 0-0 | 2-2 | 5-6 | 14-14 | 10 | 0.5 |
| Firestorm | 1 | 0-0 | 1-1 | 2-3 | 7-8 | 4 | 0.6 |

20 级伤害最低的 5 个：
- `Firestorm`：2-3，需等级 1，法力 4
- `Rabies`：5-6，需等级 18，法力 10
- `Arctic Blast`：10-10，需等级 6，法力 24
- `Raven`：37-39，需等级 1，法力 6
- `Summon Spirit Wolf`：61-65，需等级 6，法力 15

## 刺客（`ass`，16 个有伤害的技能）

| 技能 | 需等级 | L1 | L10 | L20 | L30 | 法力 | 伤害/法力(L20) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claws of Thunder | 18 | 1-80 | 1-340 | 1-1180 | 1-3220 | 4 | 147.6 |
| Lightning Sentry | 24 | 1-20 | 1-142 | 1-498 | 1-1358 | 20 | 12.5 |
| Death Sentry | 30 | 1-50 | 1-150 | 1-458 | 1-1190 | 20 | 11.5 |
| Blades of Ice | 24 | 15-35 | 107-127 | 367-395 | 1067-1135 | 3 | 127.0 |
| Fists of Fire | 6 | 6-10 | 71-77 | 301-325 | 971-1057 | 2 | 156.5 |
| Blade Shield | 30 | 1-30 | 58-87 | 196-225 | 446-475 | 27 | 7.8 |
| Shock Field | 6 | 1-10 | 1-49 | 1-179 | 1-531 | 6 | 15.0 |
| Fire Trauma | 1 | 3-4 | 24-38 | 120-166 | 484-608 | 24 | 5.9 |
| Blade Fury | 18 | 8-10 | 45-47 | 157-159 | 397-399 | 8 | 19.8 |
| Mind Blast | 24 | 10-20 | 38-48 | 140-150 | 370-380 | 15 | 9.7 |
| Charged Bolt Sentry | 12 | 1-7 | 1-42 | 1-136 | 1-338 | 13 | 5.3 |
| Blade Sentinel | 6 | 6-10 | 41-45 | 131-135 | 301-305 | 7 | 19.0 |
| Psychic Hammer | 1 | 2-6 | 26-41 | 92-131 | 234-313 | 16 | 7.0 |
| Wake of Fire Sentry | 12 | 5-10 | 29-34 | 99-108 | 273-302 | 13 | 8.0 |
| Venom | 30 | 6-8 | 24-26 | 68-70 | 160-162 | 12 | 5.8 |
| Inferno Sentry | 24 | 1-3 | 13-17 | 44-50 | 105-116 | 20 | 2.3 |

20 级伤害最低的 5 个：
- `Inferno Sentry`：44-50，需等级 24，法力 20
- `Venom`：68-70，需等级 30，法力 12
- `Wake of Fire Sentry`：99-108，需等级 12，法力 13
- `Psychic Hammer`：92-131，需等级 1，法力 16
- `Blade Sentinel`：131-135，需等级 6，法力 7

## 掌握结构审计：谁在给「降抗」，谁只给「加伤害」

`itemstatcost.txt` 里八个 `passive_*` stat 全都存在，`skills.txt` 通过 `passivestat1..5` + `passivecalc1..5` 发放。把发放者列出来，问题一目了然：

| stat | 发放它的技能 | 公式 | L20 数值 |
|---|---|---|---:|
| `passive_fire_mastery` | `Fire Mastery`、`Hydra` | `ln12` | +163% |
| `passive_fire_pierce` | `Hydra` | `stat('passive_fire_pierce'.accr)` | — |
| `passive_cold_mastery` | **无人发放** | — | — |
| `passive_cold_pierce` | `Cold Mastery` | `ln12` | -115% |
| `passive_ltng_mastery` | `Lightning Mastery` | `ln12` | +278% |
| `passive_ltng_pierce` | **无人发放** | — | — |
| `passive_pois_mastery` | **无人发放** | — | — |
| `passive_pois_pierce` | **无人发放** | — | — |

### 对高抗性怪的**实际**伤害倍率（掌握满级 20 级）

倍率 = `(1 + 伤害加成%) × (1 - 最终抗性/100)`，最终抗性下限 -100%。

| 怪物抗性 | 火系 | 冰系 | 电系 | 毒系 |
|---|---:|---:|---:|---:|
| 0% | 2.63× | 2.00× | 3.78× | 1.00× |
| 50% | 1.31× | 1.65× | 1.89× | 0.50× |
| 75% | 0.66× | 1.40× | 0.94× | 0.25× |
| 90% | 0.26× | 1.25× | 0.38× | 0.10× |
| 99% | 0.03× | 1.16× | 0.04× | 0.01× |

**读法**：抗性 0% 时火/电靠「加伤害」是赢的；一旦怪物抗性上到 75% 以上，
只剩冰系靠降抗还能维持输出。抗性越高差距越大——这就是「地狱里火系打不动」的数学原因。

## 降抗审计：全游戏只有三个技能能降低「敌人」的抗性

免疫（抗性 ≥100）只能靠降抗打破，而且对免疫怪只按 1/5 生效。
所以「自带降抗」是 1.13c 里最稀缺的资源——把 txt 里所有降抗技能列出来：

| 技能 | 职业 | 需等级 | 作用元素 | 公式 | L1 | L20 | 破免疫上限(≈L20/5) |
|---|---|---|---|---|---:|---:|---:|
| Conviction | 圣骑士 | 30 | 火 | `"-min(ln34,150)"` | -30% | **-125%** | 125% 抗性 |
| Conviction | 圣骑士 | 30 | 冰 | `"-min(ln34,150)"` | -30% | **-125%** | 125% 抗性 |
| Conviction | 圣骑士 | 30 | 电 | `"-min(ln34,150)"` | -30% | **-125%** | 125% 抗性 |
| Cold Mastery | 法师 | 30 | 冰 | `ln12` | -20% | **-115%** | 123% 抗性 |
| Lower Resist | 死灵法师 | 30 | 火 | `-dm56` | -25% | **-70%** | 114% 抗性 |
| Lower Resist | 死灵法师 | 30 | 电 | `-dm56` | -25% | **-70%** | 114% 抗性 |
| Lower Resist | 死灵法师 | 30 | 冰 | `-dm56` | -25% | **-70%** | 114% 抗性 |
| Lower Resist | 死灵法师 | 30 | 毒 | `-dm56` | -25% | **-70%** | 114% 抗性 |

**竖着读这一列「作用元素」**：火、电、毒 的降抗都不在法师手里，
只存在于死灵的诅咒和圣骑士的光环里。**法师自己只有冰系能降抗。**

> ⚠ 冰掌握能不能破免疫，社区有争议（普遍认为不能，只有信念/降抗可以）。
> 上表的「破免疫上限」是按 txt 数值 + 1/5 规则算的理论值，进游戏要验。

> 📌 解析坑：含逗号的公式在 txt 里被**双引号包住**（如 `"-min(ln34,150)"`，因为文件是 CSV 风格）。读的时候要 strip 掉引号，
否则字符串比较永远不匹配。

## 毒系：`EMin/EMax` 是速率，不是总量

毒系技能的伤害列是**每帧伤害速率**，`ELen` 是持续时间（单位：帧，25 帧 = 1 秒）。
所以 **总量 = 速率 × 持续帧数**。主表里毒系那一列若当成「单次伤害」去和火球比，
会低估一个数量级 —— 这是 1.13c 最容易被误读的一组列。

| 技能 | L20 每帧速率 | 持续（帧） | L20 总量 | 法力 | 总量/法力 |
|---|---:|---:|---:|---:|---:|
| Plague Javelin | 10.9-11.1 | — | —（时长随等级增长，不可离线核算） | 14 | — |
| Poison Dagger | 3.7-3.8 | — | —（时长随等级增长，不可离线核算） | 12 | — |
| Poison Explosion | 7.4-8.4 | — | —（时长随等级增长，不可离线核算） | 8 | — |
| Poison Nova | 12.5-13.3 | 50 | **625-666** | 20 | 32.3 |
| Rabies | 5.3-5.6 | — | —（时长随等级增长，不可离线核算） | 10 | — |
| Venom | 68.5-70.5 | 10 | **685-705** | 12 | 57.9 |

> 未列入（`HitShift` 为空、不是常规每帧伤害列）：`Poison Javelin`、`Plague Poppy`

> 对照：骨系 `Bone Spirit` L20 是 **600-645 一次性**、24 法力 → 25.9 伤害/法力。
> `Poison Nova` 的总量和它同档，但**摊在 2 秒里、而且是全屏**。
> 所以毒的定位不是「打得快」，是「放一次走人」。

## 武器百分比技能（伤害取决于武器，`skills.txt` 只有百分比）

`SrcDam` = 使用的武器伤害百分比。这些技能的实际伤害 = 武器伤害 × SrcDam%
（+ 少量固定附加）。所以改它们的伤害要改 `weapons.txt` 或 `SrcDam`，
不能只改 `skills.txt` 的 MinDam/MaxDam。

| 技能 | 职业 | 需等级 | SrcDam% | 法力 |
|---|---|---:|---:|---:|
| Fend | 亚马逊 | 24 | 128 | 5 |
| Guided Arrow | 亚马逊 | 18 | 128 | 32 |
| Impale | 亚马逊 | 12 | 128 | 3 |
| Jab | 亚马逊 | 1 | 128 | 8 |
| Multiple Shot | 亚马逊 | 6 | 96 | 4 |
| Strafe | 亚马逊 | 24 | 96 | 11 |
| Cobra Strike | 刺客 | 12 | 128 | 2 |
| Dragon Claw | 刺客 | 6 | 128 | 2 |
| Royal Strike | 刺客 | 30 | 128 | 4 |
| Tiger Strike | 刺客 | 1 | 128 | 1 |
| Bash | 野蛮人 | 1 | 128 | 2 |
| Berserk | 野蛮人 | 30 | 128 | 4 |
| Concentrate | 野蛮人 | 18 | 128 | 2 |
| Double Swing | 野蛮人 | 6 | 128 | 8 |
| Double Throw | 野蛮人 | 12 | 128 | 1 |
| Frenzy | 野蛮人 | 24 | 128 | 3 |
| Leap Attack | 野蛮人 | 18 | 128 | 9 |
| Stun | 野蛮人 | 12 | 128 | 2 |
| Whirlwind | 野蛮人 | 30 | 128 | 25 |
| Feral Rage | 德鲁伊 | 12 | 128 | 3 |
| Fury | 德鲁伊 | 30 | 128 | 4 |
| Hunger | 德鲁伊 | 24 | 128 | 3 |
| Maul | 德鲁伊 | 12 | 128 | 3 |
| Wearbear | 德鲁伊 | 6 | 128 | 15 |
| Wearwolf | 德鲁伊 | 1 | 128 | 15 |
| Charge | 圣骑士 | 12 | 128 | 9 |
| Conversion | 圣骑士 | 24 | 128 | 4 |
| Sacrifice | 圣骑士 | 1 | 128 | 0 |
| Vengeance | 圣骑士 | 18 | 128 | 16 |
| Zeal | 圣骑士 | 12 | 128 | 2 |

## 伤害不在 `skills.txt` 里的技能

这些技能在 `skills.txt` 的伤害列是空的 —— 真实伤害来自 `Missiles.txt`
（弹道伤害）或纯硬编码，改 `skills.txt` 对它们无效，需要去改 `missiles.txt`。

- **亚马逊**：Inner Sight、Critical Strike、Dodge、Slow Missiles、Avoid、Penetrate、Dopplezon、Evade、Valkyrie、Pierce
- **法师**：Warmth、Frozen Armor、Static Field、Teleport、Energy Shield、Fire Mastery、Lightning Mastery、Cold Mastery
- **死灵法师**：Amplify Damage、Bone Armor、Skeleton Mastery、Raise Skeleton、Dim Vision、Weaken、Corpse Explosion、Clay Golem、Iron Maiden、Terror、Bone Wall、Golem Mastery、Raise Skeletal Mage、Confuse、Life Tap、BloodGolem、Attract、Decrepify、Bone Prison、Summon Resist、IronGolem、Lower Resist、Revive
- **圣骑士**：Smite、Might、Prayer、Resist Fire、Thorns、Defiance、Resist Cold、Blessed Aim、Cleansing、Resist Lightning、Concentration、Vigor、Meditation、Fanaticism、Conviction、Redemption、Salvation
- **野蛮人**：Sword Mastery、Axe Mastery、Mace Mastery、Howl、Find Potion、Leap、Pole Arm Mastery、Throwing Mastery、Spear Mastery、Taunt、Shout、Increased Stamina、Find Item、Iron Skin、Battle Cry、Increased Speed、Battle Orders、Grim Ward、Natural Resistance、Battle Command
- **德鲁伊**：Shape Shifting、Oak Sage、Cycle of Life、Cyclone Armor、Heart of Wolverine、Vines、Spirit of Barbs
- **刺客**：Claw Mastery、Dragon Talon、Quickness、Weapon Block、Cloak of Shadows、Fade、Shadow Warrior、Dragon Tail、Dragon Flight、Shadow Master
