"""套装体检（`tools/p3_sets.py`）的数据完整性。

套装的价值可以来自「单件」也可以来自「凑到 N 件的加成」，所以这里钉的是
**解析有没有漏**：件数对不对、2/3 件加成有没有读进来、填充型加成能不能识别。
"""

import unittest
from collections import defaultdict

from tools.p3_items import load_bases, load_props
from tools.p3_sets import build_report, load_pieces, load_sets, partial_hits


class SetParsing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.props, _ = load_props()
        cls.bases = load_bases()
        cls.sets = load_sets(cls.props)
        cls.pieces = load_pieces(cls.props, cls.bases)
        cls.by_set = defaultdict(list)
        for p in cls.pieces:
            cls.by_set[p["set"]].append(p)
        cls.md = build_report(cls.sets, cls.pieces)

    def test_all_sets_have_pieces(self):
        missing = [n for n in self.sets if not self.by_set.get(n)]
        self.assertEqual(missing, [], f"这些套装没有解析到任何件：{missing}")

    def test_piece_counts_are_plausible(self):
        for name, plist in self.by_set.items():
            self.assertGreaterEqual(len(plist), 2, f"{name} 只有 {len(plist)} 件？")
            self.assertLessEqual(len(plist), 6, f"{name} 有 {len(plist)} 件，D2 套装最多 6 件")

    def test_two_piece_bonus_parsed_somewhere(self):
        # 至少多数套装应该有 2 件加成；一个都没有说明解析坏了
        with_bonus = [n for n, st in self.sets.items() if st["shown"].get(2)]
        self.assertGreaterEqual(len(with_bonus), 25,
                                f"只有 {len(with_bonus)} 套解析出 2 件加成，疑似解析失败")

    def test_filler_is_not_counted_as_real(self):
        # +50 防御 / +75 命中 这类纯数值填充，不能算"凑套有收益"
        self.assertEqual(partial_hits({"def": 200, "ar": 150, "ac": 100}), [])
        self.assertEqual(partial_hits({"lifesteal": 8}), ["lifesteal=8"])
        self.assertEqual(partial_hits({"res-fire": 30}), ["res-fire=30"])

    def test_below_threshold_is_not_real(self):
        self.assertEqual(partial_hits({"hp": 29}), [])
        self.assertEqual(partial_hits({"hp": 30}), ["hp=30"])

    def test_report_contains_every_set(self):
        for name in self.sets:
            self.assertIn(name, self.md, f"报告里缺套装 {name}")


if __name__ == "__main__":
    unittest.main()
