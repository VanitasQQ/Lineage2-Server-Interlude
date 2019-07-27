# Made by disKret
import sys
from ru.catssoftware.tools.random import Rnd
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "34_InSearchOfClothes"

SPINNERET = 7528
SUEDE = 1866
THREAD = 1868
SPIDERSILK = 1493
MYSTERIOUS_CLOTH = 7076

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [SPINNERET,SPIDERSILK]

 def onEvent (self,event,st) :
   htmltext = event
   cond = st.getInt("cond")
   if event == "30088-1.htm" and cond == 0:
     st.set("cond","1")
     st.setState(State.STARTED)
     st.playSound("ItemSound.quest_accept")
   if event == "30294-1.htm" and cond == 1 :
     st.set("cond","2")
   if event == "30088-3.htm" and cond == 2:
     st.set("cond","3")
   if event == "30165-1.htm" and cond == 3:
     st.set("cond","4")
   if event == "30165-3.htm" and cond == 5:
     if st.getQuestItemsCount(SPINNERET) == 10 :
       st.takeItems(SPINNERET,10)
       st.giveItems(SPIDERSILK,1)
       st.set("cond","6")
     else :
       htmltext = "You don't have enough materials"
   if event == "30088-5.htm" and cond == 6 :
     if st.getQuestItemsCount(SUEDE) >= 3000 and st.getQuestItemsCount(THREAD) >= 5000 and st.getQuestItemsCount(SPIDERSILK) == 1 :
       st.takeItems(SUEDE,3000)
       st.takeItems(THREAD,5000)
       st.takeItems(SPIDERSILK,1)
       st.giveItems(MYSTERIOUS_CLOTH,1)
       st.playSound("ItemSound.quest_finish")
       st.unset("cond")
       st.exitQuest(False)
     else :
       htmltext = "You don't have enough materials"
   return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext
   npcId = npc.getNpcId()
   id = st.getState()
   cond = st.getInt("cond")
   if id == State.COMPLETED :
     htmltext = "<html><body>This quest has already been completed.</body></html>"
   elif npcId == 30088 and cond == 0 and st.getQuestItemsCount(MYSTERIOUS_CLOTH) == 0 : 
     fwear = player.getQuestState("37_PleaseMakeMeFormalWear")
     if fwear :
       if fwear.get("cond") == "6" :
         htmltext = "30088-0.htm"
       else :
         st.exitQuest(1)
     else :
       st.exitQuest(1)
   elif id == State.STARTED :    
       if npcId == 30294 and cond == 1 :
         htmltext = "30294-0.htm"
       elif npcId == 30088 and cond == 2 :
         htmltext = "30088-2.htm"
       elif npcId == 30165 and cond == 3 :
         htmltext = "30165-0.htm"
       elif npcId == 30165 and cond == 5 :
         htmltext = "30165-2.htm"
       elif npcId == 30088 and cond == 6 :
          htmltext = "30088-4.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   partyMember = self.getRandomPartyMember(player,"4")
   if not partyMember : return

   st = partyMember.getQuestState(qn)
   if not st : return 
   if st.getState() != State.STARTED : return

   count = st.getQuestItemsCount(SPINNERET)
   if count < 10 :
     st.giveItems(SPINNERET,1)
     if count == 9 :
       st.playSound("ItemSound.quest_middle")
       st.set("cond","5")
     else :
       st.playSound("ItemSound.quest_itemget")
   return

QUEST = Quest(34,qn,"In Search of Clothes")

QUEST.addStartNpc(30088)

QUEST.addTalkId(30088)
QUEST.addTalkId(30165)
QUEST.addTalkId(30294)

QUEST.addKillId(20560)
QUEST.addKillId(20561)