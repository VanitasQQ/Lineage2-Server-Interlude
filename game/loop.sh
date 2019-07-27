# !/bin/sh
err=1
until [ $err == 0 ];
do
	java -server -Dfile.encoding=UTF-8 -XX:AutoBoxCacheMax=10000 -XX:+RelaxAccessControlCheck -XX:+UseFastAccessorMethods -XX:+AlwaysPreTouch -XX:+UseLargePages -XX:+UseParNewGC -XX:+CMSClassUnloadingEnabled -XX:+ClassUnloading -XX:MaxGCPauseMillis=25 -XX:+UseConcMarkSweepGC -XX:ParallelGCThreads=8 -XX:+CMSParallelRemarkEnabled -XX:+UseAdaptiveGCBoundary -XX:MaxTenuringThreshold=6 -XX:+AggressiveOpts -XX:+UseStringCache -XX:+OptimizeStringConcat -XX:CompileThreshold=1000 -XX:PermSize=96m -XX:MaxPermSize=96m -XX:SurvivorRatio=4 -XX:TargetSurvivorRatio=90 -XX:MaxNewSize=144m -XX:NewSize=144m -XX:+UseBiasedLocking -Xmn144m -Xmx6G -Xms768m -Xss228k -Djava.net.preferIPv4Stack=true  -cp ../libs/*:./gameserver.jar:./extensions/* ru.catssoftware.gameserver.util.BootManager 
	err=$?
	sleep 10;
done