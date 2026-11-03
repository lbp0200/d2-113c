# 改动报告

> 由 `tools/build.py` 自动生成，勿手改。基线：`vanilla/`

## Hireling.txt

| 列 | 改动行数 | 示例 |
|---|---:|---|
| `HP` | 3 | `Eastern Sorceror-Fire-Hell-21-100-3-79`: 863 → 1165；`Eastern Sorceror-Cold-Hell-22-100-3-79`: 863 → 1165；`Eastern Sorceror-Ltng-Hell-23-100-3-79`: 863 → 1165 |
| `HP/Lvl` | 3 | `Eastern Sorceror-Fire-Hell-21-100-3-79`: 27 → 36；`Eastern Sorceror-Cold-Hell-22-100-3-79`: 27 → 36；`Eastern Sorceror-Ltng-Hell-23-100-3-79`: 27 → 36 |
| `Gold` | 5 | `Eastern Sorceror-Fire-Hell-21-100-3-79`: 21000 → 12000；`Eastern Sorceror-Cold-Hell-22-100-3-79`: 27000 → 12000；`Eastern Sorceror-Ltng-Hell-23-100-3-79`: 21000 → 12000；…另 2 行 |

理由：B1 A3 铁狼地狱档 HP ×1.35（1025 → 1381 @85，= A2 的 85%）；B1b A3 铁狼雇价统一 12000（原 21000/27000/21000，比 A2 贵 40%）；B2 A5 野蛮人雇价 32000→15000（血只差 A2 12%，却贵 113%）；不加光环

## MonStats.txt

| 列 | 改动行数 | 示例 |
|---|---:|---|
| `ResFi(H)` | 89 | `zombie4`: 110 → 100；`fallen2`: 110 → 100；`fallen3`: 120 → 100；…另 86 行 |
| `ResLi(H)` | 33 | `skeleton5`: 120 → 100；`zombie2`: 110 → 100；`bighead2`: 105 → 100；…另 30 行 |
| `ResCo(H)` | 124 | `skeleton3`: 110 → 100；`zombie1`: 120 → 100；`brute2`: 120 → 100；…另 121 行 |
| `ResPo(H)` | 86 | `foulcrow2`: 105 → 100；`foulcrow3`: 110 → 100；`sandmaggot1`: 105 → 100；…另 83 行 |

理由：地狱抗性封顶 100：免疫数量不变，但任何降抗都能生效（排除 1000 的设计性绝对免疫）

## Runes.txt

| 列 | 改动行数 | 示例 |
|---|---:|---|
| `T1Code1` | 1 | `Runeword116`: light → aura |
| `T1Param1` | 1 | `Runeword116`: (空) → Conviction |
| `T1Min1` | 1 | `Runeword116`: 5 → 3 |
| `T1Max1` | 1 | `Runeword116`: 5 → 3 |
| `T1Code3` | 2 | `Runeword154`: charged → pierce-pois；`Runeword88`: light → mana |
| `T1Param3` | 1 | `Runeword154`: 83 →  |
| `T1Min3` | 2 | `Runeword154`: 27 → 15；`Runeword88`: -3 → 20 |
| `T1Max3` | 2 | `Runeword154`: 15 → 20；`Runeword88`: -3 → 20 |
| `T1Code4` | 1 | `Runeword154`: charged → pois-len |
| `T1Param4` | 1 | `Runeword154`: 92 →  |
| `T1Min4` | 1 | `Runeword154`: 11 → -50 |
| `T1Max4` | 1 | `Runeword154`: 13 → -50 |
| `T1Code5` | 1 | `Runeword88`: gold% → regen-mana |
| `T1Min5` | 1 | `Runeword88`: -33 → 25 |
| `T1Max5` | 1 | `Runeword88`: -33 → 25 |

理由：P3 中间层降抗：Radiance 的『光环半径 +5』换成『信念 L3（−40%）』（补噩梦→地狱之间的降抗空档，见 docs/p3-runes-plan.md）；P3 天底重做：去掉两条负面（light -3 / gold -33），换成 +法力 与 回蓝；P3 毒液重做：两个凑数充能 → pierce-pois 15~20 + pois-len -50 帧（毒更快跳完，总量不变；不超死亡之网）

## SetItems.txt

| 列 | 改动行数 | 示例 |
|---|---:|---|
| `prop6` | 1 | `Magnus' Skin`: (空) → balance2 |
| `min6` | 1 | `Magnus' Skin`: (空) → 20 |
| `max6` | 1 | `Magnus' Skin`: (空) → 20 |
| `prop7` | 1 | `Magnus' Skin`: (空) → hp |
| `min7` | 1 | `Magnus' Skin`: (空) → 30 |
| `max7` | 1 | `Magnus' Skin`: (空) → 30 |

理由：P3 Magnus' Skin：补 20% FHR + hp 30

## Skills.txt

| 列 | 改动行数 | 示例 |
|---|---:|---|
| `Param1` | 2 | `Fire Mastery`: 30 → 24；`Lightning Mastery`: 50 → 29 |
| `Param2` | 2 | `Fire Mastery`: 7 → 4；`Lightning Mastery`: 12 → 9 |
| `Param3` | 2 | `Fire Mastery`: (空) → 7；`Lightning Mastery`: (空) → 6 |
| `Param4` | 2 | `Fire Mastery`: (空) → 2；`Lightning Mastery`: (空) → 1 |
| `passivestat2` | 2 | `Fire Mastery`: (空) → passive_fire_pierce；`Lightning Mastery`: (空) → passive_ltng_pierce |
| `passivecalc2` | 2 | `Fire Mastery`: (空) → ln34；`Lightning Mastery`: (空) → ln34 |
| `*Param1 Description` | 2 | `Fire Mastery`: % Damage bonus → Damage bonus；`Lightning Mastery`: % Damage bonus → Damage bonus |
| `*Param2 Description` | 2 | `Fire Mastery`: % Damage bonus per level → Damage bonus per level；`Lightning Mastery`: % Damage bonus per level → Damage bonus per level |
| `*Param3 Description` | 2 | `Fire Mastery`: (空) → Enemy fire resist reduction；`Lightning Mastery`: (空) → Enemy lightning resist reduction |
| `*Param4 Description` | 2 | `Fire Mastery`: (空) → Enemy fire resist reduction per level；`Lightning Mastery`: (空) → Enemy lightning resist reduction per level |
| `mana` | 5 | `Armageddon`: 35 → 25；`Volcano`: 25 → 16；`Poison Nova`: 20 → 16；…另 2 行 |
| `EMin` | 4 | `Armageddon`: 25 → 31；`Volcano`: 8 → 10；`Poison Nova`: 16 → 20；…另 1 行 |
| `EMax` | 4 | `Armageddon`: 75 → 94；`Volcano`: 10 → 13；`Poison Nova`: 29 → 36；…另 1 行 |
| `EMinLev1` | 4 | `Armageddon`: 15 → 19；`Volcano`: 2 → 3；`Poison Nova`: 4 → 5；…另 1 行 |
| `EMinLev2` | 4 | `Armageddon`: 20 → 25；`Volcano`: 4 → 5；`Poison Nova`: 6 → 8；…另 1 行 |
| `EMinLev3` | 4 | `Armageddon`: 25 → 31；`Volcano`: 6 → 8；`Poison Nova`: 9 → 11；…另 1 行 |
| `EMinLev4` | 4 | `Armageddon`: 31 → 39；`Volcano`: 8 → 10；`Poison Nova`: 14 → 18；…另 1 行 |
| `EMinLev5` | 4 | `Armageddon`: 38 → 48；`Volcano`: 11 → 14；`Poison Nova`: 16 → 20；…另 1 行 |
| `EMaxLev1` | 4 | `Armageddon`: 16 → 20；`Volcano`: 2 → 3；`Poison Nova`: 4 → 5；…另 1 行 |
| `EMaxLev2` | 4 | `Armageddon`: 22 → 28；`Volcano`: 4 → 5；`Poison Nova`: 6 → 8；…另 1 行 |
| `EMaxLev3` | 4 | `Armageddon`: 27 → 34；`Volcano`: 6 → 8；`Poison Nova`: 9 → 11；…另 1 行 |
| `EMaxLev4` | 4 | `Armageddon`: 34 → 42；`Volcano`: 8 → 10；`Poison Nova`: 14 → 18；…另 1 行 |
| `EMaxLev5` | 4 | `Armageddon`: 40 → 50；`Volcano`: 13 → 17；`Poison Nova`: 16 → 20；…另 1 行 |
| `SrcDam` | 2 | `Multiple Shot`: 96 → 128；`Strafe`: 96 → 128 |
| `LevToHit` | 2 | `Multiple Shot`: (空) → 10；`Strafe`: (空) → 10 |

理由：P2-亚马逊元素弓：Cold Arrow 法力 → 12（原法力曲线倒挂：低阶比高阶贵一倍多）；P2-亚马逊元素弓：Fire Arrow 法力 → 8（原法力曲线倒挂：低阶比高阶贵一倍多）；P2-亚马逊物理弓：Multiple Shot SrcDam 96→128、补 LevToHit 10（与近战技能一致；实测物理弓伤害过低）；P2-亚马逊物理弓：Strafe SrcDam 96→128、补 LevToHit 10（与近战技能一致；实测物理弓伤害过低）；P2-刺客火陷阱：Inferno Sentry 伤害 ×3.2（同档同类陷阱里只有雷光守卫的 1/5）；P2-德鲁伊火系：Armageddon 法力 35→25、伤害 ×1.25；P2-德鲁伊火系：Volcano 法力 25→16、伤害 ×1.30；P2-死灵毒系：Poison Nova 法力 20→16、毒速率 ×1.25（定位 M2 全屏清场）；P2-法师火系：火掌握 伤害163%→100%，并发放 -45% 火穿透（填 passive_fire_pierce 的空口）；P2-法师电系：电掌握 +278%→+200%，并发放 -25% 电穿透（等价交换；高抗段 0.94/0.38→1.50/1.05，免疫墙不变）

## TreasureClassEx.txt

| 列 | 改动行数 | 示例 |
|---|---:|---|
| `Picks` | 79 | `Act 1 (H) Melee A`: 1 → 4；`Act 1 (H) Melee B`: 1 → 4；`Act 2 (H) Melee A`: 1 → 4；…另 76 行 |
| `Prob(Good)` | 28 | `Act 1 (H) Citem A`: 3 → 40；`Act 1 (H) Citem B`: 3 → 40；`Act 1 (H) Citem C`: 3 → 40；…另 25 行 |

理由：L1 暗金怪 Good 4→20：维持「打硬目标更值」的层级；L1 精英怪 Good 3→40：维持「打硬目标更值」的层级（白怪 Picks=4 后要跟上）；L1b 打怪掉落像翻箱子：Picks 1→4；L1b 牛场 Picks 1→4

## UniqueItems.txt

| 列 | 改动行数 | 示例 |
|---|---:|---|
| `prop7` | 5 | `Steelpillar`: (空) → ease；`Venomsward`: (空) → regen；`Heavenly Garb`: (空) → hp；…另 2 行 |
| `min7` | 5 | `Steelpillar`: (空) → -25；`Venomsward`: (空) → 15；`Heavenly Garb`: (空) → 30；…另 2 行 |
| `max7` | 5 | `Steelpillar`: (空) → -25；`Venomsward`: (空) → 15；`Heavenly Garb`: (空) → 30；…另 2 行 |
| `prop6` | 5 | `Venomsward`: (空) → hp；`Heavenly Garb`: att-undead → att-demon；`Gravepalm`: (空) → crush；…另 2 行 |
| `min6` | 5 | `Venomsward`: (空) → 40；`Gravepalm`: (空) → 10；`Razortine`: 30 → 60；…另 2 行 |
| `max6` | 5 | `Venomsward`: (空) → 60；`Gravepalm`: (空) → 10；`Razortine`: 50 → 80；…另 2 行 |
| `prop5` | 1 | `Heavenly Garb`: dmg-undead → dmg-demon |
| `min3` | 1 | `Hawkmail`: 15 → 30 |
| `max3` | 1 | `Hawkmail`: 15 → 30 |
| `min5` | 1 | `Hawkmail`: 10 → 25 |
| `max5` | 1 | `Hawkmail`: 10 → 25 |
| `prop10` | 1 | `Infernostride`: (空) → extra-fire |
| `min10` | 1 | `Infernostride`: (空) → 10 |
| `max10` | 1 | `Infernostride`: (空) → 15 |
| `prop11` | 1 | `Infernostride`: (空) → pierce-fire |
| `min11` | 1 | `Infernostride`: (空) → 15 |
| `max11` | 1 | `Infernostride`: (空) → 15 |
| `prop8` | 1 | `Blackhorn's Face`: (空) → extra-ltng |
| `min8` | 1 | `Blackhorn's Face`: (空) → 10 |
| `max8` | 1 | `Blackhorn's Face`: (空) → 10 |

理由：P3 Gravepalm：补 crush 10（低阶 CB 手套）；P3 Hawkmail：冰抗 15→30、跑速 10→25；P3 Heavenly Garb：对不死 → 对恶魔 + hp 30；P3 Razortine：伤害 30-50→60-80、ease -20%；P3 Steelpillar：力需 165 举不起来 → ease -25%；P3 Venomsward：只有毒抗 → 补 hp 50 + regen 15；P3 冰系中阶：Hawkmail 补 extra-cold 10~15；P3 毒系中阶：Wormskull 补 extra-pois 20（原版没有任何 extra-pois 装备）；P3 火系中阶：Infernostride 补 extra-fire 10~15 + pierce-fire 15；P3 电系中阶：Blackhorn's Face 补 pierce-ltng 15 + extra-ltng 10
