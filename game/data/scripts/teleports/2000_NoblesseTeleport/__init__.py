# Created by Ham Wong on 2007.02.28
import sys
from ru.catssoftware.gameserver.model.quest        import State
from ru.catssoftware.gameserver.model.quest        import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "2000_NoblesseTeleport"

NPC = [30006,30059,30080,30134,30146,30177,30233,30256,30320,30540,30576,30836,30848,30878,30899,31275,31320,31964,32163]

class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onEvent (self,event,st):
    htmltext = event
    return htmltext

 def onTalk (self,npc,player):
    st = player.getQuestState(qn)
    if player.isNoble() == 1 and st.getQuestItemsCount(6651) >= 1 :
      htmltext = "noble.htm"
    elif player.isNoble() == 1 and st.getQuestItemsCount(6651) == 0 :
      htmltext = "nobleteleporter-nogatepass.htm"
    elif player.isNoble() == 0 :
      htmltext = "nobleteleporter-no.htm"
      st.exitQuest(1)
    return htmltext

QUEST       = Quest(2000,qn,"Teleports")

for item in NPC:
   QUEST.addStartNpc(item)
   QUEST.addTalkId(item)