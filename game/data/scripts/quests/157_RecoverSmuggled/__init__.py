# Made by Mr. - Version 0.3 by DrLecter
# quest rate fix by M-095
import sys
from ru.catssoftware import Config 
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "157_RecoverSmuggled"

ADAMANTITE_ORE = 1024
BUCKLER = 20

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [ADAMANTITE_ORE]

 def onEvent (self,event,st) :
    htmltext = event
    if event == "1" :
       st.set("cond","1")
       st.setState(State.STARTED)
       st.playSound("ItemSound.quest_accept")
       htmltext = "30005-05.htm"
    elif event == "157_1" :
       htmltext = "30005-04.htm"
    return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext

   id = st.getState()
   cond = st.getInt("cond")
   if id == State.COMPLETED :
     htmltext = "<html><body>This quest has already been completed.</body></html>"

   elif cond == 0 :
     if player.getLevel() >= 5 :
        htmltext = "30005-03.htm"
     else :
        htmltext = "30005-02.htm"
        st.exitQuest(1)
   elif cond :
     if st.getQuestItemsCount(ADAMANTITE_ORE)>=20 :
        st.takeItems(ADAMANTITE_ORE,-1)
        st.exitQuest(False)
        st.playSound("ItemSound.quest_finish")
        st.giveItems(BUCKLER,1)
        htmltext = "30005-07.htm"
     else :
        htmltext = "30005-06.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return 
   if st.getState() != State.STARTED : return
   adamantite = st.getQuestItemsCount(ADAMANTITE_ORE)
   if st.getInt("cond") == 1 and adamantite < 20 :
       npcId = npc.getNpcId()
       numItems, chance = divmod(40*Config.RATE_DROP_QUEST,100)
       if st.getRandom(100) <= chance :
          numItems += 1
       numItems = int(numItems)   
       if numItems != 0 :
          if 20 <= (adamantite + numItems) :
             numItems = 20 - adamantite
             st.playSound("ItemSound.quest_middle")
             st.set("cond","2")
          else:
             st.playSound("ItemSound.quest_itemget")
          st.giveItems(ADAMANTITE_ORE,numItems)
   return

QUEST       = Quest(157,qn,"Recover Smuggled Goods")

QUEST.addStartNpc(30005)

QUEST.addTalkId(30005)
QUEST.addKillId(20121)