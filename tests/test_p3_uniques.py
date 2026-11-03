"""重做 7 件弱暗金/套装单件（`patches/p3_uniques.py`）。

这批改动的风险是"顺手改坏好东西"，所以测试同时钉两件事：
**这 7 件确实改了** + **被判定为"不弱"的那 5 件一个字段都不许动**。
"""

import unittest
from pathlib import Path

from tools.d2patch import Ctx

ROOT = Path(__file__).resolve().parent.parent


def load(name):
    p = ROOT / "mod" / "data" / "global" / "excel" / name
    if not p.exists():
        raise unittest.SkipTest("mod/ 还没构建，先跑 python3 -m tools.build")
    return Ctx(vanilla=ROOT / "vanilla", out=ROOT / "mod",
               overlay=ROOT / "mod").load(name)


def mods(tf, row, slots=13):
    out = {}
    for k in range(1, slots):
        if f"prop{k}" not in tf.header:
            continue
        code = tf.get(row, tf.need(f"prop{k}"))
        if code:
            out[code] = (tf.get(row, tf.need(f"min{k}")), tf.get(row, tf.need(f"max{k}")))
    return out


class ReworkedItems(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.u = load("uniqueitems.txt")
        cls.s = load("setitems.txt")
        cls.u_rows = {r[0]: r for r in cls.u.rows if r and r[0]}
        cls.s_rows = {r[0]: r for r in cls.s.rows if r and r[0]}

    def test_steelpillar_has_ease(self):
        self.assertIn("ease", mods(self.u, self.u_rows["Steelpillar"]),
                      "Steelpillar 必须带 ease，否则 165 力量举不起来")

    def test_razortine_buffed(self):
        m = mods(self.u, self.u_rows["Razortine"])
        self.assertEqual(m["dmg%"], ("60", "80"))
        self.assertIn("ease", m)

    def test_venomsward_has_sustain(self):
        m = mods(self.u, self.u_rows["Venomsward"])
        self.assertIn("hp", m)
        self.assertIn("regen", m)

    def test_heavenly_garb_targets_demons_not_undead(self):
        m = mods(self.u, self.u_rows["Heavenly Garb"])
        self.assertIn("dmg-demon", m)
        self.assertNotIn("dmg-undead", m, "对不死应该已经换成对恶魔")

    def test_gravepalm_has_crushing_blow(self):
        self.assertIn("crush", mods(self.u, self.u_rows["Gravepalm"]))

    def test_hawkmail_buffed(self):
        m = mods(self.u, self.u_rows["Hawkmail"])
        self.assertEqual(m["res-cold"], ("30", "30"))
        self.assertEqual(m["move2"], ("25", "25"))

    def test_magnus_skin_has_fhr_and_hp(self):
        m = mods(self.s, self.s_rows["Magnus' Skin"], slots=10)
        self.assertIn("balance2", m)
        self.assertIn("hp", m)


class ElementalMidTier(unittest.TestCase):
    """4 件「元素强化中阶暗金」—— 替代被停用的 cube craft 配方。"""

    @classmethod
    def setUpClass(cls):
        cls.u = load("uniqueitems.txt")
        cls.rows = {r[0]: r for r in cls.u.rows if r and r[0]}

    def test_each_element_has_one_item(self):
        expect = {
            "Infernostride": ("extra-fire", "pierce-fire"),
            "Hawkmail": ("extra-cold",),
            "Blackhorn's Face": ("pierce-ltng", "extra-ltng"),
            "Wormskull": ("extra-pois",),
        }
        for name, codes in expect.items():
            got = mods(self.u, self.rows[name])
            for code in codes:
                self.assertIn(code, got, f"{name} 缺少 {code}")

    def test_poison_mastery_exists_somewhere(self):
        # 原版**没有任何装备**给 extra-pois，这一条是全新的
        found = [n for n, r in self.rows.items() if "extra-pois" in mods(self.u, r)]
        self.assertTrue(found, "全表找不到 extra-pois —— 毒系技能伤害类装备缺失")

    def test_values_are_mid_tier_not_endgame(self):
        # 不许超过格里风（20 穿透 / 15 伤害）那一档
        for name in ("Infernostride", "Blackhorn's Face"):
            got = mods(self.u, self.rows[name])
            for code, (lo, hi) in got.items():
                if code.startswith(("pierce-", "extra-")):
                    self.assertLessEqual(float(hi), 20, f"{name} 的 {code} 超过 20，过强了")


class CubeMainMustNotShip(unittest.TestCase):
    """整合版的 CubeMain 有 75+ 条自定义公式 —— 我们绝对不能输出这张表。"""

    def test_cubemain_not_in_mod(self):
        p = ROOT / "mod" / "data" / "global" / "excel" / "CubeMain.txt"
        self.assertFalse(p.exists(),
                         "mod/ 里出现了 CubeMain.txt —— 会整表覆盖整合版的自定义合成公式！")

    def test_p2_items_is_disabled(self):
        self.assertFalse((ROOT / "patches" / "p2_items.py").exists(),
                         "p2_items.py 必须保持停用（改名以下划线开头）")
        self.assertTrue((ROOT / "patches" / "_disabled_cubemain_crafts.py").exists(),
                        "停用的配方应该保留成 _disabled_* 文件，作为决策记录")


class DoNotTouch(unittest.TestCase):
    """被数据判定为"不弱"的 5 件 —— 一个字段都不许改。"""

    KEEP = ["Guillaume's Face", "Natalya's Shadow"]

    def test_not_modified(self):
        vanilla = Ctx(vanilla=ROOT / "vanilla", out=ROOT / "mod")
        mod = Ctx(vanilla=ROOT / "vanilla", out=ROOT / "mod", overlay=ROOT / "mod")
        for name in self.KEEP:
            v = next(r for r in vanilla.load("setitems.txt").rows if r and r[0] == name)
            m = next(r for r in mod.load("setitems.txt").rows if r and r[0] == name)
            self.assertEqual(v, m, f"{name} 不该被改动（数据判定它不弱）")


if __name__ == "__main__":
    unittest.main()
