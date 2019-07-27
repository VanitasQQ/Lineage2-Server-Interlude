# Made by DrLecter, based on a Polo script and a DoomIta contribution
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "653_WildMaiden"

#Npc
SUKI = 32013
GALIBREDO = 30181

#Items
SOE = 736

class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onAdvEvent (self,event,npc,player) :
    htmltext = event
    st = player.getQuestState(qn)
    if not st : return
    if event == "32013-04.htm" :
      if st.getQuestItemsCount(SOE):
        st.set("cond","1")
        st.setState(State.STARTED)
        st.playSound("ItemSound.quest_accept")
        st.takeItems(SOE,1)
        htmltext = "32013-03.htm"
        npc.deleteMe()
    elif event == "32013-04a.htm" :
        st.exitQuest(1)
        st.playSound("ItemSound.quest_giveup")
    return htmltext

 def onTalk (self,npc,player):
   st = player.getQuestState(qn)
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   if not st : return htmltext
   npcId = npc.getNpcId()
   id = st.getState()
   cond=st.getInt("cond")
   if npcId == SUKI and id == State.CREATED:
       if player.getLevel() >= 36 :
           htmltext = "32013-02.htm"
       else:
           htmltext = "32013-01.htm"
           st.exitQuest(1)
   elif npcId == GALIBREDO and st.getInt("cond") :
       htmltext = "30181-01.htm"
       st.rewardItems(57,2553)
       st.playSound("ItemSound.quest_finish")
       st.exitQuest(1)
   return htmltext

QUEST       = Quest(653,qn,"Wild Maiden")

QUEST.addStartNpc(SUKI)

QUEST.addTalkId(SUKI)
QUEST.addTalkId(GALIBREDO)