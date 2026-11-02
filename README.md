# d2-113c MOD

基于暗黑破坏神 2 1.13c（LoD）的**轻度修补** MOD —— 只改原版设计上不合理的地方，不重做游戏。
详细路线见 [PLAN.md](PLAN.md)。

## 工作流

```
vanilla/   ← 从 MPQ 抽出来的 1.13c 原始 txt（只读基线，一次性）
patches/   ← 所有改动，用一句话声明（这就是"源码"）
tools/     ← Python：解析 / 构建 / 校验
mod/       ← 构建产物，只含被改过的表（gitignore）
docs/      ← changelog（自动生成）+ 设计文档
```

改一个数值 = 改 `patches/` 里的一行 → 跑构建 → 看 changelog → 把 `mod/` 同步到 VM 里试。

**永远不手改 `vanilla/` 和 `mod/` 里的 txt。** 前者是基线，后者是产物。

## 命令

```bash
# 抽取完 MPQ 后，第一件事：确认基线能被无损读回
python3 -m tools.build --check

# 构建（产出 mod/ + docs/changelog.md）
python3 -m tools.build

# 只看会改什么，不写文件
python3 -m tools.build --dry-run

# 校验产物结构（表头漂移、主键重复、Excel 事故值……）
python3 -m tools.validate

# 单测（round-trip 保证是整套工具的地基）
python3 -m unittest discover -s tests -t .
```

## vanilla 基线怎么来（P0，一次性）

1. VBox 里装好纯净 1.13c + LoD，确认能离线启动 → **打快照**。
2. 用 Ladik's MPQ Editor 打开 `d2data.mpq` / `d2exp.mpq` / `patch_d2.mpq`，
   把 `data/global/excel/` 整个抽出来（`patch_d2.mpq` 里的覆盖前两个）。
3. 按此结构放到本项目：

```
vanilla/data/global/excel/*.txt
```

4. `python3 -m tools.build --check` —— 全绿就说明基线可信。

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
