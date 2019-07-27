# Created by DraX on 2005.08.08 modified by Ariakas on 2005.09.19
import sys
from ru.catssoftware.gameserver.model.quest        import State
from ru.catssoftware.gameserver.model.quest        import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "30565_kakai_occupation_change"

KAKAI_LORD_OF_FLAME = 30565

class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onEvent (self,event,st):
   htmltext = event
   return htmltext

 def onTalk (Self,npc,player):  
   st = player.getQuestState(qn)
   npcId = npc.getNpcId()
   Race = st.getPlayer().getRace()
   ClassId = st.getPlayer().getClassId()
   # Orcs got accepted
   if npcId == KAKAI_LORD_OF_FLAME and Race in [Race.Orc]:
     if ClassId in [ClassId.orcFighter]:
       htmltext = "30565-01.htm"
       return htmltext
     if ClassId in [ClassId.orcRaider, ClassId.orcMonk, ClassId.orcShaman]:
       htmltext = "30565-09.htm"
       st.exitQuest(1)
       return htmltext
     if ClassId in [ClassId.destroyer, ClassId.tyrant, ClassId.overlord, ClassId.warcryer]:
       htmltext = "30565-10.htm"
       st.exitQuest(1)
       return htmltext
     if ClassId in [ClassId.orcMage]:
       htmltext = "30565-06.htm"
       return htmltext
   # All other Races must be out
   if npcId == KAKAI_LORD_OF_FLAME and Race in [Race.Dwarf, Race.Darkelf, Race.Elf, Race.Human]:
     st.exitQuest(1)
     return "30565-11.htm"

QUEST   = Quest(30565,qn,"village_master")

QUEST.addStartNpc(30565)

QUEST.addTalkId(30565)