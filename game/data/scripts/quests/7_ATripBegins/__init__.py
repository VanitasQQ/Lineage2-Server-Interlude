# Created by CubicVirtuoso
# Any problems feel free to drop by #l2j-datapack on irc.freenode.net
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "7_ATripBegins"

#NPCs
MIRABEL  = 30146
ARIEL    = 30148
ASTERIOS = 30154

#ITEM
ARIELS_RECOMMENDATION = 7572

#REWARDS
SCROLL_OF_ESCAPE_GIRAN = 7559
MARK_OF_TRAVELER       = 7570

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [ARIELS_RECOMMENDATION]

 def onEvent (self,event,st) :
   htmltext = event
   if event == "30146-03.htm" :
     st.set("cond","1")
     st.setState(State.STARTED)
     st.playSound("ItemSound.quest_accept")
   elif event == "30148-02.htm" :
     st.giveItems(ARIELS_RECOMMENDATION,1)
     st.set("cond","2")
     st.playSound("ItemSound.quest_middle")
   elif event == "30154-02.htm" :
     st.takeItems(ARIELS_RECOMMENDATION,-1)
     st.set("cond","3")
     st.playSound("ItemSound.quest_middle")
   elif event == "30146-06.htm" :
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
     st.set("cond","0")
     if player.getRace().ordinal() == 1 :
       if player.getLevel() >= 3 :
         htmltext = "30146-02.htm"
       else :
         htmltext = "<html><body>Quest for characters level 3 above.</body></html>"
         st.exitQuest(1)
     else :
       htmltext = "30146-01.htm"
       st.exitQuest(1)
   elif id == State.STARTED :
       if npcId == ARIEL and cond :
         if st.getQuestItemsCount(ARIELS_RECOMMENDATION) == 0 :
           htmltext = "30148-01.htm"
         else :
           htmltext = "30148-03.htm"
       elif npcId == MIRABEL and cond == 1 :
         htmltext = "30146-04.htm"
       elif npcId == ASTERIOS and cond == 2 and st.getQuestItemsCount(ARIELS_RECOMMENDATION) > 0 :
         htmltext = "30154-01.htm"
       elif npcId == ASTERIOS and cond == 3 :
         htmltext = "30154-03.htm"
       elif npcId == MIRABEL and cond == 3 :
         htmltext = "30146-05.htm"
   return htmltext

QUEST     = Quest(7,qn,"A Trip Begins")

QUEST.addStartNpc(MIRABEL)

QUEST.addTalkId(MIRABEL)
QUEST.addTalkId(ARIEL)
QUEST.addTalkId(ASTERIOS)