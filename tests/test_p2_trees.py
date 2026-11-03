"""钉住 21 系体检表的人工元数据。

技能树归属、伤害类型、场景胜场都是手写的常量 —— 手写就会打错字。
打错字不会报错，只会让某一系"少了几个技能"，体检结论跟着错。
所以这里对着真实的 `skills.txt` 校验。
"""

import unittest
from pathlib import Path

from tools.d2patch import Ctx
from tools.p2_trees import CANT, DONE, HEALTHY, SCENARIOS, T2, TODO, TREES


class TreeMetadata(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parent.parent
        cls.ctx = Ctx(vanilla=root / "vanilla", out=root / "mod")
        tf = cls.ctx.load("skills.txt")
        cls.owner = {}
        for row in tf.rows:
            if row and row[0]:
                cls.owner[row[0].strip()] = tf.get(row, tf.need("charclass")).strip().lower()

    def test_exactly_21_trees(self):
        self.assertEqual(len(TREES), 21)

    def test_three_trees_per_class(self):
        from collections import Counter
        c = Counter(t["cls"] for t in TREES)
        self.assertEqual(set(c.values()), {3}, f"每个职业应该正好 3 个系：{dict(c)}")
        self.assertEqual(len(c), 7, f"应该是 7 个职业：{dict(c)}")

    def test_every_skill_exists_and_belongs_to_the_class(self):
        for t in TREES:
            for s in t["skills"]:
                self.assertIn(s, self.owner, f"{t['cls']}·{t['tree']} 里的 `{s}` 在 skills.txt 里不存在")
                self.assertEqual(self.owner[s], t["cls"],
                                 f"`{s}` 属于 {self.owner[s]}，不该放在 {t['cls']}·{t['tree']}")

    def test_no_skill_listed_twice(self):
        seen = {}
        for t in TREES:
            for s in t["skills"]:
                key = (t["cls"], s)
                self.assertNotIn(key, seen, f"`{s}` 同时出现在 {seen.get(key)} 和新位置")
                seen[key] = f"{t['cls']}·{t['tree']}"

    def test_wins_are_known_scenarios(self):
        for t in TREES:
            for w in t["wins"]:
                self.assertIn(w, SCENARIOS, f"{t['tree']} 用了未知场景 {w}")

    def test_status_is_known(self):
        ok = {DONE, HEALTHY, T2, TODO, CANT}
        for t in TREES:
            self.assertIn(t["status"], ok, f"{t['tree']} 的状态 {t['status']!r} 不在允许集合里")

    def test_support_trees_have_no_damage_type(self):
        # 纯支援系（伤害类型「—」）不该有伤害技能之外的声明，也不该被判成死内容
        for t in TREES:
            if t["dmg"] == "—":
                self.assertTrue(all(s in self.owner for s in t["skills"]))

    def test_every_tree_has_a_note(self):
        for t in TREES:
            self.assertTrue(t.get("note", "").strip(), f"{t['tree']} 缺结论说明")
            self.assertGreaterEqual(len(t["skills"]), 8, f"{t['tree']} 技能太少，可能漏了")


if __name__ == "__main__":
    unittest.main()
