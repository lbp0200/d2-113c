# 改动报告

> 由 `tools/build.py` 自动生成，勿手改。基线：`vanilla/`

## CubeMain.txt

| 列 | 改动行数 | 示例 |
|---|---:|---|
| `(追加行)` | 4 | `magic helm + jewel + io + gpr -> fire pierce helm`: (空) → magic helm + jewel + io + gpr -> fire pierce helm；`magic helm + jewel + io + gpy -> lightning pierce helm`: (空) → magic helm + jewel + io + gpy -> lightning pierce helm；`magic helm + jewel + io + gpb -> cold pierce helm`: (空) → magic helm + jewel + io + gpb -> cold pierce helm；…另 1 行 |

理由：P2 元素穿透 craft（cold）：给没有掌握技能的职业一条降抗途径；P2 元素穿透 craft（fire）：给没有掌握技能的职业一条降抗途径；P2 元素穿透 craft（lightning）：给没有掌握技能的职业一条降抗途径；P2 元素穿透 craft（poison）：给没有掌握技能的职业一条降抗途径

## MonStats.txt

| 列 | 改动行数 | 示例 |
|---|---:|---|
| `ResFi(H)` | 89 | `zombie4`: 110 → 100；`fallen2`: 110 → 100；`fallen3`: 120 → 100；…另 86 行 |
| `ResLi(H)` | 33 | `skeleton5`: 120 → 100；`zombie2`: 110 → 100；`bighead2`: 105 → 100；…另 30 行 |
| `ResCo(H)` | 124 | `skeleton3`: 110 → 100；`zombie1`: 120 → 100；`brute2`: 120 → 100；…另 121 行 |
| `ResPo(H)` | 86 | `foulcrow2`: 105 → 100；`foulcrow3`: 110 → 100；`sandmaggot1`: 105 → 100；…另 83 行 |

理由：地狱抗性封顶 100：免疫数量不变，但任何降抗都能生效（排除 1000 的设计性绝对免疫）

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
