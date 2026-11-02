@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
echo ================ D2 MOD PACK DIAGNOSTIC ================
echo Dir: %CD%
echo.

echo [1] Main executables and DLLs
for %%f in (game.exe D2Loader.exe D2Client.dll D2Common.dll D2Game.dll D2Gfx.dll D2Win.dll D2CMP.dll Fog.dll Storm.dll) do (
  if exist "%%~f" (
    for %%v in ("%%~f") do echo   %%~f  %%~zv bytes  %%~tv
  ) else (
    echo   %%~f  -- MISSING
  )
)
echo.
echo   Version info:
powershell -NoProfile -Command "$i=Get-Item 'game.exe' -ErrorAction SilentlyContinue; if($i){'    FileVersion='+$i.VersionInfo.FileVersion; '    ProductVersion='+$i.VersionInfo.ProductVersion; '    Size='+$i.Length}"
echo.

echo [2] Loose .txt under data\global\excel  (presence = pack overrides data via txt)
if exist "data\global\excel" (
  dir /b "data\global\excel\*.txt" 2>nul
  echo   -- Count:
  dir /b "data\global\excel\*.txt" 2>nul | find /c /v ""
) else (
  echo   NO data\global\excel directory
)
echo.

echo [3] MPQ sizes  (very different from stock 1.13c = repacked)
for %%f in (d2data.mpq d2exp.mpq d2sfx.mpq d2music.mpq d2speech.mpq patch_d2.mpq) do (
  if exist "%%~f" (
    for %%v in ("%%~f") do echo   %%~f  %%~zv bytes
  ) else (
    echo   %%~f  -- MISSING
  )
)
echo.

echo [4] Plugins and configs
dir /b *.ini *.cfg *.script 2>nul
echo   -- Plugin dir:
if exist Plugin dir /b Plugin 2>nul
echo.

echo [5] Launchers (decides whether -direct -txt is usable)
for %%f in (*.bat) do (
  echo   --- %%~f
  findstr /i "game.exe D2Loader -w -direct -txt" "%%~f" 2>nul
)
echo.

echo [6] PlugY settings
if exist PlugY.ini (
  findstr /i /c:"ActivePlugin" /c:"ActiveLogFile" /c:"ActiveBigStash" /c:"ActiveSharedStash" /c:"ActiveLadderRunewords" /c:"ActiveWorldEvent" /c:"SavePath" /c:"ActiveMultiPageStashMaxPage" PlugY.ini
) else (
  echo   NO PlugY.ini
)
echo.
echo ==================== END ====================
pause
