# Made by Mr. - Version 0.3 by DrLecter
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "296_SilkOfTarantula"

TARANTULA_SPIDER_SILK = 1493
TARANTULA_SPINNERETTE = 1494
RING_OF_RACCOON = 1508
RING_OF_FIREFLY = 1509
ADENA = 57

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [TARANTULA_SPIDER_SILK, TARANTULA_SPINNERETTE]

 def onEvent (self,event,st) :
    htmltext = event
    if event == "30519-03.htm" :
      st.set("cond","1")
      st.setState(State.STARTED)
      st.playSound("ItemSound.quest_accept")
    elif event == "30519-06.htm" :
      st.takeItems(TARANTULA_SPINNERETTE,-1)
      st.exitQuest(1)
      st.playSound("ItemSound.quest_finish")
    elif event == "30548-02.htm" :
      if st.getQuestItemsCount(TARANTULA_SPINNERETTE) :
        htmltext = "30548-03.htm"
        st.giveItems(TARANTULA_SPIDER_SILK,15+st.getRandom(9))
        st.takeItems(TARANTULA_SPINNERETTE,1)
    elif event == "30519-09.htm" :
      st.exitQuest(1)
    return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if npcId != 30519 and id != State.STARTED : return htmltext
   if id == State.CREATED :
     st.set("cond","0")
   if npcId == 30519 :
     if st.getInt("cond")==0 :
       if player.getLevel() >= 15 :
         if st.getQuestItemsCount(RING_OF_RACCOON)==st.getQuestItemsCount(RING_OF_FIREFLY)==0 :
           htmltext = "30519-08.htm"
         else:
           htmltext = "30519-02.htm"
       else:
         htmltext = "30519-01.htm"
         st.exitQuest(1)
     else :
       count = st.getQuestItemsCount(TARANTULA_SPIDER_SILK)
       if count == 0 :
         htmltext = "30519-04.htm"
       else :
         htmltext = "30519-05.htm"
         st.rewardItems(ADENA,count*60)
         st.takeItems(TARANTULA_SPIDER_SILK,count)
   else :
     htmltext = "30548-01.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return 
   if st.getState() != State.STARTED : return 
   
   n = st.getRandom(100)
   if n > 95 :
     st.giveItems(TARANTULA_SPINNERETTE,1)
     st.playSound("ItemSound.quest_itemget")
   elif n > 45 :
     st.giveItems(TARANTULA_SPIDER_SILK,1)
     st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(296,qn,"Silk Of Tarantula")

QUEST.addStartNpc(30519)

QUEST.addTalkId(30519)
QUEST.addTalkId(30548)

QUEST.addKillId(20394)
QUEST.addKillId(20403)
QUEST.addKillId(20508)