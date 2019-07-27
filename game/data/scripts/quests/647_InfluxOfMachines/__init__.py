# Fix by Cromir & Black Night for Kilah
# Quest: Influx of Machines
# Rate Fix by Gnat
import sys
from ru.catssoftware import Config
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "647_InfluxOfMachines"

#Settings: drop chance in %
DROP_CHANCE=30

#Set this to non-zero to use 100% recipes as reward instead of default 60%
ALT_RP_100=0

DESTROYED_GOLEM_SHARD = 8100
RECIPES_60= [4963,4964,4965,4966,4967,4968,4969,4970,4971,4972,5000,5001,5002,5003,5004,5005,5006,5007]+[8298, 8306, 8310, 8312, 8322, 8324]
RECIPES_100= range(4181,4200)+[8297, 8305, 8309, 8311, 8321, 8323]

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [DESTROYED_GOLEM_SHARD]

 def onEvent (self,event,st) :
    htmltext = event
    if event == "32069-02.htm" :
       st.set("cond","1")
       st.setState(State.STARTED)
       st.playSound("ItemSound.quest_accept")
    elif event == "32069-06.htm" :
       if st.getQuestItemsCount(DESTROYED_GOLEM_SHARD) >= 500:
          st.takeItems(DESTROYED_GOLEM_SHARD,500)
          if ALT_RP_100 == 0 :
            item = RECIPES_60[st.getRandom(len(RECIPES_60))]
          else :
            item = RECIPES_100[st.getRandom(len(RECIPES_100))]
          st.giveItems(item,1)
          st.playSound("ItemSound.quest_finish")
          st.exitQuest(1)
       else:
          htmltext = "32069-04.htm"
    return htmltext

 def onTalk (self, npc, player):
    st = player.getQuestState(qn)
    htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
    if st :
        npcId = npc.getNpcId()
        cond = st.getInt("cond")
        count = st.getQuestItemsCount(DESTROYED_GOLEM_SHARD)
        if cond == 0 :
            if player.getLevel() >= 46 :
                htmltext = "32069-01.htm"
            else:
                htmltext = "32069-03.htm"
                st.exitQuest(1)
        elif st.getState() == State.STARTED :
            if cond==1 or count < 500 :
                htmltext = "32069-04.htm"
            elif cond==2 and count >= 500 :
                htmltext = "32069-05.htm"
    return htmltext

 def onKill(self,npc,player,isPet):
    partyMember = self.getRandomPartyMember(player,"1")
    if not partyMember: return
    st = partyMember.getQuestState(qn)
    if st :
        if st.getState() == State.STARTED :
            npcId = npc.getNpcId()
            cond = st.getInt("cond")
            count = st.getQuestItemsCount(DESTROYED_GOLEM_SHARD)
            if cond == 1 and count < 500:
               numItems, chance = divmod(DROP_CHANCE*Config.RATE_DROP_QUEST,100)
               if st.getRandom(100) < chance :
                  numItems += 1
               if numItems :
                  if count + numItems >= 500 :
                     numItems = 500 - count
                     st.playSound("ItemSound.quest_middle")
                     st.set("cond","2")
                  else:
                     st.playSound("ItemSound.quest_itemget")
                  st.giveItems(DESTROYED_GOLEM_SHARD,int(numItems))
    return

QUEST       = Quest(647,qn,"Influx of Machines")

QUEST.addStartNpc(32069)

QUEST.addTalkId(32069)

for i in range(22052,22079):
   QUEST.addKillId(i)