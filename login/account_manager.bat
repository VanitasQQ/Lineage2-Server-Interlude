@echo off
Color 0A
title Account Manager. The server made l2jlovely.net

REM ########################################################################
REM # You need to set here your JDK/JRE params in case of x64 bits System. #
REM # Remove the "REM" after set PATH variable                             #
REM # If you're not a x64 system user just leave                           # 
REM ########################################################################
REM set PATH="type here your path to java jdk/jre (including bin folder)"

:start
java -cp ../libs/*;./login.jar  -Djava.util.logging.config.file=console.cfg ru.catssoftware.accountmanager.AccountManager

