"""构建 MOD。

    python3 -m tools.build                # 构建到 mod/ 并生成 docs/changelog.md
    python3 -m tools.build --check        # 只做 vanilla 基线自检（抽取后第一件事）
    python3 -m tools.build --dry-run      # 只出报告，不写文件

流程：读 vanilla 基线（只读）→ 依次执行 patches/*.py 的声明 → 只把内容真的变了的表
写到 mod/data/global/excel/ → 生成人类可读的改动报告。
"""

from __future__ import annotations

import argparse
import importlib.util
import shutil
import sys
from pathlib import Path

from . import d2patch, d2txt
from .d2patch import Ctx, use

ROOT = Path(__file__).resolve().parent.parent


# --------------------------------------------------------------- 基线自检


def check_baseline(ctx: Ctx) -> list[str]:
    """vanilla 表自检：round-trip 必须字节一致；顺带报告列数异常。"""
    problems: list[str] = []
    files = sorted(ctx.excel.glob("*.txt"))
    if not files:
        return [f"{ctx.excel} 下没有 .txt 文件"]

    print(f"基线自检：{len(files)} 张表（{ctx.excel}）")
    for p in files:
        data = p.read_bytes()
        tf = d2txt.TxtFile.loads(data)
        if tf.dumps() != data:
            problems.append(f"{p.name}: round-trip 不是字节一致（编码/换行有异常）")
        long_rows = tf.long_rows()
        if long_rows:
            problems.append(f"{p.name}: {long_rows} 行的列数多于表头（{len(tf.header)} 列）")
        if not tf.header:
            problems.append(f"{p.name}: 空表头")

    mixed = [p.name for p in files if len(set(d2txt.TxtFile.load(p).seps)) > 1]
    if mixed:
        print(f"  提示：这些表混用了多种换行符（不影响，但记一下）：{mixed}")
    return problems


# --------------------------------------------------------------- 补丁模块


def load_patches(ctx: Ctx, patch_dir: Path) -> list[str]:
    use(ctx)
    loaded = []
    for p in sorted(patch_dir.glob("*.py")):
        if p.name.startswith("_"):
            continue
        mod_name = f"d2patches.{p.stem}"
        spec = importlib.util.spec_from_file_location(mod_name, p)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[mod_name] = mod
        spec.loader.exec_module(mod)
        loaded.append(p.name)
    return loaded


# --------------------------------------------------------------- 报告


def render_report(ctx: Ctx) -> str:
    out = ["# 改动报告", "", "> 由 `tools/build.py` 自动生成，勿手改。基线：`vanilla/`", ""]

    if not ctx.changes:
        out.append("（本次没有任何改动）")
    by_file: dict[str, dict[str, list[d2patch.Change]]] = {}
    for c in ctx.changes:
        by_file.setdefault(c.file, {}).setdefault(c.col, []).append(c)

    for f in sorted(by_file):
        out.append(f"## {f}")
        out.append("")
        out.append("| 列 | 改动行数 | 示例 |")
        out.append("|---|---:|---|")
        for col, chs in by_file[f].items():
            ex = "；".join(
                f"`{c.row}`: {c.old or '(空)'} → {c.new}" for c in chs[:3]
            )
            if len(chs) > 3:
                ex += f"；…另 {len(chs) - 3} 行"
            out.append(f"| `{col}` | {len(chs)} | {ex} |")
        whys = sorted({c.why for chs in by_file[f].values() for c in chs if c.why})
        if whys:
            out.append("")
            out.append("理由：" + "；".join(whys))
        out.append("")

    if ctx.skipped:
        out.append("## 跳过的补丁")
        out.append("")
        for f, why in ctx.skipped:
            out.append(f"- `{f}` — {why}")
        out.append("")

    if ctx.warnings:
        out.append("## 警告")
        out.append("")
        for w in ctx.warnings:
            out.append(f"- {w}")
        out.append("")

    return "\n".join(out).rstrip() + "\n"


# --------------------------------------------------------------- 主流程


def clean_out(ctx: Ctx, keep: set[str]) -> list[str]:
    """删掉 mod/ 里已经不产出内容的旧表，避免"删了补丁但文件还在"的幽灵改动。"""
    removed = []
    for p in sorted((ctx.out / ctx.out_prefix).glob("*.txt")):
        if p.name not in keep:
            p.unlink()
            removed.append(p.name)
    return removed


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tools.build", description="构建 D2 MOD 覆盖层")
    ap.add_argument("--vanilla", type=Path, default=ROOT / "vanilla", help="基线目录（只读）")
    ap.add_argument("--out", type=Path, default=ROOT / "mod", help="输出目录")
    ap.add_argument("--patches", type=Path, default=ROOT / "patches", help="补丁目录")
    ap.add_argument("--report", type=Path, default=ROOT / "docs" / "changelog.md")
    ap.add_argument("--check", action="store_true", help="只做基线自检")
    ap.add_argument("--dry-run", action="store_true", help="不写文件")
    args = ap.parse_args(argv)

    ctx = Ctx(vanilla=args.vanilla, out=args.out)

    problems = check_baseline(ctx)
    if problems:
        print("\n基线有问题：")
        for p in problems:
            print(f"  ✗ {p}")
        if args.check:
            return 1
    if args.check:
        print("\n基线自检通过" if not problems else "")
        return 0 if not problems else 1
    if problems:
        return 1

    ctx.files.clear()
    ctx.original.clear()

    names = load_patches(ctx, args.patches)
    print(f"\n补丁：{len(names)} 个文件 {names}")

    changed = ctx.changed_files()
    report = render_report(ctx)

    print(f"改动：{len(ctx.changes)} 处，涉及 {len(changed)} 张表")
    if ctx.skipped:
        print(f"跳过：{len(ctx.skipped)} 个补丁（列名对不上）")
    if ctx.warnings:
        print(f"警告：{len(ctx.warnings)} 条")

    if args.dry_run:
        print("\n" + report)
        return 0

    for name, data in changed.items():
        p = ctx.out_path(name)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        print(f"  → {p.relative_to(ROOT) if p.is_relative_to(ROOT) else p}")

    removed = clean_out(ctx, set(changed))
    if removed:
        print(f"  清理旧文件：{removed}")

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(report, encoding="utf-8")
    print(f"  报告 → {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
