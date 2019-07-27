@echo off
Color 0A
title Register Gameserver Console. The server made l2jlovely.net

:start
java -cp ../libs/*;./login.jar  ru.catssoftware.gsregistering.GameServerRegister
