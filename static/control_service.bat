@echo off
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
goto UACPrompt
) else (
goto gotAdmin
)
:UACPrompt
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\flower_optimizer_service_helper.vbs"
echo UAC.ShellExecute "%~s0", "%1", "", "runas", 1 >> "%temp%\flower_optimizer_service_helper.vbs"
"%temp%\flower_optimizer_service_helper.vbs"
exit /B
:gotAdmin
if exist "%temp%\flower_optimizer_service_helper.vbs" del "%temp%\flower_optimizer_service_helper.vbs"
sc %1 flower_optimizer
