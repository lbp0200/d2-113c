@echo off
chcp 936 >nul
cd /d "%~dp0"
if not exist "game.txt" ( echo 先跑 d2_00_set_path.bat & pause & exit /b 1 )
set /p G=<game.txt
set /a N=0
echo.
echo 备份整合版原有 .bin 到 _bin_backup\
if not exist "_bin_backup" mkdir "_bin_backup"
for %%T in (Hireling MonStats Runes SetItems Skills TreasureClassEx UniqueItems) do (
  if exist "%G%\data\global\excel\%%T.bin" (
    copy /Y "%G%\data\global\excel\%%T.bin" "_bin_backup\%%T.bin" >nul
    echo   已备份 %%~T.bin
    set /a N+=1
  ) else (
    echo   [提示] %%T.bin 不存在
  )
)
echo.
echo 备份完成 %N% 个文件。
pause
