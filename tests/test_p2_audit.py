"""`tools/p2_audit.py` 的分类逻辑。

这个工具是「确认没有任何一处是削弱」这句话的唯一证据来源，
分类搞错（比如把下降当成上升）会让整份账目失效。
"""

import tempfile
import unittest
from pathlib import Path

from tools.p2_audit import as_num, audit, build_report

FILES = {
    "skills.txt": (
        "skill\tmana\tEMin\tParam1\t*eol\r\n"
        "A\t20\t10\t30\t0\r\n"
        "B\t10\t5\t7\t0\r\n"
    ),
    "skills_after.txt": (
        "skill\tmana\tEMin\tParam1\t*eol\r\n"
        "A\t16\t12\t24\t0\r\n"
        "C\t5\t5\t5\t0\r\n"
    ),
}


class Audit(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.vanilla = root / "vanilla" / "data" / "global" / "excel"
        self.mod = root / "mod" / "data" / "global" / "excel"
        self.vanilla.mkdir(parents=True)
        self.mod.mkdir(parents=True)
        (self.vanilla / "skills.txt").write_bytes(FILES["skills.txt"].encode("latin-1"))
        (self.mod / "skills.txt").write_bytes(FILES["skills_after.txt"].encode("latin-1"))
        self.rep = audit(root / "vanilla", root / "mod")["skills.txt"]

    def tearDown(self):
        self.tmp.cleanup()

    def test_counts_up_and_down(self):
        # A: mana 20→16（下降）、EMin 10→12（上升）、Param1 30→24（下降）
        # B 在 mod 里没有了（只是没写，不是"删除"——行被 C 取代）
        ups = {(k, c) for k, c, _a, _b in self.rep["up"]}
        downs = {(k, c) for k, c, _a, _b in self.rep["down"]}
        self.assertIn(("A", "EMin"), ups)
        self.assertIn(("A", "mana"), downs)
        self.assertIn(("A", "Param1"), downs)

    def test_added_row_detected(self):
        self.assertEqual(self.rep["added"], ["C"])

    def test_comment_columns_ignored(self):
        for bucket in ("up", "down", "set"):
            for _k, col, _a, _b in self.rep.get(bucket, []):
                self.assertFalse(col.startswith("*"), f"注释列不该被算成改动：{col}")

    def test_as_num(self):
        self.assertEqual(as_num("12"), 12.0)
        self.assertEqual(as_num(" 3 "), 3.0)
        self.assertIsNone(as_num(""))
        self.assertIsNone(as_num("abc"))

    def test_report_lists_every_decrease(self):
        md = build_report({"skills.txt": self.rep})
        self.assertIn("所有「数值下降」", md)
        self.assertIn("`A`", md)


if __name__ == "__main__":
    unittest.main()
