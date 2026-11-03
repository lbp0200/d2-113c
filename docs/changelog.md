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

## TreasureClassEx.txt

| 列 | 改动行数 | 示例 |
|---|---:|---|
| `Picks` | 79 | `Act 1 (H) Melee A`: 1 → 2；`Act 1 (H) Melee B`: 1 → 2；`Act 2 (H) Melee A`: 1 → 2；…另 76 行 |
| `Prob(Good)` | 43 | `Act 1 (H) Chest A`: 2 → 0；`Act 1 (H) Chest B`: 2 → 0；`Act 1 (H) Chest C`: 2 → 0；…另 40 行 |
| `Item` | 15 | `Act 1 (H) Super A`: Act 1 (H) Uitem A → Act 1 (H) Equip A；`Act 1 (H) Super B`: Act 1 (H) Uitem B → Act 1 (H) Equip B；`Act 1 (H) Super C`: Act 1 (H) Uitem C → Act 1 (H) Equip C；…另 12 行 |

理由：L1 地狱箱子不再产符文：符文路径全部落到战斗源上；L1 暗金怪 Good 权重 4→8（打硬目标的额外回报）；L1 精英怪 Good 权重 3→6（打硬目标的额外回报）；L1 超箱（Super A/B/C）不再产符文：Uitem→Equip；L1b 打怪掉落像翻箱子：Picks 1→2；L1b 牛场 Picks 1→2
