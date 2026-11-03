"""文档一致性：21 系的状态必须在四份文件里说得一样。

收尾时最容易出的错不是代码，是**文档之间对不上**：
`p2-trees.md` 说 12 个体检通过，`p2-balance-plan.md` 写着 11，
`p2-healthy.md` 少列一个系。这种漂移没有人会手工发现，所以在这里钉死。
"""

import re
import unittest
from collections import Counter
from pathlib import Path

from tools.p2_trees import CANT, CLASSES, DONE, HEALTHY, T2, TODO, TREES

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


def read(name: str) -> str:
    return (DOCS / name).read_text(encoding="utf-8")


class DocsConsistency(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.counts = Counter(t["status"] for t in TREES)
        cls.plan = read("p2-balance-plan.md")
        cls.trees = read("p2-trees.md")
        cls.healthy = read("p2-healthy.md")

    def test_plan_stats_line_matches_trees(self):
        m = re.search(
            r"当前统计：✅已改 (\d+) / ⚪体检通过 (\d+) / ⚠️T2过强 (\d+) / "
            r"⬜待修 (\d+) / ❌修不了 (\d+) = (\d+)", self.plan)
        self.assertIsNotNone(m, "p2-balance-plan.md 里找不到「当前统计」那一行")
        got = tuple(int(x) for x in m.groups())
        want = (self.counts[DONE], self.counts[HEALTHY], self.counts[T2],
                self.counts[TODO], self.counts[CANT], len(TREES))
        self.assertEqual(got, want,
                         f"plan 的统计 {got} 与 TREES 实际 {want} 不一致（改完记得同步三处）")

    def test_p2_trees_stats_block_matches(self):
        m = re.search(r"## 状态统计(.+?)$", self.trees, re.S)
        self.assertIsNotNone(m, "p2-trees.md 缺「状态统计」——记得重跑 tools.p2_trees")
        block = m.group(1)
        for status in (DONE, HEALTHY, T2, TODO, CANT):
            want = self.counts.get(status, 0)
            row = re.search(rf"\| {re.escape(status)} \| (\d+) \|", block)
            self.assertIsNotNone(row, f"p2-trees.md 状态表缺 {status}")
            self.assertEqual(int(row.group(1)), want,
                             f"p2-trees.md 里 {status} = {row.group(1)}，实际 {want}（重跑 tools.p2_trees）")

    def test_every_healthy_tree_is_documented(self):
        missing = []
        for t in TREES:
            if t["status"] != HEALTHY:
                continue
            line = f"{CLASSES[t['cls']]} · {t['tree']}"
            if line not in self.healthy:
                missing.append(line)
        self.assertEqual(missing, [], f"p2-healthy.md 缺这几个系的结论：{missing}")

    def test_every_changed_tree_appears_in_the_plan(self):
        missing = [f"{CLASSES[t['cls']]} · {t['tree']}" for t in TREES
                   if t["status"] in (DONE, CANT) and t["tree"] not in self.plan]
        self.assertEqual(missing, [], f"p2-balance-plan.md 缺这些系的处置记录：{missing}")

    def test_progress_table_covers_all_21_trees(self):
        # 总任务契约要求：进度表 21 行全部有结论
        sec = self.plan.split("## 5 · 进度总表")[1].split("### 每一轮的固定流程")[0]
        rows = [l for l in sec.splitlines() if re.match(r"^\| \d+ \|", l)]
        self.assertEqual(len(rows), 21, f"§5 进度表应该有 21 行，现在 {len(rows)} 行")
        for r in rows:
            self.assertRegex(r, r"\| (✅|⚪|⚠️|❌|⬜)",
                             f"这一行没有判定结论：{r[:60]}")

    def test_changelog_is_newer_than_every_patch(self):
        log = DOCS / "changelog.md"
        self.assertTrue(log.exists(), "缺 docs/changelog.md —— 跑 tools.build")
        newest = max([p.stat().st_mtime for p in (ROOT / "patches").glob("*.py")]
                     + [(ROOT / "mod" / "data" / "global" / "excel" / "Skills.txt").stat().st_mtime])
        self.assertGreaterEqual(log.stat().st_mtime, newest,
                                "changelog.md 比补丁旧了 —— 改完补丁要重跑 tools.build")

    def test_areas_report_exists_and_is_fresh(self):
        # 「区域平均系数」这类数字曾经只写在文档里、算不回去 —— 现在必须有工具产物
        areas = DOCS / "p2-areas.md"
        self.assertTrue(areas.exists(), "缺 docs/p2-areas.md —— 跑 tools.p2_areas")
        text = areas.read_text(encoding="utf-8")
        self.assertTrue("tools.p2_areas" in text or "tools/p2_areas" in text,
                        "p2-areas.md 应注明它由 tools/p2_areas.py 生成")
        for f in ("Skills.txt", "MonStats.txt"):
            src = ROOT / "mod" / "data" / "global" / "excel" / f
            if src.exists():
                self.assertGreaterEqual(areas.stat().st_mtime, src.stat().st_mtime,
                                        f"p2-areas.md 比 mod/{f} 旧了 —— 重跑 tools.all")

    def test_audit_is_newer_than_mod(self):
        audit = DOCS / "p2-audit.md"
        self.assertTrue(audit.exists(), "缺 docs/p2-audit.md —— 跑 tools.p2_audit")
        for f in ("Skills.txt", "MonStats.txt", "TreasureClassEx.txt", "CubeMain.txt"):
            src = ROOT / "mod" / "data" / "global" / "excel" / f
            if src.exists():
                self.assertGreaterEqual(audit.stat().st_mtime, src.stat().st_mtime,
                                        f"p2-audit.md 比 mod/{f} 旧了 —— 重跑 tools.p2_audit")


if __name__ == "__main__":
    unittest.main()
