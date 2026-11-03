# P3 · 符文之语 vs 暗金 / 套装

> 由 `python3 -m tools.p3_runewords` 生成，**只读**。

前两份体检（暗金 380 件、套装 32 套）的结论是「单表内部几乎没有垃圾」。
这份文档测另一件事：**是不是被低阶符文之语整体比下去了。**

口径：

- RW 需求 = `max(底材需求, 最高的符文需求)`；符文需求取自 `Misc.txt`
- 符文成本 = 各符文需求等级之和（粗粒度替代稀有度）
- 槽位兼容走 `ItemTypes.txt` 的 `Equiv1/Equiv2` 祖先链（`swor → mele → weap`）
- 判定「替代」要求：槽位兼容 + **需求不更高** + **每一项都不差**
- 含触发技能/充能的**放弃判定**，不猜

## 汇总：0 件暗金/套装被符文之语完全替代

（另有 241 件因为含有无法量化的属性而没被判，可能被替代但不敢下结论）

无。

## 按需求等级段比较「强度天花板」

每一档里：**暗金最多能给几条强属性 / 套装呢 / 符文之语呢**。
RW 如果在某一档明显更高，这一档的暗金和套装就整体失去理由 —— 而这正是「某些装备谁也用不上」的真实成因（不是它差，是同一档有人更强）。

| 需求段 | 暗金最高 | 套装最高 | RW 最高 | RW 领先 |
|---|---|---|---|---|
| 1~19 | The Chieftan（8） | Cow King's Hoofs（3） | Stealth（3） | -5 |
| 20~29 | Razorswitch（7） | Hwanin's Justice（4） | Edge（8） | +1 |
| 30~39 | Fleshrender（8） | Guillaume's Face（4） | Smoke（5） | -3 |
| 40~49 | Bloodtree Stump（9） | Aldur's Gauntlet（7） | Obedience（8） | -1 |
| 50~59 | Que-Hegan's Wisdon（6） | Trang-Oul's Wing（6） | Silence（8） | +2 |
| 60~69 | Ironward（10） | Bul-Kathos' Sacred Charge（7） | Bound by Duty（8） | -2 |
| 70~+ | The Cranium Basher（9） | Immortal King's Stone Crusher（7） | — | — |

## 最「划算」的符文之语（成本低、需求低、加成多）

按「强属性条数 ÷ 符文成本」排序 —— 这一列就是「为什么中阶暗金没人用」的直接证据。

| RW | 需求 | 孔 | 符文 | 成本 | 强属性 | 槽位 |
|---|---:|---:|---|---:|---|---|
| Edge | 25 | 3 | r03 r07 r11 | 55 | item_demondamage_percent=380、item_undeaddamage_percent=280、ias=35、item_preventheal=1、skill=15、str=10、enr=10、dex=10 | miss |
| Rhyme | 29 | 2 | r13 r05 | 44 | block=20、res-fire=25、res-ltng=25、res-cold=25、item_cannotbefrozen=1、item_magicbonus=25 | shld |
| Smoke | 37 | 2 | r04 r17 | 50 | def=250、res-fire=50、res-ltng=50、res-cold=50、fhr=20 | tors |
| Stealth | 17 | 2 | r07 r05 | 32 | frw=25、fcr=25、fhr=25 | tors |
| Lionheart | 41 | 3 | r15 r17 r19 | 78 | str=15、vit=20、dex=15、hp=50、res-fire=30、res-ltng=30、res-cold=30 | tors |
| Steel | 13 | 2 | r03 r01 | 24 | ias=25、ow=50 | swor、axe、mace |
| Strength | 25 | 2 | r11 r03 | 38 | str=20、vit=10、cb=25 | mele |
| Spirit | 25 | 4 | r07 r10 r09 r11 | 86 | fhr=55、mana=112、def=250、vit=22、fcr=35、skills=2 | swor、shld |
| Obedience | 41 | 5 | r15 r18 r10 r05 r19 | 118 | ed=370、cb=40、elem_pierce=25、def=300、fhr=40、res-fire=30、res-ltng=30、res-cold=30 | pole |
| Insight | 27 | 4 | r08 r03 r07 r12 | 76 | ed=260、ar=250、item_magicbonus=23、skill=17、fcr=35 | pole、staf |
| Prudence | 49 | 2 | r23 r03 | 62 | res-fire=35、res-ltng=35、res-cold=35、fhr=25 | tors |
| Leaf | 19 | 2 | r03 r08 | 32 | res-cold=33、skill=3 | staf |
| King's Grace | 25 | 3 | r11 r08 r10 | 67 | ed=100、ar=150、item_demondamage_percent=100、item_undeaddamage_percent=50 | swor、scep |
| Splendor | 37 | 2 | r05 r17 | 52 | item_magicbonus=20、fcr=10、skills=1 | shld |
| Black | 35 | 3 | r10 r16 r04 | 71 | cb=40、ed=120、ias=15、ar=200 | club、hamm、mace |
| Holy Thunder | 21 | 4 | r05 r08 r09 r07 | 72 | elem_dmg=60、res-ltng=60、maxlightresist=5、skill=3 | scep |
| Zephyr | 21 | 2 | r09 r05 | 36 | frw=25、ias=25 | miss |
| Wind | 61 | 2 | r29 r01 | 72 | ed=160、ias=40、frw=20、fhr=15 | mele |
| Honor | 27 | 5 | r11 r01 r06 r03 r12 | 91 | ed=160、skills=1、ar=200、ds=25、str=10 | mele |
| Fury | 65 | 3 | r31 r25 r05 | 133 | ed=209、ias=40、item_preventheal=1、ow=66、lifesteal=6、ds=33、skill=5 | mele |

## 全部符文之语（按需求等级）

| RW | 需求 | 孔 | 符文 | 成本 | 加成原文 |
|---|---:|---:|---|---:|---|
| Steel | 13 | 2 | r03 r01 | 24 | swing2=25~25、dmg-min=3~3、dmg-max=3~3、openwounds=50~50、dmg%=20~20 |
| Nadir | 13 | 2 | r04 r03 | 26 | ac%=50~50、ac=10~10、light=-3~-3、charged=9~13、gold%=-33~-33、str=5~5 |
| Malice | 15 | 3 | r06 r01 r05 | 41 | openwounds=100~100、dmg-ac=-100~-100、noheal=1~1、dmg%=33~33、light=-1~-1、regen=-5~-5 |
| Stealth | 17 | 2 | r07 r05 | 32 | red-mag=3~3、dex=6~6、stam=15~15、move2=25~25、cast2=25~25、balance2=25~25 |
| Leaf | 19 | 2 | r03 r08 | 32 | fireskill=3~3、ac/lvl=16~16、res-cold=33~33、skill=3~3、skill=3~3、skill=3~3 |
| Zephyr | 21 | 2 | r09 r05 | 36 | move2=25~25、swing2=25~25、dmg%=33~33、att=66~66、gethit-skill=7~1、ac=25~25 |
| Pattern | 21 | 3 | r07 r09 r03 | 51 | att%=10~10、dmg%=40~80、dmg-fire=12~32、res-all=15~15、str=6~6、dex=6~6、block2=30~30 |
| Ancient's Pledge | 21 | 3 | r08 r09 r07 | 57 | res-cold=30~30、res-all=13~13、ac%=50~50、dmg-to-mana=10~10 |
| Holy Thunder | 21 | 4 | r05 r08 r09 r07 | 72 | dmg%=60~60、dmg-ltng=20~60、dmg-max=10~10、res-ltng=60~60、res-ltng-max=5~5、skill=3~3、charged=60~7 |
| Strength | 25 | 2 | r11 r03 | 38 | str=20~20、dmg%=35~35、vit=10~10、crush=25~25 |
| Myth | 25 | 3 | r15 r11 r04 | 38 | hit-skill=10~1、gethit-skill=3~1、bar=2~2、regen=10~10 |
| Edge | 25 | 3 | r03 r07 r11 | 55 | dmg-demon=320~380、dmg-undead=280~280、swing2=35~35、noheal=1~1、aura=15~15、all-stats=5~10、cheap=15~15 |
| King's Grace | 25 | 3 | r11 r08 r10 | 67 | dmg%=100~100、att=150~150、dmg-demon=100~100、dmg-undead=50~50、att-demon=100~100、att-undead=100~100 |
| Spirit | 25 | 4 | r07 r10 r09 r11 | 86 | balance3=55~55、mana=89~112、ac-miss=250~250、vit=22~22、cast3=25~35、abs-mag=3~8、allskills=2~2 |
| Lore | 27 | 2 | r09 r12 | 48 | enr=10~10、allskills=1~1、light=2~2、mana-kill=2~2 |
| Radiance | 27 | 3 | r04 r12 r06 | 55 | light=5~5、enr=10~10、vit=10~10、red-mag=3~3、mana=33~33、ac%=75~75 |
| Insight | 27 | 4 | r08 r03 r07 r12 | 76 | dmg%=200~260、att%=180~250、mag%=23~23、oskill=1~6、cast2=35~35、aura=12~17、all-stats=5~5 |
| Honor | 27 | 5 | r11 r01 r06 r03 r12 | 91 | dmg%=160~160、regen=10~10、allskills=1~1、att=200~200、deadly=25~25、str=10~10 |
| Rhyme | 29 | 2 | r13 r05 | 44 | block2=20~20、block=20~20、res-all=25~25、nofreeze=1~1、gold%=50~50、mag%=25~25 |
| Peace | 29 | 3 | r13 r10 r11 | 77 | hit-skill=2~15、gethit-skill=4~5、ama=2~2、oskill=2~2 |
| White | 35 | 2 | r14 r16 | 66 | skilltab=3~3、red-mag=4~4、cast2=20~20、mana=13~13、skill=3~3、skill=2~2、skill=4~4 |
| Black | 35 | 3 | r10 r16 r04 | 71 | crush=40~40、dmg%=120~120、swing2=15~15、red-mag=2~2、att=200~200、charged=12~4 |
| Smoke | 37 | 2 | r04 r17 | 50 | ac-miss=250~250、ac%=75~75、res-all=50~50、balance2=20~20、light=-1~-1、charged=18~6 |
| Splendor | 37 | 2 | r05 r17 | 52 | light=3~3、gold%=50~50、mag%=20~20、ac%=60~100、block2=20~20、cast2=10~10、allskills=1~1 |
| Memory | 37 | 4 | r17 r16 r12 r05 | 114 | mana%=20~20、red-mag=7~7、ac%=50~50、cast2=33~33、sor=3~3、skill=3~3、skill=2~2 |
| Melody | 39 | 3 | r13 r18 r04 | 81 | dmg%=50~50、skilltab=3~3、skill=3~3、skill=3~3、skill=3~3、dmg-undead=300~300 |
| Harmony | 39 | 4 | r03 r06 r12 r18 | 94 | dmg%=200~275、dmg-elem=55~160、charged=25~20、aura=10~10、oskill=2~6、regen-mana=20~20、light=2~2 |
| Lionheart | 41 | 3 | r15 r17 r19 | 78 | str=15~15、vit=20~20、dex=15~15、dmg%=20~20、hp=50~50、res-all=30~30 |
| Obedience | 41 | 5 | r15 r18 r10 r05 r19 | 118 | dmg%=370~370、crush=40~40、kill-skill=30~21、pierce-fire=25~25、ac=200~300、balance3=40~40、res-all=20~30 |
| Wealth | 43 | 3 | r20 r18 r03 | 95 | gold%=250~250、mag%=100~100 |
| Treachery | 43 | 3 | r13 r10 r20 | 95 | hit-skill=25~15、gethit-skill=5~15、ass=2~2、swing2=45~45 |
| Winter | 43 | 4 | r20 r18 r01 r02 | 104 | dmg-demon=220~350、dmg-undead=280~300、dmg-cold=100~220、pierce-cold=24~24、hit-skill=18~20、hit-skill=15~13、nofreeze=1~1 |
| Passion | 43 | 4 | r14 r09 r02 r20 | 106 | dmg%=160~210、oskill=1~1、att%=50~80、oskill=1~1、swing2=25~25、charged=12~3、stupidity=10~10 |
| Lawbringer | 43 | 3 | r11 r20 r18 | 107 | dmg-cold=130~180、dmg-fire=150~210、aura=16~18、hit-skill=20~15、ac-miss=200~250、rip=1~1、reduce-ac=50~50 |
| Enlightenment | 45 | 3 | r21 r08 r12 | 91 | hit-skill=5~15、gethit-skill=5~15、sor=2~2、oskill=1~1 |
| Crescent Moon | 47 | 3 | r13 r22 r03 | 89 | pierce-ltng=35~35、ignore-ac=1~1、dmg%=180~220、abs-mag=9~11、charged=30~18、hit-skill=7~13、hit-skill=10~17 |
| Duress | 47 | 3 | r13 r22 r10 | 99 | dmg-cold=37~133、dmg%=10~20、ac%=150~200、balance2=20~20、openwounds=33~33、crush=15~15、stamdrain=-20~-20 |
| Bone | 47 | 3 | r12 r22 r22 | 121 | hit-skill=15~10、gethit-skill=15~10、nec=2~2、mana=100~150 |
| Gloom | 47 | 3 | r19 r22 r21 | 133 | ac%=170~230、res-all=30~30、gethit-skill=15~3、balance2=10~10、dmg-to-mana=5~5、light=-3~-3、half-freeze=1~1 |
| Stone | 47 | 4 | r13 r22 r21 r17 | 158 | ac%=220~260、charged=16~16、ac-miss=300~300、charged=80~16、str=16~16、vit=16~16、balance2=40~40 |
| Prudence | 49 | 2 | r23 r03 | 62 | ac%=140~170、red-mag=10~10、red-dmg=3~3、res-all=25~35、balance2=25~25、rep-dur=~、light=1~1 |
| Rain | 49 | 3 | r09 r23 r06 | 85 | hit-skill=5~15、gethit-skill=5~15、dru=2~2、mana=100~150 |
| Venom | 49 | 3 | r07 r14 r23 | 97 | dmg-pois=312~312、ignore-ac=1~1、charged=27~15、charged=11~13、manasteal=7~7 |
| Sanctuary | 49 | 3 | r18 r18 r23 | 127 | block=20~20、block2=20~20、ac%=130~160、ac-miss=250~250、res-all=50~70、balance2=20~20、charged=60~12 |
| Oath | 49 | 4 | r13 r21 r23 r17 | 160 | dmg%=210~340、swing1=30~30、hit-skill=30~20、charged=14~17、charged=20~16、abs-mag=10~15、indestruct=1~1 |
| Delirium | 51 | 3 | r20 r24 r16 | 129 | hit-skill=11~18、charged=60~17、gethit-skill=14~13、ac=261~261、gethit-skill=6~14、gethit-skill=1~50、allskills=2~2 |
| Principle | 53 | 3 | r08 r25 r02 | 83 | hit-skill=100~5、pal=2~2、hp=100~150、dmg-undead=50~50 |
| Rift | 53 | 4 | r15 r18 r20 r25 | 135 | dmg-mag=160~250、dmg-fire=60~180、dmg-to-mana=38~38、hit-skill=20~16、att-skill=16~21、charged=40~15、all-stats=5~10 |
| Kingslayer | 53 | 4 | r23 r22 r25 r19 | 190 | swing2=30~30、dmg%=230~270、reduce-ac=25~25、crush=33~33、openwounds=25~25、oskill=1~1、gold%=40~40 |
| Death | 55 | 5 | r15 r01 r26 r09 r25 | 140 | dmg%=300~385、deadly/lvl=~、charged=15~22、att-skill=25~18、death-skill=100~44、crush=50~50、indestruct=1~1 |
| Silence | 55 | 6 | r14 r02 r15 r24 r03 r26 | 161 | manasteal=4~4、stupidity=33~33、dmg%=200~200、swing2=20~20、res-all=75~75、allskills=2~2、balance2=20~20 |
| Heart of the Oak | 55 | 4 | r18 r26 r21 r10 | 162 | cast2=40~40、charged=25~4、mana%=15~15、allskills=3~3、regen=20~20、res-all=30~40、charged=60~14 |
| Chaos | 57 | 3 | r19 r27 r22 | 145 | demon-heal=15~15、dmg%=240~290、dmg-mag=216~471、oskill=1~1、swing2=35~35、hit-skill=9~11、hit-skill=11~9 |
| Exile's Path | 57 | 4 | r26 r27 r24 r14 | 194 | block2=30~30、freeze=1~1、ac%=220~260、aura=13~16、skilltab=2~2、hit-skill=15~5、rep-dur=~ |
| Call to Arms | 57 | 5 | r11 r08 r23 r24 r27 | 201 | swing2=40~40、dmg%=200~240、allskills=1~1、oskill=2~6、oskill=1~6、oskill=1~4、regen=12~12 |
| Fortitude | 59 | 4 | r01 r12 r14 r28 | 128 | ac%=200~200、dmg%=300~300、cast3=25~25、gethit-skill=20~15、dmg-to-mana=12~12、hp/lvl=8~12、res-all=25~30 |
| Widowmaker | 59 | 5 | r05 r03 r28 r23 r08 | 155 | dmg-dem/lvl=~、dmg=340~400、swing3=30~40、hit-skill=35~15、pierce-pois=20~25、ignore-ac=1~1、heal-kill=10~15 |
| Wind | 61 | 2 | r29 r01 | 72 | dmg%=120~160、swing2=40~40、move2=20~20、reduce-ac=50~50、hit-skill=10~9、charged=127~13、balance2=15~15 |
| Dragon | 61 | 3 | r29 r28 r12 | 147 | ac=360~360、ac-miss=230~230、str/lvl=~、hit-skill=12~15、gethit-skill=20~18、aura=14~14、all-stats=3~5 |
| Bramble | 61 | 4 | r08 r27 r29 r05 | 152 | balance2=50~50、ac=300~300、aura=15~21、heal-kill=13~13、extra-pois=25~50、res-pois=100~100、charged=33~13 |
| Bound by Duty | 63 | 4 | r14 r22 r30 r24 | 192 | res-all=50~50、ac%=70~70、dmg-demon=200~200、dmg-undead=100~100、lifesteal=8~8、allskills=2~2、str=20~20 |
| Wrath | 63 | 4 | r21 r17 r30 r23 | 194 | dmg-demon=300~300、dmg-undead=250~300、dmg-ltng=41~240、dmg-mag=85~120、hit-skill=5~10、hit-skill=30~1、nofreeze=1~1 |
| The Beast | 63 | 5 | r30 r03 r22 r23 r17 | 209 | swing2=40~40、aura=9~9、dmg%=240~270、str=25~40、charged=5~13、oskill=3~3、oskill=3~3 |
| Infinity | 63 | 4 | r30 r23 r30 r24 | 226 | dmg%=255~325、move3=35~35、vit/lvl=~、aura=12~12、kill-skill=50~20、pierce-ltng=45~55、charged=30~21 |
| Eternity | 63 | 5 | r11 r30 r24 r12 r29 | 227 | dmg%=260~310、indestruct=1~1、slow=33~33、charged=88~8、regen=16~16、regen-mana=16~16、nofreeze=1~1 |
| Fury | 65 | 3 | r31 r25 r05 | 133 | dmg%=209~209、swing2=40~40、noheal=1~1、openwounds=66~66、lifesteal=6~6、deadly=33~33、skill=5~5 |
| Enigma | 65 | 3 | r31 r06 r30 | 143 | ac=750~775、heal-kill=14~14、move2=45~45、str/lvl=~、allskills=2~2、mag%/lvl=~、oskill=1~1 |
| Dream | 65 | 3 | r16 r31 r21 | 145 | ac=150~220、gethit-skill=10~15、mana/lvl=~、res-all=5~20、balance3=20~30、aura=15~15、mag%=12~25 |
| Faith | 65 | 4 | r27 r31 r20 r02 | 176 | dmg%=280~280、att%=300~300、dmg-fire=120~120、res-all=15~15、aura=12~15、reanimate=10~10、allskills=1~2 |
| Ice | 65 | 4 | r11 r13 r31 r28 | 178 | dmg%=140~210、aura=18~18、extra-cold=25~30、hit-skill=25~22、levelup-skill=100~40、pierce-cold=20~20、gold%/lvl=~ |
| Famine | 65 | 4 | r19 r27 r09 r31 | 184 | dmg%=270~320、lifesteal=12~12、swing2=30~30、noheal=1~1、dmg-mag=180~200、dmg-elem=50~200、ethereal=1~1 |
| Brand | 65 | 4 | r31 r28 r23 r25 | 226 | dmg%=260~340、dmg-demon=280~330、hit-skill=100~18、gethit-skill=35~14、knock=1~1、noheal=1~1、explosivearrow=15~15 |
| Phoenix | 65 | 4 | r26 r26 r28 r31 | 234 | dmg%=350~400、ac-miss=350~400、hit-skill=40~22、levelup-skill=100~40、pierce-fire=28~28、aura=10~15、abs-fire=15~21 |
| Destruction | 65 | 5 | r26 r28 r30 r31 r18 | 281 | dmg%=350~350、dmg-mag=100~180、hit-skill=5~23、death-skill=100~45、att-skill=15~22、hit-skill=23~12、noheal=1~1 |
| Last Wish | 65 | 6 | r31 r23 r31 r29 r31 r30 | 368 | dmg%=330~375、att-skill=20~20、hit-skill=10~18、gethit-skill=6~11、crush=40~50、mag%/lvl=~、aura=17~17 |
| Plague | 67 | 3 | r32 r19 r22 | 155 | dmg-demon=260~380、gethit-skill=20~12、hit-skill=25~15、pierce-pois=23~23、deadly/lvl=~、aura=13~17、allskills=1~2 |
| Hand of Justice | 67 | 4 | r29 r32 r11 r28 | 212 | swing2=33~33、dmg%=280~330、aura=16~16、levelup-skill=100~36、death-skill=100~48、ignore-ac=1~1、pierce-fire=20~20 |
| Pride | 67 | 4 | r32 r29 r16 r28 | 222 | dmg-dem/lvl=~、dmg-ltng=50~280、att%=260~300、aura=16~20、gethit-skill=25~17、regen=8~8、gold%/lvl=~ |
| Doomsayer | 67 | 5 | r15 r27 r22 r28 r32 | 230 | dmg%=280~320、aura=12~12、swing2=45~45、noheal=1~1、pierce-cold=40~60、allskills=2~2、hit-skill=5~18 |
| Breath of the Dying | 69 | 6 | r26 r15 r01 r02 r33 r05 | 161 | swing2=60~60、dmg-undead=125~125、lifesteal=12~15、noheal=1~1、kill-skill=50~20、dmg%=350~400、all-stats=30~30 |

## 对假设的判定：**不成立**

做这份对比前，我的假设是「中阶暗金/套装被低阶符文之语整体比下去了」。
数据不支持这个假设：

- **被完全替代的：0 件**
- 按需求档位比「强属性条数」：**多数档位是暗金领先**（1~19 领先 5 项、
  30~39 领先 3 项、60~69 领先 2 项），RW 只在 20~29 和 50~59 两档小幅领先（+1 / +2）
- 也就是说**没有哪个档位被 RW 压平**

RW 真正的问题不是「替代」，而是**个别件的性价比过于突出**
（`Spirit` 在需求 25 就给 `+2 技能 / 35% 施法 / 55% 快打 / +112 法力`），
这会让「做它」成为默认答案，但不构成「某件暗金没有任何理由存在」。

## 结论怎么读

- 「被替代」= 存在一个**同槽位、需求不更高、每项都不差**的 RW。
  这是「这件东西没有任何存在理由」的最强证据 —— 比「我觉得没人用」硬。
- 反过来说，**没被替代不等于好用**：本工具只测数值覆盖，不测组合与手感。
- 想让某件暗金重新有理由，方向是**给它一个 RW 给不了的东西**（触发技能、独有组合、特定构筑的钥匙件），而不是加数字。
