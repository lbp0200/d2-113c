# P2 审计：改了哪些数字，有没有没补偿的削弱

> 由 `python3 -m tools.p2_audit` 生成：`vanilla/` 与 `mod/` 逐单元格对比。
> 判据 T3 要求「只加不改，或拿走 A 换给 B」——所以每一个**数值下降**
> 都必须能指认出对应的上升/新增。

## 总览

| 表 | 数值上升 | 数值下降 | 非数值改动 | 新增行 |
|---|---:|---:|---:|---:|
| CubeMain.txt | 0 | 0 | 0 | 4 |
| MonStats.txt | 0 | 332 | 0 | 0 |
| Skills.txt | 50 | 9 | 10 | 0 |
| TreasureClassEx.txt | 107 | 0 | 0 | 0 |
| **合计** | **157** | **341** | **10** | **4** |

## 所有「数值下降」（必须能被解释）

| 表 | 行 | 列 | 前 | 后 |
|---|---|---|---:|---:|
| MonStats.txt | `skeleton3` | ResCo(H) | 110 | **100** |
| MonStats.txt | `skeleton5` | ResLi(H) | 120 | **100** |
| MonStats.txt | `zombie1` | ResCo(H) | 120 | **100** |
| MonStats.txt | `zombie2` | ResLi(H) | 110 | **100** |
| MonStats.txt | `zombie4` | ResFi(H) | 110 | **100** |
| MonStats.txt | `bighead2` | ResLi(H) | 105 | **100** |
| MonStats.txt | `bighead3` | ResLi(H) | 110 | **100** |
| MonStats.txt | `bighead4` | ResLi(H) | 115 | **100** |
| MonStats.txt | `bighead5` | ResLi(H) | 120 | **100** |
| MonStats.txt | `foulcrow2` | ResPo(H) | 105 | **100** |
| MonStats.txt | `foulcrow3` | ResPo(H) | 110 | **100** |
| MonStats.txt | `fallen2` | ResFi(H) | 110 | **100** |
| MonStats.txt | `fallen3` | ResFi(H) | 120 | **100** |
| MonStats.txt | `fallen4` | ResFi(H) | 125 | **100** |
| MonStats.txt | `brute2` | ResCo(H) | 120 | **100** |
| MonStats.txt | `brute3` | ResCo(H) | 130 | **100** |
| MonStats.txt | `brute4` | ResCo(H) | 140 | **100** |
| MonStats.txt | `sandraider3` | ResFi(H) | 110 | **100** |
| MonStats.txt | `sandraider4` | ResCo(H) | 110 | **100** |
| MonStats.txt | `sandraider5` | ResFi(H) | 120 | **100** |
| MonStats.txt | `corruptrogue2` | ResCo(H) | 120 | **100** |
| MonStats.txt | `corruptrogue3` | ResCo(H) | 130 | **100** |
| MonStats.txt | `corruptrogue4` | ResCo(H) | 140 | **100** |
| MonStats.txt | `corruptrogue5` | ResCo(H) | 150 | **100** |
| MonStats.txt | `baboon3` | ResLi(H) | 105 | **100** |
| MonStats.txt | `baboon4` | ResLi(H) | 105 | **100** |
| MonStats.txt | `baboon5` | ResLi(H) | 110 | **100** |
| MonStats.txt | `goatman2` | ResLi(H) | 110 | **100** |
| MonStats.txt | `goatman4` | ResFi(H) | 110 | **100** |
| MonStats.txt | `fallenshaman2` | ResFi(H) | 105 | **100** |
| MonStats.txt | `fallenshaman3` | ResFi(H) | 110 | **100** |
| MonStats.txt | `fallenshaman4` | ResFi(H) | 115 | **100** |
| MonStats.txt | `fallenshaman5` | ResFi(H) | 120 | **100** |
| MonStats.txt | `sandmaggot1` | ResPo(H) | 105 | **100** |
| MonStats.txt | `sandmaggot2` | ResPo(H) | 110 | **100** |
| MonStats.txt | `sandmaggot3` | ResPo(H) | 115 | **100** |
| MonStats.txt | `sandmaggot4` | ResPo(H) | 120 | **100** |
| MonStats.txt | `sandmaggot5` | ResPo(H) | 125 | **100** |
| MonStats.txt | `clawviper2` | ResCo(H) | 120 | **100** |
| MonStats.txt | `clawviper3` | ResCo(H) | 110 | **100** |
| MonStats.txt | `clawviper4` | ResCo(H) | 130 | **100** |
| MonStats.txt | `clawviper5` | ResCo(H) | 120 | **100** |
| MonStats.txt | `sandleaper3` | ResFi(H) | 105 | **100** |
| MonStats.txt | `pantherwoman4` | ResCo(H) | 120 | **100** |
| MonStats.txt | `scarab2` | ResLi(H) | 105 | **100** |
| MonStats.txt | `scarab3` | ResLi(H) | 110 | **100** |
| MonStats.txt | `scarab4` | ResLi(H) | 115 | **100** |
| MonStats.txt | `scarab5` | ResLi(H) | 120 | **100** |
| MonStats.txt | `mummy3` | ResPo(H) | 105 | **100** |
| MonStats.txt | `mummy4` | ResPo(H) | 105 | **100** |
| MonStats.txt | `mummy5` | ResPo(H) | 110 | **100** |
| MonStats.txt | `vulture1` | ResPo(H) | 110 | **100** |
| MonStats.txt | `mosquito1` | ResPo(H) | 105 | **100** |
| MonStats.txt | `mosquito2` | ResPo(H) | 110 | **100** |
| MonStats.txt | `mosquito3` | ResPo(H) | 115 | **100** |
| MonStats.txt | `mosquito4` | ResPo(H) | 120 | **100** |
| MonStats.txt | `willowisp2` | ResLi(H) | 105 | **100** |
| MonStats.txt | `willowisp3` | ResLi(H) | 110 | **100** |
| MonStats.txt | `willowisp4` | ResLi(H) | 115 | **100** |
| MonStats.txt | `arach1` | ResFi(H) | 110 | **100** |
| MonStats.txt | `arach2` | ResLi(H) | 105 | **100** |
| MonStats.txt | `arach3` | ResPo(H) | 110 | **100** |
| MonStats.txt | `arach4` | ResFi(H) | 115 | **100** |
| MonStats.txt | `arach5` | ResFi(H) | 120 | **100** |
| MonStats.txt | `thornhulk1` | ResCo(H) | 120 | **100** |
| MonStats.txt | `thornhulk2` | ResCo(H) | 130 | **100** |
| MonStats.txt | `thornhulk3` | ResCo(H) | 140 | **100** |
| MonStats.txt | `thornhulk4` | ResCo(H) | 150 | **100** |
| MonStats.txt | `vampire1` | ResCo(H) | 110 | **100** |
| MonStats.txt | `vampire2` | ResCo(H) | 120 | **100** |
| MonStats.txt | `vampire3` | ResCo(H) | 130 | **100** |
| MonStats.txt | `vampire4` | ResCo(H) | 140 | **100** |
| MonStats.txt | `vampire5` | ResCo(H) | 150 | **100** |
| MonStats.txt | `batdemon2` | ResLi(H) | 110 | **100** |
| MonStats.txt | `batdemon4` | ResFi(H) | 105 | **100** |
| MonStats.txt | `batdemon5` | ResLi(H) | 120 | **100** |
| MonStats.txt | `fetish4` | ResLi(H) | 110 | **100** |
| MonStats.txt | `cr_archer2` | ResFi(H) | 110 | **100** |
| MonStats.txt | `cr_archer3` | ResLi(H) | 110 | **100** |
| MonStats.txt | `cr_archer4` | ResLi(H) | 115 | **100** |
| MonStats.txt | `cr_archer5` | ResCo(H) | 130 | **100** |
| MonStats.txt | `cr_lancer2` | ResFi(H) | 110 | **100** |
| MonStats.txt | `cr_lancer3` | ResLi(H) | 110 | **100** |
| MonStats.txt | `cr_lancer4` | ResLi(H) | 115 | **100** |
| MonStats.txt | `cr_lancer5` | ResCo(H) | 130 | **100** |
| MonStats.txt | `sk_archer2` | ResPo(H) | 105 | **100** |
| MonStats.txt | `sk_archer3` | ResPo(H) | 105 | **100** |
| MonStats.txt | `sk_archer4` | ResPo(H) | 110 | **100** |
| MonStats.txt | `sk_archer5` | ResPo(H) | 110 | **100** |
| MonStats.txt | `blunderbore1` | ResFi(H) | 115 | **100** |
| MonStats.txt | `blunderbore2` | ResCo(H) | 140 | **100** |
| MonStats.txt | `bonefetish2` | ResPo(H) | 105 | **100** |
| MonStats.txt | `bonefetish3` | ResPo(H) | 110 | **100** |
| MonStats.txt | `bonefetish4` | ResPo(H) | 115 | **100** |
| MonStats.txt | `bonefetish5` | ResPo(H) | 120 | **100** |
| MonStats.txt | `sarcophagus` | ResCo(H) | 150 | **100** |
| MonStats.txt | `zealot2` | ResCo(H) | 140 | **100** |
| MonStats.txt | `cantor1` | ResCo(H) | 140 | **100** |
| MonStats.txt | `cantor3` | ResCo(H) | 160 | **100** |
| MonStats.txt | `frogdemon2` | ResCo(H) | 120 | **100** |
| MonStats.txt | `frogdemon3` | ResPo(H) | 110 | **100** |
| MonStats.txt | `tentacle2` | ResPo(H) | 105 | **100** |
| MonStats.txt | `tentacle3` | ResPo(H) | 110 | **100** |
| MonStats.txt | `tentaclehead2` | ResPo(H) | 105 | **100** |
| MonStats.txt | `tentaclehead3` | ResPo(H) | 110 | **100** |
| MonStats.txt | `fetishshaman1` | ResFi(H) | 105 | **100** |
| MonStats.txt | `fetishshaman2` | ResFi(H) | 110 | **100** |
| MonStats.txt | `fetishshaman3` | ResFi(H) | 115 | **100** |
| MonStats.txt | `fetishshaman4` | ResFi(H) | 120 | **100** |
| MonStats.txt | `fetishshaman5` | ResFi(H) | 125 | **100** |
| MonStats.txt | `maggotqueen1` | ResPo(H) | 120 | **100** |
| MonStats.txt | `maggotqueen2` | ResPo(H) | 120 | **100** |
| MonStats.txt | `maggotqueen3` | ResPo(H) | 120 | **100** |
| MonStats.txt | `maggotqueen4` | ResPo(H) | 120 | **100** |
| MonStats.txt | `maggotqueen5` | ResPo(H) | 120 | **100** |
| MonStats.txt | `baboon6` | ResPo(H) | 105 | **100** |
| MonStats.txt | `vilemother1` | ResCo(H) | 140 | **100** |
| MonStats.txt | `vilemother2` | ResCo(H) | 150 | **100** |
| MonStats.txt | `vilemother3` | ResCo(H) | 160 | **100** |
| MonStats.txt | `vilechild1` | ResCo(H) | 140 | **100** |
| MonStats.txt | `vilechild2` | ResCo(H) | 150 | **100** |
| MonStats.txt | `vilechild3` | ResCo(H) | 160 | **100** |
| MonStats.txt | `regurgitator2` | ResPo(H) | 105 | **100** |
| MonStats.txt | `regurgitator3` | ResPo(H) | 110 | **100** |
| MonStats.txt | `doomknight1` | ResFi(H) | 110 | **100** |
| MonStats.txt | `doomknight3` | ResCo(H) | 180 | **100** |
| MonStats.txt | `boneprison1` | ResPo(H) | 200 | **100** |
| MonStats.txt | `boneprison2` | ResPo(H) | 200 | **100** |
| MonStats.txt | `boneprison3` | ResPo(H) | 200 | **100** |
| MonStats.txt | `boneprison4` | ResPo(H) | 200 | **100** |
| MonStats.txt | `bonewall` | ResPo(H) | 200 | **100** |
| MonStats.txt | `councilmember1` | ResFi(H) | 120 | **100** |
| MonStats.txt | `megademon1` | ResFi(H) | 110 | **100** |
| MonStats.txt | `megademon2` | ResFi(H) | 120 | **100** |
| MonStats.txt | `megademon3` | ResFi(H) | 130 | **100** |
| MonStats.txt | `griswold` | ResPo(H) | 120 | **100** |
| MonStats.txt | `slinger1` | ResCo(H) | 120 | **100** |
| MonStats.txt | `slinger2` | ResCo(H) | 140 | **100** |
| MonStats.txt | `slinger4` | ResFi(H) | 105 | **100** |
| MonStats.txt | `skmage_cold1` | ResCo(H) | 140 | **100** |
| MonStats.txt | `skmage_cold2` | ResCo(H) | 150 | **100** |
| MonStats.txt | `skmage_cold3` | ResCo(H) | 160 | **100** |
| MonStats.txt | `skmage_cold4` | ResCo(H) | 170 | **100** |
| MonStats.txt | `skmage_fire2` | ResFi(H) | 105 | **100** |
| MonStats.txt | `skmage_fire3` | ResFi(H) | 110 | **100** |
| MonStats.txt | `skmage_fire4` | ResFi(H) | 115 | **100** |
| MonStats.txt | `skmage_ltng2` | ResLi(H) | 105 | **100** |
| MonStats.txt | `skmage_ltng3` | ResLi(H) | 110 | **100** |
| MonStats.txt | `skmage_ltng4` | ResLi(H) | 115 | **100** |
| MonStats.txt | `fetishblow3` | ResCo(H) | 140 | **100** |
| MonStats.txt | `fetishblow4` | ResPo(H) | 110 | **100** |
| MonStats.txt | `trappedsoul1` | ResCo(H) | 150 | **100** |
| MonStats.txt | `trappedsoul2` | ResCo(H) | 150 | **100** |
| MonStats.txt | `barricadetower` | ResFi(H) | 110 | **100** |
| MonStats.txt | `reanimatedhorde1` | ResCo(H) | 130 | **100** |
| MonStats.txt | `reanimatedhorde2` | ResCo(H) | 150 | **100** |
| MonStats.txt | `reanimatedhorde3` | ResCo(H) | 170 | **100** |
| MonStats.txt | `siegebeast1` | ResFi(H) | 110 | **100** |
| MonStats.txt | `siegebeast2` | ResFi(H) | 120 | **100** |
| MonStats.txt | `siegebeast3` | ResCo(H) | 120 | **100** |
| MonStats.txt | `siegebeast4` | ResCo(H) | 130 | **100** |
| MonStats.txt | `siegebeast5` | ResCo(H) | 140 | **100** |
| MonStats.txt | `snowyeti1` | ResCo(H) | 150 | **100** |
| MonStats.txt | `snowyeti2` | ResCo(H) | 170 | **100** |
| MonStats.txt | `snowyeti3` | ResCo(H) | 190 | **100** |
| MonStats.txt | `snowyeti4` | ResCo(H) | 210 | **100** |
| MonStats.txt | `minion1` | ResCo(H) | 130 | **100** |
| MonStats.txt | `minion2` | ResFi(H) | 105 | **100** |
| MonStats.txt | `minion3` | ResCo(H) | 140 | **100** |
| MonStats.txt | `minion4` | ResFi(H) | 110 | **100** |
| MonStats.txt | `minion5` | ResFi(H) | 115 | **100** |
| MonStats.txt | `minion6` | ResCo(H) | 150 | **100** |
| MonStats.txt | `minion7` | ResFi(H) | 120 | **100** |
| MonStats.txt | `minion8` | ResCo(H) | 160 | **100** |
| MonStats.txt | `suicideminion1` | ResCo(H) | 130 | **100** |
| MonStats.txt | `suicideminion2` | ResFi(H) | 105 | **100** |
| MonStats.txt | `suicideminion3` | ResCo(H) | 140 | **100** |
| MonStats.txt | `suicideminion4` | ResFi(H) | 110 | **100** |
| MonStats.txt | `suicideminion5` | ResFi(H) | 115 | **100** |
| MonStats.txt | `suicideminion6` | ResCo(H) | 150 | **100** |
| MonStats.txt | `suicideminion7` | ResFi(H) | 120 | **100** |
| MonStats.txt | `suicideminion8` | ResCo(H) | 160 | **100** |
| MonStats.txt | `succubus1` | ResFi(H) | 120 | **100** |
| MonStats.txt | `succubus2` | ResPo(H) | 110 | **100** |
| MonStats.txt | `succubus5` | ResPo(H) | 120 | **100** |
| MonStats.txt | `succubuswitch1` | ResCo(H) | 140 | **100** |
| MonStats.txt | `succubuswitch2` | ResFi(H) | 110 | **100** |
| MonStats.txt | `succubuswitch4` | ResFi(H) | 120 | **100** |
| MonStats.txt | `succubuswitch5` | ResCo(H) | 160 | **100** |
| MonStats.txt | `overseer1` | ResCo(H) | 120 | **100** |
| MonStats.txt | `overseer2` | ResCo(H) | 130 | **100** |
| MonStats.txt | `overseer3` | ResCo(H) | 140 | **100** |
| MonStats.txt | `overseer4` | ResCo(H) | 150 | **100** |
| MonStats.txt | `overseer5` | ResCo(H) | 160 | **100** |
| MonStats.txt | `imp2` | ResFi(H) | 105 | **100** |
| MonStats.txt | `imp3` | ResFi(H) | 110 | **100** |
| MonStats.txt | `imp4` | ResFi(H) | 115 | **100** |
| MonStats.txt | `imp5` | ResFi(H) | 120 | **100** |
| MonStats.txt | `frozenhorror1` | ResCo(H) | 150 | **100** |
| MonStats.txt | `frozenhorror2` | ResCo(H) | 160 | **100** |
| MonStats.txt | `frozenhorror3` | ResCo(H) | 170 | **100** |
| MonStats.txt | `frozenhorror4` | ResCo(H) | 180 | **100** |
| MonStats.txt | `frozenhorror5` | ResCo(H) | 190 | **100** |
| MonStats.txt | `bloodlord1` | ResFi(H) | 110 | **100** |
| MonStats.txt | `bloodlord4` | ResCo(H) | 135 | **100** |
| MonStats.txt | `bloodlord5` | ResFi(H) | 120 | **100** |
| MonStats.txt | `deathmauler3` | ResCo(H) | 135 | **100** |
| MonStats.txt | `deathmauler5` | ResCo(H) | 145 | **100** |
| MonStats.txt | `ancientbarb1` | ResFi(H) | 110 | **100** |
| MonStats.txt | `ancientbarb3` | ResCo(H) | 150 | **100** |
| MonStats.txt | `putriddefiler2` | ResPo(H) | 105 | **100** |
| MonStats.txt | `putriddefiler3` | ResPo(H) | 110 | **100** |
| MonStats.txt | `putriddefiler4` | ResPo(H) | 115 | **100** |
| MonStats.txt | `putriddefiler5` | ResPo(H) | 120 | **100** |
| MonStats.txt | `painworm3` | ResCo(H) | 140 | **100** |
| MonStats.txt | `painworm5` | ResCo(H) | 150 | **100** |
| MonStats.txt | `venomlord` | ResPo(H) | 120 | **100** |
| MonStats.txt | `baaltentacle1` | ResCo(H) | 110 | **100** |
| MonStats.txt | `baaltentacle2` | ResCo(H) | 115 | **100** |
| MonStats.txt | `baaltentacle3` | ResCo(H) | 120 | **100** |
| MonStats.txt | `baaltentacle4` | ResCo(H) | 125 | **100** |
| MonStats.txt | `baaltentacle5` | ResCo(H) | 130 | **100** |
| MonStats.txt | `baalminion1` | ResFi(H) | 120 | **100** |
| MonStats.txt | `baalminion2` | ResFi(H) | 120 | **100** |
| MonStats.txt | `baalminion3` | ResFi(H) | 120 | **100** |
| MonStats.txt | `sk_archer7` | ResPo(H) | 110 | **100** |
| MonStats.txt | `sk_archer8` | ResPo(H) | 120 | **100** |
| MonStats.txt | `sk_archer9` | ResPo(H) | 130 | **100** |
| MonStats.txt | `sk_archer10` | ResPo(H) | 140 | **100** |
| MonStats.txt | `goatman7` | ResCo(H) | 135 | **100** |
| MonStats.txt | `goatman8` | ResCo(H) | 155 | **100** |
| MonStats.txt | `goatman9` | ResFi(H) | 110 | **100** |
| MonStats.txt | `goatman10` | ResCo(H) | 165 | **100** |
| MonStats.txt | `foulcrow5` | ResCo(H) | 120 | **100** |
| MonStats.txt | `foulcrow7` | ResPo(H) | 110 | **100** |
| MonStats.txt | `clawviper7` | ResCo(H) | 145 | **100** |
| MonStats.txt | `clawviper7` | ResPo(H) | 110 | **100** |
| MonStats.txt | `clawviper8` | ResFi(H) | 115 | **100** |
| MonStats.txt | `clawviper9` | ResPo(H) | 110 | **100** |
| MonStats.txt | `clawviper10` | ResPo(H) | 115 | **100** |
| MonStats.txt | `sandraider6` | ResFi(H) | 120 | **100** |
| MonStats.txt | `sandraider7` | ResCo(H) | 150 | **100** |
| MonStats.txt | `sandraider8` | ResFi(H) | 125 | **100** |
| MonStats.txt | `sandraider9` | ResCo(H) | 160 | **100** |
| MonStats.txt | `sandraider10` | ResFi(H) | 130 | **100** |
| MonStats.txt | `slinger7` | ResFi(H) | 110 | **100** |
| MonStats.txt | `slinger8` | ResCo(H) | 150 | **100** |
| MonStats.txt | `cr_archer6` | ResFi(H) | 115 | **100** |
| MonStats.txt | `cr_archer7` | ResCo(H) | 140 | **100** |
| MonStats.txt | `skmage_fire5` | ResFi(H) | 125 | **100** |
| MonStats.txt | `skmage_fire5` | ResPo(H) | 110 | **100** |
| MonStats.txt | `skmage_fire6` | ResFi(H) | 130 | **100** |
| MonStats.txt | `skmage_fire6` | ResPo(H) | 110 | **100** |
| MonStats.txt | `skmage_ltng5` | ResLi(H) | 120 | **100** |
| MonStats.txt | `skmage_ltng5` | ResPo(H) | 110 | **100** |
| MonStats.txt | `skmage_ltng6` | ResLi(H) | 130 | **100** |
| MonStats.txt | `skmage_ltng6` | ResPo(H) | 110 | **100** |
| MonStats.txt | `skmage_cold5` | ResCo(H) | 160 | **100** |
| MonStats.txt | `skmage_cold5` | ResPo(H) | 110 | **100** |
| MonStats.txt | `sandleaper7` | ResCo(H) | 120 | **100** |
| MonStats.txt | `succubuswitch6` | ResCo(H) | 125 | **100** |
| MonStats.txt | `succubuswitch7` | ResCo(H) | 145 | **100** |
| MonStats.txt | `succubuswitch8` | ResCo(H) | 155 | **100** |
| MonStats.txt | `willowisp5` | ResPo(H) | 105 | **100** |
| MonStats.txt | `willowisp6` | ResPo(H) | 110 | **100** |
| MonStats.txt | `willowisp7` | ResPo(H) | 115 | **100** |
| MonStats.txt | `skeleton6` | ResPo(H) | 105 | **100** |
| MonStats.txt | `skeleton7` | ResPo(H) | 110 | **100** |
| MonStats.txt | `bloodlord6` | ResFi(H) | 140 | **100** |
| MonStats.txt | `fetish6` | ResFi(H) | 105 | **100** |
| MonStats.txt | `fetish7` | ResFi(H) | 110 | **100** |
| MonStats.txt | `fetish8` | ResFi(H) | 115 | **100** |
| MonStats.txt | `fetishblow6` | ResFi(H) | 105 | **100** |
| MonStats.txt | `fetishblow7` | ResFi(H) | 110 | **100** |
| MonStats.txt | `fetishblow8` | ResFi(H) | 115 | **100** |
| MonStats.txt | `fetishshaman6` | ResFi(H) | 120 | **100** |
| MonStats.txt | `fetishshaman7` | ResFi(H) | 125 | **100** |
| MonStats.txt | `fetishshaman8` | ResFi(H) | 130 | **100** |
| MonStats.txt | `vilemother4` | ResCo(H) | 140 | **100** |
| MonStats.txt | `vilemother5` | ResCo(H) | 145 | **100** |
| MonStats.txt | `vilechild4` | ResCo(H) | 140 | **100** |
| MonStats.txt | `vilechild5` | ResCo(H) | 145 | **100** |
| MonStats.txt | `sandmaggot6` | ResPo(H) | 105 | **100** |
| MonStats.txt | `maggotbaby6` | ResPo(H) | 105 | **100** |
| MonStats.txt | `minion9` | ResCo(H) | 130 | **100** |
| MonStats.txt | `minion10` | ResFi(H) | 110 | **100** |
| MonStats.txt | `minion11` | ResCo(H) | 135 | **100** |
| MonStats.txt | `arach6` | ResFi(H) | 120 | **100** |
| MonStats.txt | `megademon4` | ResFi(H) | 140 | **100** |
| MonStats.txt | `megademon5` | ResFi(H) | 145 | **100** |
| MonStats.txt | `imp6` | ResFi(H) | 110 | **100** |
| MonStats.txt | `imp7` | ResFi(H) | 115 | **100** |
| MonStats.txt | `bonefetish6` | ResPo(H) | 105 | **100** |
| MonStats.txt | `bonefetish7` | ResPo(H) | 110 | **100** |
| MonStats.txt | `regurgitator4` | ResPo(H) | 110 | **100** |
| MonStats.txt | `vampire6` | ResCo(H) | 125 | **100** |
| MonStats.txt | `vampire7` | ResCo(H) | 130 | **100** |
| MonStats.txt | `vampire8` | ResCo(H) | 135 | **100** |
| MonStats.txt | `reanimatedhorde6` | ResPo(H) | 120 | **100** |
| MonStats.txt | `dkfig1` | ResFi(H) | 130 | **100** |
| MonStats.txt | `dkfig2` | ResFi(H) | 140 | **100** |
| MonStats.txt | `dkmag1` | ResCo(H) | 140 | **100** |
| MonStats.txt | `dkmag2` | ResCo(H) | 145 | **100** |
| MonStats.txt | `mummy6` | ResPo(H) | 130 | **100** |
| MonStats.txt | `ubermephisto` | ResLi(H) | 110 | **100** |
| MonStats.txt | `ubermephisto` | ResPo(H) | 110 | **100** |
| MonStats.txt | `uberdiablo` | ResFi(H) | 110 | **100** |
| MonStats.txt | `uberizual` | ResCo(H) | 110 | **100** |
| MonStats.txt | `uberandariel` | ResPo(H) | 110 | **100** |
| MonStats.txt | `uberbaal` | ResCo(H) | 110 | **100** |
| MonStats.txt | `megademon6` | ResFi(H) | 145 | **100** |
| MonStats.txt | `megademon6` | ResLi(H) | 145 | **100** |
| MonStats.txt | `megademon6` | ResCo(H) | 145 | **100** |
| MonStats.txt | `megademon6` | ResPo(H) | 145 | **100** |
| MonStats.txt | `dkmag3` | ResCo(H) | 145 | **100** |
| MonStats.txt | `imp8` | ResFi(H) | 115 | **100** |
| MonStats.txt | `sandmaggot7` | ResPo(H) | 105 | **100** |
| MonStats.txt | `arach7` | ResFi(H) | 120 | **100** |
| MonStats.txt | `succubuswitch9` | ResCo(H) | 155 | **100** |
| MonStats.txt | `corruptrogue6` | ResCo(H) | 150 | **100** |
| MonStats.txt | `cr_archer8` | ResCo(H) | 140 | **100** |
| MonStats.txt | `overseer6` | ResCo(H) | 160 | **100** |
| MonStats.txt | `skeleton8` | ResPo(H) | 110 | **100** |
| MonStats.txt | `sk_archer11` | ResPo(H) | 140 | **100** |
| MonStats.txt | `skmage_fire7` | ResFi(H) | 130 | **100** |
| MonStats.txt | `skmage_fire7` | ResPo(H) | 110 | **100** |
| MonStats.txt | `skmage_ltng7` | ResLi(H) | 130 | **100** |
| MonStats.txt | `skmage_ltng7` | ResPo(H) | 110 | **100** |
| MonStats.txt | `skmage_cold6` | ResCo(H) | 160 | **100** |
| MonStats.txt | `skmage_cold6` | ResPo(H) | 110 | **100** |
| MonStats.txt | `vampire9` | ResCo(H) | 135 | **100** |
| MonStats.txt | `willowisp8` | ResPo(H) | 115 | **100** |
| Skills.txt | `Fire Arrow` | mana | 24 | **8** |
| Skills.txt | `Cold Arrow` | mana | 28 | **12** |
| Skills.txt | `Fire Mastery` | Param1 | 30 | **24** |
| Skills.txt | `Fire Mastery` | Param2 | 7 | **4** |
| Skills.txt | `Lightning Mastery` | Param1 | 50 | **29** |
| Skills.txt | `Lightning Mastery` | Param2 | 12 | **9** |
| Skills.txt | `Poison Nova` | mana | 20 | **16** |
| Skills.txt | `Volcano` | mana | 25 | **16** |
| Skills.txt | `Armageddon` | mana | 35 | **25** |

## 所有非数值改动（改名/换引用/加行）

| 表 | 行 | 列 | 前 | 后 |
|---|---|---|---|---|
| Skills.txt | `Multiple Shot` | LevToHit | `` | `10` |
| Skills.txt | `Strafe` | LevToHit | `` | `10` |
| Skills.txt | `Fire Mastery` | passivestat2 | `` | `passive_fire_pierce` |
| Skills.txt | `Fire Mastery` | passivecalc2 | `` | `ln34` |
| Skills.txt | `Fire Mastery` | Param3 | `` | `7` |
| Skills.txt | `Fire Mastery` | Param4 | `` | `2` |
| Skills.txt | `Lightning Mastery` | passivestat2 | `` | `passive_ltng_pierce` |
| Skills.txt | `Lightning Mastery` | passivecalc2 | `` | `ln34` |
| Skills.txt | `Lightning Mastery` | Param3 | `` | `6` |
| Skills.txt | `Lightning Mastery` | Param4 | `` | `1` |

新增行：
- CubeMain.txt：`magic helm + jewel + io + gpr -> fire pierce helm`
- CubeMain.txt：`magic helm + jewel + io + gpy -> lightning pierce helm`
- CubeMain.txt：`magic helm + jewel + io + gpb -> cold pierce helm`
- CubeMain.txt：`magic helm + jewel + io + gpg -> poison pierce helm`
