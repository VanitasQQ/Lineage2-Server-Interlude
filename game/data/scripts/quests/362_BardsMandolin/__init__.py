# Bards Mandolin Written By MickyLee
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "362_BardsMandolin"

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [4316, 4317]

 def onEvent (self,event,st) :
    htmltext = event
    if event == "30957_2.htm" :
        st.set("cond","1")
        st.setState(State.STARTED)
        st.playSound("ItemSound.quest_accept")
    elif event == "30957_5.htm" :
        st.rewardItems(57,10000)
        st.giveItems(4410,1)
        st.exitQuest(1)
        st.playSound("ItemSound.quest_finish")
    return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if npcId != 30957 and id != State.STARTED : return htmltext
   if id == State.CREATED :
     st.set("cond","0")
   cond = st.getInt("cond")
   if npcId == 30957 and cond == 0 :
        htmltext = "30957_1.htm"
   elif npcId == 30837 and cond == 1 :
        st.set("cond","2")
        htmltext = "30837_1.htm"
   elif npcId == 30958 and cond == 2 :
        st.set("cond","3")
        st.giveItems(4316,1)
        htmltext = "30958_1.htm"
        st.playSound("ItemSound.quest_itemget")
   elif npcId == 30957 and cond == 3 and st.getQuestItemsCount(4316) and not st.getQuestItemsCount(4317) :
        st.set("cond","4")
        st.giveItems(4317,1)
        htmltext = "30957_3.htm"
   elif npcId == 30957 and cond == 4 and st.getQuestItemsCount(4316) and st.getQuestItemsCount(4317) :
        htmltext = "30957_6.htm"
   elif npcId == 30956 and cond == 4 and st.getQuestItemsCount(4316) and st.getQuestItemsCount(4317) :
        st.takeItems(4316,1)
        st.takeItems(4317,1)
        st.set("cond","5")
        htmltext = "30956_1.htm"
   elif npcId == 30957 and cond == 5 :
        htmltext = "30957_4.htm"
   return htmltext

QUEST       = Quest(362,qn,"Bards Mandolin")

QUEST.addStartNpc(30957)

QUEST.addTalkId(30957)
QUEST.addTalkId(30956)
QUEST.addTalkId(30958)
QUEST.addTalkId(30837)