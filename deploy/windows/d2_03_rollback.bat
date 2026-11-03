@echo off
chcp 936 >nul
cd /d "%~dp0"
if not exist "game.txt" ( echo 先跑 d2_00_set_path.bat & pause & exit /b 1 )
set /p G=<game.txt
echo.
echo 回滚中...
for %%T in (Hireling MonStats Runes SetItems Skills TreasureClassEx UniqueItems) do (
  if exist "%G%\data\global\excel\%%T.txt" (
    del /Q "%G%\data\global\excel\%%T.txt"
    echo   已删 %%T.txt
  )
  if exist "_bin_backup\%%T.bin" (
    copy /Y "_bin_backup\%%T.bin" "%G%\data\global\excel\%%T.bin" >nul
    echo   已还原 %%T.bin
  )
)
echo.
echo 回滚完成。
pause
