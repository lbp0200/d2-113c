"""符文之语解析（`tools/p3_runewords.py`）的完整性。

跨表结论全部依赖三件事：槽位祖先链对不对、符文需求有没有读到、档位表是不是真在比同一批东西。
"""

import unittest

from tools.p3_items import load_props
from tools.p3_runewords import load_ancestry, load_rune_reqs, load_runewords


class Ancestry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.anc = load_ancestry()

    def test_sword_is_a_melee_weapon(self):
        self.assertIn("mele", self.anc["swor"])
        self.assertIn("weap", self.anc["swor"])

    def test_hammer_is_blunt_melee(self):
        self.assertIn("blun", self.anc["hamm"])
        self.assertIn("mele", self.anc["hamm"])

    def test_armor_families(self):
        for code in ("tors", "helm", "shie"):
            self.assertIn("armo", self.anc[code], f"{code} 应该属于 armo")

    def test_circlet_is_a_helm(self):
        self.assertIn("helm", self.anc["circ"])

    def test_ring_is_not_armor(self):
        self.assertNotIn("armo", self.anc["ring"])


class Runes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reqs = load_rune_reqs()

    def test_all_33_runes_present(self):
        self.assertEqual(len(self.reqs), 33)
        self.assertIn("r01", self.reqs)
        self.assertIn("r33", self.reqs)

    def test_deeper_runes_need_more_level(self):
        self.assertLess(self.reqs["r01"], self.reqs["r16"])
        self.assertLess(self.reqs["r16"], self.reqs["r31"])


class Runewords(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        props, _ = load_props()
        cls.rws = load_runewords(props)
        cls.by_name = {r["name"]: r for r in cls.rws}

    def test_reasonable_count(self):
        self.assertGreater(len(self.rws), 70, "D2 1.13 的符文之语数量应该在 70+")

    def test_spirit_exists_and_is_strong_for_its_level(self):
        spirit = self.by_name.get("Spirit")
        self.assertIsNotNone(spirit, "没解析到 Spirit")
        self.assertEqual(len(spirit["runes"]), 4)
        self.assertEqual(spirit["req"], 25, "Spirit 的需求应为 25（符文 r07 的需求）")
        self.assertTrue(any("skills" in s for s in ["".join(spirit["stats"])]))

    def test_req_is_max_of_its_runes(self):
        reqs = load_rune_reqs()
        for rw in self.rws:
            self.assertEqual(rw["req"], max(reqs.get(r, 0) for r in rw["runes"]))

    def test_itypes_parsed(self):
        # 至少大部分 RW 要有底材限制，否则槽位兼容判断会全错
        with_types = [r for r in self.rws if r["itypes"]]
        self.assertGreaterEqual(len(with_types), len(self.rws) * 0.9)


if __name__ == "__main__":
    unittest.main()
