"""中间层降抗：`Radiance` 必须真的带上信念 L3。

这条改动是"把一个废物属性换成功能属性"，一旦被后续补丁覆盖或写错字段，
冷门职业的元素线又会掉回 64% —— 而且工具不会报错，所以用测试钉住。
"""

import unittest
from pathlib import Path

from tools.d2patch import Ctx

ROOT = Path(__file__).resolve().parent.parent


class RadianceConviction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mod = ROOT / "mod" / "data" / "global" / "excel" / "runes.txt"
        if not mod.exists():
            raise unittest.SkipTest("mod/ 还没构建，先跑 python3 -m tools.build")
        cls.tf = Ctx(vanilla=ROOT / "vanilla", out=ROOT / "mod",
                     overlay=ROOT / "mod").load("runes.txt")
        cls.row = next((r for r in cls.tf.rows
                        if r and cls.tf.get(r, cls.tf.need("Rune Name")) == "Radiance"), None)

    def test_row_exists(self):
        self.assertIsNotNone(self.row, "找不到 Radiance")

    def test_slot1_is_conviction_aura(self):
        tf = self.tf
        self.assertEqual(tf.get(self.row, tf.need("T1Code1")), "aura")
        self.assertEqual(tf.get(self.row, tf.need("T1Param1")), "Conviction")
        self.assertEqual(tf.get(self.row, tf.need("T1Min1")), "3")
        self.assertEqual(tf.get(self.row, tf.need("T1Max1")), "3")

    def test_light_radius_is_gone(self):
        tf = self.tf
        codes = [tf.get(self.row, tf.need(f"T1Code{k}")) for k in range(1, 8)]
        self.assertNotIn("light", codes, "光环半径应该已经被换掉了")

    def test_other_properties_untouched(self):
        # 只换第一条，其余 5 条保持原样（等价交换）
        tf = self.tf
        for k, want in ((2, "enr"), (3, "vit"), (4, "red-mag"), (5, "mana"), (6, "ac%")):
            self.assertEqual(tf.get(self.row, tf.need(f"T1Code{k}")), want,
                             f"T1Code{k} 不该被改动")


if __name__ == "__main__":
    unittest.main()
