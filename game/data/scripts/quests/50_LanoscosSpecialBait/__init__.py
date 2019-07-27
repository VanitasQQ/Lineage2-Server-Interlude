# This is essentially a DrLecter's copy&paste from
# a Kilkenny's contribution to the Official L2J Datapack Project.
# Visit http://www.l2jdp.com/trac if you find a bug.
#quest rate fix by M-095
import sys
from ru.catssoftware import Config 
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "50_LanoscosSpecialBait"

#NPC
LANOSCO = 31570
#ITEMS
ESSENCE_OF_WIND = 7621
#REWARDS
WIND_FISHING_LURE = 7610
#MOB
SINGING_WIND = 21026

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [ESSENCE_OF_WIND]

 def onEvent (self,event,st) :
   htmltext = event
   if event == "31570-03.htm" :
     st.set("cond","1")
     st.setState(State.STARTED)
     st.playSound("ItemSound.quest_accept")
   elif event == "31570-07.htm" and st.getQuestItemsCount(ESSENCE_OF_WIND) == 100 :
     htmltext = "31570-06.htm"
     st.giveItems(WIND_FISHING_LURE,4)
     st.takeItems(ESSENCE_OF_WIND,-1)
     st.playSound("ItemSound.quest_finish")
     st.unset("cond")
     st.exitQuest(False)
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
      if player.getLevel() >= 27 :
         htmltext = "31570-01.htm"
      else:
         htmltext = "31570-02.htm"
         st.exitQuest(1)
   elif id == State.STARTED :
      if st.getQuestItemsCount(ESSENCE_OF_WIND) == 100 :
         htmltext = "31570-04.htm"
      else :
         htmltext = "31570-05.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   partyMember = self.getRandomPartyMember(player,"1")
   if not partyMember : return
   st = partyMember.getQuestState(qn)
   if st :
      count = st.getQuestItemsCount(ESSENCE_OF_WIND)
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
            st.giveItems(ESSENCE_OF_WIND,int(numItems))
   return

QUEST       = Quest(50,qn,"Lanosco's Special Bait")

QUEST.addStartNpc(LANOSCO)
QUEST.addTalkId(LANOSCO)

QUEST.addKillId(SINGING_WIND)