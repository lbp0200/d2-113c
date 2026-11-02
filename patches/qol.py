"""P2 · 纯 txt 的 QoL 修补：不改变手感，只减少摩擦。

全部 `soft=True`：列名对不上时只跳过、写进报告的"跳过的补丁"，不阻塞构建。
第一次跑完 `tools.build` 后，先看 `docs/changelog.md` 里有没有"跳过的补丁"，
再照真实表头改列名——这就是 P0 的核对动作。

写补丁的规矩：
  1. 每条都要有 `why=`，它会进改动报告，将来回滚时靠它判断。
  2. 优先用 where/clamp 描述"规则"，而不是逐行 set 具体值。
  3. 一次只改一个主题，一个主题一个文件。
"""

from tools.d2patch import patch

# 单机也能用天梯专属符文之语（原版被 runes.txt 的 server 列挡住）。
patch("runes.txt", why="解锁天梯符文之语（单机）", soft=True).all().set("server", "0")
