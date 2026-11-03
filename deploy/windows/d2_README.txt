部署包（Mac 端通过 utmctl file push 推进来的）

第一步  d2_00_set_path.bat   拖入游戏文件夹，保存路径
第二    d2_01_backup.bat    备份原有 .bin
第三    d2_02_apply_one.bat Hireling    ← 一次一张表
        d2_02_apply_one.bat Runes
        ...依次...
出事    d2_03_rollback.bat  一键回滚

推荐顺序（风险由低到高）：
  Hireling - Runes - SetItems - UniqueItems - Skills - TreasureClassEx - MonStats

每次部署后必须验：
  装备 + 1号符文 放盒子里 = 能不能打孔？
  能打孔 -> 整合版的自定义合成公式还在 -> 安全
  打不了孔 -> 立刻 rollback

注意：CubeMain 我们故意不部署，会毁掉整合版 75+ 条自定义公式。
