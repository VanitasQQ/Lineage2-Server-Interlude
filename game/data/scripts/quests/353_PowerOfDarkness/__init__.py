# Power of Darkness - Version 0.1 by DrLecter
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "353_PowerOfDarkness"

#NPC
GALMAN=31044

#Items
STONE=5862
ADENA=57

#BASE CHANCE FOR DROP
CHANCE = 50

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [STONE]

 def onEvent (self,event,st) :
   htmltext = event
   cond = st.getInt("cond")
   if event == "31044-04.htm" and cond == 0 :
     st.set("cond","1")
     st.setState(State.STARTED)
     st.playSound("ItemSound.quest_accept")
   elif event == "31044-08.htm" :
     st.exitQuest(1)
     st.playSound("ItemSound.quest_finish")
   return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   cond = st.getInt("cond")
   if cond == 0 :
     if player.getLevel() >= 55 :
       htmltext = "31044-02.htm"
     else:
       htmltext = "31044-01.htm"
       st.exitQuest(1)
   else :
     stone=st.getQuestItemsCount(STONE)
     if not stone :
       htmltext = "31044-05.htm"
     else :
       st.rewardItems(ADENA,2500+230*stone)
       st.takeItems(STONE,-1)
       htmltext = "31044-06.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return 
   if st.getState() != State.STARTED : return 
   
   if st.getRandom(100) < CHANCE :
     st.giveItems(STONE,1)
     st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(353,qn,"Power of Darkness")

QUEST.addStartNpc(GALMAN)

QUEST.addTalkId(GALMAN)

for mob in [20284,20245,20244,20283] :
    QUEST.addKillId(mob)