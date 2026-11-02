import tempfile
import unittest
from pathlib import Path

from tools import d2patch
from tools.d2patch import Ctx, gt, patch, use


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.excel = self.root / "vanilla" / "data" / "global" / "excel"
        self.excel.mkdir(parents=True)
        (self.excel / "monstats.txt").write_bytes(
            b"Id\tResFi(H)\tMinHP\r\n"
            b"skeleton1\t110\t10\r\n"
            b"zombie\t0\t20\r\n"
            b"fallen\t130\t30\r\n"
        )
        (self.excel / "runes.txt").write_bytes(b"Name\tserver\r\nEnigma\t1\r\n")
        self.ctx = Ctx(vanilla=self.root / "vanilla", out=self.root / "mod")
        use(self.ctx)

    def tearDown(self):
        use(None)
        self.tmp.cleanup()


class TestOps(Base):
    def test_set_all(self):
        patch("runes.txt", why="单机").all().set("server", "0")
        self.assertEqual(
            self.ctx.files["runes.txt"].dumps(), b"Name\tserver\r\nEnigma\t0\r\n"
        )
        self.assertEqual(len(self.ctx.changes), 1)

    def test_clamp_where(self):
        patch("monstats.txt", why="抗性封顶").where("ResFi(H)", gt(100)).clamp("ResFi(H)", hi=100)
        out = self.ctx.files["monstats.txt"].dumps()
        self.assertIn(b"skeleton1\t100\t10", out)
        self.assertIn(b"zombie\t0\t20", out)
        self.assertIn(b"fallen\t100\t30", out)

    def test_mul_and_add(self):
        patch("monstats.txt").all().mul("MinHP", 2).add("MinHP", 1)
        out = self.ctx.files["monstats.txt"].dumps()
        self.assertIn(b"skeleton1\t110\t21", out)
        self.assertIn(b"fallen\t130\t61", out)

    def test_selector_no_match_warns(self):
        patch("monstats.txt", why="x").where("MinHP", gt(9999)).set("MinHP", 1)
        self.assertTrue(any("没匹配到任何行" in w for w in self.ctx.warnings))

    def test_changed_files_only_outputs_touched(self):
        patch("runes.txt").all().set("server", "0")
        self.assertEqual(list(self.ctx.changed_files()), ["runes.txt"])

    def test_unchanged_value_records_nothing(self):
        patch("monstats.txt").all().set("MinHP", lambda old: old)
        self.assertEqual(self.ctx.changes, [])
        self.assertEqual(self.ctx.changed_files(), {})

    def test_soft_skips_missing_column(self):
        patch("runes.txt", why="拼错了", soft=True).all().set("ladderOnly", "0")
        self.assertEqual(len(self.ctx.skipped), 1)
        self.assertEqual(self.ctx.changed_files(), {})

    def test_hard_fails_on_missing_column(self):
        with self.assertRaises(SystemExit):
            patch("runes.txt", why="拼错了").all().set("ladderOnly", "0")


class TestPredicates(unittest.TestCase):
    """谓词曾经在重构里丢掉 `return f` —— 静默返回 None 会让 where() 静默失效。"""

    def test_all_predicates_return_callables(self):
        cases = [
            (d2patch.gt(100), "110", True), (d2patch.gt(100), "100", False),
            (d2patch.ge(100), "100", True),
            (d2patch.lt(100), "99", True), (d2patch.lt(100), "100", False),
            (d2patch.le(100), "100", True),
            (d2patch.num_eq(1), "1", True), (d2patch.num_eq(1), "2", False),
            (d2patch.eq("x"), "x", True), (d2patch.ne("x"), "y", True),
            (d2patch.one_of("a", "b"), "b", True), (d2patch.one_of("a"), "c", False),
            (d2patch.matches(r"^skeleton"), "skeleton1", True),
            (d2patch.blank(), "", True), (d2patch.nonblank(), " ", False),
            (d2patch.isnum(), "1.5", True), (d2patch.not_(d2patch.blank()), "x", True),
        ]
        for pred, val, want in cases:
            self.assertTrue(callable(pred), f"{pred} 不是可调用对象")
            self.assertIs(pred(val), want, f"{pred}('{val}')")

    def test_predicate_on_non_numeric_is_false(self):
        for pred in (d2patch.gt(1), d2patch.lt(1), d2patch.le(1), d2patch.ge(1)):
            self.assertFalse(pred(""), "空单元格不应被当成数字")
            self.assertFalse(pred("-"))


if __name__ == "__main__":
    unittest.main()
