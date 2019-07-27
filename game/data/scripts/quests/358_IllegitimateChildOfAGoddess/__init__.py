#    Illegitimate Child Of A Goddess version 0.1 
#    by DrLecter
#    Rate Fix by Gnat
import sys
from ru.catssoftware import Config
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

#Quest info
QUEST_NUMBER,QUEST_NAME,QUEST_DESCRIPTION = 358,"IllegitimateChildOfAGoddess","Illegitimate Child Of A Goddess"
qn = "358_IllegitimateChildOfAGoddess"

#Variables
DROP_CHANCE=12  #in %
REQUIRED=108

#Quest items
SN_SCALE = 5868

#Rewards
REWARDS=range(6329,6340,2)+range(5364,5367,2)

#Changing this value to non-zero, will turn recipes to 100% instead of 70/60%
ALT_RP_100 = 0

#Messages
default   = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"

#NPCs
OLTLIN = 30862

#Mobs
MOBS = [ 20672,20673 ]

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [SN_SCALE]

 def onEvent (self,event,st) :
    htmltext = event
    if event == "30862-5.htm" :
       st.setState(State.STARTED)
       st.set("cond","1")
       st.playSound("ItemSound.quest_accept")
    elif event == "30862-6.htm" :
       st.exitQuest(1)
    elif event == "30862-7.htm" :
       if st.getQuestItemsCount(SN_SCALE) >= REQUIRED :
          st.takeItems(SN_SCALE,REQUIRED)
          item=REWARDS[st.getRandom(len(REWARDS))]
          if ALT_RP_100: item +=1
          st.giveItems(item ,1)
          st.exitQuest(1)
          st.playSound("ItemSound.quest_finish")
       else :
          htmltext = "30862-4.htm"
    return htmltext

 def onTalk (self,npc,player):
   htmltext = default
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if id == State.CREATED :
      st.set("cond","0")
      if player.getLevel() < 63 :
         st.exitQuest(1)
         htmltext = "30862-1.htm"
      else :
         htmltext = "30862-2.htm"
   elif id == State.STARTED :
      if st.getQuestItemsCount(SN_SCALE) >= REQUIRED :
         htmltext = "30862-3.htm"
      else :
         htmltext = "30862-4.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
     st = player.getQuestState(qn)
     if not st : return 
     if st.getState() != State.STARTED : return    
     count = st.getQuestItemsCount(SN_SCALE)
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
        st.giveItems(SN_SCALE,int(numItems))
     return

QUEST       = Quest(QUEST_NUMBER, str(QUEST_NUMBER)+"_"+QUEST_NAME, QUEST_DESCRIPTION)

QUEST.addStartNpc(OLTLIN)

QUEST.addTalkId(OLTLIN)

for i in MOBS :
  QUEST.addKillId(i)