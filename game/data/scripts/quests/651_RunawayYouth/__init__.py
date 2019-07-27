# Made by Polo & DrLecter
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "651_RunawayYouth"

#Npc
IVAN = 32014
BATIDAE = 31989

#Items
SOE = 736

class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onAdvEvent (self,event,npc,player) :
    htmltext = event
    st = player.getQuestState(qn)
    if not st : return
    if event == "32014-04.htm" :
      if st.getQuestItemsCount(SOE):
        st.set("cond","1")
        st.setState(State.STARTED)
        st.playSound("ItemSound.quest_accept")
        st.takeItems(SOE,1)
        htmltext = "32014-03.htm"
        npc.deleteMe()
    elif event == "32014-04a.htm" :
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
   if npcId == IVAN and id == State.CREATED:
      if player.getLevel()>=26 :
         htmltext = "32014-02.htm"
      else:
         htmltext = "32014-01.htm"
         st.exitQuest(1)
   elif npcId == BATIDAE and st.getInt("cond") :
      htmltext = "31989-01.htm"
      st.rewardItems(57,2883)
      st.playSound("ItemSound.quest_finish")
      st.exitQuest(1)
   return htmltext

QUEST       = Quest(651,qn,"Runaway Youth")

QUEST.addStartNpc(IVAN)

QUEST.addTalkId(IVAN)
QUEST.addTalkId(BATIDAE)