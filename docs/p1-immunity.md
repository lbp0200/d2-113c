# P1 · 地狱免疫墙报告

> 由 `tools/p1_immunity.py` 从 `vanilla/` 自动生成。只读分析，不代表任何改动。

## 总览（735 个怪物条目）

| 元素 | 免疫数(>=100) | 占比 | 其中 >100 | 其中 >=200 | 绝对(>=1000) |
|---|---:|---:|---:|---:|---:|
| 火 | 113 | 15% | 89 | 0 | 0 |
| 冰 | 137 | 19% | 125 | 2 | 1 |
| 电 | 105 | 14% | 33 | 0 | 0 |
| 毒 | 131 | 18% | 102 | 21 | 16 |
| 物理 | 20 | 3% | 0 | 0 | 0 |
| 魔法 | 11 | 1% | 1 | 0 | 0 |

### 可破性（关键：免疫 ≠ 无解）

假设你能凑到 **100.0** 点降抗（信念/无限 + 降抗诅咒 + 装备），
对免疫怪按 1/5 生效 → 实际可破上限 = **抗性 120**。
超过这条线的怪，免疫数量再多也不是「难」，而是「无解」。

| 元素 | 免疫(>=100) | 无解(>阈值) | 最高抗性 |
|---|---:|---:|---:|
| 火 | 113 | **16** | 145 |
| 冰 | 137 | **102** | 1000 |
| 电 | 105 | **3** | 145 |
| 毒 | 131 | **27** | 1000 |
| 物理 | 20 | **0** | 100 |
| 魔法 | 11 | **1** | 145 |

## 抗性值分布

抗性 R 降到 100 以下需要 `-res >= R-100`；对免疫怪降抗只按 1/5 生效，
所以真正需要的是 `5*(R-100)` 点降抗。这就是「某些免疫打不穿」的数学原因。

| 需要的降抗量 | 火 | 冰 | 电 | 毒 | 物理 | 魔法 |
|---|---:|---:|---:|---:|---:|---:|
| 0（本来不免疫） | 657 | 610 | 709 | 652 | 735 | 734 |
| 1~50 | 41 | 8 | 18 | 42 | 0 | 0 |
| 51~100 | 32 | 39 | 7 | 17 | 0 | 0 |
| 101~200 | 5 | 78 | 1 | 24 | 0 | 1 |
| >200 | 0 | 0 | 0 | 0 | 0 | 0 |

## 区域：单元素 build 的死路

按幕列出「该区域里**免疫且破不开**（抗性 > 120）的怪物占比」。
100% = 纯该元素的 build 在该区域完全无解。
（只统计 `levels.txt` 里挂在该区域下的怪物，不含随机刷新的精英词缀与特殊事件。）

### 第 1 幕

| 区域 | 地狱等级 | 怪物数 | 火 | 冰 | 电 | 毒 | 物理 | 魔法 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Act 1 - Wilderness 1 | 67 | 3 | – | – | – | – | – | – |
| Act 1 - Wilderness 2 | 68 | 4 | – | – | – | – | – | – |
| Act 1 - Wilderness 3 | 68 | 5 | – | – | – | – | – | – |
| Act 1 - Wilderness 4 | 68 | 5 | – | – | – | – | – | – |
| Act 1 - Wilderness 5 | 69 | 6 | – | – | – | – | – | – |
| Act 1 - Wilderness 6 | 69 | 5 | – | 20% | – | – | – | – |
| Act 1 - Cave 1 | 79 | 3 | – | – | – | – | – | – |
| Act 1 - Cave 2 | 77 | 3 | – | – | – | – | – | – |
| Act 1 - Cave 3 | 69 | 4 | – | – | – | – | – | – |
| Act 1 - Cave 4 | 80 | 4 | – | – | – | – | – | – |
| Act 1 - Cave 5 | 85 | 4 | – | 25% | – | – | – | – |
| Act 1 - Cave 2 Treasure | 78 | 3 | – | – | – | – | – | – |
| Act 1 - Cave 3 Treasure | 83 | 4 | – | – | – | – | – | – |
| Act 1 - Cave 4 Treasure | 81 | 4 | – | – | – | – | – | – |
| Act 1 - Cave 5 Treasure | 85 | 4 | – | 25% | – | – | – | – |
| Act 1 - Graveyard | 80 | 2 | – | – | – | – | – | – |
| Act 1 - Crypt 1 A | 83 | 2 | – | – | – | – | – | – |
| Act 1 - Crypt 2 A | 85 | 2 | – | – | – | – | – | – |
| Act 1 - Crypt 3 A | 75 | 4 | – | – | – | – | – | – |
| Act 1 - Crypt 3 B | 76 | 4 | – | – | – | – | – | – |
| Act 1 - Crypt 3 C | 77 | 4 | – | – | – | – | – | – |
| Act 1 - Crypt 3 D | 78 | 4 | – | – | – | – | – | – |
| Act 1 - Crypt 3 E | 79 | 4 | – | – | – | – | – | – |
| Act 1 - Monastery | 70 | 4 | – | 25% | – | – | – | – |
| Act 1 - Courtyard 1 | 70 | 4 | – | 50% | – | – | – | – |
| Act 1 - Barracks | 70 | 5 | – | 20% | – | – | – | – |
| Act 1 - Jail 1 | 71 | 5 | 20% | – | – | – | – | – |
| Act 1 - Jail 2 | 71 | 5 | 20% | – | – | – | – | – |
| Act 1 - Jail 3 | 71 | 5 | 20% | – | – | – | – | – |
| Act 1 - Courtyard 2 | 72 | 3 | 33% | – | – | – | – | – |
| Act 1 - Cathedral | 72 | 3 | – | – | – | – | – | – |
| Act 1 - Catacombs 1 | 72 | 3 | – | – | – | – | – | – |
| Act 1 - Catacombs 2 | 73 | 3 | – | – | – | – | – | – |
| Act 1 - Catacombs 3 | 73 | 3 | – | 33% | – | – | – | – |
| Act 1 - Catacombs 4 | 73 | 2 | – | – | – | – | – | – |
| Act 1 - Tristram | 76 | 4 | – | – | – | – | – | – |
| Act 1 - Moo Moo Farm | 81 | 1 | – | – | – | – | – | – |

### 第 2 幕

| 区域 | 地狱等级 | 怪物数 | 火 | 冰 | 电 | 毒 | 物理 | 魔法 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Act 2 - Desert 1 | 75 | 5 | – | – | – | – | – | – |
| Act 2 - Desert 2 | 76 | 4 | – | – | – | – | – | – |
| Act 2 - Desert 3 | 76 | 5 | – | – | – | – | – | – |
| Act 2 - Desert 4 | 77 | 5 | – | – | – | – | – | – |
| Act 2 - Desert 5 | 77 | 4 | – | – | – | – | – | – |
| Act 2 - Valley of the Kings | 79 | 5 | – | 20% | – | – | – | – |
| Act 2 - Sewer 1 A | 74 | 4 | – | – | – | – | – | – |
| Act 2 - Sewer 1 B | 74 | 4 | – | – | – | – | – | – |
| Act 2 - Sewer 1 C | 75 | 4 | – | – | – | – | – | – |
| Act 2 - Corrupt Harem 1 | 78 | 5 | – | 20% | – | – | – | – |
| Act 2 - Basement 1 | 78 | 5 | – | – | – | – | – | – |
| Act 2 - Basement 2 | 78 | 5 | – | – | – | – | – | – |
| Act 2 - Basement 3 | 78 | 5 | – | – | – | – | – | – |
| Act 2 - Tomb 1 A | 78 | 3 | – | – | – | – | – | – |
| Act 2 - Tomb 2 A | 79 | 4 | – | 25% | – | – | – | – |
| Act 2 - Tomb 2 B | 81 | 4 | – | 25% | – | – | – | – |
| Act 2 - Tomb 3 A | 82 | 4 | – | – | – | – | – | – |
| Act 2 - Tomb 1 Treasure | 79 | 3 | – | – | – | – | – | – |
| Act 2 - Tomb 2 Treasure | 82 | 4 | – | 25% | – | – | – | – |
| Act 2 - Tomb 3 Treasure | 83 | 4 | – | – | – | – | – | – |
| Act 2 - Lair 1 A | 84 | 5 | – | – | – | – | – | – |
| Act 2 - Lair 1 B | 84 | 5 | – | – | – | – | – | – |
| Act 2 - Lair 1 Treasure | 85 | 5 | – | – | – | – | – | – |
| Act 2 - Sewer 2 A | 85 | 4 | – | – | – | – | – | – |
| Act 2 - Tomb Tal 1 | 80 | 6 | – | 17% | – | – | – | – |
| Act 2 - Tomb Tal 2 | 80 | 6 | – | 17% | – | – | – | – |
| Act 2 - Tomb Tal 3 | 80 | 6 | – | 17% | – | – | – | – |
| Act 2 - Tomb Tal 4 | 80 | 6 | – | 17% | – | – | – | – |
| Act 2 - Tomb Tal 5 | 80 | 6 | – | 17% | – | – | – | – |
| Act 2 - Tomb Tal 6 | 80 | 6 | – | 17% | – | – | – | – |
| Act 2 - Tomb Tal 7 | 80 | 6 | – | 17% | – | – | – | – |
| Act 2 - Duriel's Lair | 80 | 6 | – | 17% | – | – | – | – |
| Act 2 - Arcane | 79 | 3 | – | – | – | – | – | – |

### 第 3 幕

| 区域 | 地狱等级 | 怪物数 | 火 | 冰 | 电 | 毒 | 物理 | 魔法 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Act 3 - Jungle 1 | 79 | 6 | – | – | – | – | – | – |
| Act 3 - Jungle 2 | 80 | 6 | – | 17% | – | – | – | – |
| Act 3 - Jungle 3 | 80 | 7 | – | 14% | – | – | – | – |
| Act 3 - Kurast 1 | 80 | 4 | – | – | – | – | – | – |
| Act 3 - Kurast 2 | 81 | 4 | – | 75% | – | – | – | – |
| Act 3 - Kurast 3 | 81 | 4 | – | 25% | – | – | – | – |
| Act 3 - Kurast 4 | 81 | 3 | – | 33% | – | – | – | – |
| Act 3 - Travincal | 82 | 2 | – | 50% | – | – | – | – |
| Act 3 - Spider 1 | 79 | 4 | – | – | – | – | – | – |
| Act 3 - Spider 2 | 79 | 4 | – | – | – | – | – | – |
| Act 3 - Dungeon 1 A | 80 | 5 | – | – | – | – | – | – |
| Act 3 - Dungeon 1 B | 81 | 5 | – | – | – | – | – | – |
| Act 3 - Dungeon 2 A | 81 | 8 | – | 12% | – | – | – | – |
| Act 3 - Dungeon 2 B | 82 | 8 | – | 12% | – | – | – | – |
| Act 3 - Dungeon 1 Treasure | 82 | 4 | – | – | – | – | – | – |
| Act 3 - Dungeon 2 Treasure | 83 | 8 | – | 12% | – | – | – | – |
| Act 3 - Sewer 1 | 84 | 5 | – | – | – | – | – | – |
| Act 3 - Sewer 2 | 85 | 5 | – | – | – | – | – | – |
| Act 3 - Temple 1 | 84 | 4 | – | 25% | – | – | – | – |
| Act 3 - Temple 2 | 84 | 4 | – | 25% | – | – | – | – |
| Act 3 - Temple 3 | 84 | 4 | – | 25% | – | – | – | – |
| Act 3 - Temple 4 | 85 | 4 | – | 25% | – | – | – | – |
| Act 3 - Temple 5 | 85 | 4 | – | 25% | – | – | – | – |
| Act 3 - Temple 6 | 85 | 4 | – | 25% | – | – | – | – |
| Act 3 - Mephisto 1 | 83 | 4 | – | 25% | – | – | – | – |
| Act 3 - Mephisto 2 | 83 | 4 | – | 25% | – | – | – | – |
| Act 3 - Mephisto 3 | 83 | 1 | – | **100%** | – | – | – | – |

### 第 4 幕

| 区域 | 地狱等级 | 怪物数 | 火 | 冰 | 电 | 毒 | 物理 | 魔法 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Act 4 - Mesa 1 | 82 | 6 | 17% | 17% | – | – | – | – |
| Act 4 - Mesa 2 | 83 | 6 | 17% | 17% | – | – | – | – |
| Act 4 - Mesa 3 | 84 | 7 | – | 14% | – | – | – | – |
| Act 4 - Lava 1 | 85 | 7 | – | 14% | – | 14% | – | – |
| Act 4 - Diablo 1 | 85 | 3 | 33% | 33% | – | – | – | – |

### 第 5 幕

| 区域 | 地狱等级 | 怪物数 | 火 | 冰 | 电 | 毒 | 物理 | 魔法 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Act 5 - Siege 1 | 80 | 7 | – | 14% | – | – | – | – |
| Act 5 - Barricade 1 | 81 | 2 | – | – | – | – | – | – |
| Act 5 - Barricade 2 | 81 | 2 | – | 50% | – | – | – | – |
| Act 5 - Ice Cave 1 | 82 | 3 | – | 33% | – | – | – | – |
| Act 5 - Ice Cave 1A | 83 | 3 | – | 67% | – | – | – | – |
| Act 5 - Ice Cave 2 | 83 | 3 | – | **100%** | – | – | – | – |
| Act 5 - Ice Cave 2A | 84 | 2 | – | 50% | – | – | – | – |
| Act 5 - Barricade Snow | 81 | 2 | – | – | – | – | – | – |
| Act 5 - Ice Cave 3 | 82 | 3 | – | 67% | – | – | – | – |
| Act 5 - Ice Cave 3A | 83 | 3 | – | 67% | – | – | – | – |
| Act 5 - Mountain Top | 87 | 3 | – | 33% | – | – | – | – |
| Act 5 - Temple 1 | 83 | 2 | – | 50% | – | – | – | – |
| Act 5 - Temple 2 | 84 | 3 | – | – | – | – | – | – |
| Act 5 - Temple Boss | 84 | 3 | – | 33% | – | – | – | – |
| Act 5 - Hell 1 | 81 | 2 | – | – | – | – | – | – |
| Act 5 - Hell 2 | 82 | 2 | – | 50% | – | – | – | – |
| Act 5 - Hell 3 | 83 | 2 | – | 50% | – | – | – | – |
| Act 5 - Baal Temple 1 | 85 | 3 | – | – | – | – | – | – |
| Act 5 - Baal Temple 2 | 85 | 2 | – | 50% | – | – | – | – |
| Act 5 - Baal Temple 3 | 85 | 3 | – | – | – | – | – | – |
| Act 5 - Throne Room | 85 | 2 | – | – | – | – | – | – |
| Act 5 - Pandemonium 1 | 83 | 5 | – | 60% | – | – | – | – |
| Act 5 - Pandemonium 2 | 83 | 4 | – | – | – | – | – | – |
| Act 5 - Pandemonium 3 | 83 | 4 | 25% | 75% | 25% | 25% | – | 25% |

## 无解死角（某元素全部怪抗性都 > 120 的区域）

- **火**：0 个区域 → 无
- **冰**：2 个区域 → A3 Act 3 - Mephisto 3、A5 Act 5 - Ice Cave 2
- **电**：0 个区域 → 无
- **毒**：0 个区域 → 无
- **物理**：0 个区域 → 无
- **魔法**：0 个区域 → 无

## 抗性 > 120 的怪物（按当前降抗预算 = 无解）

- `barricadedoor1` 毒抗性 1000
- `barricadedoor2` 毒抗性 1000
- `barricadetower` 毒抗性 1000
- `barricadewall1` 毒抗性 1000
- `barricadewall2` 毒抗性 1000
- `catapult1` 毒抗性 1000
- `catapult2` 毒抗性 1000
- `catapult3` 毒抗性 1000
- `catapult4` 毒抗性 1000
- `compellingorb` 毒抗性 1000
- `firetower` 毒抗性 1000
- `gargoyletrap` 冰抗性 1000
- `lightningspire` 毒抗性 1000
- `prisondoor` 毒抗性 1000
- `turret1` 毒抗性 1000
- `turret2` 毒抗性 1000
- `turret3` 毒抗性 1000
- `snowyeti4` 冰抗性 210
- `boneprison1` 毒抗性 200
- `boneprison2` 毒抗性 200
- `boneprison3` 毒抗性 200
- `boneprison4` 毒抗性 200
- `bonewall` 毒抗性 200
- `frozenhorror5` 冰抗性 190
- `snowyeti3` 冰抗性 190
- `doomknight3` 冰抗性 180
- `frozenhorror4` 冰抗性 180
- `frozenhorror3` 冰抗性 170
- `reanimatedhorde3` 冰抗性 170
- `skmage_cold4` 冰抗性 170
- `snowyeti2` 冰抗性 170
- `goatman10` 冰抗性 165
- `cantor3` 冰抗性 160
- `frozenhorror2` 冰抗性 160
- `minion8` 冰抗性 160
- `overseer5` 冰抗性 160
- `overseer6` 冰抗性 160
- `sandraider9` 冰抗性 160
- `skmage_cold3` 冰抗性 160
- `skmage_cold5` 冰抗性 160
- `skmage_cold6` 冰抗性 160
- `succubuswitch5` 冰抗性 160
- `suicideminion8` 冰抗性 160
- `vilechild3` 冰抗性 160
- `vilemother3` 冰抗性 160
- `goatman8` 冰抗性 155
- `succubuswitch8` 冰抗性 155
- `succubuswitch9` 冰抗性 155
- `ancientbarb3` 冰抗性 150
- `corruptrogue5` 冰抗性 150
- `corruptrogue6` 冰抗性 150
- `frozenhorror1` 冰抗性 150
- `minion6` 冰抗性 150
- `overseer4` 冰抗性 150
- `painworm5` 冰抗性 150
- `reanimatedhorde2` 冰抗性 150
- `sandraider7` 冰抗性 150
- `sarcophagus` 冰抗性 150
- `skmage_cold2` 冰抗性 150
- `slinger8` 冰抗性 150
- `snowyeti1` 冰抗性 150
- `suicideminion6` 冰抗性 150
- `thornhulk4` 冰抗性 150
- `trappedsoul1` 冰抗性 150
- `trappedsoul2` 冰抗性 150
- `vampire5` 冰抗性 150
- `vilechild2` 冰抗性 150
- `vilemother2` 冰抗性 150
- `clawviper7` 冰抗性 145
- `deathmauler5` 冰抗性 145
- `dkmag2` 冰抗性 145
- `dkmag3` 冰抗性 145
- `megademon5` 火抗性 145
- `megademon6` 火抗性 145
- `megademon6` 冰抗性 145
- `megademon6` 电抗性 145
- `megademon6` 毒抗性 145
- `megademon6` 魔法抗性 145
- `succubuswitch7` 冰抗性 145
- `vilechild5` 冰抗性 145
- `vilemother5` 冰抗性 145
- `bloodlord6` 火抗性 140
- `blunderbore2` 冰抗性 140
- `brute4` 冰抗性 140
- `cantor1` 冰抗性 140
- `corruptrogue4` 冰抗性 140
- `cr_archer7` 冰抗性 140
- `cr_archer8` 冰抗性 140
- `dkfig2` 火抗性 140
- `dkmag1` 冰抗性 140
- `fetishblow3` 冰抗性 140
- `megademon4` 火抗性 140
- `minion3` 冰抗性 140
- `overseer3` 冰抗性 140
- `painworm3` 冰抗性 140
- `siegebeast5` 冰抗性 140
- `sk_archer10` 毒抗性 140
- `sk_archer11` 毒抗性 140
- `skmage_cold1` 冰抗性 140
- `slinger2` 冰抗性 140
- `succubuswitch1` 冰抗性 140
- `suicideminion3` 冰抗性 140
- `thornhulk3` 冰抗性 140
- `vampire4` 冰抗性 140
- `vilechild1` 冰抗性 140
- `vilechild4` 冰抗性 140
- `vilemother1` 冰抗性 140
- `vilemother4` 冰抗性 140
- `zealot2` 冰抗性 140
- `bloodlord4` 冰抗性 135
- `deathmauler3` 冰抗性 135
- `goatman7` 冰抗性 135
- `minion11` 冰抗性 135
- `vampire8` 冰抗性 135
- `vampire9` 冰抗性 135
- `baaltentacle5` 冰抗性 130
- `brute3` 冰抗性 130
- `clawviper4` 冰抗性 130
- `corruptrogue3` 冰抗性 130
- `cr_archer5` 冰抗性 130
- `cr_lancer5` 冰抗性 130
- `dkfig1` 火抗性 130
- `fetishshaman8` 火抗性 130
- `megademon3` 火抗性 130
- `minion1` 冰抗性 130
- `minion9` 冰抗性 130
- `mummy6` 毒抗性 130
- `overseer2` 冰抗性 130
- `reanimatedhorde1` 冰抗性 130
- `sandraider10` 火抗性 130
- `siegebeast4` 冰抗性 130
- `sk_archer9` 毒抗性 130
- `skmage_fire6` 火抗性 130
- `skmage_fire7` 火抗性 130
- `skmage_ltng6` 电抗性 130
- `skmage_ltng7` 电抗性 130
- `suicideminion1` 冰抗性 130
- `thornhulk2` 冰抗性 130
- `vampire3` 冰抗性 130
- `vampire7` 冰抗性 130
- `baaltentacle4` 冰抗性 125
- `fallen4` 火抗性 125
- `fetishshaman5` 火抗性 125
- `fetishshaman7` 火抗性 125
- `sandmaggot5` 毒抗性 125
- `sandraider8` 火抗性 125
- `skmage_fire5` 火抗性 125
- `succubuswitch6` 冰抗性 125
- `vampire6` 冰抗性 125
