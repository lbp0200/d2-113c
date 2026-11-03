@echo off
chcp 936 >nul
cd /d "%~dp0"
if not exist "game.txt" ( echo 先跑 d2_00_set_path.bat & pause & exit /b 1 )
set /p G=<game.txt
set "TABLES=Hireling MonStats Runes SetItems Skills TreasureClassEx UniqueItems"
if "%~1"=="" (
  echo.
  echo 用法: d2_02_apply_one.bat 表名
  echo.
  echo 可用表（建议按这个顺序，一次一张）:
  echo    Hireling  Runes  SetItems  UniqueItems  Skills  TreasureClassEx  MonStats
  pause & exit /b 0
)
if not exist "d2_%~1.txt" ( echo [错误] 找不到 d2_%~1.txt & pause & exit /b 1 )
echo.
echo 部署 %~1.txt ...
copy /Y "d2_%~1.txt" "%G%\data\global\excel\%~1.txt" >nul
if errorlevel 1 ( echo [错误] 拷贝失败（文件被占用？关掉游戏） & pause & exit /b 1 )
echo   完成。
echo.
echo --------------------------------------------------
echo  现在进游戏验两条：
echo   1^) 改动生效了吗
echo   2^) 拿一件装备 + 1号符文 放盒子里，能打孔吗？
echo      能打孔 = 整合版自定义公式还活着 = 安全
echo.
echo  如果第 2 条失败，立刻跑 d2_03_rollback.bat
echo --------------------------------------------------
pause
