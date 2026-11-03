# 改动报告

> 由 `tools/build.py` 自动生成，勿手改。基线：`vanilla/`

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
| `Param1` | 1 | `Fire Mastery`: 30 → 24 |
| `Param2` | 1 | `Fire Mastery`: 7 → 4 |
| `Param3` | 1 | `Fire Mastery`: (空) → 7 |
| `Param4` | 1 | `Fire Mastery`: (空) → 2 |
| `passivestat2` | 1 | `Fire Mastery`: (空) → passive_fire_pierce |
| `passivecalc2` | 1 | `Fire Mastery`: (空) → ln34 |
| `*Param1 Description` | 1 | `Fire Mastery`: % Damage bonus → Damage bonus |
| `*Param2 Description` | 1 | `Fire Mastery`: % Damage bonus per level → Damage bonus per level |
| `*Param3 Description` | 1 | `Fire Mastery`: (空) → Enemy fire resist reduction |
| `*Param4 Description` | 1 | `Fire Mastery`: (空) → Enemy fire resist reduction per level |

理由：P2-法师火系：火掌握 伤害163%→100%，并发放 -45% 火穿透（填 passive_fire_pierce 的空口）

## TreasureClassEx.txt

| 列 | 改动行数 | 示例 |
|---|---:|---|
| `Picks` | 79 | `Act 1 (H) Melee A`: 1 → 4；`Act 1 (H) Melee B`: 1 → 4；`Act 2 (H) Melee A`: 1 → 4；…另 76 行 |
| `Prob(Good)` | 28 | `Act 1 (H) Citem A`: 3 → 40；`Act 1 (H) Citem B`: 3 → 40；`Act 1 (H) Citem C`: 3 → 40；…另 25 行 |

理由：L1 暗金怪 Good 4→20：维持「打硬目标更值」的层级；L1 精英怪 Good 3→40：维持「打硬目标更值」的层级（白怪 Picks=4 后要跟上）；L1b 打怪掉落像翻箱子：Picks 1→4；L1b 牛场 Picks 1→4
