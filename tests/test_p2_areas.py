"""区域元素适配度（`tools/p2_areas.py`）的规则与数字。

这份数据曾经只存在于文档里、而且算错了（把"穿透"当成能破免疫，得出
"归零区域 6→0"的结论）。这里把规则和关键数字钉死，防止再错。
"""

import unittest
from pathlib import Path
from statistics import mean

from tools.d2patch import Ctx
from tools.p1_immunity import areas, monster_resists
from tools.p2_areas import area_stats, factor, point_mult

ROOT = Path(__file__).resolve().parent.parent


class ImmunityRule(unittest.TestCase):
    """`passive_*_pierce` 破不了免疫 —— 这是全部结论的前提。"""

    def test_pierce_never_breaks_immunity_in_strict_rule(self):
        for res in (100, 110, 145):
            for pierce in (0, 25, 115, 9999):
                self.assertEqual(factor(res, pierce, "strict"), 0.0,
                                 f"抗性 {res} 穿透 {pierce} 在严格规则下必须还是 0")

    def test_pierce_applies_below_immunity(self):
        self.assertAlmostEqual(factor(75, 25), 0.50, places=6)
        self.assertAlmostEqual(factor(90, 25), 0.35, places=6)

    def test_resistance_floor_is_minus_100(self):
        self.assertAlmostEqual(factor(0, 999), 2.0, places=6)

    def test_point_mult_includes_damage_bonus(self):
        # 电系修后：+200% 伤害、−25% 穿透
        self.assertAlmostEqual(point_mult(200, 25, 0), 3.75, places=2)
        self.assertAlmostEqual(point_mult(200, 25, 90), 1.05, places=2)

    def test_breaking_rule_is_a_counterfactual(self):
        # 反事实假设下才会变成"能打"，默认规则不这样算
        self.assertGreater(factor(100, 9999, "breaking"), 0.0)
        self.assertEqual(factor(100, 9999, "strict"), 0.0)


class VanillaEnvironment(unittest.TestCase):
    """裸抗性的环境系数（与补丁无关：封顶 110→100 前后都还是免疫）。"""

    @classmethod
    def setUpClass(cls):
        ctx = Ctx(vanilla=ROOT / "vanilla", out=ROOT / "mod")
        cls.res = monster_resists(ctx.load("monstats.txt"))
        cls.ars = areas(ctx.load("levels.txt"))

    def _avg(self, elem: str) -> tuple[float, int, int]:
        """-> (区域平均系数, **归零区域数**, 区域总数)。"""
        means = []
        for _a, _n, _l, ids in self.ars:
            s = area_stats(ids, self.res, elem, 0, 0, "strict")
            if s:
                means.append(s[0])          # s[1] 是"打不动的怪物个数"，不是区域数
        return mean(means), sum(1 for m in means if m == 0), len(means)

    def test_known_coefficients(self):
        expected = {"火": 0.61, "冰": 0.57, "电": 0.61, "毒": 0.61, "物理": 0.63, "魔法": 0.90}
        for elem, want in expected.items():
            avg, _zero, _n = self._avg(elem)
            self.assertAlmostEqual(avg, want, delta=0.01, msg=f"{elem} 的环境系数应约 {want}")

    def test_known_zero_area_counts(self):
        # 这些是被独立核对过的数字：电 6 个归零区域，魔法/物理/毒 一个都没有
        expected = {"火": 2, "冰": 3, "电": 6, "毒": 0, "物理": 0, "魔法": 0}
        for elem, want in expected.items():
            _avg, zero, _n = self._avg(elem)
            self.assertEqual(zero, want, f"{elem} 的归零区域数应为 {want}")

    def test_magic_has_no_zero_areas(self):
        # 这是"锤子骑为什么强"的全部依据：魔法伤害在任何区域都不归零
        _avg, zero, n = self._avg("魔法")
        self.assertEqual(zero, 0)
        self.assertGreater(n, 100)


if __name__ == "__main__":
    unittest.main()
