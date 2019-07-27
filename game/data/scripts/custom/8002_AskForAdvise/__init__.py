# Created by L2Emu Team
import sys
from ru.catssoftware.gameserver.model.quest        import State
from ru.catssoftware.gameserver.model.quest        import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn="8002_AskForAdvise"

NPC = [30598,30599,30600,30601,30602]

class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onTalk (Self,npc,player):
     st = player.getQuestState(qn)
     npcId = npc.getNpcId()
     Race = st.getPlayer().getRace()
     if npcId == 30598 :
         if Race in [Race.Human] :
             htmltext = str(npcId) + ".htm"
         else :
             htmltext = str(npcId) + "-no.htm"
     if npcId == 30599 :
         if Race in [Race.Elf] :
             htmltext = str(npcId) + ".htm"
         else :
             htmltext = str(npcId) + "-no.htm"
     if npcId == 30600 :
         if Race in [Race.Darkelf] :
             htmltext = str(npcId) + ".htm"
         else :
             htmltext = str(npcId) + "-no.htm"
     if npcId == 30601 :
         if Race in [Race.Dwarf] :
             htmltext = str(npcId) + ".htm"
         else :
             htmltext = str(npcId) + "-no.htm"
     if npcId == 30602 :
         if Race in [Race.Orc] :
             htmltext = str(npcId) + ".htm"
         else :
             htmltext = str(npcId) + "-no.htm"
     st.exitQuest(1)
     return htmltext

QUEST = Quest(8002,qn,"custom")

for i in NPC:
    QUEST.addStartNpc(i)
    QUEST.addTalkId(i)