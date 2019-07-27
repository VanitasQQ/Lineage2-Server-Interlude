# Created by DraX on 2005.08.08
import sys
from ru.catssoftware.gameserver.model.quest        import State
from ru.catssoftware.gameserver.model.quest        import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "30154_asterios_occupation_change"

HIERARCH_ASTERIOS = 30154

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
   # Elfs got accepted
   if npcId == HIERARCH_ASTERIOS and Race in [Race.Elf]:
     if ClassId in [ClassId.elvenFighter]:
       return "30154-01.htm"
     if ClassId in [ClassId.elvenMage]:
       return "30154-02.htm"
     if ClassId in [ClassId.elvenWizard, ClassId.oracle, ClassId.elvenKnight, ClassId.elvenScout]:
       st.exitQuest(1)
       return "30154-12.htm"
     else:
       st.exitQuest(1)
       return "30154-13.htm"
   # All other Races must be out
   if npcId == HIERARCH_ASTERIOS and Race in [Race.Dwarf, Race.Human, Race.Darkelf, Race.Orc]:
     st.exitQuest(1)
     return "30154-11.htm"

QUEST     = Quest(30154,qn,"village_master")

QUEST.addStartNpc(30154)

QUEST.addTalkId(30154)