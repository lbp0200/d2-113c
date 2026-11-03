"""P1 只读分析：经济结构（收益挂钩挑战）。

回答的问题是 **S2：收益是不是跟"处理了什么难度"挂钩**，以及 **L1 改动前后符文产出往哪走**。

核心指标：**每小时能触发多少次 "Good" 判定**（`Good` 是符文、珠宝、宝石的入口，
再往下 10.77% 才是符文）。之所以不直接算符文，是因为 Good 的链条在各幕不同
（Act3→Runes 15、Act4→Runes 16、Act5→Runes 17），分档混算会失真。

⚠ 路线的事件密度是**行为假设**，不是数据。改之前先看 §"假设"那张表；
它只用于"量级对比"，不要当成精确预测。

用法：
    python3 -m tools.p1_economy                     # 现状 → docs/p1-economy.md
    python3 -m tools.p1_economy --overlay mod       # 打上补丁后
    python3 -m tools.p1_economy --compare mod       # 前后对比（推荐）
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from .d2tc import TreasureClasses
from .d2patch import Ctx

ROOT = Path(__file__).resolve().parent.parent

# 路线 → (代表 TC, 每小时事件数)。事件密度是**假设**，写在报告里让人自己改。
ROUTES: list[tuple[str, str, float]] = [
    ("LK 超箱 6 个（15 秒/趟）", "Act 3 (H) Super A", 6 * 3600 / 15),
    ("普通箱子（同趟顺手开）", "Act 3 (H) Chest B", 6 * 3600 / 15),
    ("牛场清场（约 50 杀/秒上限的 1/6）", "Cow (H)", 3000),
    ("白怪清场（Act5 近战）", "Act 5 (H) H2H A", 3000),
    ("精英怪（一场 8 群、5 分钟一趟）", "Act 5 (H) Champ A", 96),
    ("暗金怪（同上，数量约为精英的一半）", "Act 5 (H) Unique A", 48),
    ("崔凡克（9 只/趟、30 秒/趟）", "Council (H)", 9 * 120),
]


def good_prob(tc: TreasureClasses, name: str, players: float = 8, depth: int = 0) -> float:
    """一次事件能触发几次 Good 判定。

    到达名为 `*Good` 的 TC 即算命中并停止展开（Good 内部是珠宝/宝石/符文，不关心）。
    `Picks` 为负表示「保证掉落、忽略 NoDrop」，所以取绝对值当次数。
    """
    if depth > 12:
        return 0.0
    e, nod = tc.entries(name)
    picks = tc.picks(name)
    total = sum(p for _, p in e)
    if picks > 0:
        if players > 1:
            n = int(nod)
            for i in range(1, int(players)):
                n = n * (int(players) - i) // (int(players) - i + 1)
            total += n
    elif picks < 0:
        total = sum(p for _, p in e)  # 负数 Picks：NoDrop 不参与
    if total <= 0:
        return 0.0

    acc = 0.0
    for item, p in e:
        share = p / total
        if re.search(r"Good$", item):
            acc += share
        elif item in tc:
            acc += share * good_prob(tc, item, players, depth + 1)
    return abs(picks) * acc


def rune_tier(tc: TreasureClasses, name: str, depth: int = 0) -> str:
    """这个 TC 最终走到的符文档（`Runes N`），用来判断最高能出什么。"""
    if depth > 12:
        return ""
    e, _ = tc.entries(name)
    for item, _ in e:
        if item.startswith("Runes"):      # 直接命中符文档
            return item
        if item in tc:
            t = rune_tier(tc, item, depth + 1)
            if t:
                return t
    return ""


def report(ctx: Ctx, players: float = 8) -> tuple[list[list[str]], list[str]]:
    tc = TreasureClasses(ctx.load("treasureclassex.txt"))
    rows, warns = [], []
    for label, name, density in ROUTES:
        if name not in tc:
            warns.append(f"{name} 不存在")
            continue
        g = good_prob(tc, name, players)
        rows.append([label, name, f"{density:.0f}", f"{g:.2%}", f"{g * density:.0f}",
                     rune_tier(tc, name)])
    return rows, warns


HEADER = ["路线", "代表 TC", "事件/小时", "Good/事件", "Good/小时", "符文档位"]


def render(title: str, rows: list[list[str]], warns: list[str], players: float) -> list[str]:
    L = [f"## {title}", ""]
    L.append("| " + " | ".join(HEADER) + " |")
    L.append("|---|---|---:|---:|---:|---|")
    for r in rows:
        L.append("| " + " | ".join(r) + " |")
    L += ["", f"（`/players {players:.0f}`；符文档位 = 该路线 Good 能走到哪一档 `Runes N`）", ""]
    for w in warns:
        L.append(f"- ⚠ {w}")
    if warns:
        L.append("")
    return L


def build_md(before: list[list[str]], after: list[list[str]] | None,
             warns: list[str], players: float) -> str:
    L = [
        "# P1 · 经济结构报告（收益挂钩挑战）",
        "",
        "> 由 `tools/p1_economy.py` 生成。指标是**每小时触发的 Good 判定次数**"
        "（Good 是符文/珠宝/宝石的入口，其中约 10.77% 才是符文）。",
        "",
        "**为什么看 Good 而不是符文**：各幕的 Good 指向不同符文档"
        "（Act3→`Runes 15` 最高 Ber、Act4→`Runes 16` 最高 Cham、Act5→`Runes 17` 最高 Zod），"
        "混算会失真。所以先比次数，再看档位。",
        "",
        "### 事件密度是假设，不是数据",
        "",
        "| 路线 | 假设的事件密度 |",
        "|---|---|",
        "| LK 超级箱子 | 6 箱 / 15 秒 |",
        "| 牛场 / 白怪清场 | 3000 杀 / 小时 |",
        "| 精英 / 暗金 | 96 / 48 只每小时（8 群一趟、5 分钟一趟） |",
        "| 崔凡克 | 9 只 / 30 秒 |",
        "",
        "这些数字只用来比**量级**，不要当预测。真实效率只有进游戏才能测。",
        "",
    ]
    L += render("现状（`vanilla/`）", before, warns, players)
    if after is not None:
        L += render("打上补丁后（`--overlay mod`）", after, [], players)
        L += ["### 变化", ""]
        L.append("| 路线 | Good/小时 前 | 后 | 倍数 |")
        L.append("|---|---:|---:|---:|")
        for b, a in zip(before, after):
            if b[1] != a[1]:
                continue
            try:
                nb, na = float(b[4]), float(a[4])
            except ValueError:
                continue
            mult = "—" if nb == 0 else f"{na / nb:.2f}×"
            L.append(f"| {b[0]} | {nb:.0f} | {na:.0f} | {mult} |")
        L.append("")
        L += [
            "**看这张表的方法**：目标不是「每条路线都变高」，而是「打怪路线 ≥ 开箱路线」，",
            "而且总产出大致持平（P1 毕业时间不变）。",
            "",
        ]
    return "\n".join(L).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tools.p1_economy")
    ap.add_argument("--vanilla", type=Path, default=ROOT / "vanilla")
    ap.add_argument("--out", type=Path, default=ROOT / "docs" / "p1-economy.md")
    ap.add_argument("--overlay", type=Path, default=None)
    ap.add_argument("--compare", type=Path, default=None,
                    help="同时输出与某个叠加层的对比（一般传 mod）")
    ap.add_argument("--players", type=float, default=8)
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args(argv)

    base_ctx = Ctx(vanilla=args.vanilla, out=ROOT / "mod")
    before, warns = report(base_ctx, args.players)
    after = None
    if args.overlay or args.compare:
        ov = args.overlay or args.compare
        after, _ = report(Ctx(vanilla=args.vanilla, out=ROOT / "mod", overlay=ov), args.players)
    md = build_md(before, after, warns, args.players)
    if args.stdout:
        print(md)
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(md, encoding="utf-8")
        print(f"→ {args.out}  ({len(md.splitlines())} 行)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
