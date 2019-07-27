# Contributed by Kilkenny to the Official L2J Datapack Project.
# with little cleanups by DrLecter.
# Visit http://www.l2jdp.com/trac if you find a bug.
# quest rate fix by M-095
import sys
from ru.catssoftware import Config 
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "51_OFullesSpecialBait"

#NPC
OFULLE = 31572
#ITEMS
LOST_BAIT = 7622
#REWARDS
ICY_AIR_LURE = 7611
#MOB
FETTERED_SOUL = 20552

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [LOST_BAIT]

 def onEvent (self,event,st) :
   htmltext = event
   if event == "31572-03.htm" :
     st.set("cond","1")
     st.setState(State.STARTED)
     st.playSound("ItemSound.quest_accept")
   elif event == "31572-07.htm" and st.getQuestItemsCount(LOST_BAIT) == 100 :
     htmltext = "31572-06.htm"
     st.giveItems(ICY_AIR_LURE,4)
     st.takeItems(LOST_BAIT,-1)
     st.playSound("ItemSound.quest_finish")
     st.exitQuest(False)
     st.unset("cond")
   return htmltext

 def onTalk (Self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext
   npcId = npc.getNpcId()
   id = st.getState()
   cond = st.getInt("cond")
   if id == State.COMPLETED :
      htmltext = "<html><body>This quest has already been completed.</body></html>"

   elif cond == 0 :
      if player.getLevel() >= 36 :
         htmltext = "31572-01.htm"
      else:
         htmltext = "31572-02.htm"
         st.exitQuest(1)
   elif id == State.STARTED :
      if st.getQuestItemsCount(LOST_BAIT) == 100 :
         htmltext = "31572-04.htm"
      else :
         htmltext = "31572-05.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   partyMember = self.getRandomPartyMember(player,"1")
   if not partyMember : return
   st = partyMember.getQuestState(qn)
   if st :
      count = st.getQuestItemsCount(LOST_BAIT)
      if st.getInt("cond") == 1 and count < 100 :
         chance = 33 * Config.RATE_DROP_QUEST
         numItems, chance = divmod(chance,100)
         if st.getRandom(100) < chance : 
            numItems += 1
         if numItems :
            if count + numItems >= 100 :
               numItems = 100 - count
               st.playSound("ItemSound.quest_middle")
               st.set("cond","2")
            else:
               st.playSound("ItemSound.quest_itemget")
            st.giveItems(LOST_BAIT,int(numItems))
   return

QUEST       = Quest(51,qn,"O'Fulle's Special Bait")

QUEST.addStartNpc(OFULLE)
QUEST.addTalkId(OFULLE)

QUEST.addKillId(FETTERED_SOUL)