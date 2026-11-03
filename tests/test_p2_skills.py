"""钉住「掌握审计」用到的公式求值。

这些公式是 `docs/p2-balance-plan.md` 与 `patches/p2_skills.py` 里所有数值的依据，
算错了整份平衡报告就全错，所以值得单独测。
"""

import unittest

from tools.p1_skills import _eval_calc


class TestEvalCalc(unittest.TestCase):
    def test_ln12_fire_mastery_vanilla(self):
        # 原版火掌握：Param1=30, Param2=7 → L20 = 30 + 7*19 = 163
        self.assertEqual(_eval_calc("ln12", ["30", "7"], 20), (30.0, 163.0))

    def test_ln12_fire_mastery_patched(self):
        # A2 之后：Param1=24, Param2=4 → L20 = 24 + 4*19 = 100
        self.assertEqual(_eval_calc("ln12", ["24", "4"], 20), (24.0, 100.0))

    def test_ln34_needs_param3_and_4(self):
        # A2 的火穿透：Param3=7, Param4=2 → L20 = 7 + 2*19 = 45
        params = ["24", "4", "7", "2"]
        self.assertEqual(_eval_calc("ln34", params, 20), (7.0, 45.0))

    def test_conviction_matches_known_value(self):
        # 信念：P3=30 P4=5 → L20 = 30 + 5*19 = 125（与原版 -125% 一致）
        params = ["20", "0", "30", "5", "40", "100"]
        self.assertEqual(_eval_calc("-min(ln34,150)", params, 20), (-30.0, -125.0))

    def test_lower_resist_dm56(self):
        # 降抗诅咒：P5=25 P6=70
        params = ["7", "1", "500", "50", "25", "70"]
        self.assertEqual(_eval_calc("-dm56", params, 20), (-25.0, -70.0))

    def test_quoted_formula_is_stripped(self):
        # txt 里含逗号的公式会被双引号包住（CSV 风格），必须能吃掉引号
        params = ["20", "0", "30", "5", "40", "100"]
        self.assertEqual(_eval_calc('"-min(ln34,150)"', params, 20), (-30.0, -125.0))

    def test_unknown_formula_returns_none(self):
        # 不认识的公式必须返回 None（标 "—"），不能猜一个数字出来
        self.assertIsNone(_eval_calc("whatever", ["1"], 20))


class TestMasteryMultiplier(unittest.TestCase):
    """倍率公式 = (1+伤害%) × (1-最终抗性/100)，下限 -100%。"""

    @staticmethod
    def mult(dmg: float, pierce: float, res: float) -> float:
        final = max(-100.0, res - pierce)
        return (1 + dmg / 100) * (1 - final / 100)

    def test_fire_after_a2(self):
        # A2 后：伤害 +100、穿透 45
        self.assertAlmostEqual(self.mult(100, 45, 0), 2.90, places=2)
        self.assertAlmostEqual(self.mult(100, 45, 75), 1.40, places=2)
        self.assertAlmostEqual(self.mult(100, 45, 90), 1.10, places=2)

    def test_cold_baseline(self):
        # 冰掌握：无伤害加成、穿透 115
        self.assertAlmostEqual(self.mult(0, 115, 0), 2.00, places=2)
        self.assertAlmostEqual(self.mult(0, 115, 90), 1.25, places=2)

    def test_a2_ties_cold_at_75_res(self):
        # A2 的设计目标：75% 抗性处与冰系正好相等
        self.assertAlmostEqual(self.mult(100, 45, 75), self.mult(0, 115, 75), places=6)

    def test_resistance_floor(self):
        # 抗性下限 -100：穿透再多，倍率也不会超过 (1+伤害%)×2
        self.assertAlmostEqual(self.mult(0, 500, 0), 2.00, places=2)


if __name__ == "__main__":
    unittest.main()
