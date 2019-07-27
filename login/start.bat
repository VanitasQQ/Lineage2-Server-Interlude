@echo off
Color 0A
title Login Server Console.

:start
java  -Dfile.encoding=UTF-8 -Xmx258m -cp ./login.jar;../libs/* ru.catssoftware.loginserver.L2LoginServer

if ERRORLEVEL 2 goto start
pause