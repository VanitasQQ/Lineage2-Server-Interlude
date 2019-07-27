#    Made by Kerb
#    Rate Fix by Gnat
import sys
from ru.catssoftware import Config
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "645_GhostsOfBatur"

#Drop rate
DROP_CHANCE = 75

#Npc
KARUDA = 32017

#Items
GRAVE_GOODS = 8089

#Rewards
REWARDS={
    "BDH":[1878,72],
    "CKS":[1879, 28],
    "STL":[1880, 16],
    "CBP":[1881, 24],
    "LTR":[1882,40],
    "STM":[1883, 8]
    }

#Mobs
MOBS = [ 22007,22009,22010,22011,22012,22013,22014,22015,22016 ]

class Quest (JQuest) :
 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [GRAVE_GOODS]

 def onEvent (self,event,st) :
   htmltext = event
   if event == "32017-03.htm" :
      if st.getPlayer().getLevel() < 23 :
         htmltext = "32017-02.htm"
         st.exitQuest(1)
      else :
         st.set("cond","1")
         st.setState(State.STARTED)
         st.playSound("ItemSound.quest_accept")
   elif event in REWARDS.keys() :
      if st.getQuestItemsCount(GRAVE_GOODS) == 180 :
         item,qty = REWARDS[event]
         st.takeItems(GRAVE_GOODS,-1)
         st.rewardItems(item,qty)
         st.playSound("ItemSound.quest_finish")
         st.exitQuest(1)
         htmltext = "32017-07.htm"
      else :
         htmltext = "32017-04.htm"
   return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext
   npcId = npc.getNpcId()
   id = st.getState()
   cond = st.getInt("cond")
   if cond == 0 :
      htmltext = "32017-01.htm"
   elif cond == 1 :
      htmltext = "32017-04.htm"
   elif cond == 2 :
      if st.getQuestItemsCount(GRAVE_GOODS) == 180 :
         htmltext = "32017-05.htm"
      else :
         htmltext = "32017-01.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
  partyMember = self.getRandomPartyMember(player,"1")
  if not partyMember: return
  st = partyMember.getQuestState(qn)
  if st :
    count = st.getQuestItemsCount(GRAVE_GOODS)
    if st.getInt("cond") == 1 and count < 180 :
      numItems, chance = divmod(DROP_CHANCE*Config.RATE_DROP_QUEST,100)
      if st.getRandom(100) < chance :
         numItems += 1
      if numItems :
         if count + numItems >= 180 :
            numItems = 180 - count
            st.playSound("ItemSound.quest_middle")
            st.set("cond","2")
         else:
            st.playSound("ItemSound.quest_itemget")
         st.giveItems(GRAVE_GOODS,int(numItems))
  return

QUEST       = Quest(645, qn, "Ghosts of Batur")

QUEST.addStartNpc(KARUDA)

QUEST.addTalkId(KARUDA)

for i in MOBS :
  QUEST.addKillId(i)