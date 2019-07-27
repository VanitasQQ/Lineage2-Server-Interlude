# Made by Renji v0.1
# Rate fix by Gnat
import sys
from ru.catssoftware import Config
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "631_DeliciousTopChoiceMeat"

#NPC
TUNATUN = 31537

#ITEMS
TOP_QUALITY_MEAT = 7546

#CHANCE
DROP_CHANCE = 100

#REWARDS
MOLD_GLUE,MOLD_LUBRICANT,MOLD_HARDENER,ENRIA,ASOFE,THONS = 4039,4040,4041,4042,4043,4044
REWARDS={"1":[MOLD_GLUE,60],"2":[ASOFE,60],"3":[THONS,60],"4":[MOLD_LUBRICANT,40],"5":[ENRIA,40],"6":[MOLD_HARDENER,20]}


class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [TOP_QUALITY_MEAT]

 def onEvent (self,event,st) :
   htmltext = event
   if event == "31537-03.htm" :
     st.set("cond","1")
     st.setState(State.STARTED)
     st.playSound("ItemSound.quest_accept")
   elif event == "31537-05.htm" and st.getQuestItemsCount(TOP_QUALITY_MEAT) == 120 :
     st.set("cond","3")
   elif event in REWARDS.keys() :
     htmltext = "31537-07.htm"
     item,qty=REWARDS[event]
     if st.getQuestItemsCount(TOP_QUALITY_MEAT) == 120 and st.getInt("cond") == 3:
       htmltext = "31537-06.htm"
       st.takeItems(TOP_QUALITY_MEAT,120)
       st.rewardItems(item,qty)
       st.playSound("ItemSound.quest_finish")
       st.exitQuest(1)
   return htmltext

 def onTalk (self,npc,player):
   st = player.getQuestState(qn)
   if st :
        npcId = npc.getNpcId()
        htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
        id = st.getState()
        cond = st.getInt("cond")
        if cond == 0 :
            if player.getLevel() >= 65 :
                htmltext = "31537-01.htm"
            else:
                htmltext = "31537-02.htm"
                st.exitQuest(1)
        elif id == State.STARTED :
            if cond == 1 :
                htmltext = "31537-01a.htm"
            elif cond == 2 and st.getQuestItemsCount(TOP_QUALITY_MEAT) == 120 :
                htmltext = "31537-04.htm"
            elif cond == 3 :
                htmltext = "31537-05.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   partyMember = self.getRandomPartyMember(player, "1")
   if not partyMember: return
   st = partyMember.getQuestState(qn)
   if st :
      if st.getState() == State.STARTED :
         count = st.getQuestItemsCount(TOP_QUALITY_MEAT)
         if st.getInt("cond") == 1 and count < 120 :
            numItems, chance = divmod(DROP_CHANCE*Config.RATE_DROP_QUEST,100)
            if st.getRandom(100) < chance : 
               numItems += 1
            if numItems :
               if count + numItems >= 120 :
                  numItems = 120 - count
                  st.playSound("ItemSound.quest_middle")
                  st.set("cond","2")
               else:
                  st.playSound("ItemSound.quest_itemget")
               st.giveItems(TOP_QUALITY_MEAT,int(numItems))
   return

QUEST       = Quest(631,qn,"Delicious Top Choice Meat")

QUEST.addStartNpc(TUNATUN)

QUEST.addTalkId(TUNATUN)

for npcId in range(21460,21468)+ range(21479,21487)+range(21498,21506) :
    QUEST.addKillId(npcId)