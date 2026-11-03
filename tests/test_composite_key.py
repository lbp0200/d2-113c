"""复合主键（`hireling.txt`）。

`hireling.txt` 单看任何一列都不唯一：每行是「佣兵 × 子类型 × 编号 × 版本 × 难度 × 等级断点」。
第一版用 `Id` 当主键，`tools.validate` 直接报了 180 个"重复"错误 —— 这个测试锁住修正。
"""

import tempfile
import unittest
from pathlib import Path

from tools.d2patch import COMPOSITE_KEYS, Ctx, eq, patch, row_key, use
from tools.validate import validate  # noqa: F401  （存在性检查即可）

FIXTURE = (
    "Hireling\tSubType\tVersion\tId\tClass\tAct\tDifficulty\tLevel\tGold\tHP\t*eol\r\n"
    "Eastern Sorceror\tFire-Hell\t100\t21\t271\t3\t3\t61\t21000\t574\t0\r\n"
    "Eastern Sorceror\tCold-Hell\t100\t22\t271\t3\t3\t61\t21000\t574\t0\r\n"
    "Eastern Sorceror\tFire-Hell\t100\t21\t271\t3\t3\t79\t21000\t863\t0\r\n"
    "Eastern Sorceror\tFire-Hell\t0\t21\t271\t3\t3\t61\t21000\t574\t0\r\n"
)


class CompositeKey(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.excel = root / "vanilla" / "data" / "global" / "excel"
        self.excel.mkdir(parents=True)
        (self.excel / "hireling.txt").write_bytes(FIXTURE.encode("latin-1"))
        self.ctx = Ctx(vanilla=root / "vanilla", out=root / "mod")
        use(self.ctx)
        self.tf = self.ctx.load("hireling.txt")

    def tearDown(self):
        self.tmp.cleanup()

    def test_registered(self):
        self.assertIn("hireling.txt", COMPOSITE_KEYS)
        self.assertIn("Version", COMPOSITE_KEYS["hireling.txt"])

    def test_keys_are_unique_in_fixture(self):
        keys = [row_key(self.tf, r, "hireling.txt") for r in self.tf.rows if r and r[0]]
        self.assertEqual(len(keys), len(set(keys)), f"重复键：{keys}")

    def test_version_distinguishes_classic_from_expansion(self):
        a = row_key(self.tf, self.tf.rows[0], "hireling.txt")
        d = row_key(self.tf, self.tf.rows[3], "hireling.txt")
        self.assertNotEqual(a, d, "Version 0 和 100 应该是不同的行")

    def test_level_bracket_distinguishes_rows(self):
        a = row_key(self.tf, self.tf.rows[0], "hireling.txt")
        c = row_key(self.tf, self.tf.rows[2], "hireling.txt")
        self.assertNotEqual(a, c, "不同 Level 断点应该是不同的行")

    def test_patch_filters_on_version(self):
        # 只改资料片（Version=100）的地狱档，不能连经典行一起改
        patch("hireling.txt", why="t").where_cols(
            [("Version", eq("100")), ("Difficulty", eq("3"))]
        ).set("Gold", 12000)
        rows = [r for r in self.ctx.load("hireling.txt").rows if r and r[0]]
        self.assertEqual(len([r for r in rows if r[10 - 2] == "12000"]), 3)  # 3 行资料片
        self.assertEqual(rows[3][10 - 2], "21000", "Version=0 的行不该被改")


if __name__ == "__main__":
    unittest.main()
