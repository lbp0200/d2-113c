"""TreasureClass 展开工具。

写这个模块的原因：分析掉落时我手写了 5 遍同样的递归，每次都可能踩同一个坑——

**`TreasureClassEx.txt` 最后 4 列是元数据（`SumItems` / `TotalProb` / `DropChance` / `Term`），
不是物品。** 按"下标 9 开始每两列一组"的朴素写法会把它们读成物品名，
得到 `'36'`、`'0.977'` 这种荒谬的"物品"。所以这里严格按表头 `ItemN`/`ProbN` 配对。

另一个必须知道的事：`weapN` / `armoN` 不是文件里的行（`TreasureClassEx.txt` 里查不到），
它们是游戏按物品 `level` 自动生成的带：
    weapN  =  `level` 在 (N-3, N] 区间内的武器
    armoN  =  同理
所以 N 是"带上限"。地狱装备 TC 引用的最低带是 `weap54`，但通过长链降级仍然能落到 `weap3`。
"""

from __future__ import annotations

from pathlib import Path

from . import d2txt


class TreasureClasses:
    def __init__(self, tf: d2txt.TxtFile):
        self.tf = tf
        h = tf.header
        self._rows = {tf.get(r, 0): r for r in tf.rows}
        # 严格按表头取 ItemN / ProbN 对
        self._pairs = [
            (h.index(f"Item{i}"), h.index(f"Prob{i}"))
            for i in range(1, 128)
            if f"Item{i}" in h and f"Prob{i}" in h
        ]
        self._nodrop = h.index("NoDrop") if "NoDrop" in h else None
        self._picks = h.index("Picks") if "Picks" in h else None

    @classmethod
    def load(cls, path: str | Path) -> "TreasureClasses":
        return cls(d2txt.TxtFile.load(path))

    def __contains__(self, name: str) -> bool:
        return name in self._rows

    def picks(self, name: str) -> float:
        r = self._rows.get(name)
        if not r or self._picks is None:
            return 1.0
        v = d2txt.to_number(self.tf.get(r, self._picks))
        return float(v) if v else 1.0

    def entries(self, name: str) -> tuple[list[tuple[str, float]], float]:
        """-> ([(item, prob)], nodrop_prob)"""
        r = self._rows.get(name)
        if r is None:
            return [], 0.0
        out = []
        for ii, pi in self._pairs:
            if ii < len(r) and r[ii].strip():
                p = d2txt.to_number(self.tf.get(r, pi)) or 0.0
                out.append((r[ii], float(p)))
        nod = 0.0
        if self._nodrop is not None and self._nodrop < len(r):
            nod = float(d2txt.to_number(self.tf.get(r, self._nodrop)) or 0.0)
        return out, nod

    def expand(self, name: str, max_depth: int = 40) -> dict[str, float]:
        """把 TC 展开成 `{叶子: 概率}`，叶子可能是 TC 之外的物品代码（如 `weap12`）。

        概率按**单次抽取**归一化（不乘 Picks），所以可以理解为"每个物品槽的期望分布"。
        """
        return self._expand(name, 1.0, 0, max_depth)

    def _expand(self, name: str, prob: float, depth: int, max_depth: int) -> dict[str, float]:
        if depth > max_depth:
            return {}
        ents, nod = self.entries(name)
        total = sum(p for _, p in ents) + nod
        if total <= 0:
            return {}
        out: dict[str, float] = {}
        for item, p in ents:
            p2 = prob * p / total
            if item in self._rows:
                for k, v in self._expand(item, p2, depth + 1, max_depth).items():
                    out[k] = out.get(k, 0.0) + v
            else:
                out[item] = out.get(item, 0.0) + p2
        return out


def band_summary(dist: dict[str, float], prefix: str) -> dict[str, float]:
    """把 `{weap12: 0.05, ...}` 按低/中/高档聚合，用于看"地狱到底掉多少垃圾"。"""
    buckets = {"低阶 (<=30)": 0.0, "中阶 (33~51)": 0.0, "高阶 (>=54)": 0.0}
    for k, v in dist.items():
        if not k.startswith(prefix) or not k[4:].isdigit():
            continue
        n = int(k[4:])
        if n <= 30:
            buckets["低阶 (<=30)"] += v
        elif n <= 51:
            buckets["中阶 (33~51)"] += v
        else:
            buckets["高阶 (>=54)"] += v
    tot = sum(buckets.values()) or 1.0
    return {k: v / tot for k, v in buckets.items()}
