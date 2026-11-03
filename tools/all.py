"""一条命令重生成所有派生产物，顺序不能错。

顺序是有依赖的：
  1. `build`      —— 从 `vanilla/` + `patches/` 生成 `mod/` 和 `docs/changelog.md`
  2. 之后的分析工具读 `mod/`，所以必须排在 build 后面

漏跑任何一步，某份报告就会比 `mod/` 旧 —— `tests/test_p2_docs.py` 会直接报错
（"p2-audit.md 比 mod/Skills.txt 旧了"）。这就是它存在的意义。

用法：
    python3 -m tools.all              # 全部重生成
    python3 -m tools.all --skip check # 跳过自检
"""

from __future__ import annotations

import argparse
import subprocess
import sys

# (模块, 说明, 是否可跳过)
STEPS = [
    ("tools.build", "从补丁生成 mod/ 与 changelog", False),
    ("tools.validate", "校验生成的表是否能被游戏读", True),
    ("tools.p1_skills", "技能伤害/掌握/降抗/毒系总量", False),
    ("tools.p1_immunity", "地狱免疫墙", False),
    ("tools.p1_economy", "掉落与箱子经济学", False),
    ("tools.p2_trees", "21 系体检表", False),
    ("tools.p2_areas", "区域元素适配度（区域平均系数的唯一来源）", False),
    ("tools.p2_audit", "改动审计（数值下降对账）", False),
    ("tools.p3_items", "装备体检表（暗金）", False),
    ("tools.p3_sets", "套装体检表", False),
]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tools.all")
    ap.add_argument("--skip", action="append", default=[],
                    help="跳过某一步（可重复），如 --skip validate")
    ap.add_argument("--reports", action="store_true",
                    help="p1_economy 同时给出与 mod/ 的对照")
    args = ap.parse_args(argv)

    for mod, desc, skippable in STEPS:
        if mod.split(".")[-1] in args.skip:
            print(f"-- 跳过 {mod}（{desc}）")
            continue
        print(f"== {mod}  ({desc})")
        cmd = [sys.executable, "-m", mod]
        if mod == "tools.p1_economy" and args.reports:
            cmd.append("--compare")
            cmd.append("mod")
        r = subprocess.run(cmd)
        if r.returncode != 0:
            print(f"!! {mod} 失败（exit {r.returncode}）", file=sys.stderr)
            return r.returncode
    print("全部完成。检查一致性：python3 -m unittest discover -s tests -t .")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
