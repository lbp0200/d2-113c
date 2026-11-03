"""L1 · 让"打硬目标"比"打白怪"更值：维持掉落层级。

## 已定参数（2025-11，第二版）

- **P1 毕业时间：不再坚持"不变"**（见下面的取舍说明）
- **P2 不提难度**
- **P3 允许加法**

## 取舍说明（重要）

第一版的做法是「削箱子」：把地狱箱子/超箱的符文路径砍掉，让符文只从战斗来。
**这个做法被否掉了**，改为「把怪物提到箱子的绝对水平」（`patches/drops.py` 把
地狱怪物主掉落的 `Picks` 从 1 提到 4，等于箱子的抽取次数）。

后果要说清楚：**总产出上升，毕业时间缩短**。箱子保持原样也存在，
所以"零战斗的高频源"仍然存在。这是有意接受的代价——换来的是"打怪明显更爽"。

## 本文件负责的事：别让层级崩掉

白怪 `Picks=4` 之后 Good/事件 从 2.78% 涨到 **11.11%**，反而超过了原来的
精英（1.50%）和暗金（6.45%）—— **打白怪会变成比打暗金更赚**，这跟 S2 相反。

所以要跟着把精英/暗金的 `Good` 权重提上来，维持 `白怪 < 精英 < 暗金`：

| | Good/事件 | 说明 |
|---|---:|---|
| 白怪（Picks=4 后） | 11.11% | 基准 |
| 精英 `Citem` 3→40 | 14.71% | 比白怪高 32% |
| 暗金 `Uitem` 4→20 | 25.64% | 比白怪高 131% |

**箱子（`Chest` / `Super`）一律不动。**
"""

from tools.d2patch import matches, patch

# 精英怪：Good 3 → 25
patch(
    "treasureclassex.txt",
    why="L1 精英怪 Good 3→40：维持「打硬目标更值」的层级（白怪 Picks=4 后要跟上）",
).where(
    "Treasure Class", matches(r"^Act \d \(H\) Citem [ABC]$")
).item_prob(r"Good$", 40, label="Prob(Good)")

# 暗金怪：Good 4 → 20
patch(
    "treasureclassex.txt",
    why="L1 暗金怪 Good 4→20：维持「打硬目标更值」的层级",
).where(
    "Treasure Class", matches(r"^Act \d \(H\) Uitem [ABC]$")
).item_prob(r"Good$", 20, label="Prob(Good)")
