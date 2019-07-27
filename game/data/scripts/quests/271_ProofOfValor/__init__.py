# Made by Mr. - Version 0.3 by DrLecter
# quest rate fix by M-095
import sys
from ru.catssoftware import Config 
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "271_ProofOfValor"

KASHA_WOLF_FANG = 1473
NECKLACE_OF_VALOR = 1507
NECKLACE_OF_COURAGE = 1506

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [KASHA_WOLF_FANG]

 def onEvent (self,event,st) :
    htmltext = event
    if event == "30577-03.htm" :
      st.set("cond","1")
      st.setState(State.STARTED)
      st.playSound("ItemSound.quest_accept")
      if st.getQuestItemsCount(NECKLACE_OF_COURAGE) or st.getQuestItemsCount(NECKLACE_OF_VALOR) :
        htmltext = "30577-07.htm"
    return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if id == State.CREATED :
     st.set("cond","0")
   if id == State.COMPLETED :
     htmltext = "30577-06.htm"
   elif st.getInt("cond") == 0 :
     if player.getRace().ordinal() != 3 :
        htmltext = "30577-00.htm"
        st.exitQuest(1)
     else :
        if player.getLevel() < 4 :
           htmltext = "30577-01.htm"
           st.exitQuest(1)
        else :
           htmltext = "30577-02.htm"
   elif st.getInt("cond") == 1 :
     htmltext = "30577-04.htm"
   elif st.getQuestItemsCount(KASHA_WOLF_FANG) >= 50 :
     st.set("cond","0")
     st.exitQuest(False)
     st.playSound("ItemSound.quest_finish")
     st.takeItems(KASHA_WOLF_FANG,-1)
     if st.getRandom(100) <= 13 :
        st.giveItems(NECKLACE_OF_VALOR,1)
     else :
        st.giveItems(NECKLACE_OF_COURAGE,1)
     htmltext = "30577-05.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return 
   if st.getState() != State.STARTED : return 
   
   count = st.getQuestItemsCount(KASHA_WOLF_FANG)
   if count < 50 :
      numItems, chance = divmod(125*Config.RATE_DROP_QUEST,100)
      if st.getRandom(100) <= chance :
         numItems += 1
      numItems = int(numItems)
      if numItems != 0 :
         if 50 <= (count + numItems) :
            numItems = 50 - count
            st.playSound("ItemSound.quest_middle")
            st.set("cond","2")
         else:
            st.playSound("ItemSound.quest_itemget")
         st.giveItems(KASHA_WOLF_FANG,numItems)
   return

QUEST       = Quest(271,qn,"Proof Of Valor")

QUEST.addStartNpc(30577)

QUEST.addTalkId(30577)

QUEST.addKillId(20475)