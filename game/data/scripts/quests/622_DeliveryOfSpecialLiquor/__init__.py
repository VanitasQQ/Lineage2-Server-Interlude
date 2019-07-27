# Made by disKret
# quest rate fix by M-095
import sys
from ru.catssoftware import Config 
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "622_DeliveryOfSpecialLiquor"

#NPC
LIETTA = 31267
JEREMY = 31521
PULIN = 31543
NAFF = 31544
CROCUS = 31545
KUBER = 31546
BEORIN = 31547

#QUEST ITEMS
SPECIAL_DRINK = 7197
FEE_OF_DRINK = 7198

#REWARDS
ADENA = 57
HASTE_POTION = 734

#Chance to get an S-grade random recipe instead of just adena and haste potion
RPCHANCE=10
#Change this value to 1 if you wish 100% recipes, default 70%
ALT_RP100=0

#MESSAGES
default="<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [SPECIAL_DRINK, FEE_OF_DRINK]

 def onEvent (self,event,st) :
   htmltext = event
   cond=st.getInt("cond")
   if event == "31521-1.htm" :
     if cond==0:
       st.set("cond","1")
       st.setState(State.STARTED)
       st.giveItems(SPECIAL_DRINK,5)
       st.playSound("ItemSound.quest_accept")
     else:
       htmltext=default
   elif event == "31547-1.htm" :
     if st.getQuestItemsCount(SPECIAL_DRINK):
       if cond==1:
         st.takeItems(SPECIAL_DRINK,1)
         st.giveItems(FEE_OF_DRINK,1)
         st.set("cond","2")
       else:
         htmltext=default
     else:
       htmltext="LMFAO!"
       st.exitQuest(1)
   elif event == "31546-1.htm" :
     if st.getQuestItemsCount(SPECIAL_DRINK):
       if cond==2:
         st.takeItems(SPECIAL_DRINK,1)
         st.giveItems(FEE_OF_DRINK,1)
         st.set("cond","3")
       else:
         htmltext=default
     else:
       htmltext="LMFAO!"
       st.exitQuest(1)
   elif event == "31545-1.htm" :
     if st.getQuestItemsCount(SPECIAL_DRINK):
       if cond==3:
         st.takeItems(SPECIAL_DRINK,1)
         st.giveItems(FEE_OF_DRINK,1)
         st.set("cond","4")
       else:
         htmltext=default
     else:
       htmltext="LMFAO!"
       st.exitQuest(1)
   elif event == "31544-1.htm" :
     if st.getQuestItemsCount(SPECIAL_DRINK):
       if cond==4:
         st.takeItems(SPECIAL_DRINK,1)
         st.giveItems(FEE_OF_DRINK,1)
         st.set("cond","5")
       else:
         htmltext=default
     else:
       htmltext="LMFAO!"
       st.exitQuest(1)
   elif event == "31543-1.htm" :
     if st.getQuestItemsCount(SPECIAL_DRINK):
       if cond==5:
         st.takeItems(SPECIAL_DRINK,1)
         st.giveItems(FEE_OF_DRINK,1)
         st.set("cond","6")
       else:
         htmltext=default
     else:
       htmltext="LMFAO!"
       st.exitQuest(1)
   elif event == "31521-3.htm" :
     st.set("cond","7")
   elif event == "31267-2.htm" :
     if st.getQuestItemsCount(FEE_OF_DRINK) == 5:
        st.takeItems(FEE_OF_DRINK,5)
        random = st.getRandom(1000)
        if random < 800 :
          st.giveItems(ADENA,18800)
          st.giveItems(HASTE_POTION,int(Config.RATE_QUESTS_REWARD_ITEMS))
        elif random < 880 :
          st.giveItems(6849+ALT_RP100,1)
        elif random < 960 :
          st.giveItems(6847+ALT_RP100,1)
        elif random < 1000 :
          st.giveItems(6851+ALT_RP100,1)
        st.playSound("ItemSound.quest_finish")
        st.exitQuest(1)
     else:
        htmltext=default
   return htmltext

 def onTalk (self,npc,player):
   htmltext = default
   st = player.getQuestState(qn)
   if st :
        npcId = npc.getNpcId()
        id = st.getState()
        if id == State.CREATED :
             st.set("cond","0")
        cond = st.getInt("cond")
        if npcId == 31521 and cond == 0 :
         if player.getLevel() >= 68 :
               htmltext = "31521-0.htm"
         else:
               st.exitQuest(1)
        elif id == State.STARTED :
           if npcId == 31547 and cond == 1 and st.getQuestItemsCount(SPECIAL_DRINK) :
                 htmltext = "31547-0.htm"
           elif npcId == 31546 and cond == 2 and st.getQuestItemsCount(SPECIAL_DRINK) :
                 htmltext = "31546-0.htm"
           elif npcId == 31545 and cond == 3 and st.getQuestItemsCount(SPECIAL_DRINK) :
                 htmltext = "31545-0.htm"
           elif npcId == 31544 and cond == 4 and st.getQuestItemsCount(SPECIAL_DRINK) :
                 htmltext = "31544-0.htm"
           elif npcId == 31543 and cond == 5 and st.getQuestItemsCount(SPECIAL_DRINK) :
                 htmltext = "31543-0.htm"
           elif npcId == 31521 and cond == 6 and st.getQuestItemsCount(FEE_OF_DRINK) == 5 :
                 htmltext = "31521-2.htm"
           elif npcId == 31521 and cond == 7 and st.getQuestItemsCount(FEE_OF_DRINK) == 5 :
                 htmltext = "31521-4.htm"
           elif npcId == 31267 and cond == 7 and st.getQuestItemsCount(FEE_OF_DRINK) == 5 :
                 htmltext = "31267-1.htm"
   return htmltext

QUEST       = Quest(622,qn,"Delivery of special liquor")

QUEST.addStartNpc(31521)

for i in range(31543,31548)+[31267,31521]:
    QUEST.addTalkId(i)