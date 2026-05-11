@echo off
REM ============================================================================
REM mirror_instructions.bat
REM
REM Regenerates the Markdown mirror files for every YAML under
REM C:\Users\rtoth\.cursor\commands\bootstrap that contains an
REM `instructions_md` field. Mirrors land in this folder.
REM
REM Run this any time you edit the prose section of a command YAML.
REM ============================================================================
setlocal

pushd "%~dp0"

where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    py -3 "mirror_instructions.py"
) else (
    where python >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        python "mirror_instructions.py"
    ) else (
        echo FATAL: Neither 'py' nor 'python' is on PATH.
        echo        Install Python 3 from https://www.python.org/downloads/
        popd
        exit /b 2
    )
)

set EXITCODE=%ERRORLEVEL%
popd
exit /b %EXITCODE%
