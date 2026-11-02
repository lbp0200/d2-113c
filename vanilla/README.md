# vanilla/ —— 1.13c 原始数据基线（只读）

## 来源

| 项 | 值 |
|---|---|
| 上游 | https://github.com/whipowill/d2-113c-txt |
| 原始出处 | PhrozenKeep 论坛，由 **CountDracula** 整理 / 提取 |
| 内容 | Diablo II LoD **1.13c** 的 `Data/Global/Excel/*.txt`，92 个文件（3.2 MB） |
| 取用时间 | 2025-11 |

论坛帖：[Source](https://d2mods.info/forum/viewtopic.php?t=56033) ·
[Documentation](https://d2mods.info/forum/viewtopic.php?t=34455)

## 本地布局

上游目录是 `Data/Global/Excel/`（大写），这里落到标准游戏路径：

```
vanilla/data/global/excel/*.txt     ← 真实文件名保留大写，如 MonStats.txt
```

工具链对文件名做 **大小写不敏感解析**（`monstats.txt` → `MonStats.txt`），
因为游戏跑在 Windows 上，而我们的工具跑在 macOS。

## 规矩

1. **这个目录只读。** 任何改动都写在 `patches/` 里，构建产物落 `mod/`。
2. 不要在这里做格式化（换行、编码、去掉空列）。基线一旦漂移，
   `tools.validate` 的"与基线对比"就失去意义。
3. 唯一允许的修改是**替换整个文件**（比如上游更新了 1.13c 的某个表），
   替换后立刻跑 `python3 -m tools.build --check` 确认仍是字节级 round-trip。

## 已做的校验

```
python3 -m tools.build --check
→ 基线自检：91 张表 … 基线自检通过
```

- **92** 个 `.txt` 全部通过 `parse → emit` **字节级一致**（编码/换行/列数/末行换行都不漂移）。
  这是整套工具链的地基，见 `tests/test_d2txt.py`。
- `AiParms.txt` 被排除：它不是数据表，是 234 行的自由文本（`Description of Ai Parameters`），
  游戏不当作数据读。排除名单在 `tools/build.py` 的 `NON_TABLE`。

## 已知的 1.13c 数据特征（写补丁时的坑）

- 列名大小写不统一：`Id` / `id` / `ResFi(H)` / `mon1`（levels.txt 用小写）。
  工具链已做大小写不敏感匹配。
- `levels.txt` 的 `Act` 列**大面积为空且编号不可靠**（`Act 5 - Barricade` 挂在 `Act=4` 下）。
  幕号请从 `Name` 的 `Act N - ` 前缀取。
- `Runes.txt` 的 `server` 列存在但 **169 行全为空**——它不是 1.13c 的天梯开关
  （天梯限制硬编码在 Dll 里）。别在这列上做文章。
- 空单元格与 `-` 都表示"无值"，`to_number()` 会返回 `None`；数值操作会自动跳过它们并告警。
