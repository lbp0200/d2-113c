# P3 · 装备体检表（暗金）

> 由 `python3 -m tools.p3_items` 生成，**只读**。
>
> 判据（装备层的 E1~E3，对应技能层的 T1~T3）：
>
> - **E1 每件一个身份**：能说出「什么构筑 / 什么阶段 / 为了哪一项属性」穿它 —— 说不出来就是垃圾
> - **E2 不许造新 BiS**：改动不能让某件同时成为多个槽位的最优
> - **E3 加法或等价交换**：和 T3 一样，不许只拿走不给

**本表不判死**：「谁会穿」那一列是空的，必须由人填。这里只负责把候选挑出来。

已知边界：触发技能（`hit-skill`/`gethit-skill`/`charged`）、光环、武器速度档位都没有计入「有效伤害」，所以 A 类候选里**一定有误判**。

## 汇总

- 可用暗金：**380** 件（另有 5 件任务物品已剔除：Staff of Kings、Horadric Staff、Hell Forge Hammer、KhalimFlail、SuperKhalimFlail）
- A 类「被完全覆盖」候选：**0** 件（纯数值可比，未计入触发技能/光环）
- 因含未量化属性（触发技能/光环/充能）而**放弃比较**：244 件 —— 它们的身份可能就在那些属性里
- B 类「低贡献」候选：**4** 件
- 有身份待填：**380** 行（全表见下）

## A 类候选：被同槽位、需求不更高的装备全面覆盖

无。

> 复核方法：从 `uniqueitems.txt` 查两件的 `prop*` 逐条比。
> 特别检查它有没有**触发技能/光环/CB/攻速**这类没被计入的东西 —— 有的话这个候选就是误判。

## B 类候选：没有任何一项够看的属性（且不含触发技能/光环）

| 装备 | 需求 | 槽位 | 它到底给了什么（全部达不到强属性线） |
|---|---:|---|---|
| War Bonnet | 3 | helm | ar=30、def=14、ed=30、hp=15、mana=15 |
| Lenyms Cord | 7 | belt | item_lightradius=1、mana=15、manarecoverybonus=30、res-cold=5、res-fire=5、res-ltng=5 |
| Coif of Glory | 14 | helm | def=100、item_attackertakeslightdamage=7、item_stupidity=1、res-ltng=15 |
| The Centurion | 14 | tors | ar=50、def=30、dr=2、hp=15、hpregen=5、item_staminadrainpct=25、mana=15、maxstamina=15 |

## 参考：在**本槽位同需求段**内没有任何一项最强的（不要直接当结论）

共 15 件。**这一类的参考价值有限**：D2 装备的价值常常来自**属性的组合**（例如 `Lightsabre` 单看每一项都不最强，但"攻速+闪电伤害+吸蓝"合在一起就是它的理由）。所以这里只当线索，不当判定。

| 装备 | 需求 | 槽位 | 它够强的属性（但都不是最强） |
|---|---:|---|---|
| Wisp | 76 | ring | item_magicbonus=20 |
| Hellslayer | 66 | axe | ed=100、eff_dmg=186、elem_dmg=250 |
| The Rising Sun | 65 | amul | elem_dmg=48 |
| Lightsabre | 58 | swor | ed=200、eff_dmg=99、elem_dmg=200、ias=20、manasteal=7 |
| Hellmouth | 47 | glov | elem_dmg=72 |
| Blackleach Blade | 42 | pole | ed=140、eff_dmg=80、lifesteal=8 |
| Chromatic Ire | 35 | staf | fcr=20、res-cold=40、res-fire=40、res-ltng=40、skill=1 |
| Mosers Blessed Circle | 31 | shie | block=25、res-cold=25、res-fire=25、res-ltng=25 |
| Infernostride | 29 | boot | frw=20、maxfireresist=10、res-fire=30 |
| The Salamander | 21 | staf | res-fire=30、skill=3 |
| Steelclash | 17 | shie | block=25 |
| Coif of Glory | 14 | helm | — |
| The Centurion | 14 | tors | — |
| Lenyms Cord | 7 | belt | — |
| War Bonnet | 3 | helm | — |

## ⚠️ 关于「死属性」：这一类**做错过，已经删掉**

第一版把「`+X% 伤害` / 附加元素伤害 写在护甲上」当成死属性，列了 43 件。**那是错的**：

- 反例一：**Fortitude** 在**衣服**上给 `+300% 强化伤害`，是全身最重要的物理增伤之一
- 反例二：**Steelrend**（手套）的招牌就是 `+30~60% 强化伤害`
- 反例三：带 ED 的珠宝可以镶在头盔/衣服里并照常生效

这些 stat（`item_maxdamage_percent`、元素附加伤害）都是**全局**的，
写在哪个槽位都生效 —— 只有「武器上的 `ac%`」这一类还存疑（武器本身没有防御值）。

所以本工具**不再输出「死属性」结论**。要判断一件装备的某条属性是不是白给，
唯一可靠的办法是进游戏实测（这正是 `TODO.md` 里那一串待验证项的意义）。

## 全表（按槽位）

「谁会穿」一列留空 —— E1 必须人工填，填不出来的才是要改的。

### tors（37 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Greyform | 7 | 10 防 | red-mag=3~3、res-cold=20~20、res-fire=20~20、dex=10~10 | — |  |
| Blinkbats Form | 12 | 16 防 | ac-miss=50~50、move2=10~10、ac=25~25、fire-min=3~3 | — |  |
| The Centurion | 14 | 22 防 | ac=30~30、att=50~50、red-dmg=2~2、hp=15~15 | — |  |
| Darkglow | 14 | 93 防 | att=20~20、res-all-max=5~5、light=3~3、ac-hth=50~50 | — |  |
| Hawkmail | 15 | 117 防 | ac%=80~100、res-cold-max=15~15、res-cold=15~15、nofreeze=1~1 | — |  |
| Twitchthroe | 16 | 34 防 | swing2=20~20、dex=10~10、block=25~25、ac=25~25 | — |  |
| Sparking Mail | 17 | 136 防 | ac%=75~85、dmg-ltng=1~20、light-thorns=10~14、res-ltng=30~30 | — |  |
| Venomsward | 20 | 133 防 | res-pois-max=15~15、res-pois-len=50~50、res-pois=90~90、light=2~2 | — |  |
| Iceblink | 22 | 166 防 | freeze=1~1、res-cold=30~30、light=4~4、red-mag=1~1 | — |  |
| Boneflesh | 26 | 246 防 | lifesteal=5~5、ac%=100~120、att=35~35、openwounds=25~25 | — |  |
| Rockfleece | 28 | 237 防 | ease=-10~-10、ac%=100~130、red-dmg%=10~10、red-dmg=5~5 | — |  |
| Goldskin | 28 | 389 防 | ac%=120~150、res-all=35~35、thorns=10~10、light=2~2 | — |  |
| Victors Silk | 28 | 496 防 | manasteal=5~5、allskills=1~1、light=2~2、ac%=100~120 | — |  |
| The Spirit Shroud | 28 | 274 防 | nofreeze=1~1、allskills=1~1、red-mag=7~11、regen=10~10 | — |  |
| Rattlecage | 29 | 132 防 | howl=52~52、att=45~45、crush=25~25、ac=200~200 | — |  |
| Heavenly Garb | 29 | 197 防 | ac%=100~100、res-all=10~10、regen-mana=25~25、enr=15~15 | — |  |
| Skin of the Vipermagi | 29 | 261 防 | ac%=120~120、res-all=20~35、cast3=30~30、red-mag=9~13 | — |  |
| Skin of the Flayerd One | 31 | 374 防 | rep-dur=~、regen=15~25、dur=30~30、lifesteal=5~7 | — |  |
| Ironpelt | 33 | 291 防 | dur=125~125、hp=25~25、red-mag=10~16、red-dmg=15~20 | — |  |
| Spiritforge | 35 | 429 防 | light=4~4、hp/lvl=~、dmg-fire=20~65、res-fire=5~5 | — |  |
| Crow Caw | 37 | 512 防 | openwounds=35~35、ac%=150~180、dex=15~15、balance2=15~15 | — |  |
| Shaftstop | 38 | 658 防 | ac-miss=250~250、red-dmg%=30~30、hp=60~60、ac%=180~220 | — |  |
| Duriel's Shell | 41 | 585 防 | str=15~15、ac/lvl=~、hp/lvl=~、ac%=160~200 | — |  |
| Skullder's Ire | 42 | 702 防 | allskills=1~1、mag%/lvl=~、ac%=160~200、dur=60~60 | — |  |
| Guardian Angel | 45 | 789 防 | light=4~4、pal=1~1、ac%=180~200、block2=30~30 | pal |  |
| Toothrow | 48 | 800 防 | thorns=20~40、ac=40~60、str=10~10、openwounds=40~40 | — |  |
| Atma's Wail | 51 | 760 防 | dex=15~15、regen=10~10、mana%=15~15、balance2=30~30 | — |  |
| Que-Hegan's Wisdon | 51 | 632 防 | cast2=20~20、mana-kill=3~3、red-mag=6~10、enr=15~15 | — |  |
| Black Hades | 53 | 986 防 | light=-2~-2、att-demon=200~250、half-freeze=1~1、sock=~ | — |  |
| Corpsemourn | 55 | 1214 防 | str=8~8、vit=10~10、res-cold=35~35、gethit-skill=6~2 | gethit-skill、charged |  |
| Leviathan | 65 | 1410 防 | ac%=170~200、ac=100~150、red-dmg%=15~25、str=40~50 | — |  |
| Steel Carapice | 66 | 1605 防 | ac%=190~220、balance2=20~20、red-dmg=9~14、res-cold=40~60 | gethit-skill |  |
| Templar's Might | 74 | 1739 防 | ac%=170~220、balance2=20~20、ac-miss=250~300、stam=40~50 | — |  |
| Ormus' Robes | 75 | 414 防 | ac=10~20、cast2=20~20、extra-fire=10~15、extra-cold=10~15 | skill-rand |  |
| Tyrael's Might | 84 | 1359 防 | ease=-100~-100、indestruct=1~1、ac%=120~150、rip=1~1 | — |  |
| The Gladiator's Bane | 85 | 1284 防 | ac%=150~200、red-mag=15~20、red-dmg=15~20、thorns=20~20 | — |  |
| Arkaine's Valor | 85 | 1298 防 | ac%=150~180、balance2=30~30、allskills=1~2、red-dmg=10~15 | — |  |

### swor（35 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Rixots Keen | 2 | 9 伤 | dmg-min=5~5、att%=20~20、light=2~2、crush=25~25 | — |  |
| Blood Crescent | 7 | 7 伤 | res-all=15~15、dmg%=60~80、hp=15~15、light=4~4 | — |  |
| Krintizs Skewer | 10 | 8 伤 | ignore-ac=1~1、str=10~10、dex=10~10、manasteal=7~7 | — |  |
| Shadowfang | 12 | 25 伤 | manasteal=9~9、res-cold=20~20、light=-2~-2、dmg-cold=10~30 | — |  |
| Gleamscythe | 13 | 26 伤 | light=3~3、mana=30~30、ac=20~20、swing2=20~20 | — |  |
| Griswolds Edge | 17 | 23 伤 | fire-min=10~12、fire-max=15~25、att=100~100、swing1=10~10 | — |  |
| Soulflay | 19 | 43 伤 | manasteal=4~10、lifesteal=4~4、dmg%=70~100、res-all=5~5 | — |  |
| Hellplague | 22 | 20 伤 | manasteal=5~5、lifesteal=5~5、pois-min=48~48、pois-max=96~96 | fireskill |  |
| Kinemils Awl | 23 | 37 伤 | att=100~150、mana=20~20、fire-min=6~6、fire-max=20~40 | — |  |
| Blacktongue | 26 | 38 伤 | dmg-pois=192~192、noheal=1~1、att=50~50、res-pois=50~50 | — |  |
| Ripsaw | 26 | 39 伤 | openwounds=80~80、dmg-max=15~15、manasteal=6~6、dmg%=80~100 | — |  |
| Culwens Point | 29 | 25 伤 | allskills=1~1、res-pois-len=50~50、balance2=20~20、swing2=20~20 | — |  |
| The Patriarch | 29 | 74 伤 | red-dmg=3~3、red-mag=3~3、stupidity=1~1、gold%=100~100 | — |  |
| Bloodletter | 30 | 36 伤 | dmg-norm=12~45、att=90~90、lifesteal=8~8、stamdrain=10~10 | — |  |
| Coldsteel Eye | 31 | 51 伤 | stupidity=1~1、slow=30~30、deadly=50~50、dur=50~50 | — |  |
| Hexfire | 33 | 44 伤 | charged=36~6、ignore-ac=1~1、res-fire=25~25、res-fire-max=10~10 | charged、fireskill |  |
| Blade of Ali Baba | 35 | 56 伤 | sock=~、gold%/lvl=~、mag%/lvl=~、mana=15~15 | — |  |
| Ginther's Rift | 37 | 60 伤 | red-mag=7~12、swing2=30~30、rep-dur=~、dur=40~40 | — |  |
| Headstriker | 39 | 62 伤 | noheal=1~1、str=15~15、deadly/lvl=~、dmg/lvl=~ | — |  |
| Plague Bearer | 41 | 65 伤 | hit-skill=5~4、dmg-pois=384~384、dmg-norm=10~45、dmg%=150~150 | hit-skill |  |
| The Atlantian | 42 | 107 伤 | dur=100~100、ac=75~75、str=16~16、dex=12~12 | pal |  |
| Crainte Vomir | 42 | 87 伤 | slow=35~35、dmg-ac=-70~-70、move2=20~20、red-dmg%=10~10 | — |  |
| Bing Sz Wang | 43 | 113 伤 | ease=-30~-30、dmg-cold=50~140、str=20~20、freeze=2~2 | hit-skill |  |
| The Vile Husk | 44 | 116 伤 | hit-skill=6~1、dmg-und/lvl=~、res-pois=50~50、dmg-pois=426~426 | hit-skill |  |
| Cloudcrack | 45 | 148 伤 | hit-skill=6~7、dmg-ltng=1~240、ac=30~30、light=2~2 | hit-skill |  |
| Todesfaelle Flamme | 46 | 108 伤 | dmg-fire=50~200、res-fire=40~40、abs-fire=10~10、att-skill=10~6 | att-skill、charged、charged |  |
| Swordguard | 48 | 178 伤 | ease=-50~-50、ac/lvl=~、res-all=10~20、ac-miss=100~100 | — |  |
| Lightsabre | 58 | 99 伤 | light=7~7、att-skill=5~0、ignore-ac=1~1、abs-ltng%=25~25 | att-skill |  |
| Bloodmoon | 61 | 140 伤 | dmg%=210~260、lifesteal=10~15、charged=9~15、heal-kill=7~13 | charged |  |
| Djinnslayer | 65 | 122 伤 | dmg%=190~240、dmg-fire=250~500、dmg-demon=100~150、att-demon=200~300 | — |  |
| Doombringer | 69 | 270 伤 | hp%=20~20、dmg%=180~250、att%=40~40、indestruct=1~1 | hit-skill |  |
| Frostwind | 70 | 135 伤 | dmg%=180~230、freeze=4~4、half-freeze=1~1、dmg-cold=237~486 | — |  |
| Flamebellow | 71 | 294 伤 | dmg%=170~240、dmg-fire=233~482、fireskill=3~3、abs-fire%=20~30 | fireskill、hit-skill |  |
| The Grandfather | 81 | 303 伤 | str=20~20、dex=20~20、vit=20~20、enr=20~20 | — |  |
| Azurewrath | 85 | 122 伤 | dmg-mag=250~500、dmg%=230~270、aura=10~13、dmg-cold=250~500 | — |  |

### axe（28 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| The Gnasher | 5 | 8 伤 | str=8~8、openwounds=50~50、crush=20~20、dmg%=60~70 | — |  |
| Fechmars Axe | 8 | 18 伤 | dmg%=70~90、freeze=3~3、res-cold=50~50、light=2~2 | — |  |
| Deathspade | 9 | 13 伤 | stupidity=1~1、dmg-min=8~8、att%=15~15、mana-kill=4~4 | — |  |
| Goreshovel | 14 | 21 伤 | swing3=30~30、str=25~25、openwounds=60~60、dmg%=40~50 | — |  |
| Bladebone | 15 | 14 伤 | dmg-undead=100~100、att-undead=40~40、swing2=20~20、ac=20~20 | — |  |
| The Chieftan | 19 | 44 伤 | dmg%=100~100、res-all=10~20、mana-kill=6~6、swing2=20~20 | — |  |
| Mindrend | 21 | 18 伤 | stupidity=2~2、regen-mana=20~20、ltng-min=1~1、ltng-max=12~15 | — |  |
| Brainhew | 25 | 35 伤 | dmg-min=14~14、mana=25~25、light=4~4、manasteal=10~13 | — |  |
| Rakescar | 27 | 35 伤 | pois-min=128~128、pois-max=128~128、pois-len=75~75、att=50~50 | — |  |
| The Humongous | 29 | 74 伤 | str=20~30、dmg-min=8~8、dmg-max=15~25、crush=33~33 | — |  |
| Warlord's Trust | 35 | 66 伤 | ac=75~75、regen=20~20、vit/lvl=~、res-all=10~10 | — |  |
| Coldkill | 36 | 45 伤 | dmg-cold=40~40、res-cold=15~15、res-cold-max=15~15、swing3=30~30 | hit-skill、gethit-skill |  |
| Butcher's Pupil | 39 | 64 伤 | deadly=35~35、openwounds=25~25、dmg%=150~200、indestruct=1~1 | — |  |
| Spellsteel | 39 | 93 伤 | ease=-60~-60、mana=100~100、red-mag=12~15、cast1=10~10 | charged、charged、charged |  |
| Stormrider | 41 | 101 伤 | hit-skill=5~10、hit-skill=10~0、dmg-ltng=1~200、dmg-norm=35~75 | hit-skill、hit-skill、gethit-skill |  |
| Boneslayer Blade | 42 | 141 伤 | att-und/lvl=~、dmg-und/lvl=~、str=8~8、swing2=20~20 | charged、gethit-skill |  |
| Islestrike | 43 | 74 伤 | dru=2~2、str=10~10、dex=10~10、vit=10~10 | dru |  |
| Pompe's Wrath | 45 | 65 伤 | hit-skill=4~8、slow=50~50、dmg-fire=35~150、knock=1~1 | hit-skill |  |
| The Minataur | 45 | 192 伤 | stupidity=2~2、half-freeze=1~1、str=15~20、slow=50~50 | — |  |
| Guardian Naga | 48 | 85 伤 | hit-skill=5~8、thorns=15~15、res-pois=30~30、dmg%=150~180 | hit-skill |  |
| Cranebeak | 63 | 156 伤 | dmg%=240~300、dmg-ltng=1~305、swing2=40~40、reduce-ac=25~25 | charged |  |
| Hellslayer | 66 | 186 伤 | str/lvl=~、vit/lvl=~、dmg%/lvl=~、dmg-fire=150~250 | att-skill |  |
| Razoredge | 67 | 148 伤 | dmg%=175~225、swing2=40~40、reduce-ac=33~33、deadly=50~50 | — |  |
| Messerschmidt's Reaver | 70 | 230 伤 | dmg%/lvl=~、dmg%=200~200、str=15~15、dex=15~15 | — |  |
| Deathcleaver | 70 | 180 伤 | dmg%=230~280、deadly=66~66、reduce-ac=33~33、swing2=40~40 | — |  |
| Runemaster | 72 | 183 伤 | dmg%=220~270、sock=3~5、res-cold-max=5~5、nofreeze=1~1 | — |  |
| Ethereal Edge | 74 | 241 伤 | dmg%=150~180、swing2=25~25、abs-fire=10~12、dmg-demon=150~200 | ethereal |  |
| Executioner's Justice | 75 | 359 伤 | dmg%=240~290、crush=25~25、reduce-ac=33~33、kill-skill=50~6 | kill-skill |  |

### helm（23 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| War Bonnet | 3 | 4 防 | hp=15~15、att=30~30、dmg%=30~30、mana=15~15 | — |  |
| Coif of Glory | 14 | 16 防 | light-thorns=7~7、stupidity=1~1、res-ltng=15~15、ac-miss=100~100 | — |  |
| Tarnhelm | 15 | 10 防 | gold%=75~75、mag%=25~50、allskills=1~1 | — |  |
| Duskdeep | 17 | 37 防 | light=-2~-2、res-all=15~15、red-dmg=7~7、dmg-max=8~8 | — |  |
| The Face of Horror | 20 | 18 防 | howl=64~64、str=20~20、res-all=10~10、dmg-undead=50~50 | — |  |
| Wormskull | 21 | 34 防 | nec=1~1、lifesteal=5~5、mana=10~10、res-pois=25~25 | nec |  |
| Howltusk | 25 | 58 防 | red-mag=2~2、thorns=3~3、ac%=80~80、dmg-to-mana=35~35 | — |  |
| Peasent Crown | 28 | 98 防 | enr=20~20、vit=20~20、allskills=1~1、move2=15~15 | — |  |
| Undead Crown | 29 | 56 防 | lifesteal=5~5、ac=40~40、res-pois=50~50、half-freeze=1~1 | — |  |
| Rockstopper | 31 | 182 防 | res-ltng=20~40、red-dmg%=10~10、balance2=30~30、ac%=160~220 | — |  |
| Stealskull | 35 | 230 防 | manasteal=5~5、lifesteal=5~5、balance2=10~10、swing2=10~10 | — |  |
| Darksight Helm | 38 | 80 防 | light=-4~-4、ac/lvl=~、nofreeze=1~1、manasteal=5~5 | gethit-skill、charged |  |
| Blackhorn's Face | 41 | 224 防 | light-thorns=25~25、slow=20~20、noheal=1~1、abs-ltng=20~20 | — |  |
| Vampiregaze | 41 | 185 防 | manasteal=6~8、lifesteal=6~8、stamdrain=15~15、red-dmg%=15~20 | — |  |
| Valkiry Wing | 44 | 274 防 | ac%=150~200、move2=20~20、balance2=20~20、ama=1~2 | ama |  |
| Crown of Thieves | 49 | 286 防 | dex=25~25、lifesteal=9~12、hp=50~50、mana=35~35 | — |  |
| Harlequin Crest | 62 | 120 防 | allskills=2~2、hp/lvl=~、mana/lvl=~、mag%=50~50 | — |  |
| Steelshade | 62 | 292 防 | ac%=100~130、abs-fire=5~11、manasteal=4~8、regen=10~18 | — |  |
| Giantskull | 65 | 128 防 | ac=250~320、str=25~35、crush=10~10、sock=1~2 | — |  |
| Nightwing's Veil | 67 | 300 防 | ac%=90~120、allskills=2~2、dex=10~20、abs-cold=5~9 | — |  |
| Veil of Steel | 73 | 218 防 | res-all=50~50、ac%=60~60、str=15~15、vit=15~15 | — |  |
| Crown of Ages | 82 | 207 防 | balance2=30~30、res-all=20~30、allskills=1~1、ac=100~150 | — |  |
| Andariel's Visage | 83 | 319 防 | ac%=100~150、res-pois=70~70、allskills=2~2、res-pois-max=10~10 | gethit-skill、charged |  |

### shie（22 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Pelta Lunata | 2 | 7 防 | ac=30~30、vit=10~10、str=2~2、enr=10~10 | — |  |
| Umbral Disk | 9 | 14 防 | stupidity=1~1、dex=10~10、ac=30~30、hp=20~20 | — |  |
| Stormguild | 13 | 21 防 | red-mag=1~1、res-ltng=25~25、ac=30~30、dmg-ltng=1~6 | — |  |
| Swordback Hold | 15 | 32 防 | thorns=5~5、block=20~20、openwounds=50~50、bloody=3~5 | — |  |
| Steelclash | 17 | 34 防 | block=25~25、pal=1~1、red-dmg=3~3、light=3~3 | pal |  |
| Bverrit Keep | 19 | 52 防 | ac=30~30、res-fire=75~75、str=5~5、red-mag=5~5 | — |  |
| Wall of the Eyeless | 20 | 28 防 | mana-kill=5~5、manasteal=3~3、cast2=20~20、res-pois=20~20 | — |  |
| The Ward | 26 | 65 防 | ac=40~40、red-mag=2~2、str=10~10、block=10~10 | — |  |
| Visceratuant | 28 | 112 防 | sor=1~1、block2=30~30、block=30~30、ac%=100~150 | sor |  |
| Mosers Blessed Circle | 31 | 163 防 | res-all=25~25、block=25~25、sock=~、ac%=180~220 | — |  |
| Stormchaser | 35 | 182 防 | dmg-ltng=1~60、block=20~20、half-freeze=1~1、res-ltng=50~50 | gethit-skill、gethit-skill |  |
| Lance Guard | 35 | 150 防 | hp=50~50、balance2=30~30、dmg-to-mana=15~15、thorns=47~47 | — |  |
| Tiamat's Rebuke | 38 | 189 防 | dmg-cold=27~53、dmg-fire=35~95、dmg-ltng=1~120、res-all=25~35 | gethit-skill、gethit-skill、gethit-skill |  |
| Lidless Wall | 41 | 230 防 | light=1~1、allskills=1~1、cast2=20~20、mana-kill=3~5 | — |  |
| Kerke's Sanctuary | 44 | 248 防 | red-dmg=11~16、red-mag=14~18、regen=15~15、ac%=180~240 | — |  |
| Radimant's Sphere | 50 | 260 防 | dmg-pois=204~204、gethit-skill=5~5、res-pois=75~75、ac%=160~200 | gethit-skill、charged |  |
| Blackoak Shield | 61 | 346 防 | dex/lvl=~、ac%=160~200、abs-cold/lvl=~、gethit-skill=4~5 | gethit-skill |  |
| Spirit Ward | 68 | 452 防 | ac%=130~180、abs-cold=6~11、res-all=30~40、block=20~30 | gethit-skill |  |
| Spike Thorn | 70 | 388 防 | ac%=120~150、thorns/lvl=~、dur=250~250、balance2=30~30 | — |  |
| Stormshield | 73 | 140 防 | ac/lvl=~、red-dmg%=35~35、str=30~30、indestruct=1~1 | — |  |
| Headhunter's Glory | 75 | 166 防 | ac=320~420、ac-miss=300~350、res-pois=30~40、sock=1~3 | — |  |
| Medusa's Gaze | 76 | 428 防 | ac%=150~180、slow=20~20、gethit-skill=10~7、lifesteal=5~9 | gethit-skill、death-skill |  |

### bow（19 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Pluckeye | 7 | 5 伤 | att=28~28、dmg%=100~100、hp=10~10、light=2~2 | — |  |
| Witherstring | 13 | 6 伤 | swing3=30~30、dmg-min=1~1、dmg-max=3~3、att=50~50 | — |  |
| Rimeraven | 15 | 11 伤 | att%=50~50、dex=3~3、explosivearrow=3~3、str=3~3 | — |  |
| Piercerib | 20 | 10 伤 | res-all=10~10、deadly=30~30、att=60~60、dmg-undead=100~100 | — |  |
| Pullspite | 25 | 15 伤 | dmg-ltng=1~30、str=8~8、att=28~28、pierce=25~25 | — |  |
| Wizendraw | 26 | 19 伤 | magicarrow=5~5、mana=30~30、swing2=20~20、res-cold=26~26 | — |  |
| Hellclap | 27 | 19 伤 | swing1=10~10、fire-min=15~15、fire-max=30~50、att=50~75 | fireskill |  |
| Blastbark | 28 | 30 伤 | dmg%=70~130、str=5~5、ama=1~1、manasteal=3~3 | ama |  |
| Skystrike | 28 | 38 伤 | dmg-ltng=1~250、att=100~100、enr=10~10、swing3=30~30 | hit-skill、ama |  |
| Riphook | 31 | 48 伤 | openwounds=30~30、dmg%=180~220、slow=30~30、mana=35~35 | — |  |
| Kuko Shakaku | 33 | 55 伤 | skill=3~3、explosivearrow=7~7、dmg%=150~180、pierce=50~50 | — |  |
| Endlesshail | 36 | 59 伤 | res-cold=35~35、mana=40~40、ac-miss=50~50、skill=3~5 | — |  |
| Whichwild String | 39 | 58 伤 | hit-skill=2~5、res-all=40~40、deadly/lvl=~、dmg%=150~170 | hit-skill |  |
| Cliffkiller | 41 | 86 伤 | ama=2~2、dmg%=190~230、ac-miss=80~80、knock=1~1 | ama |  |
| Magewrath | 43 | 61 伤 | manasteal=15~15、red-mag=9~13、skill=3~3、att=200~250 | ama |  |
| Godstrike Arch | 46 | 105 伤 | dmg%=200~250、att%=100~150、dmg-undead=100~200、dmg-demon=100~200 | hit-skill |  |
| Widowmaker | 65 | 110 伤 | dmg%=150~200、deadly=33~33、ignore-ac=1~1、magicarrow=11~11 | — |  |
| Eaglehorn | 69 | 117 伤 | ignore-ac=1~1、att/lvl=~、dmg%/lvl=~、dmg%=200~200 | ama |  |
| Windforce | 73 | 136 伤 | dex=5~5、dmg/lvl=~、regen-stam=30~30、manasteal=6~8 | — |  |

### pole（16 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Dimoaks Hew | 8 | 28 伤 | dex=15~15、dmg%=100~100、swing2=20~20、ac=-8~-8 | — |  |
| Steelgoad | 14 | 24 伤 | howl=96~96、deadly=30~30、att=30~30、res-all=5~5 | — |  |
| Soul Harvest | 19 | 27 伤 | openwounds=30~30、att=45~45、res-all=20~20、dmg%=50~90 | — |  |
| The Battlebranch | 25 | 48 伤 | swing3=30~30、dex=10~10、dmg%=50~70、att=50~100 | — |  |
| Woestave | 28 | 40 伤 | slow=50~50、openwounds=50~50、stupidity=3~3、dmg-ac=-50~-50 | — |  |
| The Grim Reaper | 29 | 31 伤 | deadly=100~100、noheal=1~1、manasteal=5~5、dmg%=20~20 | — |  |
| The Meat Scraper | 41 | 96 伤 | dmg%=150~200、swing2=30~30、lifesteal=10~10、openwounds=50~50 | — |  |
| Blackleach Blade | 42 | 80 伤 | ease=-25~-25、hit-skill=5~5、light=-2~-2、lifesteal=8~8 | hit-skill |  |
| Athena's Wrath | 42 | 88 伤 | dru=1~3、dex=15~15、swing2=30~30、hp/lvl=~ | dru |  |
| Pierre Tombale Couant | 43 | 174 伤 | deadly=55~55、bar=3~3、balance2=30~30、manasteal=6~6 | bar |  |
| Husoldal Evo | 44 | 147 伤 | regen=20~20、att=200~250、noheal=1~1、dmg-norm=20~32 | — |  |
| Grim's Burning Dead | 45 | 140 伤 | dmg-fire=131~232、res-fire=45~45、dmg%=140~180、thorns=8~8 | nec |  |
| Bonehew | 64 | 363 伤 | dmg%=270~320、swing2=30~30、charged=30~14、hit-skill=50~16 | charged、hit-skill |  |
| Stormspire | 70 | 270 伤 | res-ltng=50~50、gethit-skill=5~5、dmg%=150~250、str=10~10 | gethit-skill、gethit-skill |  |
| The Reaper's Toll | 75 | 260 伤 | dmg%=190~240、hit-skill=33~1、ignore-ac=1~1、lifesteal=11~15 | hit-skill |  |
| Tomb Reaver | 84 | 348 伤 | swing2=60~60、light=4~4、dmg%=200~280、dmg-undead=150~230 | reanimate |  |

### amul（13 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Amulet of the Viper | 0 | — | mana=10~10、res-pois=25~25、hp=10~10 | — |  |
| Nokozan Relic | 10 | — | dmg-fire=3~6、res-fire-max=10~10、res-fire=50~50、light=3~3 | — |  |
| The Eye of Etlich | 15 | — | ac-miss=10~40、light=1~5、allskills=1~1、lifesteal=3~7 | — |  |
| The Mahim-Oak Curio | 25 | — | dex=10~10、str=10~10、enr=10~10、vit=10~10 | — |  |
| Saracen's Chance | 47 | — | res-all=15~25、gethit-skill=10~2、str=12~12、dex=12~12 | gethit-skill |  |
| The Cat's Eye | 50 | — | move2=30~30、swing2=20~20、ac=100~100、ac-miss=100~100 | — |  |
| Crescent Moon | 50 | — | manasteal=11~15、red-mag=10~10、dmg-to-mana=10~10、light=-2~-2 | — |  |
| Atma's Scarab | 60 | — | dmg-pois=102~102、res-pois=75~75、light=3~3、thorns=5~5 | hit-skill |  |
| The Rising Sun | 65 | — | abs-fire/lvl=~、light=4~4、gethit-skill=2~0、dmg-fire=24~48 | gethit-skill、fireskill |  |
| Highlord's Wrath | 65 | — | res-ltng=35~35、dmg-ltng=1~30、swing2=20~20、allskills=1~1 | — |  |
| Seraph's Hymn | 65 | — | allskills=2~2、skilltab=1~2、dmg-demon=25~50、dmg-undead=25~50 | — |  |
| Mara's Kaleidoscope | 67 | — | allskills=2~2、res-all=20~30、str=5~5、dex=5~5 | — |  |
| Metalgrid | 81 | — | ac=300~350、res-all=25~35、att=400~450、charged=11~22 | charged、charged |  |

### belt（13 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Lenyms Cord | 7 | 2 防 | mana=15~15、regen-mana=30~30、res-all=5~5、light=1~1 | — |  |
| Snakecord | 12 | 4 防 | dmg-pois=40~40、res-pois=25~25、ac=10~10、ac%=20~30 | — |  |
| Nightsmoke | 20 | 8 防 | res-all=10~10、dmg-to-mana=50~50、mana=20~20、red-dmg=2~2 | — |  |
| Goldwrap | 27 | 10 防 | mag%=30~30、light=2~2、ac=25~25、swing2=10~10 | — |  |
| Bladebuckle | 29 | 19 防 | thorns=8~8、ac=30~30、red-dmg=3~3、str=5~5 | — |  |
| String of Ears | 29 | 88 防 | red-mag=10~15、red-dmg%=10~15、lifesteal=6~8、ac%=150~180 | — |  |
| Razortail | 32 | 84 防 | thorns/lvl=~、dex=15~15、pierce=33~33、ac=15~15 | — |  |
| Gloomstrap | 36 | 94 防 | light=-3~-3、mana%=15~15、manasteal=5~5、ac%=120~150 | — |  |
| Snowclash | 42 | 107 防 | gethit-skill=5~0、abs-cold=15~15、res-cold-max=15~15、dmg-cold=13~21 | gethit-skill |  |
| Thudergod's Vigor | 47 | 140 防 | gethit-skill=5~7、dmg-ltng=1~50、res-ltng-max=10~10、abs-ltng=20~20 | gethit-skill |  |
| Nosferatu's Coil | 51 | 60 防 | str=15~15、mana-kill=2~2、slow=10~10、lifesteal=5~7 | — |  |
| Verdugo's Hearty Cord | 63 | 148 防 | ac%=90~140、vit=30~40、stam=100~120、balance2=10~10 | — |  |
| Arachnid Mesh | 80 | 129 防 | ac%=90~120、cast2=20~20、charged=11~3、allskills=1~1 | charged |  |

### boot（13 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Hotspur | 5 | 3 防 | res-fire-max=15~15、hp=15~15、dmg-fire=3~6、ac=6~6 | — |  |
| Gorefoot | 9 | 7 防 | bloody=3~5、move2=20~20、manasteal=2~2、thorns=2~2 | — |  |
| Treads of Cthon | 15 | 12 防 | move2=30~30、ac-miss=50~50、stamdrain=50~50、hp=10~10 | — |  |
| Goblin Toe | 22 | 16 防 | crush=25~25、red-dmg=1~1、red-mag=1~1、ac=15~15 | — |  |
| Tearhaunch | 29 | 24 防 | ac=35~35、str=5~5、dex=5~5、move2=20~20 | — |  |
| Infernostride | 29 | 79 防 | dmg-fire=12~33、move2=20~20、res-fire-max=10~10、res-fire=30~30 | gethit-skill |  |
| Waterwalk | 32 | 112 防 | ac-miss=100~100、move2=20~20、dex=15~15、ac%=180~210 | — |  |
| Silkweave | 36 | 117 防 | ac%=150~190、mana-kill=5~5、ac-miss=200~200、mana%=10~10 | — |  |
| Wartraveler | 42 | 125 防 | vit=10~10、str=10~10、mag%=30~50、dur=30~30 | — |  |
| Gorerider | 47 | 144 防 | ease=-25~-25、deadly=15~15、move2=30~30、crush=15~15 | — |  |
| Sandstorm Trek | 64 | 163 防 | ac%=140~170、move2=20~20、balance2=20~20、stam/lvl=~ | — |  |
| Marrowwalk | 66 | 189 防 | ac%=170~200、move2=20~20、charged=13~33、charged=10~12 | charged、charged |  |
| Shadowdancer | 71 | 133 防 | ac%=70~100、move2=30~30、balance2=30~30、dex=15~25 | — |  |

### glov（13 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| The Hand of Broc | 5 | 3 防 | manasteal=3~3、lifesteal=3~3、res-pois=10~10、mana=20~20 | — |  |
| Bloodfist | 9 | 7 防 | dmg-min=5~5、hp=40~40、balance2=30~30、ac=10~10 | — |  |
| Chance Guards | 15 | 11 防 | gold%=200~200、mag%=25~40、att=25~25、ac=15~15 | — |  |
| Magefist | 23 | 13 防 | cast3=20~20、regen-mana=25~25、fireskill=1~1、dmg-fire=1~6 | fireskill |  |
| Frostburn | 29 | 16 防 | ac=30~30、dmg%=5~5、mana%=40~40、dmg-cold=1~6 | — |  |
| Venom Grip | 29 | 82 防 | res-pois=30~30、res-pois-max=5~5、dmg-pois=153~153、crush=5~5 | — |  |
| Gravepalm | 32 | 101 防 | enr=10~10、str=10~10、dmg-undead=100~200、att-undead=100~200 | — |  |
| Ghoulhide | 36 | 117 防 | att-und/lvl=~、dmg-und/lvl=~、manasteal=4~5、hp=20~20 | — |  |
| Lavagout | 42 | 129 防 | res-fire=24~24、half-freeze=1~1、hit-skill=2~10、swing2=20~20 | hit-skill |  |
| Hellmouth | 47 | 144 防 | dmg-fire=15~72、abs-fire=15~15、ac%=150~200、dur=15~15 | hit-skill、hit-skill |  |
| Steelrend | 70 | 66 防 | ac=170~210、str=15~20、dmg%=30~60、crush=10~10 | — |  |
| Souldrain | 74 | 139 防 | ac%=90~120、manasteal=4~7、lifesteal=4~7、hit-skill=8~3 | hit-skill |  |
| Dracul's Grasp | 76 | 133 防 | ac%=90~120、lifesteal=7~10、openwounds=25~25、hit-skill=5~10 | hit-skill |  |

### spea（13 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| The Dragon Chang | 8 | 9 伤 | att=35~35、dmg-min=10~10、light=2~2、dmg-undead=100~100 | — |  |
| Razortine | 12 | 18 伤 | slow=25~25、reduce-ac=50~50、str=15~15、dex=8~8 | — |  |
| Bloodthief | 17 | 20 伤 | openwounds=35~35、str=10~10、lifesteal=8~12、hp=26~26 | — |  |
| Lance of Yaggai | 22 | 19 伤 | thorns=8~8、ltng-min=1~1、ltng-max=60~60、res-all=15~15 | — |  |
| The Tannr Gorerod | 27 | 77 伤 | fire-min=23~23、fire-max=54~54、res-fire-max=15~15、hp=30~30 | — |  |
| The Impaler | 31 | 63 伤 | ignore-ac=1~1、att=150~150、swing2=20~20、openwounds=40~40 | — |  |
| Kelpie Snare | 33 | 78 伤 | slow=75~75、res-fire=50~50、hp/lvl=~、dmg-norm=30~50 | — |  |
| Soulfeast Tine | 35 | 81 伤 | ease=-20~-20、lifesteal=7~7、manasteal=7~7、stamdrain=20~20 | — |  |
| Hone Sundan | 37 | 132 伤 | sock=~、dmg-norm=20~40、crush=45~45、rep-dur=~ | — |  |
| Spire of Honor | 39 | 212 伤 | att%=25~25、light=3~3、regen=20~20、balance2=20~20 | — |  |
| Steelpillar | 69 | 380 伤 | dmg%=210~260、swing2=25~25、reduce-ac=20~20、ac%=50~80 | — |  |
| Viperfork | 71 | 228 伤 | dmg%=190~240、dmg-pois=333~333、swing2=50~50、att=200~250 | hit-skill |  |
| Arioc's Needle | 81 | 254 伤 | dmg%=180~230、dmg-pois=403~403、deadly=50~50、ignore-ac=1~1 | — |  |

### staf（12 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Bane Ash | 5 | 5 伤 | fire-min=4~4、fire-max=6~6、res-fire=50~50、mana=30~30 | — |  |
| Serpent Lord | 9 | 7 伤 | dmg-pois=40~40、res-pois=50~50、light=-1~-1、mana=10~10 | — |  |
| Lazarus Spire | 18 | 8 伤 | res-ltng=75~75、red-dmg=5~5、enr=15~15、skill=1~1 | sor |  |
| The Salamander | 21 | 10 伤 | dmg-fire=15~32、res-fire=30~30、skill=1~1、skill=2~2 | fireskill |  |
| The Iron Jang Bong | 28 | 40 伤 | ac=30~30、cast3=20~20、dmg%=100~100、att%=50~50 | sor |  |
| Razorswitch | 28 | 14 伤 | cast3=30~30、thorns=15~15、mana=175~175、hp=80~80 | — |  |
| Ribcracker | 31 | 68 伤 | dmg-norm=30~65、dmg%=200~300、crush=50~50、dex=15~15 | — |  |
| Chromatic Ire | 35 | 22 伤 | sor=3~3、res-all=20~40、cast1=20~20、light-thorns=20~20 | sor |  |
| Warpspear | 39 | 24 伤 | sor=3~3、ignore-ac=1~1、skill=3~3、skill=3~3 | sor |  |
| Skullcollector | 41 | 41 伤 | mana%=20~20、mana-kill=20~20、allskills=2~2、mag%/lvl=~ | — |  |
| Ondal's Wisdom | 66 | 86 伤 | cast2=45~45、enr=40~50、allskills=2~4、ac=450~550 | — |  |
| Mang Song's Lesson | 82 | 91 伤 | allskills=5~5、pierce-fire=7~15、pierce-ltng=7~15、pierce-cold=7~15 | — |  |

### hamm（11 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Bonesob | 24 | 146 伤 | dmg%=200~300、crush=40~40、res-fire=30~30、res-cold=30~30 | — |  |
| Ironstone | 27 | 60 伤 | att=100~150、dmg%=100~150、ltng-min=1~1、ltng-max=10~10 | — |  |
| Steeldriver | 29 | 168 伤 | ease=-50~-50、swing3=40~40、regen-stam=25~25、dmg%=150~250 | — |  |
| Earthshaker | 43 | 130 伤 | hit-skill=5~7、knock=1~1、swing3=30~30、dmg%=180~180 | hit-skill |  |
| The Gavel of Pain | 45 | 208 伤 | hit-skill=5~1、gethit-skill=5~1、thorns=26~26、indestruct=1~1 | hit-skill、gethit-skill、charged |  |
| Bloodtree Stump | 48 | 210 伤 | crush=50~50、dmg%=180~220、res-all=20~20、str=25~25 | — |  |
| Stone Crusher | 68 | 233 伤 | dmg%=280~320、str=20~30、crush=40~40、reduce-ac=25~25 | — |  |
| Windhammer | 68 | 302 伤 | dmg%=180~230、crush=50~50、swing2=60~60、hit-skill=33~22 | hit-skill |  |
| Earthshifter | 69 | 426 伤 | dmg%=250~300、hit-skill=25~14、crush=33~33、swing2=10~10 | hit-skill、charged |  |
| Schaefer's Hammer | 79 | 128 伤 | hit-skill=20~10、hp=50~50、att/lvl=~、res-ltng=75~75 | hit-skill |  |
| The Cranium Basher | 87 | 362 伤 | swing2=20~20、indestruct=1~1、str=25~25、res-all=25~25 | hit-skill |  |

### knif（11 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Gull | 4 | 2 伤 | dmg-min=1~1、dmg-max=15~15、mag%=100~100、mana=-5~-5 | — |  |
| The Diggler | 11 | 9 伤 | dex=10~10、dmg%=50~50、swing3=30~30、res-cold=25~25 | — |  |
| The Jade Tan Do | 19 | 6 伤 | att=100~150、nofreeze=1~1、dmg-pois=460~460、res-pois=95~95 | — |  |
| Irices Shard | 25 | 10 伤 | cast3=50~50、mana=50~50、att=55~55、res-all=10~10 | — |  |
| Spineripper | 32 | 41 伤 | ignore-ac=1~1、lifesteal=8~8、noheal=1~1、swing3=15~15 | nec |  |
| Heart Carver | 36 | 61 伤 | deadly=35~35、ignore-ac=1~1、dmg-norm=15~35、dmg%=190~240 | — |  |
| Blackbog's Sharp | 38 | 23 伤 | slow=50~50、ac=50~50、dmg-norm=15~45、swing3=30~30 | — |  |
| Stormspike | 41 | 69 伤 | dmg-ltng=1~120、light-thorns=20~20、gethit-skill=25~3、dmg%=150~150 | gethit-skill |  |
| Wizardspike | 61 | 36 伤 | mana/lvl=~、regen-mana=15~15、mana%=15~15、res-all=75~75 | — |  |
| Ghostflame | 62 | 133 伤 | dmg%=190~240、ignore-ac=1~1、dmg-mag=108~108、manasteal=10~15 | ethereal |  |
| Fleshripper | 68 | 144 伤 | dmg%=200~300、reduce-ac=50~50、noheal=1~1、crush=25~25 | — |  |

### wand（10 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Iros Torch | 5 | 3 伤 | nec=1~1、lifesteal=6~6、dmg-fire=5~9、light=3~3 | nec |  |
| Maelstromwrath | 14 | 5 伤 | ltng-min=1~1、ltng-max=9~9、res-ltng=40~40、mana=13~13 | — |  |
| Gravenspine | 20 | 5 伤 | str=10~10、dex=10~10、cold-min=4~4、cold-max=8~8 | nec |  |
| Umes Lament | 28 | 8 伤 | nec=2~2、mana=40~40、cast2=20~20、howl=64~64 | nec |  |
| Suicide Branch | 33 | 13 伤 | thorns=25~25、cast2=50~50、res-all=10~10、mana%=10~10 | — |  |
| Carin Shard | 35 | 16 伤 | hp/lvl=~、cast2=10~10、mana/lvl=~、balance2=30~30 | nec |  |
| Arm of King Leoric | 36 | 16 伤 | skilltab=2~2、gethit-skill=5~10、mana/lvl=~、gethit-skill=10~2 | gethit-skill、gethit-skill |  |
| Blackhand Key | 41 | 21 伤 | skilltab=1~1、dmg-to-mana=20~20、hp=50~50、light=-2~-2 | nec、charged |  |
| Deaths's Web | 66 | 25 伤 | allskills=2~2、pierce-pois=40~50、heal-kill=7~12、mana-kill=7~12 | — |  |
| Boneshade | 79 | 20 伤 | nec=2~2、cast2=25~25、skill=4~5、skill=4~5 | nec |  |

### xbow（10 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Leadcrow | 9 | 13 伤 | dex=10~10、hp=10~10、dmg%=70~70、res-pois=30~30 | — |  |
| Ichorsting | 18 | 19 伤 | dmg-pois=102~102、dex=20~20、pierce=50~50、att=50~50 | — |  |
| Hellcast | 27 | 36 伤 | explosivearrow=5~5、res-fire-max=15~15、res-fire=15~15、att=70~70 | — |  |
| Doomspittle | 28 | 18 伤 | ama=1~1、pierce=35~35、swing3=30~30、hp=15~15 | ama |  |
| Langer Briser | 32 | 62 伤 | knock=1~1、dmg%=170~200、mag%=30~60、hp=30~30 | — |  |
| Pus Spiter | 36 | 99 伤 | dmg-pois=192~192、hit-skill=4~1、nec=2~2、ease=-60~-60 | hit-skill、nec、gethit-skill |  |
| Buriza-Do Kyanon | 41 | 132 伤 | pierce=100~100、dex=35~35、ac=75~150、dmg/lvl=~ | — |  |
| Demon Machine | 49 | 51 伤 | ac=321~321、mana=36~36、pierce=66~66、explosivearrow=6~6 | — |  |
| Gutsiphon | 71 | 106 伤 | dmg%=160~220、pierce=33~33、lifesteal=12~18、slow=25~25 | — |  |
| Hellrack | 76 | 203 伤 | dmg%=180~230、dmg-elem=63~324、swing2=20~20、att%=100~150 | charged |  |

### mace（9 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Crushflange | 9 | 10 伤 | str=15~15、knock=1~1、light=2~2、res-fire=50~50 | — |  |
| Bloodrise | 15 | 25 伤 | dmg%=120~120、att%=50~50、openwounds=25~25、light=2~2 | — |  |
| The Generals Tan Do Li Ga | 21 | 20 伤 | dmg-min=1~1、dmg-max=20~20、slow=50~50、ac=25~25 | — |  |
| Sureshrill Frost | 39 | 53 伤 | dmg-cold=63~112、nofreeze=1~1、dmg%=150~180、dmg-norm=5~10 | charged |  |
| Moonfall | 42 | 64 伤 | hit-skill=5~6、dmg-fire=55~115、red-mag=9~12、dmg%=120~150 | hit-skill、charged |  |
| Baezil's Vortex | 45 | 72 伤 | hit-skill=5~8、dmg-ltng=1~150、mana=100~100、res-ltng=25~25 | hit-skill、charged |  |
| Horizon's Tornado | 64 | 158 伤 | dmg%=230~280、swing2=50~50、slow=20~20、hit-skill=20~15 | hit-skill |  |
| Baranar's Star | 65 | 144 伤 | att%=200~200、dmg%=200~200、dex=15~15、str=15~15 | — |  |
| Stormlash | 82 | 166 伤 | dmg%=240~300、swing2=30~30、hit-skill=15~10、hit-skill=20~18 | hit-skill、hit-skill |  |

### ring（9 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Nagelring | 7 | — | red-mag=3~3、thorns=3~3、att=50~75、mag%=15~30 | — |  |
| Manald Heal | 15 | — | manasteal=4~7、regen=5~8、hp=20~20、regen-mana=20~20 | — |  |
| The Stone of Jordan | 29 | — | mana=20~20、mana%=25~25、ltng-min=1~1、allskills=1~1 | — |  |
| Dwarf Star | 45 | — | gold%=100~100、stam=40~40、regen-stam=15~15、hp=40~40 | — |  |
| Raven Frost | 45 | — | nofreeze=1~1、dmg-cold=15~45、abs-cold%=20~20、mana=40~40 | — |  |
| Bul Katho's Wedding Band | 58 | — | hp/lvl=~、allskills=1~1、lifesteal=3~5、stam=50~50 | — |  |
| Carrion Wind | 60 | — | ac-miss=100~160、lifesteal=6~9、res-pois=55~55、gethit-skill=10~10 | gethit-skill、charged、hit-skill |  |
| Nature's Peace | 69 | — | noheal=1~1、rip=1~1、red-dmg=7~11、res-pois=20~30 | charged |  |
| Wisp | 76 | — | abs-ltng%=10~20、hit-skill=10~16、mag%=10~20、charged=15~2 | hit-skill、charged、charged |  |

### scep（9 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Knell Striker | 5 | 15 伤 | crush=25~25、res-fire=20~20、res-pois=20~20、mana=15~15 | — |  |
| Rusthandle | 17 | 21 伤 | pal=1~1、dmg-norm=3~7、red-mag=1~1、lifesteal=8~8 | pal |  |
| Stormeye | 23 | 30 伤 | dmg-ltng=1~6、dmg-cold=3~5、regen=10~10、dmg%=80~120 | — |  |
| Zakarum's Hand | 37 | 59 伤 | manasteal=8~8、ignore-ac=1~1、regen-mana=10~10、regen-stam=15~15 | hit-skill |  |
| The Fetid Sprinkler | 38 | 72 伤 | pal=2~2、hit-skill=5~1、hit-skill=10~1、dmg-pois=409~409 | pal、hit-skill、hit-skill |  |
| Hand of Blessed Light | 42 | 70 伤 | pal=2~2、dmg%=130~160、att%=100~100、ac=50~50 | pal、hit-skill |  |
| Ironward | 60 | 156 伤 | dmg%=240~290、slow=25~25、att%=150~200、swing2=10~10 | — |  |
| Heaven's Light | 61 | 184 伤 | dmg%=250~300、swing2=20~20、reduce-ac=33~33、light=3~3 | pal |  |
| The Reedeemer | 72 | 184 伤 | dmg%=250~300、dmg-demon=200~250、pal=2~2、ease=-60~-60 | pal |  |

### jewl（8 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Rainbow Facet | 49 | — | dmg-ltng=1~74、pierce-ltng=3~5、extra-ltng=3~5、death-skill=100~47 | death-skill |  |
| Rainbow Facet | 49 | — | dmg-cold=24~38、pierce-cold=3~5、extra-cold=3~5、death-skill=100~37 | death-skill |  |
| Rainbow Facet | 49 | — | dmg-fire=17~45、pierce-fire=3~5、extra-fire=3~5、death-skill=100~31 | death-skill |  |
| Rainbow Facet | 49 | — | dmg-pois=187~187、pierce-pois=3~5、extra-pois=3~5、death-skill=100~51 | death-skill |  |
| Rainbow Facet | 49 | — | dmg-ltng=1~74、pierce-ltng=3~5、extra-ltng=3~5、levelup-skill=100~41 | levelup-skill |  |
| Rainbow Facet | 49 | — | dmg-cold=24~38、pierce-cold=3~5、extra-cold=3~5、levelup-skill=100~43 | levelup-skill |  |
| Rainbow Facet | 49 | — | dmg-fire=17~45、pierce-fire=3~5、extra-fire=3~5、levelup-skill=100~29 | levelup-skill |  |
| Rainbow Facet | 49 | — | dmg-pois=187~187、pierce-pois=3~5、extra-pois=3~5、levelup-skill=100~23 | levelup-skill |  |

### club（6 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Felloak | 3 | 6 伤 | res-ltng=60~60、res-fire=20~20、knock=1~1、fire-min=6~6 | — |  |
| Stoutnail | 5 | 13 伤 | thorns=3~10、dmg%=100~100、vit=7~7、red-mag=2~2 | — |  |
| Dark Clan Crusher | 34 | 40 伤 | dru=2~2、dmg-demon=200~200、att-demon=200~200、dmg%=195~195 | dru |  |
| Fleshrender | 38 | 57 伤 | openwounds=25~25、noheal=1~1、crush=20~20、deadly=20~20 | dru |  |
| Demonlimb | 63 | 148 伤 | dmg%=180~230、dmg-fire=222~333、lifesteal=7~13、charged=20~23 | charged |  |
| Nord's Tenderizer | 68 | 168 伤 | dmg%=270~330、freeze=2~4、swing2=25~25、charged=12~16 | charged |  |

### h2h2（4 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Cutthroat1 | 42 | 84 伤 | ass=2~2、skilltab=1~1、dmg%=150~200、balance2=30~30 | ass |  |
| Jadetalon | 66 | 134 伤 | dmg%=190~240、manasteal=10~15、res-all=40~50、balance2=30~30 | — |  |
| Firelizard's Talons | 67 | 139 伤 | dmg%=200~270、swing2=15~15、skilltab=1~3、dmg-fire=236~480 | — |  |
| Shadowkiller | 78 | 125 伤 | dmg%=170~220、reduce-ac=25~25、freeze=2~2、mana-kill=10~15 | hit-skill、ethereal |  |

### pelt（4 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Jalal's Mane | 42 | 256 防 | dru=2~2、skilltab=2~2、ac%=150~200、balance2=30~30 | dru |  |
| Cerebus | 63 | 295 防 | ac%=130~140、skilltab=2~4、lifesteal=7~10、att%=60~120 | — |  |
| Spiritkeeper | 67 | 376 防 | ac%=170~190、balance2=20~20、abs-ltng=9~14、res-fire=30~40 | dru |  |
| Ravenlore | 74 | 322 防 | ac%=120~150、res-all=15~25、skilltab=3~3、enr=20~30 | — |  |

### phlm（4 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Arreat's Face | 42 | 320 防 | bar=2~2、skilltab=2~2、ac%=150~200、balance2=30~30 | bar |  |
| Demonhorn's Edge | 61 | 347 防 | ac%=120~160、swing2=10~10、lifesteal=3~6、thorns=55~77 | — |  |
| Halaberd's Reign | 77 | 369 防 | ac%=140~170、skilltab=1~1、bar=2~2、balance2=20~20 | bar |  |
| Wolfhowl | 79 | 319 防 | ac%=120~150、skilltab=2~3、str=8~15、dex=8~15 | charged |  |

### ashd（3 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Herald of Zakarum | 42 | 468 防 | pal=2~2、skilltab=2~2、ac%=150~200、block2=30~30 | pal |  |
| Alma Negra | 77 | 468 防 | ac%=180~210、block2=30~30、pal=1~2、block=20~20 | pal |  |
| Dragonscale | 80 | 543 防 | ac%=170~200、abs-fire%=10~20、res-fire-max=5~5、str=15~25 | — |  |

### head（3 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Homunculus | 42 | 192 防 | nec=2~2、skilltab=2~2、ac%=150~200、block2=30~30 | nec |  |
| Darkforge Spawn | 64 | 351 防 | ac%=140~180、cast2=30~30、mana%=10~10、skilltab=1~3 | — |  |
| Boneflame | 72 | 308 防 | ac%=120~150、move2=20~20、gethit-skill=15~3、nec=2~3 | gethit-skill、nec |  |

### jave（3 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Demon's Arch | 68 | 149 伤 | dmg%=160~210、dmg-fire=232~323、lifesteal=6~12、rep-quant=~ | — |  |
| Gargoyle's Bite | 70 | 102 伤 | dmg%=180~230、rep-quant=~、dmg-pois=300~300、lifesteal=9~15 | charged |  |
| Wraithflight | 76 | 115 伤 | dmg%=150~190、rep-quant=~、lifesteal=9~13、mana-kill=15~15 | ethereal |  |

### orb（3 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| The Oculus | 42 | 30 伤 | sor=3~3、gethit-skill=25~1、res-all=20~20、cast2=30~30 | sor、gethit-skill |  |
| Eschuta's temper | 72 | 34 伤 | sor=1~3、cast2=40~40、extra-fire=10~20、extra-ltng=10~20 | sor |  |
| Fathom | 73 | 42 伤 | sor=3~3、extra-cold=15~30、cast2=20~20、res-fire=25~40 | sor |  |

### taxe（3 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| The Scalper | 57 | 50 伤 | rep-quant=~、dmg%=150~200、att%=25~25、swing2=20~20 | — |  |
| Lacerator | 68 | 104 伤 | dmg%=150~210、rep-quant=~、swing2=30~30、noheal=1~1 | hit-skill |  |
| Gimmershred | 70 | 127 伤 | dmg%=160~210、dmg-fire=218~483、dmg-cold=176~397、dmg-ltng=29~501 | — |  |

### abow（2 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Lycander's Aim | 42 | 90 伤 | ama=2~2、skilltab=2~2、dmg%=150~200、swing2=20~20 | ama |  |
| Bloodraven's Charge | 71 | 111 伤 | dmg%=180~230、att%=200~300、explosivearrow=13~13、skilltab=2~4 | charged |  |

### ajav（2 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Titan's Revenge | 42 | 80 伤 | ama=2~2、skilltab=2~2、dmg%=150~200、move2=30~30 | ama |  |
| Thunderstroke | 69 | 126 伤 | dmg%=150~200、dmg-ltng=1~511、hit-skill=20~14、swing2=15~15 | hit-skill |  |

### aspe（2 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Lycander's Flank | 42 | 214 伤 | ama=2~2、skilltab=2~2、dmg%=150~200、swing2=30~30 | ama |  |
| Stoneraven | 64 | 304 伤 | dmg%=230~280、dmg-mag=101~187、res-all=30~50、ac=400~600 | — |  |

### circ（2 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Griffon's Eye | 76 | 55 防 | ac=100~200、cast2=25~25、allskills=1~1、extra-ltng=10~15 | — |  |
| Kira's Guardian | 77 | 45 防 | ac=50~120、res-all=50~70、nofreeze=1~1、balance2=20~20 | — |  |

### tkni（2 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Deathbit | 44 | 34 伤 | deadly=40~40、dmg%=130~180、att=200~450、lifesteal=7~9 | — |  |
| Warshrike | 75 | 108 伤 | dmg%=200~250、pierce=50~50、swing2=30~30、deadly=50~50 | hit-skill |  |

### lcha（1 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Gheed's Fortune | 62 | — | mag%=20~40、gold%=80~160、cheap=10~15 | — |  |

### mcha（1 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Hellfire Torch | 75 | — | randclassskill=0~6、all-stats=10~20、res-all=10~20、light=8~8 | randclassskill、hit-skill、charged |  |

### scha（1 件）

| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |
|---|---:|---:|---|---|---|
| Annihilus | 70 | — | allskills=1~1、all-stats=10~20、res-all=10~20、addxp=5~10 | — |  |

## 怎么用这份表（下一步）

**第一批要动的不是「垃圾暗金」，而是「死属性」。** 理由：

1. **客观** —— 死属性不需要判断「有没有人用」，规则在引擎里是确定的
2. **等价交换**（E3）—— 白给的属性换成起作用的属性，不改变强度分布，不造新 BiS
3. **风险最低** —— 不动这件装备的核心功能（比如 Magefist 的 FCR/火技能完全不动）

注意 **死属性 ≠ 垃圾**：`Magefist` 有死属性（手套上的火伤害），但它是法系手套的常用件。改它只是把白给的那一条换掉，不是重做。

第二批才是 B 类「没有任何强属性」的那几件 —— 那时候才需要回答 E1：给它一个身份（谁、什么阶段、为了什么），填不出来就别改。
