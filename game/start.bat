@echo off
Color 0A
title Game Server Console.

:start
java -Dfile.encoding=UTF-8 -Xmx1024m -Xms1024m -Xmn1024m -XX:PermSize=256m -XX:SurvivorRatio=8 -Xnoclassgc -XX:+AggressiveOpts -cp ../libs/*;./gameserver.jar;./extensions/* ru.catssoftware.gameserver.util.BootManager 
if ERRORLEVEL 2 goto start
pause
