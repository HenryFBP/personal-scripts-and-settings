@ECHO off

SET back=%cd%

FOR /D %%i in (*) DO (
ECHO Going to: "%%i"
CD "%%i"

ECHO Current directory:


ECHO Executing: 
REM %*

REM pause
)
cd %back%
