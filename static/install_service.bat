@echo off
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
goto UACPrompt
) else (
goto gotAdmin
)
:UACPrompt
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\flower_optimizer_service_installer_helper.vbs"
echo UAC.ShellExecute "%~s0", "%1 %2", "", "runas", 1 >> "%temp%\flower_optimizer_service_installer_helper.vbs"
"%temp%\flower_optimizer_service_installer_helper.vbs"
exit /B
:gotAdmin
if exist "%temp%\flower_optimizer_service_installer_helper.vbs" del "%temp%\flower_optimizer_service_installer_helper.vbs"

cd /d %2\static
echo %2	
nssm install flower_optimizer %1
nssm set flower_optimizer AppDirectory %2
nssm set flower_optimizer AppParameters flower_optimizer.api
nssm set flower_optimizer AppStdout %2\log.txt
nssm set flower_optimizer AppStderr %2\log.txt
echo Service Installed Successfully!
pause
