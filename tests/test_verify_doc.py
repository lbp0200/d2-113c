"""验证清单（`docs/verify.md`）的自洽性。

清单是进游戏后唯一的行动依据，所以它引用的文件必须真实存在、
每一项都必须有判据 —— 否则到现场才发现"要改的文件找不到"就太晚了。
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = (ROOT / "docs" / "verify.md").read_text(encoding="utf-8")


class VerifyDoc(unittest.TestCase):
    def test_every_referenced_repo_path_exists(self):
        paths = set(re.findall(r"`((?:patches|tools|docs)/[\w./-]+)`", TEXT))
        self.assertTrue(paths, "清单里应该引用具体的文件和工具")
        missing = [p for p in paths if not (ROOT / p).exists()]
        self.assertEqual(missing, [], f"清单引用了不存在的文件：{missing}")

    def test_every_item_has_criteria(self):
        items = re.split(r"^### ", TEXT, flags=re.M)[1:]
        self.assertGreaterEqual(len(items), 15, f"清单项目太少（{len(items)}）")
        for block in items:
            title = block.splitlines()[0]
            self.assertIn("判据", block, f"{title} 没有「判据」")
            self.assertIn("不通过", block, f"{title} 没有「不通过怎么办」")

    def test_constants_mentioned_match_the_patches(self):
        # 清单里点名的常量必须真的在补丁里存在，防止改名后清单失效
        drops = (ROOT / "patches" / "drops.py").read_text(encoding="utf-8")
        self.assertIn("MONSTER_PICKS", drops)
        self.assertIn("MONSTER_PICKS", TEXT)
        for f in ("p2_skills.py", "p2_items.py", "economy.py", "balance.py"):
            self.assertTrue((ROOT / "patches" / f).exists(), f"缺 {f}")

    def test_priority_section_names_three_items(self):
        self.assertIn("A1", TEXT)
        self.assertIn("B1", TEXT)
        self.assertIn("B2", TEXT)


if __name__ == "__main__":
    unittest.main()
