@echo off
set error_log=celery_worker.log
echo %path%|findstr "venv">nul
if %errorlevel% equ 1 (
	call :say "Local virtual env..."
	call venv\scripts\activate.bat
)


:loop
call :say "start worker..."
celery -A tbd worker -Q celery,broadcast_tasks -l info
call :say "worker stopped, restart it!"
goto :loop


:say
echo %date% %time% %1
echo %date% %time% %1 >>%error_log%
goto :EOF

