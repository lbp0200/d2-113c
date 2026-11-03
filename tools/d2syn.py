"""技能协同（synergy）求值 —— **本仓库最重要的一次认知修正**。

## 之前错在哪

`docs/p1-skills.md` 和 `docs/design-goal.md` 一直写着：

> 「1.13c 的协同加成硬编码在 Dll 里，txt 没有任何 syn 列」

那是**错的**。当时只搜了列名里带 `syn` 的列，而真正的列叫：

- **`DmgSymPerCalc`** —— 物理伤害协同
- **`EDmgSymPerCalc`** —— 元素伤害协同

它们不是空的，而是**完整的公式字符串**，例如：

```
Fire Ball   : (skill('Fire Bolt'.blvl)+skill('Meteor'.blvl))*par8     (par8 = 14)
Blessed Hammer: (skill('Vigor'.blvl)+skill('Blessed Aim'.blvl))*par8   (par8 = 14)
War Cry     : (skill('Howl'.blvl)+skill('Taunt'.blvl)+skill('Battle Cry'.blvl))*par8  (par8 = 6)
```

`skills.txt` 里**有 68 个技能**带这两列。

## 这意味着什么

1. **协同是可以改的** —— 之前"协同改不了，所以只能加本体伤害"这条硬约束不成立
2. **所有只看本体伤害的结论都要重新审视** —— 例如火球本体 324-366，
   但 Fire Bolt 20 + Meteor 20 会给 +560%
3. 反过来，有些技能**本体弱但协同强**（`Frozen Orb` 只有 +2%/级，
   这就是它"本体不强却好用"的原因）

## 求值方式

公式里只有三种东西：`skill('X'.blvl)`、`parN`（= `ParamN` 列）、以及 `+ - * / ( )`。
所以用白名单正则把这三类替换掉之后求值，不做任何别的解释。
"""

from __future__ import annotations

import re

from . import d2txt
from .d2patch import Ctx

SKILL_REF = re.compile(r"skill\s*\(\s*'([^']+)'\s*\.\s*blvl\s*\)")
PAR_REF = re.compile(r"\bpar([1-8])\b")
SAFE = re.compile(r"^[0-9+\-*/(). ]*$")


def _formula(tf: d2txt.TxtFile, row: list[str]) -> str:
    for col in ("DmgSymPerCalc", "EDmgSymPerCalc"):
        i = tf.find(col)
        if i is not None:
            v = tf.get(row, i).strip().strip('"')
            if v:
                return v
    return ""


def _eval(expr: str, levels: dict[str, int], params: list[str]) -> float | None:
    def sub_skill(m: re.Match) -> str:
        return str(int(levels.get(m.group(1), 0)))

    def sub_par(m: re.Match) -> str:
        idx = int(m.group(1)) - 1
        try:
            return repr(float(params[idx] or 0))
        except (ValueError, IndexError):
            return "0"

    expr = SKILL_REF.sub(sub_skill, expr)
    expr = PAR_REF.sub(sub_par, expr)
    expr = expr.replace(" ", "")
    if not SAFE.match(expr):
        return None
    try:
        return float(eval(expr, {"__builtins__": {}}, {}))  # noqa: S307 —— 已白名单
    except Exception:
        return None


def load(ctx: Ctx) -> tuple[dict[str, list[str]], d2txt.TxtFile, dict[str, int]]:
    """-> ({技能名: 协同公式}, 表, {技能名: 行号})"""
    tf = ctx.load("skills.txt")
    i_skill = tf.need("skill")
    formulas = {}
    index = {}
    for i, row in enumerate(tf.rows):
        name = tf.get(row, i_skill).strip()
        if not name:
            continue
        index[name] = i
        f = _formula(tf, row)
        if f:
            formulas[name] = f
    return formulas, tf, index


def synergy_pct(ctx: Ctx, skill: str, levels: dict[str, int] | None = None,
                default: int = 20) -> float | None:
    """返回该技能的协同加成百分比（0 = 无协同）。

    `levels` 里没列出的协同技能按 `default` 级算（默认 20 —— 也就是
    "主技能点满、协同也都点满"的典型终局构筑）。
    """
    formulas, tf, index = load(ctx)
    f = formulas.get(skill)
    if not f:
        return None
    row = tf.rows[index[skill]]
    params = [tf.get(row, tf.need(f"Param{k}")) for k in range(1, 9)]
    lv = {name: default for name in SKILL_REF.findall(f)}
    if levels:
        lv.update({k: v for k, v in levels.items() if k in lv})
    return _eval(f, lv, params)


def report_rows(ctx: Ctx) -> list[dict]:
    """所有带协同的技能的：本体 L20 / 满协同 / 倍率。"""
    from .p1_skills import skill_damage

    formulas, tf, index = load(ctx)
    out = []
    for name, f in formulas.items():
        row = tf.rows[index[name]]
        base = skill_damage(tf, row, 20)
        pct = synergy_pct(ctx, name) or 0.0
        mult = 1 + pct / 100
        out.append({
            "skill": name,
            "base": base,
            "pct": pct,
            "mult": mult,
            "full": (base[0] * mult, base[1] * mult),
        })
    out.sort(key=lambda r: -r["mult"])
    return out
