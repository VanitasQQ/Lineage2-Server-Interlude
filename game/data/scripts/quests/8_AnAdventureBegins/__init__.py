# Created by CubicVirtuoso
# Any problems feel free to drop by #l2j-datapack on irc.freenode.net
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "8_AnAdventureBegins"

#NPCs
JASMINE = 30134
ROSELYN = 30355
HARNE   = 30144

#ITEM
ROSELYNS_NOTE = 7573

#REWARDS
SCROLL_OF_ESCAPE_GIRAN = 7559
MARK_OF_TRAVELER       = 7570

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [ROSELYNS_NOTE]

 def onEvent (self,event,st) :
   htmltext = event
   if event == "30134-03.htm" :
     st.set("cond","1")
     st.setState(State.STARTED)
     st.playSound("ItemSound.quest_accept")
   elif event == "30355-02.htm" :
     st.giveItems(ROSELYNS_NOTE,1)
     st.set("cond","2")
     st.playSound("ItemSound.quest_middle")
   elif event == "30144-02.htm" :
     st.takeItems(ROSELYNS_NOTE,-1)
     st.set("cond","3")
     st.playSound("ItemSound.quest_middle")
   elif event == "30134-06.htm" :
     st.giveItems(SCROLL_OF_ESCAPE_GIRAN,1)
     st.giveItems(MARK_OF_TRAVELER,1)
     st.unset("cond")
     st.exitQuest(False)
     st.playSound("ItemSound.quest_finish")
   return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext
   npcId = npc.getNpcId()
   cond = st.getInt("cond")
   id = st.getState()

   if id == State.COMPLETED :
     htmltext = "<html><body>This quest has already been completed.</body></html>"
   elif id == State.CREATED :
     if player.getRace().ordinal() == 2 :
       if player.getLevel() >= 3 :
         htmltext = "30134-02.htm"
       else :
         htmltext = "<html><body>Quest for characters level 3 and above.</body></html>"
         st.exitQuest(1)
     else :
       htmltext = "30134-01.htm"
       st.exitQuest(1)
   elif id == State.STARTED :
       if npcId == ROSELYN and cond :
         if st.getQuestItemsCount(ROSELYNS_NOTE) == 0 :
           htmltext = "30355-01.htm"
         else :
           htmltext = "30355-03.htm"
       elif npcId == JASMINE and cond == 1 :
         htmltext = "30134-04.htm"
       elif npcId == HARNE and cond == 2 and st.getQuestItemsCount(ROSELYNS_NOTE) > 0 :
         htmltext = "30144-01.htm"
       elif npcId == JASMINE and cond == 3 :
         htmltext = "30134-05.htm"
   return htmltext

QUEST     = Quest(8,qn,"An Adventure Begins")

QUEST.addStartNpc(JASMINE)

QUEST.addTalkId(JASMINE)
QUEST.addTalkId(ROSELYN)
QUEST.addTalkId(HARNE)