# Made by Mr. Have fun! Version 0.2
# Rate fix by Gnat

import sys
from ru.catssoftware import Config
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "291_RedBonnetsRevenge"

BLACK_WOLF_PELT = 1482
GRANDMAS_PEARL,GRANDMAS_MIRROR,GRANDMAS_NECKLACE,GRANDMAS_HAIRPIN = range(1502,1506)
SOE=736
DROP_CHANCE=100

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [BLACK_WOLF_PELT]

 def onEvent (self,event,st) :
    htmltext = event
    if event == "30553-03.htm" :
      st.set("cond","1")
      st.setState(State.STARTED)
      st.playSound("ItemSound.quest_accept")
    return htmltext


 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if id == State.CREATED :
     st.set("cond","0")
   if st.getInt("cond")==0 :
      if player.getLevel() < 4 :
          htmltext = "30553-01.htm"
          st.exitQuest(1)
      else:
          htmltext = "30553-02.htm"
   else :
      if st.getQuestItemsCount(BLACK_WOLF_PELT) < 40 :
        htmltext = "30553-04.htm"
      else:
          htmltext = "30553-05.htm"
          st.exitQuest(1)
          st.playSound("ItemSound.quest_finish")
          st.takeItems(BLACK_WOLF_PELT,-1)
          n = st.getRandom(100)
          if n <= 2 :
            st.giveItems(GRANDMAS_PEARL,1)
          elif n <= 20 :
            st.giveItems(GRANDMAS_MIRROR,1)
          elif n <= 45 :
            st.giveItems(GRANDMAS_NECKLACE,1)
          else :
            st.giveItems(GRANDMAS_HAIRPIN,1)
          st.giveItems(SOE,1)
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return 
   if st.getState() != State.STARTED : return
   count = st.getQuestItemsCount(BLACK_WOLF_PELT)
   if count < 40 :
     numItems, chance = divmod(DROP_CHANCE*Config.RATE_DROP_QUEST,100)
     if st.getRandom(100) < chance : 
        numItems += 1
     if numItems :
        if count + numItems >= 40 :
           numItems = 40 - count
           st.playSound("ItemSound.quest_middle")
           st.set("cond","2")
        else:
           st.playSound("ItemSound.quest_itemget")
        st.giveItems(BLACK_WOLF_PELT,int(numItems))
   return

QUEST       = Quest(291,qn,"Red Bonnets Revenge")

QUEST.addStartNpc(30553)

QUEST.addTalkId(30553)

QUEST.addKillId(20317)