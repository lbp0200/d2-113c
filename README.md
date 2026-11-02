# d2-113c MOD

基于暗黑破坏神 2 1.13c（LoD）的 MOD —— **重做激励结构，让它像一款游戏**：
让玩家的选择、技巧、构筑决定结果，而不是让"点箱子的次数"和随机数决定结果。

- 目标与验收标准：**[docs/design-goal.md](docs/design-goal.md)**（先看这个）
- 路线与决策记录：[PLAN.md](PLAN.md)
- 数据报告：`docs/p1-*.md`

## 工作流

```
vanilla/   ← 1.13c 原始 txt（只读基线，已内置，来源见 vanilla/README.md）
patches/   ← 所有改动，用一句话声明（这就是"源码"）
tools/     ← Python：解析 / 构建 / 校验
mod/       ← 构建产物，只含被改过的表（gitignore）
docs/      ← changelog（自动生成）+ 设计文档
```

改一个数值 = 改 `patches/` 里的一行 → 跑构建 → 看 changelog → 把 `mod/` 同步到 VM 里试。

**永远不手改 `vanilla/` 和 `mod/` 里的 txt。** 前者是基线，后者是产物。

## 命令

```bash
# 第一件事：确认基线能被无损读回（当前 91 张表全绿）
python3 -m tools.build --check

# P1 只读分析（不改任何数据）
python3 -m tools.p1_immunity     # 地狱免疫墙 → docs/p1-immunity.md
python3 -m tools.p1_skills       # 技能本体伤害曲线 → docs/p1-skills.md
python3 -m tools.p1_merc         # 佣兵数值对比 → docs/p1-merc.md

# 量化"打上补丁之后世界会变成什么样"（叠加层）
python3 -m tools.p1_immunity --overlay mod

# 构建（产出 mod/ + docs/changelog.md）
python3 -m tools.build

# 只看会改什么，不写文件
python3 -m tools.build --dry-run

# 校验产物结构（表头漂移、主键重复、Excel 事故值……）
python3 -m tools.validate

# 单测（round-trip 保证是整套工具的地基）
python3 -m unittest discover -s tests -t .
```

## vanilla 基线

已内置（来自 [whipowill/d2-113c-txt](https://github.com/whipowill/d2-113c-txt)，
原出处 PhrozenKeep / CountDracula），92 个文件布局为 `vanilla/data/global/excel/*.txt`。
来源、校验结果与 1.13c 数据坑详见 **[vanilla/README.md](vanilla/README.md)**。

想自己从 MPQ 重抽也行，抽完跑 `python3 -m tools.build --check` 对比即可。

## 写补丁

```python
from tools.d2patch import patch, gt

# 规则式：所有大于 100 的地狱抗性封顶到 100
patch("monstats.txt", why="消灭绝对免疫").where("ResFi(H)", gt(100)).clamp("ResFi(H)", hi=100)

# 全表置值
patch("runes.txt", why="单机可用天梯符文之语").all().set("server", "0")

# 数值批量缩放（非数字单元格自动跳过并告警）
patch("skills.txt", why="火系前期手感").only("Skill", ["Fire Bolt", "Fire Ball"]).mul("EMin", 1.15)
```

* `why=` 必填，会进改动报告，将来回滚靠它判断。
* `soft=True`：列名对不上时只跳过并记进报告，不阻塞构建（用于还没核对的列名）。
* 选择器：`all()` / `where(col, 谓词)` / `only(col, [值...])` / `where_cols([...])`。
* 谓词：`gt ge lt le num_eq eq ne one_of matches blank nonblank isnum not_`。
* 操作：`set add mul clamp swap`。

## 为什么不用 Excel / D2Excel 改 txt

Excel 会改引号、改换行、改编码、吞掉空列、把 `-` 转成日期；而 D2 的解析器**解析失败不报错**
——静默丢行或直接启动崩溃。所以这里用 Python 做 `读 → 改单元格 → 原样写回`，
并用单测保证**未改动的字节完全一致**（`tests/test_d2txt.py`）。

## 已知约束

- txt 必须保持 ASCII；中文全走 `string.tbl`（代码页 936），不进 txt。
- `itemstatcost.txt` 的 `Save Bits` / 已有 stat ID 一律不动（会毁存档）。
- `-direct -txt` 会在 `data/global/excel/` 里写回 `.bin`；换构建方式时先清 bin。
- 版本锁死 1.13c（1.14 移除了 `-direct -txt`）。
