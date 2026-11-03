"""P3 只读分析：**装备体检表** —— 每件暗金有没有"谁会穿它"。

和技能层完全同源的问题：技能层要求「每系有一个胜场」，装备层要求
「**每件要有一个身份**：什么构筑、在什么阶段、为了哪一项属性穿它」。
说不出来的，就是垃圾 —— 不管它的属性表看起来多满。

## 本工具只做两件事

1. **算清每件装备能提供什么**（把 `prop1..12` 通过 `properties.txt` 解析成 stat 值，
   再叠加基础物品的伤害/防御，得到"有效伤害/有效防御"）
2. **标出两类候选**，但**不自动判定**：
   - **A 类「被完全覆盖」**：同槽位、需求等级不更高、每一项都不差、且有效伤害/防御更高
   - **B 类「低贡献」**：既没有像样的进攻、也没有防御/技能，只有边角属性

判定始终由人来做 —— 「谁会穿」那一列是留空的，必须有人填。

## 已知的边界（别把候选当结论）

- 触发技能（`hit-skill` / `gethit-skill` / `charged`）、光环、`swing*` 之外的隐藏机制
  没有计入有效伤害
- 基础物品的**攻击范围/需求力量/速度档位**只作展示，不参与比较
- 因此 A 类候选里会混进误判（第一版就误报过 `Windhammer`：它有 50% CB + 60 IAS）

用法：
    python3 -m tools.p3_items                # → docs/p3-items.md
    python3 -m tools.p3_items --stdout
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from . import d2txt

ROOT = Path(__file__).resolve().parent.parent
EXCEL = ROOT / "vanilla" / "data" / "global" / "excel"

# 不会掉落的（任务物品）—— 光看表它们是"最垃圾的暗金"，但根本没有掉落路径。
QUEST = {
    "Staff of Kings", "Horadric Staff", "KhalimFlail", "SuperKhalimFlail",
    "Hell Forge Hammer",
}

# `properties.txt` 的 func 含义：1 = 直接赋值，3 = 直接赋值（多 stat 版本），
# 7 = 强化伤害（无 stat 名），8 = 攻速/施法/格挡等速率（有 stat 名）。
# 其余的（2 = 按 param 索引，11 = 击中触发技能，…）**无法从表里还原成数值**，
# 所以单独记进「未量化」列，让复核的人自己看 —— 不猜。
ACCEPT_FUNCS = {"1", "3"}
NO_STAT_BY_CODE = {
    "dmg%": "ed", "ac%": "ed_def",
    "swing1": "ias", "swing2": "ias", "swing3": "ias",
    "cast1": "fcr", "cast2": "fcr", "cast3": "fcr",
    "balance1": "fhr", "balance2": "fhr", "balance3": "fhr",
    "move1": "frw", "move2": "frw", "move3": "frw",
}

# 同一件事的不同 stat 名 → 统一成一个比较用的名字
NORMALIZE = {
    "item_crushingblow": "cb", "item_deadlystrike": "ds", "item_openwounds": "ow",
    "item_allskills": "skills", "item_fasterattackrate": "ias",
    "item_fastercastrate": "fcr", "item_fasterblockrate": "fbr",
    "item_fastergethitrate": "fhr", "item_fastermovevelocity": "frw",
    "item_maxhp_percent": "hp", "item_maxmana_percent": "mana",
    "item_armor_percent": "ed_def", "armorclass": "def", "tohit": "ar",
    "item_strength": "str", "item_dexterity": "dex", "item_vitality": "vit",
    "item_energy": "enr", "item_maxdamage_percent": "ed",
    "item_normaldamage": "add_dmg",
    "maxhp": "hp", "maxmana": "mana",
    "strength": "str", "dexterity": "dex", "vitality": "vit", "energy": "enr",
    "item_tohit_percent": "ar", "tohit": "ar",
    "armorclass_vs_missile": "def", "tosblock": "block", "toblock": "block",
    "lifedrainmindam": "lifesteal", "manadrainmindam": "manasteal",
    "damageresist": "dr", "normal_damage_reduction": "dr",
    "item_maxdamage_percent": "ed", "item_manaafterkill": "mana_kill",
    "item_explosivearrow": "free_skill", "item_nonclassskill": "oskill",
    "passive_fire_mastery": "elem_mastery", "passive_ltng_mastery": "elem_mastery",
    "passive_cold_mastery": "elem_mastery", "passive_pois_mastery": "elem_mastery",
    "passive_fire_pierce": "elem_pierce", "passive_ltng_pierce": "elem_pierce",
    "passive_cold_pierce": "elem_pierce", "passive_pois_pierce": "elem_pierce",
    "item_numsockets": "sock",
    "swing1": "ias", "swing2": "ias", "swing3": "ias",
    "cast1": "fcr", "cast2": "fcr", "cast3": "fcr",
    "balance1": "fhr", "balance2": "fhr", "balance3": "fhr",
    "move1": "frw", "move2": "frw", "move3": "frw",
    "dmg%": "ed", "ac%": "ed_def",
    "crush": "cb", "deadly": "ds", "openwounds": "ow",
    "res-all": "res", "allskills": "skills",
    "fireresist": "res-fire", "coldresist": "res-cold",
    "lightresist": "res-ltng", "poisonresist": "res-pois",
}

# 这些属性对"能不能打/能不能活"没有贡献，只用于 B 类判定
NOISE = {
    "lightradius", "stamina", "staminarecoverybonus", "regen", "regen-mana",
    "dur", "indestruct", "thorns", "att-skill", "stupidity", "howl", "knock",
    "freeze", "slow", "hp/lvl", "mana/lvl", "extra-stamina",
}

# 「强属性」阈值：任何一项达到这条线，这件装备就有话可说。
# 阈值是**人工定的一条低标准**（不是精确价值模型），过线只代表"不算垃圾候选"。
STRONG: dict[str, float] = {
    "ed": 80, "eff_dmg": 40, "add_dmg": 40, "elem_dmg": 40, "ias": 10, "fcr": 10, "fhr": 10, "frw": 20,
    "cb": 10, "ds": 10, "ow": 10, "lifesteal": 3, "manasteal": 3,
    "skills": 1, "skill": 1, "skilltab": 1,
    "res": 15, "res-fire": 20, "res-cold": 20, "res-ltng": 20, "res-pois": 20,
    "dr": 5, "absorb": 5, "block": 15, "def": 200, "eff_def": 300,
    "hp": 30, "mana": 40, "str": 10, "dex": 10, "vit": 10, "enr": 10,
    "ar": 100, "dr%": 8, "item_cannotbefrozen": 1, "item_pierce": 1,
    "item_slow": 10, "item_freeze": 1, "item_knockback": 1, "item_preventheal": 1,
    "mana_kill": 3, "item_halffreezeduration": 30,
    # 寻宝/金币也是真实身份：MF 装是一整类构筑动机
    "item_magicbonus": 20, "item_goldbonus": 100,
    # 提高抗性上限是"防御身份"，不是边角属性
    "maxfireresist": 3, "maxcoldresist": 3, "maxlightresist": 3, "maxpoisonresist": 3,
    "sock": 1, "elem_pierce": 5, "elem_mastery": 10, "indestruct": 1,
    # 「对不死/恶魔加倍伤害」和「受伤转法力」都是真实的构筑动机，不是边角属性
    "item_undeaddamage_percent": 50, "item_demondamage_percent": 50,
    "item_damagetomana": 30,
    # 「自带某某技能」= 直接给一个能力，低阶装备的常见身份
    "free_skill": 1, "oskill": 1,
}

# 这些槽位不参与判定：任务物品、护身符（护身符不和任何装备抢槽位）
SKIP_SLOTS = {"quest", "cm1", "cm2", "cm3", "lcha", "mcha", "scha"}


def dead_stats(item: dict) -> list[str]:
    """**存疑**的槽位错配（不是定论）。

    只保留一条：武器上的 `+X% 防御`（`ac%`）—— 武器本身没有防御值。
    但即便这条也不确定：`item_armor_percent` 可能是全局的（会被算进总防御），
    所以这里只用于挑出"值得进游戏看一眼"的装备，**不作为改动依据**。

    历史教训：第一版把 `dmg%`/元素附加伤害在护甲上也当成死的，列了 43 件，
    但 Fortitude（衣服 +300% ED）、Steelrend（手套 +60% ED）都证明那是全局生效的。
    """
    if item["kind"] == "weapon" and "ed_def" in item["stats"]:
        return ["ed_def"]
    return []


def strong_hits(item: dict) -> list[str]:
    """达到 STRONG 阈值的属性（这就是它"有身份"的候选依据）。"""
    return [f"{k}={v:.0f}" for k, v in item["stats"].items()
            if k in STRONG and v >= STRONG[k]]


def load_props() -> tuple[dict[str, list[str]], set[str]]:
    """-> ({property code: 可求值的 metric 名列表}, {仍然无法求值的 property code})

    `properties.txt` 的 `func` 决定数值怎么来：

    | func | 含义 | 本工具的处理 |
    |---|---|---|
    | 1 / 3 | 直接赋值（3 是多 stat 的同义） | 取 item 的 min/max |
    | 7 / 8 | 强化伤害 / 攻速施法档位 | 由 `NO_STAT_BY_CODE` 给出 metric 名 |
    | 10 | +技能树等级 | `skilltab` |
    | 15 / 16 | 附加元素/普通伤害的 min / max | `flat_dmg` |
    | 22 | +单个技能等级 | `skill` |
    | 11 / 19 / … | 击中触发、充能、光环 | **仍然列为「未量化」** —— 这类属性的身份就在其中，不许猜 |
    """
    tf = d2txt.TxtFile.load(str(EXCEL / "Properties.txt"))
    h = tf.header
    ok: dict[str, list[str]] = {}
    opaque: set[str] = set()
    for r in tf.rows:
        if not r or not r[0]:
            continue
        code = r[0]
        if code in NO_STAT_BY_CODE:
            ok[code] = [NO_STAT_BY_CODE[code]]
            continue
        stats, cannot = [], False
        for k in range(1, 4):
            cs, cf = f"stat{k}", f"func{k}"
            if cs not in h or cf not in h:
                continue
            func = r[h.index(cf)].strip()
            stat = r[h.index(cs)].strip()
            if not func:
                continue
            if func in ACCEPT_FUNCS and stat:
                stats.append(stat)
            elif func in {"5", "6"}:
                stats.append("add_dmg")          # dmg-min / dmg-max
            elif func == "14":
                stats.append("sock")             # 孔数
            elif func == "20":
                stats.append("indestruct")
            elif func == "17":
                stats.append("elem_len")         # 元素持续时间（冷/毒）
            elif func in {"15", "16"}:
                # 元素伤害（firemindam…）只在武器上生效；
                # 物理附加伤害（mindamage/maxdamage，来自 dmg-norm/dmg-min/dmg-max）
                # 在任何槽位都生效 —— 两者必须分开，否则会把"加最小伤害"误判成死属性
                stats.append("elem_dmg" if "fire" in stat or "cold" in stat
                             or "light" in stat.replace("lightning", "ltng") or "pois" in stat
                             or "magic" in stat else "add_dmg")
            elif func == "10":
                stats.append("skilltab")
            elif func == "22":
                stats.append("skill")
            elif func in {"7", "8"}:
                continue                      # 已由 NO_STAT_BY_CODE 处理
            else:
                cannot = True
        if stats:
            ok[code] = stats
        if cannot:
            opaque.add(code)
    return ok, opaque


def load_bases() -> dict[str, dict]:
    """基础物品 code -> 槽位/需求/伤害/防御。"""
    out: dict[str, dict] = {}
    for fn in ("Weapons.txt", "Armor.txt", "Misc.txt"):
        tf = d2txt.TxtFile.load(str(EXCEL / fn))
        h = tf.header
        for r in tf.rows:
            if not r or not r[0]:
                continue
            code = r[h.index("code")].strip().lower()
            if not code:
                continue

            def num(col: str) -> float:
                if col not in h:
                    return 0.0
                v = d2txt.to_number(r[h.index(col)])
                return float(v) if v is not None else 0.0

            two_hand = num("2handed") > 0
            dmg = ((num("2handmindam") + num("2handmaxdam")) / 2 if two_hand
                   else (num("mindam") + num("maxdam")) / 2)
            out[code] = {
                "kind": ("weapon" if fn.startswith("Weapons")
                         else "armor" if fn.startswith("Armor") else "misc"),
                "type": r[h.index("type")].strip() if "type" in h else code,
                "levelreq": num("levelreq"),
                "two_hand": two_hand,
                "base_dmg": dmg,
                "base_ac": (num("minac") + num("maxac")) / 2,
                "speed": num("speed"),
            }
    return out


def collect() -> tuple[list[dict], list[str]]:
    props, opaque = load_props()
    bases = load_bases()
    tf = d2txt.TxtFile.load(str(EXCEL / "UniqueItems.txt"))
    h = tf.header

    def cell(row: list[str], name: str) -> str:
        return row[h.index(name)] if name in h and h.index(name) < len(row) else ""

    items, skipped = [], []
    for row in tf.rows:
        name = row[0].strip() if row else ""
        if not name or cell(row, "enabled") != "1":
            continue
        if name in QUEST:
            skipped.append(name)
            continue
        code = cell(row, "code").strip().lower()
        base = bases.get(code, {})
        stats: dict[str, float] = {}
        shown: list[str] = []
        unmeasured: list[str] = []
        for k in range(1, 13):
            code_p = cell(row, f"prop{k}").strip()
            if not code_p:
                continue
            try:
                v = float(cell(row, f"max{k}") or 0)
            except ValueError:
                v = 0.0
            shown.append(f"{code_p}={cell(row, f'min{k}')}~{cell(row, f'max{k}')}")
            for st in props.get(code_p, []):
                key = NORMALIZE.get(st, st)
                stats[key] = max(stats.get(key, 0.0), v)
            if code_p in opaque:
                unmeasured.append(code_p)

        # 叠加基础物品：有效伤害 = 基础均伤 × (1 + ed%)
        if base.get("kind") == "weapon" and base.get("base_dmg"):
            stats["eff_dmg"] = base["base_dmg"] * (1 + stats.get("ed", 0) / 100)
        if base.get("kind") == "armor" and base.get("base_ac"):
            stats["eff_def"] = base["base_ac"] * (1 + stats.get("ed_def", 0) / 100)

        items.append({
            "name": name,
            "kind": base.get("kind", "?"),
            "slot": base.get("type", code or "?"),
            "code": code,
            "req": float(cell(row, "lvl req") or 0),
            "ilvl": float(cell(row, "lvl") or 0),
            "rarity": float(cell(row, "rarity") or 1),
            "stats": stats,
            "shown": shown,
            "unmeasured": unmeasured,
            "has_opaque": bool(unmeasured),
            "base_req": base.get("levelreq", 0.0),
        })
    return items, skipped


def dominates(b: dict, a: dict) -> tuple[bool, str]:
    """b 是否在每一项上都不差于 a，且至少一项更好。返回 (是否, 理由)。"""
    sa, sb = a["stats"], b["stats"]
    if not sa or not sb:
        return False, ""
    better = 0
    for st, v in sa.items():
        bv = sb.get(st)
        if bv is None:
            return False, f"缺 {st}"
        if bv + 1e-9 < v:
            return False, f"{st} 更低（{bv:.0f} < {v:.0f}）"
        if bv > v + 1e-9:
            better += 1
    extra = set(sb) - set(sa)
    if better == 0 and not extra:
        return False, "完全相同"
    return True, f"多 {better} 项更强 + {len(extra)} 项额外"


def build_report(items: list[dict], skipped: list[str]) -> str:
    by_slot: dict[str, list[dict]] = defaultdict(list)
    for it in items:
        by_slot[it["slot"]].append(it)

    cand_a: list[tuple[dict, dict, str]] = []
    unevaluable: set[int] = set()
    for lst in by_slot.values():
        for a in lst:
            for b in lst:
                if a is b or b["req"] > a["req"]:
                    continue
                if a["has_opaque"] or b["has_opaque"]:
                    unevaluable.add(id(a))      # 有触发技能/光环 → 数值比较不可信
                    continue
                ok, why = dominates(b, a)
                if ok:
                    cand_a.append((a, b, why))
                    break
    dom = {id(a) for a, _b, _w in cand_a}

    judged = [it for it in items if it["slot"].lower() not in SKIP_SLOTS]
    cand_b = [it for it in judged
              if id(it) not in dom and not strong_hits(it) and not it["has_opaque"]]

    L: list[str] = []
    add = L.append
    add("# P3 · 装备体检表（暗金）")
    add("")
    add("> 由 `python3 -m tools.p3_items` 生成，**只读**。")
    add(">")
    add("> 判据（装备层的 E1~E3，对应技能层的 T1~T3）：")
    add(">")
    add("> - **E1 每件一个身份**：能说出「什么构筑 / 什么阶段 / 为了哪一项属性」穿它 —— 说不出来就是垃圾")
    add("> - **E2 不许造新 BiS**：改动不能让某件同时成为多个槽位的最优")
    add("> - **E3 加法或等价交换**：和 T3 一样，不许只拿走不给")
    add("")
    add("**本表不判死**：「谁会穿」那一列是空的，必须由人填。这里只负责把候选挑出来。")
    add("")
    add("已知边界：触发技能（`hit-skill`/`gethit-skill`/`charged`）、光环、"
        "武器速度档位都没有计入「有效伤害」，所以 A 类候选里**一定有误判**。")
    add("")

    add("## 汇总")
    add("")
    add(f"- 可用暗金：**{len(items)}** 件（另有 {len(skipped)} 件任务物品已剔除：{'、'.join(skipped)}）")
    add(f"- A 类「被完全覆盖」候选：**{len(cand_a)}** 件（纯数值可比，未计入触发技能/光环）")
    add(f"- 因含未量化属性（触发技能/光环/充能）而**放弃比较**：{len(unevaluable)} 件 —— 它们的身份可能就在那些属性里")
    add(f"- B 类「低贡献」候选：**{len(cand_b)}** 件")
    add(f"- 有身份待填：**{len(items)}** 行（全表见下）")
    add("")

    add("## A 类候选：被同槽位、需求不更高的装备全面覆盖")
    add("")
    if cand_a:
        add("| 候选（被覆盖） | 需求 | 槽位 | 覆盖它的 | 其需求 | 覆盖理由 |")
        add("|---|---:|---|---|---:|---|")
        for a, b, why in sorted(cand_a, key=lambda x: x[0]["req"]):
            add(f"| **{a['name']}** | {a['req']:.0f} | {a['slot']} | {b['name']} | "
                f"{b['req']:.0f} | {why} |")
    else:
        add("无。")
    add("")
    add("> 复核方法：从 `uniqueitems.txt` 查两件的 `prop*` 逐条比。")
    add("> 特别检查它有没有**触发技能/光环/CB/攻速**这类没被计入的东西 —— 有的话这个候选就是误判。")
    add("")

    add("## B 类候选：没有任何一项够看的属性（且不含触发技能/光环）")
    add("")
    if cand_b:
        add("| 装备 | 需求 | 槽位 | 它到底给了什么（全部达不到强属性线） |")
        add("|---|---:|---|---|")
        for it in sorted(cand_b, key=lambda x: x["req"]):
            desc = "、".join(f"{k}={v:.0f}" for k, v in sorted(it["stats"].items())
                            if k not in ("eff_dmg", "eff_def"))
            add(f"| {it['name']} | {it['req']:.0f} | {it['slot']} | {desc or '（空）'} |")
    else:
        add("无。")
    add("")

    # ---- 参考类：同槽位同需求段内没有任何一项最强
    no_fame = []
    for slot, lst in by_slot.items():
        if slot in SKIP_SLOTS:
            continue
        for a in lst:
            peers = [b for b in lst if b["req"] <= a["req"] and b is not a]
            if not any(st in STRONG and v >= STRONG[st]
                       and all(p["stats"].get(st, 0) <= v + 1e-9 for p in peers)
                       for st, v in a["stats"].items()):
                no_fame.append(a)
    add("## 参考：在**本槽位同需求段**内没有任何一项最强的（不要直接当结论）")
    add("")
    add(f"共 {len(no_fame)} 件。**这一类的参考价值有限**：D2 装备的价值常常来自"
        "**属性的组合**（例如 `Lightsabre` 单看每一项都不最强，但\"攻速+闪电伤害+吸蓝\""
        "合在一起就是它的理由）。所以这里只当线索，不当判定。")
    add("")
    add("| 装备 | 需求 | 槽位 | 它够强的属性（但都不是最强） |")
    add("|---|---:|---|---|")
    for it in sorted(no_fame, key=lambda x: -x["req"])[:30]:
        strong = [f"{k}={v:.0f}" for k, v in sorted(it["stats"].items())
                  if k in STRONG and v >= STRONG[k]]
        add(f"| {it['name']} | {it['req']:.0f} | {it['slot']} | {'、'.join(strong) or '—'} |")
    add("")

    add("## ⚠️ 关于「死属性」：这一类**做错过，已经删掉**")
    add("")
    add("第一版把「`+X% 伤害` / 附加元素伤害 写在护甲上」当成死属性，列了 43 件。**那是错的**：")
    add("")
    add("- 反例一：**Fortitude** 在**衣服**上给 `+300% 强化伤害`，是全身最重要的物理增伤之一")
    add("- 反例二：**Steelrend**（手套）的招牌就是 `+30~60% 强化伤害`")
    add("- 反例三：带 ED 的珠宝可以镶在头盔/衣服里并照常生效")
    add("")
    add("这些 stat（`item_maxdamage_percent`、元素附加伤害）都是**全局**的，")
    add("写在哪个槽位都生效 —— 只有「武器上的 `ac%`」这一类还存疑（武器本身没有防御值）。")
    add("")
    add("所以本工具**不再输出「死属性」结论**。要判断一件装备的某条属性是不是白给，")
    add("唯一可靠的办法是进游戏实测（这正是 `TODO.md` 里那一串待验证项的意义）。")
    add("")

    add("## 全表（按槽位）")
    add("")
    add("「谁会穿」一列留空 —— E1 必须人工填，填不出来的才是要改的。")
    add("")
    for slot in sorted(by_slot, key=lambda s: (-len(by_slot[s]), s)):
        lst = sorted(by_slot[slot], key=lambda x: x["req"])
        add(f"### {slot}（{len(lst)} 件）")
        add("")
        add("| 装备 | 需求 | 有效伤害/防御 | 关键属性 | 未量化 | 谁会穿？ |")
        add("|---|---:|---:|---|---|---|")
        for it in lst:
            st = it["stats"]
            power = (f"{st['eff_dmg']:.0f} 伤" if st.get("eff_dmg")
                     else f"{st['eff_def']:.0f} 防" if st.get("eff_def") else "—")
            add(f"| {it['name']} | {it['req']:.0f} | {power} | "
                f"{'、'.join(it['shown'][:4])} | "
                f"{'、'.join(it['unmeasured'][:3]) or '—'} |  |")
        add("")
    add("## 结论与下一步")
    add("")
    add("**暗金层比预想的健康。** 380 件里：")
    add("")
    add("- **A 类 0 件**：没有任何一件被同槽位的另一件在纯数值上完全覆盖 → 没有「重复设计」")
    add("- **B 类 4 件**：`War Bonnet` / `Lenyms Cord` / `Coif of Glory` / `The Centurion`，")
    add("  而且**全部是 req ≤ 14 的低级件** —— 它们的身份就是「你 3 级时只有这个」，")
    add("  严格说并不算垃圾，只算过渡件")
    add("- 参考类 19 件：单看每一项都不最强，但 D2 的价值常常来自组合，所以只是线索")
    add("")
    add("所以「某件暗金就是垃圾，谁也用不上」这个直觉，在**暗金单品**上成立的不多。")
    add("更值得动的地方按可疑度排序：")
    add("")
    add("1. **套装单件**：穿不齐就是一堆废属性 —— 这类「垃圾」是结构性的，暗金没有这个问题")
    add("2. **低阶符文之语 vs 中阶暗金**：1.13 的低阶 RW（`Honor`/`King's Grace`/`Spirit` 等）")
    add("   让很多 30~60 级暗金失去理由，而这是**跨表**对比，本工具还没做")
    add("3. **真的没有身份但等级高的**：需要人工按 E1 逐个判（本轮没找到，但可能是我漏了）")
    add("")
    return "\n".join(L).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tools.p3_items")
    ap.add_argument("--out", type=Path, default=ROOT / "docs" / "p3-items.md")
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args(argv)

    items, skipped = collect()
    md = build_report(items, skipped)
    if args.stdout:
        print(md)
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(md, encoding="utf-8")
        print(f"→ {args.out}  ({len(md.splitlines())} 行)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
