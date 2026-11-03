# Runbook · 游戏到手后的执行顺序

> 状态：**游戏还没装好，所以这份文档只是计划**，未执行。
> 目标：从"VBox 里装完 D2"到"B 档改动上线并验收"，每一步都有明确的判据和回滚点。

---

## 0. 一页总览

```
[1] VBox 设置 + 装游戏 + 打快照 pristine-113c
        │
[2] 跑 tools/vm_diag.bat  → 贴输出 → 走「整合版能不能用」决策树
        │
        ├─ 能用 → 双层基线（--base 整合版数据层）
        └─ 不能用 → [3] 再装一份纯净 1.13c 只做基线
        │
[4] 部署 mod/ 到 VM + 启动参数 -direct -txt
        │
[5] 首次生效验证（.bin 时间戳）
        │
[6] B1/B2 佣兵改动实施 + 手感验收
        │
[7] 主线必经点复查（B3）
```

**铁律**：每次动 Dll / PlugY / 注册表 **之前** 打快照；只动 `data/global/excel/*.txt` 的话不用打（txt 可随时删掉回滚）。

---

## 1. VM 准备

### 1.1 VBox 设置

| 项 | 值 | 原因 |
|---|---|---|
| 内存 | ≥ 2 GB | D2 只需要几百 MB，留余量给宿主 |
| 显存 | 128 MB，**3D 加速关闭** | D2 是 DirectDraw 老程序，开 3D 加速反而容易黑屏 |
| 共享文件夹 | 自动挂载，指向 `~/Projects/d2-113c` | 只用于同步，**不要从共享目录直接启动游戏** |
| 快照 | 装完纯净 1.13c 立刻打 `pristine-113c` | 后面所有回滚都靠它 |

### 1.2 装游戏

1. 装 1.13c + LoD，确认能离线启动（光盘镜像挂载 / no-cd 启动器）
2. `D2VidTst.exe` 跑一遍，选 DirectDraw（3D 容易在 VBox 里出问题）
3. 进一次游戏，建个角色进出，确认存档能写
4. **打快照 `pristine-113c`**
5. （可选，但强烈建议）装 **PlugY**（1.13c 版）→ 再打快照 `pristine-plugy`
   - 一次解决：共享仓库、无限页、天梯符文之语（`ActiveLadderRunewords=1`）、单机 Diablo Clone
   - 零 txt 风险，是性价比最高的一步

---

## 2. 整合版能不能用？—— 决策树

把 `tools/vm_diag.bat` 拷到游戏根目录双击，按输出走：

| 诊断结果 | 结论 | 动作 |
|---|---|---|
| `data\global\excel\*.txt` **有**散文件 | 好消息：能直接 diff 出作者的改动清单 | 走 [2.1] 双层基线 |
| 只有 `.bin` 没有 `.txt` | 改动在 MPQ 或 Dll 里 | 走 [2.2] 单独装纯净 |
| MPQ 体积与官方 1.13c 差异极大 | 被重打包过，抽出来也不可信 | 走 [2.2] |
| `game.exe` 版本不是 1.13c | 版本对不上，偏移/PlugY 全会错 | 走 [2.2]，并告诉我版本号 |
| 启动器里带 `-direct -txt` | 它已经在用数据目录覆盖 | 走 [2.1] |

### 2.1 双层基线（整合版可用时）

思路：**我们的补丁叠在整合版的数据层上**，纯净基线只用于校验和报告。

```bash
# 把整合版自带的 data/global/excel/*.txt 拉回 mac
# → 放到 base/  （新增目录，不是 vanilla/）
python3 -m tools.build --vanilla base --out mod        # 叠在整合版之上
python3 -m tools.validate --dir mod --baseline vanilla  # 仍与纯净基线对比
```

> 工具目前只支持 `--vanilla` 单层。**如果走这条路，我需要把 build 扩成
> `--base`（构建输入）+ `--reference`（纯净基线，只用于校验/报告）**，约半小时的活。

### 2.2 单独装纯净（推荐路径）

整合版留着玩，另装一份纯净 1.13c 只做基线。VBox 里两份加起来约 10 GB。

---

## 3. 部署与启动

### 3.1 同步（**不要用 /MIR**）

```bat
:: 在 VM 里执行。注意是 /E 不是 /MIR
:: /MIR 会删掉游戏目录里整合版自己的 data 文件，那是不可逆的
robocopy "\\VBOXSVR\d2-113c\mod\data" "C:\Diablo II\data" /E /NJH /NJS /NDL
```

**先备份**：`xcopy "C:\Diablo II\data" "C:\Diablo II\data.bak\" /E /I`（只做一次）

### 3.2 启动

```bat
@echo off
cd /d "C:\Diablo II"
start "" Game.exe -direct -txt -w
```

- `-direct`：从 `data\` 目录读文件（覆盖 MPQ）
- `-txt`：读 `.txt` 并现场编译成 `.bin`
- `-w`：窗口模式，方便截图/切窗口
- 如果整合版用 D2GL 启动器，把这几个参数加到它那一行（需实测是否透传）

### 3.3 清 `.bin` 的时机

`-direct -txt` 会自动重编译，**不要**手动编译 bin 再混用。只有在"改回不带 `-txt` 启动"时，
才需要删掉 `data\global\excel\*.bin`，否则会读到旧的。

---

> 本文只讲"怎么把游戏装起来并让改动生效"。
> **每一处改动到底有没有按预期生效、没生效改哪里 —— 见 [verify.md](verify.md)。**

## 4. 首次生效验证（关键，别跳过）

改 txt 之后，怎么确定游戏真的读了它？**看 `.bin` 的时间戳**：

```bat
dir /od "C:\Diablo II\data\global\excel\*.bin" | findstr /i "MonStats"
```

- `.bin` 的修改时间是**刚才启动的时间** → txt 被读了、编译成功
- 没有生成 / 时间戳没变 → 参数没生效，或游戏从 MPQ 读的

补充判据：
- **能正常进游戏**本身就是一次语法校验——txt 格式错时 D2 通常直接崩或丢行
- 我们的数值改动（抗性封顶）离线已经量化过，**游戏内只需要验收"不崩 + 手感正常"**，
  不需要在游戏里重新验证数字

---

## 5. B 档实施步骤

> **已启用**：实际补丁在 `patches/merc.py`。§5.1 保留草稿原文作为决策记录。

### 5.1 草稿补丁（等游戏可测后启用）

```python
# patches/merc.py  —— 草稿，等游戏可测后再启用
from tools.d2patch import patch, eq

A3 = "Eastern Sorceror"

# B1 · A3 铁狼地狱档 HP ×1.35（85 级 1025 → 约 1384，达到 A2 的 85%）
#      不动技能等级：它打得不弱（火球 23 级 436-489），弱在活得短
#      ndigits=0 必须写：HP 是整数列，1165.05 这种值 D2 解析不了
patch("hireling.txt", why="B1 A3 铁狼地狱档 HP ×1.35").where_cols(
    [("Hireling", eq(A3)), ("Difficulty", eq("3"))]
).mul("HP", 1.35, ndigits=0).mul("HP/Lvl", 1.35, ndigits=0)

# B1b · A3 雇价统一到 12000（原 21000/27000/21000 三档不同）
patch("hireling.txt", why="B1b A3 雇价下调").where_cols(
    [("Hireling", eq(A3)), ("Difficulty", eq("3"))]
).set("Gold", 12000)

# B2 · A5 野蛮人：只改定价 32000 → 15000，不改技能
#      （给它光环就是"第二个 A2"，会抹掉职业差异）
patch("hireling.txt", why="B2 A5 雇价下调").where_cols(
    [("Hireling", eq("Barbarian")), ("Difficulty", eq("3"))]
).set("Gold", 15000)
```

实测这组草稿会产出 22 处改动，A3 地狱档变成 HP 1165(+36.45/级)、雇价 12000。

**注意**：`hireling.txt` 每行是「佣兵 × 难度档」，所以改价格/HP 要用
`where_cols([("Hireling", eq("Eastern Sorceror")), ("Difficulty", eq("3"))])`
精确到行，不能整类一把梭。

### 5.2 验收标准

| 项 | 判据 |
|---|---|
| 不崩 | 进地狱带 30 分钟不跳错 |
| A3 不该变成肉盾 | 对比 A2：A3 仍然更容易死，只是"不那么容易" |
| A5 仍然是没人选 | 如果调价后突然变成最优解，说明价格改过头（说明"它本来就该被忽略"） |
| 存档完好 | 换回 vanilla 数据后存档能读、装备不消失 |

---

## 6. 回滚

| 改了什么 | 怎么回滚 |
|---|---|
| `mod/` 里的 txt | 删掉 `C:\Diablo II\data\global\excel\*.txt` + `*.bin`，游戏自动回 MPQ |
| PlugY / Dll / 注册表 | VBox 快照回滚到 `pristine-113c` |
| 存档 | 每次动数据前备份整个存档目录（`PlugY.ini` 的 `SavePath`） |

---

## 7. 卡住了怎么办

| 现象 | 排查顺序 |
|---|---|
| 点启动没反应 | game.exe 兼容性 → XP SP2；`D2VidTst` 改兼容性再跑一遍；装运行库 |
| 黑屏 / 花屏 | VBox 关 3D 加速；或上 `cnc-ddraw` 兜底 |
| 进游戏后数据没变 | `-direct -txt` 没生效：检查 `data` 是不是在 Game.exe 同级；看 `.bin` 时间戳 |
| 启动直接崩 | txt 语法错（tab 数不对/表头被改）；`git stash` 回到上一个提交再试，二分定位 |
| 存档读不出来 | 换回 vanilla 数据；确认没碰 `itemstatcost.txt` |
| 中文乱码 | 只可能在改过 `string.tbl` 之后发生；txt 保持 ASCII 就不会有这问题 |

---

## 8. 这份计划里**不做**的事

- 不写 `.bat` 自动启动游戏（手动跑，方便看报错）
- 不做"多倍爆率/多倍怪"（那是另一个玩法方向）
- 不碰 Dll（除非 B 档做完且确实需要）
- 不在 VM 里编辑 txt（编辑永远在 mac 上，VM 只当播放器）
