# 部署（Windows 虚拟机）

目标环境：UTM 里的 Windows，游戏是「精修收藏版」，`data/global/excel/` 只有 `.bin`、没有 `.txt`。

## 关键约束

| 约束 | 原因 |
|---|---|
| **绝不部署 `CubeMain.txt`** | `-direct -txt` 是**整表覆盖**。整合版有 75+ 条自定义合成公式（打孔/复制/定制 charm/红门），一覆盖全没 |
| **一次只放一张表** | 不知道作者精修过哪几张 `.bin`，出问题要能定位 |
| **先备份 `.bin`** | `01_backup` 就是干这个的 |

## 怎么用

```bash
./deploy/push.sh          # 把脚本 + 7 张表推到 C:\Users\Public\d2_*
```

然后在虚拟机里：

```
C:\Users\Public\
  1. d2_00_set_path.bat      拖入游戏文件夹 → 保存路径
  2. d2_01_backup.bat        备份原有 .bin 到 _bin_backup\
  3. d2_02_apply_one.bat Hireling      ← 一次一张
  4. 进游戏验（见下）
  出事: d2_03_rollback.bat
```

推荐顺序（风险由低到高）：

```
Hireling → Runes → SetItems → UniqueItems → Skills → TreasureClassEx → MonStats
```

## 每次部署后必验的一条

> 拿一件装备 + `1号符文` 放盒子里，**能不能打孔**。

能打孔 = 整合版的自定义公式还活着 = 没污染 `CubeMain`。
**打不了孔就立刻 rollback。**

## 为什么不用 `utmctl exec`

实测（UTM 5.0.8 + Windows guest + 已装 `qemu-ga-x86_64.msi`）：

| 命令 | 结果 |
|---|---|
| `utmctl ip-address` | ✅ |
| `utmctl file pull` | ✅ |
| `utmctl file push` | ✅ |
| `utmctl exec` | ❌ 静默失败：单参数报 `Failed to execute child process`；多 `--cmd` 返回码永远 0，而命令根本没跑 |

所以流程是「程序推文件，人双击」。UTM 也没有暴露 guest agent 的串口模式
（`QEMUSerialMode` 只有 `Terminal`/`TcpClient`/`TcpServer`/`Ptty`，见 UTM 源码
`Configuration/QEMUConstant.swift`）——agent 是 UTM 自动挂的，装了 MSI 就能用。
