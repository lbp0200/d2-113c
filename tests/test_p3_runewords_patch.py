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

    def test_venom_is_poison_weapon(self):
        tf = self.tf
        row = next(r for r in tf.rows
                   if r and tf.get(r, tf.need("Rune Name")) == "Venom")
        codes = [tf.get(row, tf.need(f"T1Code{k}")) for k in range(1, 8)]
        self.assertIn("pierce-pois", codes, "毒液应该有毒穿透")
        self.assertIn("pois-len", codes, "毒液应该有缩短毒持续时间")
        # 不许有 extra-pois（那会直接超过死亡之网，违反 E2）
        self.assertNotIn("extra-pois", codes, "毒液不能加毒系技能伤害（会造新 BiS）")
        # 两个凑数的充能技能应该被换掉
        self.assertNotIn("charged", codes, "凑数的充能技能应已替换")

    def test_venom_pois_len_is_negative(self):
        tf = self.tf
        row = next(r for r in tf.rows
                   if r and tf.get(r, tf.need("Rune Name")) == "Venom")
        for k in range(1, 8):
            if tf.get(row, tf.need(f"T1Code{k}")) == "pois-len":
                self.assertEqual(float(tf.get(row, tf.need(f"T1Max{k}"))), -50.0,
                                 "毒持续时间要缩短（负值）")
                return
        self.fail("找不到 pois-len")

    def test_nadir_has_no_negatives(self):
        tf = self.tf
        row = next(r for r in tf.rows
                   if r and tf.get(r, tf.need("Rune Name")) == "Nadir")
        for k in range(1, 8):
            code = tf.get(row, tf.need(f"T1Code{k}"))
            if not code:
                continue
            self.assertNotIn(code, ("light", "gold%"), f"天底不该再有负面属性 {code}")
            v = float(tf.get(row, tf.need(f"T1Max{k}")) or 0)
            self.assertGreaterEqual(v, 0, f"天底的 {code} 不该是负数")

    def test_other_properties_untouched(self):
        # 只换第一条，其余 5 条保持原样（等价交换）
        tf = self.tf
        for k, want in ((2, "enr"), (3, "vit"), (4, "red-mag"), (5, "mana"), (6, "ac%")):
            self.assertEqual(tf.get(self.row, tf.need(f"T1Code{k}")), want,
                             f"T1Code{k} 不该被改动")


if __name__ == "__main__":
    unittest.main()
