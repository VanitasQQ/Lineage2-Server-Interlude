# Created by L2Emu Team
import sys
from ru.catssoftware.gameserver.model.quest        import State
from ru.catssoftware.gameserver.model.quest        import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "7001_ClanItems"

class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onFirstTalk (Self,npc,player):
   st = player.getQuestState(qn)
   npcId = npc.getNpcId()
   if npcId in [32024,32025] :
     if player.isClanLeader() :
       htmltext = str(npcId) + ".htm"
     else :
       htmltext = str(npcId) + "-no.htm"
   return htmltext

QUEST = Quest(7001,qn,"custom")

QUEST.addStartNpc(32024)
QUEST.addStartNpc(32025)

QUEST.addFirstTalkId(32024)
QUEST.addFirstTalkId(32025)