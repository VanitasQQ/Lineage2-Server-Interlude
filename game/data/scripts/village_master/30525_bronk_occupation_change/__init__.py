# Created by DraX on 2005.08.08 modified by Ariakas on 2005.09.19
import sys
from ru.catssoftware.gameserver.model.quest        import State
from ru.catssoftware.gameserver.model.quest        import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "30525_bronk_occupation_change"

HEAD_BLACKSMITH_BRONK = 30525

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
   # Dwarfs got accepted
   if npcId == HEAD_BLACKSMITH_BRONK and Race in [Race.Dwarf]:
     if ClassId in [ClassId.dwarvenFighter]:
       htmltext = "30525-01.htm"
       return htmltext
     if ClassId in [ClassId.artisan]:
       htmltext = "30525-05.htm"
       st.exitQuest(1)
       return htmltext
     if ClassId in [ClassId.warsmith]:
       htmltext = "30525-06.htm"
       st.exitQuest(1)
       return htmltext
     if ClassId in [ClassId.scavenger, ClassId.bountyHunter]:
       htmltext = "30525-07.htm"
       st.exitQuest(1)
       return htmltext
   # All other Races must be out
   if npcId == HEAD_BLACKSMITH_BRONK and Race in [Race.Orc, Race.Darkelf, Race.Elf, Race.Human]:
     st.exitQuest(1)
     return "30525-07.htm"

QUEST   = Quest(30525,qn,"village_master")

QUEST.addStartNpc(30525)

QUEST.addTalkId(30525)