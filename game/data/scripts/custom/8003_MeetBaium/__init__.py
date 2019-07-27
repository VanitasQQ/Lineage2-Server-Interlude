# Created by L2Emu Team
import sys
from ru.catssoftware.gameserver.model.quest        import State
from ru.catssoftware.gameserver.model.quest        import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest
from ru.catssoftware.gameserver.instancemanager.grandbosses import BaiumManager

qn = "8003_MeetBaium"

class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onEvent(self,event,st):
    htmltext = event
    if event == "31862-3.htm" :
      htmltext = "31862-3.htm"
      st.exitQuest(1)
    return htmltext

 def onTalk(self,npc,player):
    htmltext = ""
    st = player.getQuestState(qn)
    if not st :
      st = self.newQuestState(player)
    htmltext = "31862-2.htm"
    return htmltext

 def onFirstTalk (self,npc,player):
   st = player.getQuestState(qn)
   if not st :
     st = self.newQuestState(player)
   npcId = npc.getNpcId()
   if npcId == 31862 :
     if BaiumManager.getInstance().isEnableEnterToLair() and st.getQuestItemsCount(4295) :
       htmltext = "31862.htm"
     else :
       htmltext = "31862-no.htm"
   return htmltext

QUEST = Quest(8003,qn,"custom")

QUEST.addStartNpc(31862)

QUEST.addTalkId(31862)

QUEST.addFirstTalkId(31862)