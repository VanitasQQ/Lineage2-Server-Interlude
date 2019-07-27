# Made by disKret
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "360_PlunderTheirSupplies"

#NPC
COLEMAN = 30873

#MOBS
TAIK_SEEKER = 20666
TAIK_LEADER = 20669

#QUEST ITEMS
SUPPLY_ITEM = 5872
SUSPICIOUS_DOCUMENT = 5871
RECIPE_OF_SUPPLY = 5870

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [RECIPE_OF_SUPPLY, SUPPLY_ITEM, SUSPICIOUS_DOCUMENT]

 def onEvent (self,event,st) :
   htmltext = event
   if event == "30873-2.htm" :
     st.set("cond","1")
     st.setState(State.STARTED)
     st.playSound("ItemSound.quest_accept")
   elif event == "30873-6.htm" :
     st.takeItems(SUPPLY_ITEM,-1)
     st.takeItems(SUSPICIOUS_DOCUMENT,-1)
     st.takeItems(RECIPE_OF_SUPPLY,-1)
     st.playSound("ItemSound.quest_finish")
     st.exitQuest(1)
   return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   cond=st.getInt("cond")
   supplies = st.getQuestItemsCount(SUPPLY_ITEM)
   if cond == 0 :
     if player.getLevel() >= 52 :
       htmltext = "30873-0.htm"
     else:
       htmltext = "<html><body>Quest for characters level 52 or above.</body></html>"
       st.exitQuest(1)
   elif not supplies :
     htmltext = "30873-3.htm"
   elif supplies :
     DOCS = st.getQuestItemsCount(RECIPE_OF_SUPPLY)*6000
     REWARD = 6000+(supplies*100)+DOCS
     st.takeItems(SUPPLY_ITEM,-1)
     st.takeItems(RECIPE_OF_SUPPLY,-1)
     st.rewardItems(57,REWARD)
     htmltext = "30873-5.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return 
   if st.getState() != State.STARTED : return 
   
   st.giveItems(SUPPLY_ITEM,1)  
   if st.getRandom(10) == 1 :        # % chance is custom
     st.giveItems(SUSPICIOUS_DOCUMENT,1)
     if st.getQuestItemsCount(SUSPICIOUS_DOCUMENT) == 5 :
       st.takeItems(SUSPICIOUS_DOCUMENT,5)
       st.giveItems(RECIPE_OF_SUPPLY,1)
       st.playSound("ItemSound.quest_itemget")
   st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(360,qn,"Plunder Their Supplies")

QUEST.addStartNpc(COLEMAN)

QUEST.addTalkId(COLEMAN)

QUEST.addKillId(TAIK_SEEKER)
QUEST.addKillId(TAIK_LEADER)