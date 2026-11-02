# P1 · 佣兵数值对比

> 由 `tools/p1_merc.py` 从 `vanilla/data/global/excel/Hireling.txt` 生成。只读分析。
> 只统计 `Version=100`（LoD 资料片佣兵）。

## 地狱难度 · 各佣兵在 85 级的属性

| 佣兵 | 类型 | HP | 物理伤害 | 命中 AR | 每级 HP | 每级伤害 | 雇价 |
|---|---|---:|---:|---:|---:|---:|---:|
| A1 罗格 | Fire - Hell / Ice - Hell | 1319 | 131-133 | 1646 | +30 | +6 | 14000 |
| A2 沙漠佣兵 | Comb-Hell / Def-Hell / Off-Hell | 1630 | 124-131 | 1398 | +40 | +8 | 15000 |
| A3 铁狼 | Cold-Hell / Fire-Hell / Ltng-Hell | 1025 | 53-60 | 1207 | +27 | +4 | 21000 |
| A5 野蛮人 | 1hs-Hell | 1430 | 97-101 | 1526 | +45 | +8 | 32000 |

## 成长曲线（地狱）

| 佣兵 | HP@80 | 伤害@80 | HP@85 | 伤害@85 | HP@90 | 伤害@90 |
|---|---:|---:|---:|---:|---:|---:|
| A1 罗格 | 1169 | 101-103 | 1319 | 131-133 | 1469 | 161-163 |
| A2 沙漠佣兵 | 1430 | 84-91 | 1630 | 124-131 | 1830 | 164-171 |
| A3 铁狼 | 890 | 33-40 | 1025 | 53-60 | 1160 | 73-80 |
| A5 野蛮人 | 1205 | 57-61 | 1430 | 97-101 | 1655 | 137-141 |

## 相对差距（以 A2 沙漠佣兵为基准，85 级地狱）

| 佣兵 | HP | 相对 A2 | 物理伤害上限 | 相对 A2 |
|---|---:|---:|---:|---:|
| A1 罗格 | 1319 | -19% | 133 | +2% |
| A2 沙漠佣兵 | 1630 | +0% | 131 | +0% |
| A3 铁狼 | 1025 | -37% | 60 | -54% |
| A5 野蛮人 | 1430 | -12% | 101 | -23% |

## 技能与光环（这才是 A2 强、A3/A5 弱的真正原因）

等级写的是「该难度下最低断点 → 最高断点」的技能等级区间。
只有 A2 提供**光环**；A1 的 Inner Sight 是减防 debuff；A3 是纯输出法术；
A5 两个技能都是单体控制。

| 佣兵 | 难度 | 类型 | 技能（技能等级区间） |
|---|---|---|---|
| A1 罗格 | 普通 | Fire - Normal | Inner Sight L1→22、Fire Arrow L1→22 |
| A1 罗格 | 普通 | Ice - Normal | Inner Sight L1→22、Cold Arrow L1→22 |
| A1 罗格 | 噩梦 | Fire - Nightmare | Inner Sight L11→21、Fire Arrow L11→21 |
| A1 罗格 | 噩梦 | Ice - Nightmare | Inner Sight L11→21、Cold Arrow L11→21 |
| A1 罗格 | 地狱 | Fire - Hell | Inner Sight L20、Fire Arrow L20 |
| A1 罗格 | 地狱 | Ice - Hell | Inner Sight L20、Cold Arrow L20 |
| A2 沙漠佣兵 | 普通 | Comb-Normal | Jab L3→24、Prayer L3→18 |
| A2 沙漠佣兵 | 普通 | Def-Normal | Jab L3→24、Defiance L3→18 |
| A2 沙漠佣兵 | 普通 | Off-Normal | Jab L3→24、Blessed Aim L3→18 |
| A2 沙漠佣兵 | 噩梦 | Comb-Nightmare | Jab L13→23、Thorns L5→15 |
| A2 沙漠佣兵 | 噩梦 | Def-Nightmare | Jab L13→23、Holy Freeze L6→16 |
| A2 沙漠佣兵 | 噩梦 | Off-Nightmare | Jab L13→23、Might L7→15 |
| A2 沙漠佣兵 | 地狱 | Comb-Hell | Jab L22、Prayer L16 |
| A2 沙漠佣兵 | 地狱 | Def-Hell | Jab L22、Defiance L16 |
| A2 沙漠佣兵 | 地狱 | Off-Hell | Jab L22、Blessed Aim L16 |
| A3 铁狼 | 普通 | Fire-Normal | Inferno L6→27、Fire Ball L4→25 |
| A3 铁狼 | 普通 | Cold-Normal | Glacial Spike L1→12、Frozen Armor L2→23、Ice Blast L6→27 |
| A3 铁狼 | 普通 | Ltng-Normal | Charged Bolt L4→15、Lightning L3→24 |
| A3 铁狼 | 噩梦 | Fire-Nightmare | Inferno L16→26、Fire Ball L14→24 |
| A3 铁狼 | 噩梦 | Cold-Nightmare | Glacial Spike L6→11、Frozen Armor L12→22、Ice Blast L16→26 |
| A3 铁狼 | 噩梦 | Ltng-Nightmare | Charged Bolt L9→14、Lightning L13→23 |
| A3 铁狼 | 地狱 | Fire-Hell | Inferno L25、Fire Ball L23 |
| A3 铁狼 | 地狱 | Cold-Hell | Glacial Spike L10、Frozen Armor L21、Ice Blast L25 |
| A3 铁狼 | 地狱 | Ltng-Hell | Charged Bolt L13、Lightning L22 |
| A5 野蛮人 | 普通 | 1hs-Normal | Bash L4→21、Stun L3→17 |
| A5 野蛮人 | 噩梦 | 1hs-Nightmare | Bash L13→20、Stun L10→16 |
| A5 野蛮人 | 地狱 | 1hs-Hell | Bash L19、Stun L15 |

## A3 铁狼的元素输出（按地狱档基础技能等级）

上表的 `Dmg-Min/Max` 只算了它的近战平砍。它真实的输出来自这些法术，
用 `skills.txt` 的本体伤害公式算（不含协同，见 [p1-skills.md](p1-skills.md)）：

| 类型 | 技能 | 技能等级 | 单次伤害 |
|---|---|---:|---:|
| Fire-Hell | Inferno | 25 | 22-23 |
| Fire-Hell | Fire Ball | 23 | 436-489 |
| Cold-Hell | Glacial Spike | 10 | 105-118 |
| Cold-Hell | Ice Blast | 25 | 687-718 |
| Ltng-Hell | Charged Bolt | 13 | 10-12 |
| Ltng-Hell | Lightning | 22 | 1-496 |

对照：A3 的法术单发伤害其实不低（火球 23 级约 500），
所以它的问题不是「打不动」，而是 **HP 最低、没有光环、且施法频率受 AI/冷却限制**。

## 结论

- **A2 沙漠佣兵的优势不在面板，在光环。** 面板上 A5 野蛮人的伤害甚至更高，
  但 A2 提供的是**全队乘算**：噩梦档给「力量(Might) / 神圣冰冻(Holy Freeze) / 荆棘(Thorns)」，
  地狱档给「祈祷(Prayer) / 反抗(Defiance) / 祝福瞄准(Blessed Aim)」。
  所以正确的雇佣姿势是**在噩梦雇一个 A2 再带进地狱**——这是数据里能直接看出来的机制。
- **A3 铁狼是纯数值弱**：HP 与每级成长都明显低于其他三个，且没有光环。
  它的 `Dmg-Min/Max` 只代表近战平砍，真实输出来自元素技能（火球/冰爆/闪电），
  所以「伤害」这一项对它是低估；但 HP 低、无光环、且吃不到武器伤害加成，是它常年垫底的结构性原因。
- **A5 野蛮人面板不差**（HP 与 A2 接近，伤害更高），问题是没光环 + 两个技能都是纯单体控制，
  对队伍没有任何增益。要「修」它，加数值是没用的，得给它一个定位。
