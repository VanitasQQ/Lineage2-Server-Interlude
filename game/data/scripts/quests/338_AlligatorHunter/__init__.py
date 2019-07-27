# Made by mtrix
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "338_AlligatorHunter"

ADENA = 57
ALLIGATOR = 20135
ALLIGATOR_PELTS = 4337
CHANCE = 90

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [ALLIGATOR_PELTS]

 def onEvent (self,event,st) :
     htmltext = event
     if event == "30892-00a.htm" :
         htmltext = "30892-00a.htm"
         st.exitQuest(1)
     elif event == "30892-02.htm" :
         st.setState(State.STARTED)
         st.set("cond","1")
         st.playSound("ItemSound.quest_accept")
     elif event == "2" :
         st.exitQuest(1)
         st.playSound("ItemSound.quest_finish")
     return htmltext

 def onTalk (self,npc,player):
     htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
     st = player.getQuestState(qn)
     if not st : return htmltext

     npcId = npc.getNpcId()
     id = st.getState()
     level = player.getLevel()
     cond = st.getInt("cond")
     bonus = 3430
     amount = st.getQuestItemsCount(ALLIGATOR_PELTS)
     if id == State.CREATED :
        if level >= 40 :
           htmltext = "30892-01.htm"
        else :
           htmltext = "30892-00.htm"
     elif cond==1 :
        if amount :
           htmltext = "30892-03.htm"
           st.rewardItems(ADENA,amount*60+bonus)
           st.takeItems(ALLIGATOR_PELTS,-1)
        else :
           htmltext = "30892-04.htm"
     return htmltext

 def onKill(self,npc,player,isPet):
     st = player.getQuestState(qn)
     if not st : return

     if st.getState() != State.STARTED : return
     npcId = npc.getNpcId()
     if st.getRandom(100) < CHANCE :
         st.giveItems(ALLIGATOR_PELTS,1)
         st.playSound("ItemSound.quest_itemget")
     return

QUEST       = Quest(338,qn,"Alligator Hunter")

QUEST.addStartNpc(30892)

QUEST.addTalkId(30892)

QUEST.addKillId(ALLIGATOR)