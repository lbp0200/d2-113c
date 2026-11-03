"""L1b · 打怪掉落"像翻箱子"：给怪物主掉落加抽取次数。

## 发现：怪物和箱子的掉落**构成几乎一模一样**，差的只有 `Picks`

| | gld | Junk | Equip | Good | Picks |
|---|---:|---:|---:|---:|---:|
| `Act 3 (H) Chest B`（A3 箱子） | 35.7% | 35.7% | 23.8% | 4.8% | **4** |
| `Act 5 (H) H2H A`（白怪） | 35.0% | 35.0% | 26.7% | 3.3% | **1** |

所以"让怪物掉得和翻箱子一样"= **把 Picks 提上去**，不需要动构成。

## 但 Picks 直接决定总产出，会撞 P1（毕业时间不变）

`/players 8`，每小时 Good 判定（符文路径）：

| Picks | 白怪 83→ | 牛场 125→ | 说明 |
|---|---:|---:|---|
| **1（现状）** | 83 | 125 | 每次击杀 0.83 件 |
| **2** | **167** | **250** | 每次击杀 1.67 件 |
| 3 | 250 | 375 | |
| 4（=箱子） | 333 | 500 | 是原 LK（213）的 1.6~2.3 倍 |

**取 2 的理由**：白怪 167 + 牛场 250，与原 LK 的 213 同量级 → **P1 保住**。
取 4 会让牛场冲到 500/h（原 LK 的 2.35 倍），毕业后那条长尾会被砍掉一半以上，
违反 N9（不缩短毕业后的刷）。

想改力度就改这一个数字：`MONSTER_PICKS = 2`。
"""

from tools.d2patch import matches, patch

MONSTER_PICKS = 2

# 地狱普通怪物的主掉落 TC（按攻击类型分家族），Picks 1 → MONSTER_PICKS
patch(
    "treasureclassex.txt",
    why=f"L1b 打怪掉落像翻箱子：Picks 1→{MONSTER_PICKS}",
).where(
    "Treasure Class", matches(r"^Act \d \(H\) (H2H|Cast|Miss|Bow|Melee|Skeleton|Wraith) [ABC]$")
).set("Picks", MONSTER_PICKS)

# 牛场同理（它不在 Act 家族命名里）
patch(
    "treasureclassex.txt",
    why=f"L1b 牛场 Picks 1→{MONSTER_PICKS}",
).where(
    "Treasure Class", matches(r"^Cow \(H\)$")
).set("Picks", MONSTER_PICKS)

# 有意不动：`Council (H)`（Picks 已经是 3，崔凡克保持现状）、
# Champ/Unique（Picks 是负数=保证掉落，语义不同）、Super/Chest（已在 economy.py 处理）
