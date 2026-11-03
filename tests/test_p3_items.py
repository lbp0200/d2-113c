"""装备体检表（`tools/p3_items.py`）的规则。

这里钉死的是"什么算死属性"和"哪些东西不该被判定" —— 这两件事一旦搞错，
整张候选表就会像第一版那样把 Mara's Kaleidoscope 判成垃圾。
"""

import unittest

from tools.p3_items import SKIP_SLOTS, collect, dead_stats, strong_hits


class ItemCollection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items, cls.skipped = collect()
        cls.by_name = {it["name"]: it for it in cls.items}

    def test_quest_items_are_excluded(self):
        for q in ("Staff of Kings", "Horadric Staff", "KhalimFlail",
                  "SuperKhalimFlail", "Hell Forge Hammer"):
            self.assertNotIn(q, self.by_name, f"任务物品 {q} 不该进表")
        self.assertEqual(len(self.skipped), 5)

    def test_charms_are_in_skip_slots(self):
        # 护身符（护身符不和任何装备抢槽位）必须在 SKIP_SLOTS 里
        charm_slots = {it["slot"].lower() for it in self.items if "cha" in it["slot"].lower()}
        self.assertTrue(charm_slots, "数据里应该能找到护身符")
        self.assertTrue(charm_slots <= SKIP_SLOTS, f"这些护身符槽位没被排除：{charm_slots - SKIP_SLOTS}")

    def test_eff_dmg_only_on_weapons(self):
        for it in self.items:
            if "eff_dmg" in it["stats"]:
                self.assertEqual(it["kind"], "weapon",
                                 f"{it['name']} 不是武器却算了有效伤害")
            if "eff_def" in it["stats"]:
                self.assertEqual(it["kind"], "armor",
                                 f"{it['name']} 不是护甲却算了有效防御")


class DeadStats(unittest.TestCase):
    """「死属性」这一类**做错过**，这里的测试锁的是更正后的结论。

    教训：`dmg%`（`item_maxdamage_percent`）和元素附加伤害是**全局**的，
    写在护甲上照样生效 —— Fortitude（衣服 +300% ED）、Steelrend（手套 +60% ED）、
    以及可以镶在任意部位的 ED 珠宝都是反例。第一版把它们判成死属性，列了 43 件，是错的。
    """

    @staticmethod
    def item(kind: str, slot: str, **stats) -> dict:
        return {"name": "X", "kind": kind, "slot": slot, "stats": dict(stats)}

    def test_ed_on_helm_is_not_dead(self):
        # Fortitude 的 +300% ED 就在衣服上，照样生效
        self.assertEqual(dead_stats(self.item("armor", "helm", ed=30)), [])

    def test_ed_on_gloves_is_not_dead(self):
        # Steelrend 的招牌就是手套上的 +30~60% ED
        self.assertEqual(dead_stats(self.item("armor", "glov", ed=60)), [])

    def test_elemental_damage_off_weapon_is_not_dead(self):
        # 离手附加伤害同样生效
        self.assertEqual(dead_stats(self.item("armor", "boot", elem_dmg=6)), [])

    def test_ed_on_shield_is_not_dead(self):
        # 圣骑士 Smite 用盾牌伤害
        self.assertEqual(dead_stats(self.item("armor", "shie", ed=30)), [])

    def test_added_physical_damage_anywhere_is_alive(self):
        self.assertEqual(dead_stats(self.item("misc", "ring", add_dmg=15)), [])

    def test_only_weapon_ac_percent_is_flagged(self):
        # 唯一保留的那条「存疑」：武器没有防御值，所以 ac% 可能白给
        self.assertEqual(dead_stats(self.item("weapon", "staf", ed_def=50)), ["ed_def"])
        self.assertEqual(dead_stats(self.item("armor", "tors", ed_def=50)), [])


class StrongBar(unittest.TestCase):
    def test_skills_always_count(self):
        it = {"stats": {"skills": 1}}
        self.assertTrue(strong_hits(it))

    def test_magic_find_counts_as_identity(self):
        it = {"stats": {"item_magicbonus": 40}}
        self.assertTrue(strong_hits(it))

    def test_light_radius_never_counts(self):
        it = {"stats": {"item_lightradius": 5, "item_goldbonus": 20}}
        self.assertFalse(strong_hits(it))

    def test_thresholds_are_low_but_not_zero(self):
        self.assertFalse(strong_hits({"stats": {"ed": 79}}))
        self.assertTrue(strong_hits({"stats": {"ed": 80}}))


if __name__ == "__main__":
    unittest.main()
