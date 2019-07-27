# Created by DraX on 2005.08.08
import sys
from ru.catssoftware.gameserver.model.quest        import State
from ru.catssoftware.gameserver.model.quest        import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "30358_thifiell_occupation_change"

TETRARCH_THIFIELL = 30358

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
   # DarkElfs got accepted
   if npcId == TETRARCH_THIFIELL and Race in [Race.Darkelf]:
     if ClassId in [ClassId.darkFighter]:
       return "30358-01.htm"
     if ClassId in [ClassId.darkMage]:
       return "30358-02.htm"
     if ClassId in [ClassId.darkWizard, ClassId.shillienOracle, ClassId.palusKnight, ClassId.assassin]:
       st.exitQuest(1)
       return "30358-12.htm"
     else:
       st.exitQuest(1)
       return "30358-13.htm"
   # All other Races must be out
   if npcId == TETRARCH_THIFIELL and Race in [Race.Dwarf, Race.Human, Race.Elf, Race.Orc]:
     st.exitQuest(1)
     return "30358-11.htm"

QUEST     = Quest(30358,qn,"village_master")

QUEST.addStartNpc(30358)

QUEST.addTalkId(30358)