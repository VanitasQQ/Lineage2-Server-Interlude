# For Sleepless Deadmen version 0.1 
# by DrLecter
#    Rate Fix by Gnat
import sys
from ru.catssoftware import Config
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

#Quest info
QUEST_NUMBER,QUEST_NAME,QUEST_DESCRIPTION = 359,"ForSleeplessDeadmen","For Sleepless Deadmen"
qn = "359_ForSleeplessDeadmen"

#Variables
DROP_CHANCE = 10 #in %

REQUIRED = 60 #how many items will be paid for a reward

#Quest items
REMAINS = 5869

#Rewards
REWARDS = range(6341,6347)+range(5494,5496)

#Messages
default = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"

#NPCs
ORVEN = 30857

#Mobs
MOBS = range(21006,21009)

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [REMAINS]

 def onEvent (self,event,st) :
    htmltext = event
    if event == "30857-6.htm" :
       st.setState(State.STARTED)
       st.set("cond","1")
       st.playSound("ItemSound.quest_accept")
    elif event == "30857-7.htm" :
       st.exitQuest(1)
       st.playSound("ItemSound.quest_finish")
    elif event == "30857-8.htm" :
       st.set("cond","1")
       st.giveItems(REWARDS[st.getRandom(len(REWARDS))] ,4)
    return htmltext

 def onTalk (self,npc,player):
   htmltext = default
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if id == State.CREATED :
      st.set("cond","0")
      if player.getLevel() < 60 :
         st.exitQuest(1)
         htmltext = "30857-1.htm"
      else :
         htmltext = "30857-2.htm"
   elif id == State.STARTED :
      cond=st.getInt("cond")
      if cond == 3 :
         htmltext = "30857-3.htm"
      elif cond == 2 and st.getQuestItemsCount(REMAINS) >= REQUIRED :
         st.takeItems(REMAINS,REQUIRED)
         st.set("cond","3")
         htmltext = "30857-4.htm"
      else :
         htmltext = "30857-5.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
     st = player.getQuestState(qn)
     if not st : return 
     if st.getState() != State.STARTED : return 
     
     count = st.getQuestItemsCount(REMAINS)
     if count < REQUIRED :
        numItems, chance = divmod(DROP_CHANCE*Config.RATE_DROP_QUEST,100)
        if st.getRandom(100) < chance : 
           numItems += 1
        if numItems :
           if count + numItems >= REQUIRED :
              numItems = REQUIRED - count
              st.playSound("ItemSound.quest_middle")
              st.set("cond","2")
           else:
              st.playSound("ItemSound.quest_itemget")
           st.giveItems(REMAINS,int(numItems))
     return

QUEST       = Quest(QUEST_NUMBER, str(QUEST_NUMBER)+"_"+QUEST_NAME, QUEST_DESCRIPTION)

QUEST.addStartNpc(ORVEN)

QUEST.addTalkId(ORVEN)

for i in MOBS :
  QUEST.addKillId(i)