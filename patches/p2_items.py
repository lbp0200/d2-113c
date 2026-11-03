"""P2 · 元素穿透 craft（给「没有掌握技能」的职业一条路）

## 为什么需要它

`docs/p2-skills-classes.md` 的结论：地狱里的强弱 = **免疫覆盖率 × 自带降抗**。
但**降抗只存在于三个技能里**，而且全是法师(冰)/死灵/圣骑士的。

德鲁伊、刺客、亚马逊**连一个"掌握类"被动都没有** —— 所以技能层（`skills.txt`）
对他们无效：没有可以挂 `passivestat` 的被动技能。他们只能靠装备。

原版自己的答案就是装备：格利风之眼 / 无限 / 塔格奥之鳞 —— 全是 `passive_*_pierce`。
我们走的正是同一条路，只是把它做成**可合成**而不是靠掉落。

## 为什么是 cbue 配方而不是新符文之语/新暗金

- 新符文之语/新暗金都要在字符串表里加名字 → 整合版是 **Big5 繁体**，改 tbl 风险极高
- craft 的输出名字就是**底材名**（"头盔"），mod 行由引擎自动生成
  （`passive_fire_pierce` 的 `descfunc=20` + `descstrpos=Moditemenresfiresk`
  → 自动显示成「−X% 敌人火焰抗性」），**完全不需要碰 tbl**
- P3 明确允许「新增 cube 配方」

## 数值怎么定的：先看原版给了什么

原版所有「−% 敌人抗性」的来源（`UniqueItems.txt` / `SetItems.txt`）：

| 装备 | 元素 | 穿透 |
|---|---|---:|
| 死亡之网 Death's Web | 毒 | 40~50 |
| 女族长 Wizendraw | 冰 | 20~35 |
| 塔格奥之翼 Trang-Oul's Wing | 毒 | 25 |
| **乌鸦之灵 Ravenlore**（德鲁伊专属头盔） | **火** | **10~20** |
| 塔拉夏的眼球 | 火 / 电 | 15 |
| 格利风之眼 Griffon's Eye | 电 | 15~20 |
| 曼颂的教训 / 雷霆之击 | 各系 | 7~15 |
| **彩虹刻面**（可镶嵌多颗） | 各系 | 3~5 / 颗 |

所以「做一件 craft 装备」的合理区间是 **10~20** —— 和乌鸦之灵同级，
不超过格利风之眼的上限。原版本来就有「用珠宝堆穿透」这条路（3 孔 = 最多 15%），
我们只是给了它一个**可合成、不靠掉落**的版本。

配合第二条 mod「+% 该系技能伤害」（原版 `extra-fire` 等，格利风之眼同款），
对**没有掌握技能**的职业合起来约等于「半套掌握」：

| 无掌握职业的火系 | 区域平均系数 |
|---|---:|
| 裸装 | 0.61 |
| +10 穿透 +10% 伤害 | ~0.77 |
| +20 穿透 +15% 伤害 | ~0.88 |

（126 个钉了怪的区域取平均；0 = 完全打不动，1 = 无抗性。）

**这不足以让火德追上风德**（两者还差一个技能本体伤害的档次），
那个缺口要单独在技能层（`skills.txt`）修 —— 见 `docs/p2-balance-plan.md` 第 5 节 #2。

## 为什么只做头盔

头盔只能戴一个 → 玩家最多拿一条穿透，不会叠。这比让每个部位都能 craft 安全得多。
"""

from tools.d2patch import patch

# 一个配方家族：魔法头盔 + 珠宝 + 埃欧(r16) + 完美宝石 → 带该系穿透的头盔
# 结构完全照抄原版的血系 craft（`enabled/version/numinputs/output/plvl/ilvl` 一致），
# 只换 mod 和宝石，避免自创输入语法踩坑。
_BASE = {
    "enabled": 1,
    "version": 100,
    "numinputs": 4,
    "input 1": '"hlm,mag,upg"',
    "input 2": "jew",
    "input 3": "r16",
    "output": '"usetype,crf"',
    "plvl": 50,
    "ilvl": 50,
}

ELEMS = [
    # (元素, 完美宝石, pierce property, resist property, extra-%damage 后缀)
    ("fire", "gpr", "pierce-fire", "res-fire", "fire"),
    ("lightning", "gpy", "pierce-ltng", "res-ltng", "ltng"),
    ("cold", "gpb", "pierce-cold", "res-cold", "cold"),
    ("poison", "gpg", "pierce-pois", "res-pois", "pois"),
]

for elem, gem, pierce_prop, resist_prop, extra_suffix in ELEMS:
    patch(
        "cubemain.txt",
        why=f"P2 元素穿透 craft（{elem}）：给没有掌握技能的职业一条降抗途径",
    ).append_row({
        **_BASE,
        "description": f"magic helm + jewel + io + {gem} -> {elem} pierce helm",
        "input 4": gem,
        # 1) −% 敌人该系抗性（和乌鸦之灵同级，不超过格利风之眼）
        "mod 1": pierce_prop,
        "mod 1 min": 10,
        "mod 1 max": 20,
        # 2) +% 该系技能伤害（格利风之眼同款 property）
        "mod 2": f"extra-{extra_suffix}",
        "mod 2 min": 10,
        "mod 2 max": 15,
        # 3) 小量该系抗性（craft 该有的护身 mod）
        "mod 3": resist_prop,
        "mod 3 min": 20,
        "mod 3 max": 30,
    })
