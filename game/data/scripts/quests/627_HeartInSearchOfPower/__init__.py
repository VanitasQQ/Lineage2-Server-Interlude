# Made by disKret
# Rate fix by Gnat

import sys
from ru.catssoftware import Config
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "627_HeartInSearchOfPower"

#NPC
M_NECROMANCER,ENFEUX = 31518,31519

#ITEMS
SEAL_OF_LIGHT,BEAD_OF_OBEDIENCE,GEM_OF_SAINTS = 7170,7171,7172

#CHANCE
DROP_CHANCE = 90

#REWARDS
ADENA = 57
MOLD_HARDENER,ENRIA,ASOFE,THONS = 4041,4042,4043,4044

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [BEAD_OF_OBEDIENCE]

 def onEvent (self,event,st) :
   htmltext = event
   if event == "31518-1.htm" :
     st.set("cond","1")
     st.setState(State.STARTED)
     st.playSound("ItemSound.quest_accept")
   elif event == "31518-3.htm" :
     st.takeItems(BEAD_OF_OBEDIENCE,300)
     st.giveItems(SEAL_OF_LIGHT,1)
     st.set("cond","3")
   elif event == "31519-1.htm" :
     st.takeItems(SEAL_OF_LIGHT,1)
     st.giveItems(GEM_OF_SAINTS,1)
     st.set("cond","4")
   elif event == "31518-5.htm" and st.getQuestItemsCount(GEM_OF_SAINTS) == 1 :
     st.takeItems(GEM_OF_SAINTS,1)
     st.set("cond","5")
   else :
     if event == "31518-6.htm" :
       st.rewardItems(ADENA,100000)
     elif event == "31518-7.htm" :
       st.rewardItems(ASOFE,52)
       st.rewardItems(ADENA,6400)
     elif event == "31518-8.htm" :
       st.rewardItems(THONS,52)
       st.rewardItems(ADENA,6400)
     elif event == "31518-9.htm" :
       st.rewardItems(ENRIA,24)
       st.rewardItems(ADENA,13600)
     elif event == "31518-10.htm" :
       st.rewardItems(MOLD_HARDENER,12)
       st.rewardItems(ADENA,17200)
     st.playSound("ItemSound.quest_finish")
     st.exitQuest(1)
   return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if st :
     npcId = npc.getNpcId()
     id = st.getState()
     cond = st.getInt("cond")
     if cond == 0 :
       if player.getLevel() >= 60 : # and player.getLevel() <= 71
         htmltext = "31518-0.htm"
       else:
         htmltext = "31518-0a.htm"
         st.exitQuest(1)
     elif id == State.STARTED :
       if npcId == M_NECROMANCER :
          if cond == 1 :
            htmltext = "31518-1a.htm"
          elif st.getQuestItemsCount(BEAD_OF_OBEDIENCE) == 300 :
            htmltext = "31518-2.htm"
          elif st.getQuestItemsCount(GEM_OF_SAINTS) :
            htmltext = "31518-4.htm"
          elif cond == 5 :
            htmltext = "31518-5.htm"
       elif npcId == ENFEUX and st.getQuestItemsCount(SEAL_OF_LIGHT) :
         htmltext = "31519-0.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
  st = player.getQuestState(qn)
  if st :
    if st.getState() == State.STARTED :
      count = st.getQuestItemsCount(BEAD_OF_OBEDIENCE)
      if st.getInt("cond") == 1 and count < 300 :
        numItems, chance = divmod(DROP_CHANCE*Config.RATE_DROP_QUEST,100)
        if st.getRandom(100) < chance : 
           numItems += 1
        if numItems :
           if count + numItems >= 300 :
              numItems = 300 - count
              st.playSound("ItemSound.quest_middle")
              st.set("cond","2")
           else:
              st.playSound("ItemSound.quest_itemget")
           st.giveItems(BEAD_OF_OBEDIENCE,int(numItems))
  return

QUEST       = Quest(627,qn,"Heart In Search Of Power")

QUEST.addStartNpc(31518)

QUEST.addTalkId(31518)
QUEST.addTalkId(31519)

for mobs in range(21520,21541):
  QUEST.addKillId(mobs)