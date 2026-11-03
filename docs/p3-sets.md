# P3 · 套装体检表

> 由 `python3 -m tools.p3_sets` 生成，**只读**。单件强度沿用 `p3_items` 的同一把尺子。

判据（E1 的套装版）：**每一套要能回答「几件之后值得穿」**。
三种情况：

- ✅ **单件就有身份**：某件单穿就够强
- ✅ **凑到 2~3 件有身份**：加成够强，且件数门槛低 —— 这是套装最健康的设计
- ⚠️ **只有全套才有意义**：单件弱、2/3 件加成也弱 —— 单机开荒里基本等于不存在

> `add func` 是「套装加成随件数增长」的函数编号，行为在硬编码里，本工具不猜。

## 总表（按套装等级）

| 套装 | 件数 | 需求 | 部位 | 最强单件 | 2/3 件加成 | 全套加成 | 判定 |
|---|---:|---:|---|---|---|---|---|
| Arctic Gear | 4 | 2~2 | belt、bow、glov、tors | Arctic Binding（1 项） | 3件:hp=50 | — | ✅ 单件够强，凑 2~3 件还有真加成 |
| Hsarus' Defense | 3 | 3~3 | belt、boot、shie | Hsarus' Iron Heel（2 项） | — | 1项 | ✅ 单件有身份；凑套加成偏低 |
| Berserker's Garb | 3 | 3~3 | axe、helm、tors | Berserker's Headgear（1 项） | 2件:hp=50 | — | ✅ 单件够强，凑 2~3 件还有真加成 |
| Cleglaw's Brace | 3 | 4~4 | glov、shie、swor | Cleglaw's Pincers（2 项） | — | 3项 | ✅ 单件有身份；凑套加成偏低 |
| Infernal Tools | 3 | 5~5 | belt、helm、wand | Infernal Cranium（0 项） | — | 2项 | ⚠️ 只有全套有意义 |
| Death's Disguise | 3 | 6~6 | belt、glov、swor | Death's Hand（1 项） | 2件:lifesteal=8 | 3项 | ✅ 单件够强，凑 2~3 件还有真加成 |
| Sigon's Complete Steel | 6 | 6~6 | belt、boot、glov、helm、shie、tors | Sigon's Sabot（2 项） | 2件:lifesteal=10 | — | ✅ 单件够强，凑 2~3 件还有真加成 |
| Isenhart's Armory | 4 | 8~8 | helm、shie、swor、tors | Isenhart's Lightbrand（1 项） | — | 1项 | ✅ 单件有身份；凑套加成偏低 |
| Civerb's Vestments | 3 | 9~9 | amul、scep、shie | Civerb's Ward（1 项） | — | 1项 | ✅ 单件有身份；凑套加成偏低 |
| Cathan's Traps | 5 | 11~11 | amul、helm、ring、staf、tors | Cathan's Visage（1 项） | 3件:res-ltng=25 | 4项 | ✅ 单件够强，凑 2~3 件还有真加成 |
| Angelical Raiment | 4 | 12~12 | amul、ring、swor、tors | Angelic Sickle（1 项） | 3件:mana=50 | 4项 | ✅ 单件够强，凑 2~3 件还有真加成 |
| Vidala's Rig | 4 | 14~14 | amul、boot、bow、tors | Vidala's Fetlock（1 项） | — | — | ✅ 单件有身份；凑套加成偏低 |
| Arcanna's Tricks | 4 | 15~15 | amul、helm、staf、tors | Arcanna's Deathwand（1 项） | 3件:hp=50 | 2项 | ✅ 单件够强，凑 2~3 件还有真加成 |
| Cow King's Leathers | 3 | 13~25 | boot、helm、tors | Cow King's Hoofs（3 项） | 2件:res-pois=25 | 2项 | ✅ 单件够强，凑 2~3 件还有真加成 |
| McAuley's Folly | 4 | 20~28 | boot、glov、helm、wand | McAuley's Riprap（3 项） | — | 4项 | ✅ 单件有身份；凑套加成偏低 |
| Iratha's Finery | 4 | 15~15 | amul、belt、glov、helm | Iratha's Coil（2 项） | — | 3项 | ✅ 单件有身份；凑套加成偏低 |
| M'avina's Battle Hymn | 5 | 32~70 | abow、belt、circ、glov、tors | M'avina's Embrace（2 项） | — | 4项 | ✅ 单件有身份；凑套加成偏低 |
| Natalya's Odium | 4 | 25~79 | boot、h2h2、helm、tors | Natalya's Totem（5 项） | — | 6项 | ✅ 单件有身份；凑套加成偏低 |
| Milabrega's Regalia | 4 | 17~17 | helm、scep、shie、tors | Milabrega's Orb（1 项） | — | 2项 | ✅ 单件有身份；凑套加成偏低 |
| Tal Rasha's Wrappings | 5 | 53~71 | amul、belt、helm、orb、tors | Tal Rasha's Lidless Eye（5 项） | 3件:item_magicbonus=65 | 4项 | ✅ 单件够强，凑 2~3 件还有真加成 |
| Tancred's Battlegear | 5 | 20~20 | amul、axe、boot、helm、tors | Tancred's Spine（2 项） | 3件:lifesteal=5 | 1项 | ✅ 单件够强，凑 2~3 件还有真加成 |
| Hwanin's Majesty | 4 | 28~45 | belt、helm、pole、tors | Hwanin's Justice（4 项） | — | 5项 | ✅ 单件有身份；凑套加成偏低 |
| Aldur's Watchtower | 4 | 36~76 | boot、mace、pelt、tors | Aldur's Gauntlet（7 项） | 3件:item_magicbonus=50 | 5项 | ✅ 单件够强，凑 2~3 件还有真加成 |
| Trang-Oul's Avatar | 5 | 45~65 | belt、glov、head、helm、tors | Trang-Oul's Wing（6 项） | 2件:skill=18/3件:skill=13 | 6项 | ✅ 单件够强，凑 2~3 件还有真加成 |
| Sazabi's Grand Tribute | 3 | 43~73 | helm、swor、tors | Sazabi's Cobalt Redeemer（5 项） | — | 4项 | ✅ 单件有身份；凑套加成偏低 |
| Immortal King | 6 | 29~76 | belt、boot、glov、hamm、phlm、tors | Immortal King's Stone Crusher（7 项） | — | 4项 | ✅ 单件有身份；凑套加成偏低 |
| The Disciple | 5 | 29~65 | amul、belt、boot、glov、tors | Laying of Hands（3 项） | — | 5项 | ✅ 单件有身份；凑套加成偏低 |
| Orphan's Call | 4 | 29~42 | belt、glov、helm、shie | Guillaume's Face（4 项） | 2件:hp=35 | 2项 | ✅ 单件够强，凑 2~3 件还有真加成 |
| Naj's Ancient Set | 3 | 28~78 | circ、staf、tors | Naj's Light Plate（7 项） | — | 5项 | ✅ 单件有身份；凑套加成偏低 |
| Griswold's Legacy | 4 | 45~69 | ashd、helm、scep、tors | Griswold's Heart（4 项） | — | 5项 | ✅ 单件有身份；凑套加成偏低 |
| Bul-Kathos' Children | 2 | 54~61 | swor | Bul-Kathos' Sacred Charge（7 项） | — | 1项 | ✅ 单件有身份；凑套加成偏低 |
| Heaven's Brethren | 4 | 44~81 | helm、mace、shie、tors | Heaven's Taebaek（4 项） | — | 4项 | ✅ 单件有身份；凑套加成偏低 |

## 候选：只有全套才有意义 / 全套也弱

| 套装 | 件数 | 需求 | 2~5 件加成原文 | 为什么可疑 |
|---|---:|---:|---|---|
| Infernal Tools | 3 | 5~5 | 2件: dmg-pois=25~25；3件: mana=10~10 | ⚠️ 只有全套有意义 |

## 单件表（按套装 → 需求等级）

| 件 | 套装 | 部位 | 需求 | 强属性 | 未量化 | 单穿值得吗？ |
|---|---|---|---:|---|---|---|
| Arctic Horn | Arctic Gear | bow | 2 | — | — |  |
| Arctic Furs | Arctic Gear | tors | 2 | — | — |  |
| Arctic Binding | Arctic Gear | belt | 2 | res-cold=40 | — |  |
| Arctic Mitts | Arctic Gear | glov | 2 | ias=10 | — |  |
| Hsarus' Iron Heel | Hsarus' Defense | boot | 3 | res-fire=25、frw=20 | — |  |
| Hsarus' Iron Fist | Hsarus' Defense | shie | 3 | str=10 | — |  |
| Hsarus' Iron Stay | Hsarus' Defense | belt | 3 | res-cold=20 | — |  |
| Berserker's Headgear | Berserker's Garb | helm | 3 | res-fire=25 | — |  |
| Berserker's Hauberk | Berserker's Garb | tors | 3 | — | 是（含触发技能/充能） |  |
| Berserker's Hatchet | Berserker's Garb | axe | 3 | manasteal=5 | — |  |
| Cleglaw's Tooth | Cleglaw's Brace | swor | 4 | ds=50 | — |  |
| Cleglaw's Claw | Cleglaw's Brace | shie | 4 | — | — |  |
| Cleglaw's Pincers | Cleglaw's Brace | glov | 4 | item_knockback=1、item_slow=25 | — |  |
| Infernal Cranium | Infernal Tools | helm | 5 | — | — |  |
| Infernal Torch | Infernal Tools | wand | 5 | — | 是（含触发技能/充能） |  |
| Infernal Sign | Infernal Tools | belt | 5 | — | — |  |
| Death's Hand | Death's Disguise | glov | 6 | res-pois=50 | — |  |
| Death's Guard | Death's Disguise | belt | 6 | item_cannotbefrozen=1 | — |  |
| Death's Touch | Death's Disguise | swor | 6 | lifesteal=4 | — |  |
| Sigon's Gage | Sigon's Complete Steel | glov | 6 | str=10 | — |  |
| Sigon's Visor | Sigon's Complete Steel | helm | 6 | — | — |  |
| Sigon's Shelter | Sigon's Complete Steel | tors | 6 | res-ltng=30 | — |  |
| Sigon's Sabot | Sigon's Complete Steel | boot | 6 | frw=20、res-cold=40 | — |  |
| Sigon's Wrap | Sigon's Complete Steel | belt | 6 | res-fire=20 | — |  |
| Sigon's Guard | Sigon's Complete Steel | shie | 6 | skills=1、block=20 | — |  |
| Isenhart's Lightbrand | Isenhart's Armory | swor | 8 | ias=20 | — |  |
| Isenhart's Parry | Isenhart's Armory | shie | 8 | — | — |  |
| Isenhart's Case | Isenhart's Armory | tors | 8 | — | — |  |
| Isenhart's Horns | Isenhart's Armory | helm | 8 | — | — |  |
| Civerb's Ward | Civerb's Vestments | shie | 9 | block=15 | — |  |
| Civerb's Icon | Civerb's Vestments | amul | 9 | — | — |  |
| Civerb's Cudgel | Civerb's Vestments | scep | 9 | — | — |  |
| Cathan's Rule | Cathan's Traps | staf | 11 | — | 是（含触发技能/充能） |  |
| Cathan's Mesh | Cathan's Traps | tors | 11 | — | — |  |
| Cathan's Visage | Cathan's Traps | helm | 11 | res-cold=25 | — |  |
| Cathan's Sigil | Cathan's Traps | amul | 11 | fhr=10 | — |  |
| Cathan's Seal | Cathan's Traps | ring | 11 | lifesteal=6 | — |  |
| Angelic Sickle | Angelical Raiment | swor | 12 | item_undeaddamage_percent=250 | — |  |
| Angelic Mantle | Angelical Raiment | tors | 12 | — | — |  |
| Angelic Halo | Angelical Raiment | ring | 12 | — | — |  |
| Angelic Wings | Angelical Raiment | amul | 12 | — | — |  |
| Vidala's Barb | Vidala's Rig | bow | 14 | — | — |  |
| Vidala's Fetlock | Vidala's Rig | boot | 14 | frw=30 | — |  |
| Vidala's Ambush | Vidala's Rig | tors | 14 | dex=11 | — |  |
| Vidala's Snare | Vidala's Rig | amul | 14 | res-cold=20 | — |  |
| Arcanna's Sign | Arcanna's Tricks | amul | 15 | — | — |  |
| Arcanna's Deathwand | Arcanna's Tricks | staf | 15 | ds=25 | — |  |
| Arcanna's Head | Arcanna's Tricks | helm | 15 | — | — |  |
| Arcanna's Flesh | Arcanna's Tricks | tors | 15 | — | — |  |
| Cow King's Hoofs | Cow King's Leathers | boot | 13 | frw=30、item_magicbonus=25、dex=20 | — |  |
| Cow King's Hide | Cow King's Leathers | tors | 18 | hp=30 | — |  |
| Cow King's Horns | Cow King's Leathers | helm | 25 | item_damagetomana=35 | — |  |
| McAuley's Riprap | McAuley's Folly | boot | 20 | frw=40、ar=100、dex=10 | — |  |
| McAuley's Paragon | McAuley's Folly | helm | 25 | item_magicbonus=35 | — |  |
| McAuley's Superstition | McAuley's Folly | wand | 25 | manasteal=8、fcr=20、elem_dmg=75 | — |  |
| McAuley's Taboo | McAuley's Folly | glov | 28 | ias=20、hp=40 | — |  |
| Iratha's Collar | Iratha's Finery | amul | 15 | res-pois=30 | — |  |
| Iratha's Cuff | Iratha's Finery | glov | 15 | res-cold=30 | — |  |
| Iratha's Coil | Iratha's Finery | helm | 15 | res-fire=30、res-ltng=30 | — |  |
| Iratha's Cord | Iratha's Finery | belt | 15 | — | — |  |
| M'avina's Icy Clutch | M'avina's Battle Hymn | glov | 32 | str=10、dex=15 | — |  |
| M'avina's Tenet | M'avina's Battle Hymn | belt | 45 | frw=20、manasteal=5 | — |  |
| M'avina's True Sight | M'avina's Battle Hymn | circ | 59 | ias=30 | — |  |
| M'avina's Embrace | M'avina's Battle Hymn | tors | 70 | skilltab=2、def=350 | — |  |
| M'avina's Caster | M'avina's Battle Hymn | abow | 70 | ed=188、ias=40 | — |  |
| Natalya's Soul | Natalya's Odium | boot | 25 | frw=40、res-cold=25、res-ltng=25 | — |  |
| Natalya's Totem | Natalya's Odium | helm | 59 | dex=30、str=20、res-fire=20、res-ltng=20、res-cold=20 | — |  |
| Natalya's Shadow | Natalya's Odium | tors | 73 | def=225、skilltab=2、res-pois=25、sock=3 | — |  |
| Natalya's Mark | Natalya's Odium | h2h2 | 79 | ias=40、ed=200、elem_dmg=50、item_undeaddamage_percent=200、item_demondamage_percent=200 | — |  |
| Milabrega's Orb | Milabrega's Regalia | shie | 17 | item_magicbonus=20 | — |  |
| Milabrega's Rod | Milabrega's Regalia | scep | 17 | — | 是（含触发技能/充能） |  |
| Milabrega's Diadem | Milabrega's Regalia | helm | 17 | — | — |  |
| Milabrega's Robe | Milabrega's Regalia | tors | 17 | — | — |  |
| Tal Rasha's Fire-Spun Cloth | Tal Rasha's Wrappings | belt | 53 | dex=20、item_damagetomana=37 | — |  |
| Tal Rasha's Lidless Eye | Tal Rasha's Wrappings | orb | 65 | hp=57、mana=77、enr=10、fcr=20、skill=2 | — |  |
| Tal Rasha's Horadric Crest | Tal Rasha's Wrappings | helm | 66 | hp=60、lifesteal=10、manasteal=10 | — |  |
| Tal Rasha's Adjudication | Tal Rasha's Wrappings | amul | 67 | res-ltng=33、hp=50、mana=42 | — |  |
| Tal Rasha's Howling Wind | Tal Rasha's Wrappings | tors | 71 | item_magicbonus=88、res-cold=40、res-fire=40、res-ltng=40、def=400 | — |  |
| Tancred's Crowbill | Tancred's Battlegear | axe | 20 | ed=80 | — |  |
| Tancred's Spine | Tancred's Battlegear | tors | 20 | hp=40、str=15 | — |  |
| Tancred's Hobnails | Tancred's Battlegear | boot | 20 | dex=10 | — |  |
| Tancred's Weird | Tancred's Battlegear | amul | 20 | — | — |  |
| Tancred's Skull | Tancred's Battlegear | helm | 20 | — | — |  |
| Hwanin's Justice | Hwanin's Majesty | pole | 28 | ar=330、indestruct=1、ias=40、ed=200 | — |  |
| Hwanin's Refuge | Hwanin's Majesty | tors | 30 | def=200、res-pois=27、hp=100 | — |  |
| Hwanin's Seal | Hwanin's Majesty | belt | 35 | item_preventheal=1 | — |  |
| Hwanin's Splendor | Hwanin's Majesty | helm | 45 | res-cold=37 | — |  |
| Aldur's Stony Gaze | Aldur's Watchtower | pelt | 36 | fhr=25、res-cold=50、sock=2 | — |  |
| Aldur's Gauntlet | Aldur's Watchtower | mace | 42 | add_dmg=62、elem_dmg=75、lifesteal=10、ias=30、item_demondamage_percent=200、manasteal=5、sock=5 | — |  |
| Aldur's Advance | Aldur's Watchtower | boot | 45 | indestruct=1、hp=50、frw=40、res-fire=50 | — |  |
| Aldur's Deception | Aldur's Watchtower | tors | 76 | def=300、skilltab=1、str=20、dex=15、res-ltng=50 | — |  |
| Trang-Oul's Claws | Trang-Oul's Avatar | glov | 45 | fcr=20、res-cold=30、skilltab=2 | — |  |
| Trang-Oul's Girth | Trang-Oul's Avatar | belt | 47 | hp=66、item_cannotbefrozen=1、mana=50 | — |  |
| Trang-Oul's Scales | Trang-Oul's Avatar | tors | 49 | res-pois=40、skilltab=2、frw=40 | — |  |
| Trang-Oul's Wing | Trang-Oul's Avatar | head | 54 | str=25、dex=15、res-fire=45、block=30、res-pois=40、skilltab=2 | — |  |
| Trang-Oul's Guise | Trang-Oul's Avatar | helm | 65 | fhr=25、mana=150 | — |  |
| Sazabi's Mental Sheath | Sazabi's Grand Tribute | helm | 43 | skills=1、res-fire=20、res-ltng=20 | — |  |
| Sazabi's Ghost Liberator | Sazabi's Grand Tribute | tors | 67 | def=400、fhr=30、str=25、hp=75 | — |  |
| Sazabi's Cobalt Redeemer | Sazabi's Grand Tribute | swor | 73 | ed=150、ias=40、item_demondamage_percent=318、indestruct=1、dex=15 | — |  |
| Immortal King's Detail | Immortal King | belt | 29 | res-fire=28、res-ltng=31、str=25 | — |  |
| Immortal King's Forge | Immortal King | glov | 30 | str=20、dex=20 | — |  |
| Immortal King's Pillar | Immortal King | boot | 31 | frw=40、ar=110、hp=44 | — |  |
| Immortal King's Will | Immortal King | phlm | 47 | skilltab=2、item_magicbonus=40、sock=2 | — |  |
| Immortal King's Soul Cage | Immortal King | tors | 76 | def=400、skilltab=2、res-pois=50 | — |  |
| Immortal King's Stone Crusher | Immortal King | hamm | 76 | indestruct=1、ias=40、item_demondamage_percent=200、item_undeaddamage_percent=200、cb=40、ed=200、sock=2 | — |  |
| Rite of Passage | The Disciple | boot | 29 | frw=30 | — |  |
| Telling of Beads | The Disciple | amul | 30 | res-pois=50、skills=1 | — |  |
| Spiritual Custodian | The Disciple | tors | 43 | def=415、res-fire=24、elem_dmg=175 | — |  |
| Laying of Hands | The Disciple | glov | 63 | ias=20、res-fire=50、item_demondamage_percent=350 | — |  |
| Credendum | The Disciple | belt | 65 | str=10、dex=10 | — |  |
| Wihtstan's Guard | Orphan's Call | shie | 29 | block=55 | — |  |
| Guillaume's Face | Orphan's Call | helm | 34 | fhr=30、cb=35、ds=15、str=15 | — |  |
| Magnus' Skin | Orphan's Call | glov | 37 | ias=20、ar=100 | — |  |
| Wilhelm's Pride | Orphan's Call | belt | 42 | manasteal=5、lifesteal=5 | — |  |
| Naj's Circlet | Naj's Ancient Set | circ | 28 | str=15 | — |  |
| Naj's Light Plate | Naj's Ancient Set | tors | 71 | hp=65、res-fire=25、res-ltng=25、res-cold=25、item_damagetomana=45、skills=1、def=300 | — |  |
| Naj's Puzzler | Naj's Ancient Set | staf | 78 | enr=35、ed=150、fcr=30、elem_dmg=45、mana=70、skills=1 | — |  |
| Griswold's Heart | Griswold's Legacy | tors | 45 | def=500、skilltab=2、sock=3、str=20 | — |  |
| Griswolds's Redemption | Griswold's Legacy | scep | 53 | ed=240、ias=40、item_undeaddamage_percent=200、sock=4 | — |  |
| Griswold's Honor | Griswold's Legacy | ashd | 68 | block=20、res-fire=45、res-ltng=45、res-cold=45 | — |  |
| Griswold's Valor | Griswold's Legacy | helm | 69 | sock=2、item_magicbonus=30 | — |  |
| Bul-Kathos' Tribal Guardian | Bul-Kathos' Children | swor | 54 | res-fire=50、elem_dmg=255、ias=20、str=20、ed=200 | — |  |
| Bul-Kathos' Sacred Charge | Bul-Kathos' Children | swor | 61 | cb=35、res-fire=20、res-ltng=20、res-cold=20、ias=20、item_knockback=1、ed=200 | — |  |
| Haemosu's Adament | Heaven's Brethren | tors | 44 | def=500、hp=75 | — |  |
| Dangoon's Teaching | Heaven's Brethren | mace | 68 | ias=40 | — |  |
| Ondal's Almighty | Heaven's Brethren | helm | 69 | str=10、dex=15、fhr=24 | — |  |
| Heaven's Taebaek | Heaven's Brethren | shie | 81 | mana=100、res-ltng=30、indestruct=1、block=25 | — |  |
