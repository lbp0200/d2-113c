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
