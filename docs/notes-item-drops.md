# 笔记：地狱会不会掉普通底材？（以水晶剑为例）

> 数据源：`TreasureClassEx.txt` / `Weapons.txt` / `ItemTypes.txt`（vanilla 1.13c）。
> 工具：`tools/d2tc.py`（TC 展开，已按表头严格配对，见文末「踩坑」）。

## 结论

**会掉，而且是地狱白装的绝对大头。** 地狱装备掉落里，**低阶底材（武器/护甲等级 ≤30）占 49%~59%**，
精英档只占 11%~26%。这正是"都打到地狱了还满地垃圾"的数据解释。

但"能掉"和"能用"是两件事 —— 见 §4。

## 1. 机制：`weapN` / `armoN` 是按物品等级分带，不是按物品名

`TreasureClassEx.txt` 里查不到 `weap3`、`weap54` 这些行。它们是游戏**按物品的 `level` 自动生成**的带：

```
weapN  =   Weapons.txt 里 level 落在 (N-3, N] 区间的武器
armoN  =   Armor.txt   同理
```

所以 N 是**带上限**，带宽 3。举例：

| 带 | 包含（`level`） |
|---|---|
| `weap3` | Club(1)、Javelin(1)、Short Bow(1)、Short Staff(1)… |
| `weap12` | Pilum(10)、Two-Handed Sword(10)、**Crystal Sword(11)**、Falchion(11)、Voulge(11)、Broad Axe(12)… 共 11 项 |
| `weap54` | Gothic Bow(52)、Truncheon(52)、Martel de Fer(53)、Chu-Ko-Nu(54)、Executioner Sword(54)… |
| `weap87` | Archon Staff(85)、Berserker Axe(85)、Colossus Blade(85)、Giant Thresher(85)… |

> ⚠ `weapons.txt` 里普通/扩展/精英三档是**各自独立的行**，各有自己的 `level`。
> 所以同一个带里可能混着不同档位的物品 —— 带号不等于档位。

## 2. 地狱的装备 TC 是"长链降级"，所以长尾拖到最底层

`Act 1 (H) Equip A` 直接引用的是 `weap54/57/60/63`，但它的条目里有一条**权重极大的降级链**：

```
Act 1 (H) Equip A → Act 5 (N) Equip C → Act 5 (N) Equip B → … →
Act 1 (N) Equip A → Act 5 Equip C → … → Act 1 Equip C → weap3
```

24 跳。所以低阶底材虽然"离得很远"，但因为每一跳的降级权重都远大于高档权重，
**最终分布反而是低阶占多数**。

实测（每个物品槽的期望分布）：

| 根 TC | 低阶 ≤30 | 中阶 33~51 | 高阶 ≥54 | 其中 `weap12` |
|---|---:|---:|---:|---:|
| `Act 1 Equip C`（普通 Act1 后期） | 100% | 0% | 0% | 5.56% |
| `Act 1 (N) Equip A`（噩梦 Act1） | 80.6% | 19.4% | 0% | 6.62% |
| `Act 1 (H) Equip A`（地狱 Act1） | **59.4%** | 29.9% | 10.6% | 4.86% |
| `Act 5 (H) Equip A`（地狱 Act5） | **49.4%** | 24.9% | 25.7% | 4.04% |

## 3. 水晶剑的具体概率

`weap12` 带里有 11 个物品，假设带内均匀：

```
P(水晶剑) ≈ 4.86% / 11 ≈ 0.44%  （地狱 Act1 每次装备掉落）
```

也就是说：**地狱里每掉 200 多件装备，就有一件水晶剑**。不少。

## 4. 但地狱掉的水晶剑，做不了「精神」

这是真正的关键 —— **ilvl 由怪物等级决定，不由 TC 带决定**。

地狱的怪等级 76~85，所以掉出来的水晶剑 `ilvl ≈ 80`。而剑类的孔数上限是：

| `ItemTypes.txt`（Sword） | 值 |
|---|---|
| `MaxSock1`（ilvl 1~25） | **3 孔** |
| `MaxSock25`（ilvl 26~40） | **4 孔** |
| `MaxSock40`（ilvl 41+） | **6 孔** |

所以：

- 地狱的水晶剑 → 拉苏克打孔给 **6 孔**，精神要 4 孔，**废了**
- 噩梦（ilvl 26~40）的水晶剑 → 拉苏克给 **4 孔** ✓
- 例外：白色带孔装备是**随机孔数掉落**的，所以地狱也可能直接掉一个 4 孔水晶剑（运气）

**实用结论**：要做精神，去**噩梦 Act1~Act3**（怪物等级 26~40）打白水晶剑再拉苏克。
地狱掉的那些只能当材料或卖钱。

## 5. 踩坑：`TreasureClassEx.txt` 最后 4 列不是物品

```
... Item9 | Prob9 | Item10 | Prob10 | SumItems | TotalProb | DropChance | Term
... Act 3 (H) Equip B | 1530 | (空) | (空) | 36 | 1566 | 0.977 | 0
```

朴素写法（"从下标 9 开始每两列一组"）会把 `36`、`0.977` 当成物品名，
于是掉落链里出现 `'36'` 这种幽灵条目。**必须按表头 `ItemN` / `ProbN` 配对**。

已封装进 `tools/d2tc.py`，以后别手写递归。
