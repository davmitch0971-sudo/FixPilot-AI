@echo off
title FixPilot‑AI ULTRA PC Edition Installer
color 0A

echo.
echo ================================================
echo   FixPilot‑AI ULTRA PC Edition - Installer
echo   Source‑Intelligent Architect Certified
echo ================================================
echo.

REM Create program directory
set "TARGET=%USERPROFILE%\FixPilot-AI-PC"
if not exist "%TARGET%" (
    mkdir "%TARGET%"
)

REM Copy PowerShell engine
echo Copying FixPilot-ULTRA-PC.ps1 to %TARGET% ...
copy /Y "FixPilot-ULTRA-PC.ps1" "%TARGET%" >nul

REM Create logs folder
if not exist "%TARGET%\FixPilot-Logs" (
    mkdir "%TARGET%\FixPilot-Logs"
)

REM Create desktop shortcut
echo Creating desktop shortcut...
set "VBS=%TEMP%\fixpilot_shortcut.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS%"
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\FixPilot-AI PC Edition.lnk" >> "%VBS%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS%"
echo oLink.TargetPath = "powershell.exe" >> "%VBS%"
echo oLink.Arguments = "-ExecutionPolicy Bypass -File ""%TARGET%\FixPilot-ULTRA-PC.ps1""" >> "%VBS%"
echo oLink.IconLocation = "powershell.exe,0" >> "%VBS%"
echo oLink.Save >> "%VBS%"
cscript //nologo "%VBS%"
del "%VBS%"

echo.
echo Installation complete.
echo A desktop shortcut has been created:
echo   "FixPilot-AI PC Edition"
echo.
echo To run manually:
echo   powershell -ExecutionPolicy Bypass -File "%TARGET%\FixPilot-ULTRA-PC.ps1"
echo.
pause
exit
