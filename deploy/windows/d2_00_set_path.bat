@echo off
chcp 936 >nul
cd /d "%~dp0"
echo ================================================
echo   设置游戏目录
echo ================================================
echo.
echo  把游戏文件夹（含 Game.exe 的那一层）直接拖进这个窗口，
echo  然后按回车。
echo.
set /p "G=游戏目录: "
set "G=%G:"=%"
if not exist "%G%\data\global\excel\UniqueItems.bin" (
  echo.
  echo [错误] %G%\data\global\excel\UniqueItems.bin 不存在
  echo        请确认选的是游戏根目录。
  pause & exit /b 1
)
> "%~dp0game.txt" echo %G%
echo.
echo 已保存: %G%
pause
