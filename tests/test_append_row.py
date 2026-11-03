"""`patch(...).append_row(...)` 的行为。

新增 cube 配方 / 新增 TC 行都依赖它，写错一个列名就会静默生产一张游戏读不了的表，
所以把边界钉死。
"""

import tempfile
import unittest
from pathlib import Path

from tools.d2patch import Ctx, patch, use


class AppendRow(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.excel = self.root / "vanilla" / "data" / "global" / "excel"
        self.excel.mkdir(parents=True)
        (self.excel / "cubemain.txt").write_bytes(
            b"description\tenabled\tversion\tmod 1\t*eol\r\n"
            b"Recipe A\t1\t100\tlifesteal\t0\r\n"
        )
        self.ctx = Ctx(vanilla=self.root / "vanilla", out=self.root / "mod")
        use(self.ctx)

    def tearDown(self):
        self.tmp.cleanup()

    def test_appends_one_row(self):
        patch("cubemain.txt", why="t").append_row(
            {"description": "Recipe B", "enabled": 1, "version": 100, "mod 1": "pierce-fire"}
        )
        tf = self.ctx.load("cubemain.txt")
        self.assertEqual(len(tf.rows), 2)
        self.assertEqual(tf.rows[1][0], "Recipe B")
        self.assertEqual(tf.rows[1][3], "pierce-fire")

    def test_fills_eol_default(self):
        patch("cubemain.txt", why="t").append_row({"description": "Recipe B", "enabled": 1})
        tf = self.ctx.load("cubemain.txt")
        self.assertEqual(tf.rows[1][4], "0")

    def test_row_width_matches_header(self):
        patch("cubemain.txt", why="t").append_row({"description": "Recipe B", "enabled": 1})
        tf = self.ctx.load("cubemain.txt")
        self.assertEqual(len(tf.rows[1]), len(tf.header))

    def test_unknown_column_is_an_error(self):
        # 不做"猜列名"：写错列必须炸，而不是静默丢数据
        with self.assertRaises(SystemExit):
            patch("cubemain.txt", why="t").append_row({"description": "B", "no such column": 1})

    def test_is_idempotent(self):
        row = {"description": "Recipe B", "enabled": 1, "version": 100}
        patch("cubemain.txt", why="t").append_row(row)
        patch("cubemain.txt", why="t").append_row(row)
        self.assertEqual(len(self.ctx.load("cubemain.txt").rows), 2)

    def test_records_a_change(self):
        patch("cubemain.txt", why="为测试加的配方").append_row(
            {"description": "Recipe B", "enabled": 1}
        )
        keys = [c.row for c in self.ctx.changes]
        self.assertIn("Recipe B", keys)
        self.assertTrue(any("为测试加的配方" in c.why for c in self.ctx.changes))


if __name__ == "__main__":
    unittest.main()
