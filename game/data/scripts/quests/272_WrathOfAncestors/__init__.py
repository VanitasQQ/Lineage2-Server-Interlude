# Made by Mr. - Version 0.3 by DrLecter
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "272_WrathOfAncestors"

GRAVE_ROBBERS_HEAD = 1474
ADENA = 57

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [GRAVE_ROBBERS_HEAD]

 def onEvent (self,event,st) :
    htmltext = event
    if event == "30572-03.htm" :
      st.set("cond","1")
      st.setState(State.STARTED)
      st.playSound("ItemSound.quest_accept")
    return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if id == State.CREATED :
     st.set("cond","0")
   if st.getInt("cond") == 0 :
     if player.getRace().ordinal() != 3 :
        htmltext = "30572-00.htm"
        st.exitQuest(1)
     else :
        if player.getLevel() < 5 :
          htmltext = "30572-01.htm"
          st.exitQuest(1)
        else:
          htmltext = "30572-02.htm"
   else :
     if st.getQuestItemsCount(GRAVE_ROBBERS_HEAD) < 50 :
        htmltext = "30572-04.htm"
     else:
        htmltext = "30572-05.htm"
        st.exitQuest(1)
        st.playSound("ItemSound.quest_finish")
        st.rewardItems(ADENA,1500)
        st.takeItems(GRAVE_ROBBERS_HEAD,-1)
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return
   if st.getState() != State.STARTED : return
   
   count = st.getQuestItemsCount(GRAVE_ROBBERS_HEAD)
   if count < 50 :
      st.giveItems(GRAVE_ROBBERS_HEAD,1)
      if count < 49 :
         st.playSound("ItemSound.quest_itemget")
      else:
         st.playSound("ItemSound.quest_middle")
         st.set("cond","2")
   return

QUEST       = Quest(272,qn,"Wrath Of Ancestors")

QUEST.addStartNpc(30572)

QUEST.addTalkId(30572)

QUEST.addKillId(20319)
QUEST.addKillId(20320)