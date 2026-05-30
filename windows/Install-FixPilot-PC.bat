@echo off
setlocal

echo [*] Installing FixPilot-AI ULTRA PC (SIA Core Engine)...

set TARGET=%USERPROFILE%\FixPilot-AI-PC
if not exist "%TARGET%" mkdir "%TARGET%"

echo [*] Copying core engine...
copy "%~dp0FixPilot-ULTRA-PC.ps1" "%TARGET%\FixPilot-ULTRA-PC.ps1" /Y >nul

echo [*] Creating desktop shortcut...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$s=(New-Object -COM WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Desktop') + '\FixPilot-AI ULTRA PC.lnk');" ^
  "$s.TargetPath='powershell.exe';" ^
  "$s.Arguments='-ExecutionPolicy Bypass -File ""%TARGET%\FixPilot-ULTRA-PC.ps1""';" ^
  "$s.WorkingDirectory='%TARGET%';" ^
  "$s.IconLocation='powershell.exe,0';" ^
  "$s.Save()"

echo.
echo [*] Install complete.
echo [*] Launch from desktop: FixPilot-AI ULTRA PC
pause
endlocal
