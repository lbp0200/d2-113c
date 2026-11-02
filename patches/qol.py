"""P2 · 纯 txt 的 QoL 修补：不改变手感，只减少摩擦。

全部 `soft=True`：列名对不上时只跳过、写进报告的「跳过的补丁」，不阻塞构建。
新加补丁前先 `python3 -m tools.build --dry-run` 确认真实表头。

写补丁的规矩：
  1. 每条都要有 `why=`，它会进改动报告，将来回滚时靠它判断。
  2. 优先用 where/clamp 描述「规则」，而不是逐行 set 具体值。
  3. 一次只改一个主题，一个主题一个文件。

---

**已核对（2025-11，基于真实 1.13c 数据）：天梯专属符文之语不是 txt 能解决的。**

Runes.txt 里确实有 `server` 列，但 1.13c 里该列 **169 行全为空**（旧版遗留，
在 1.13c 已不再作为天梯开关使用）。天梯限制是硬编码在 Dll 里的判定
（对免疫怪降抗那条思路不适用，这里是 runeword 索引白名单）。

可行方案只有两个：
  - PlugY.ini 里 `ActiveLadderRunewords=1`（整合包就是这么做的，零风险）
  - 打 Dll 补丁（P4，需要 1.13c 偏移表，且与整合包已 patch 的 Dll 冲突）

结论：这一项从 P2（纯 txt）移到 **P0.5（装 PlugY）/ P4（Dll）**。
本文件因此暂时是空模板。
"""

from tools.d2patch import patch  # noqa: F401
