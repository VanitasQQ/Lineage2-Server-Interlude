# Made by Polo - Have fun! - Fixed by BiTi
# v0.3.1 by DrLecter
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "636_TruthBeyond"

#Npc
ELIYAH = 31329
FLAURON = 32010

#Items
MARK = 8064

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)

 def onEvent (self,event,st) :
    htmltext = event
    if htmltext == "31329-04.htm" :
      st.set("cond","1")
      st.setState(State.STARTED)
      st.playSound("ItemSound.quest_accept")
    elif htmltext == "32010-02.htm" :
      st.giveItems(MARK,1)
      st.exitQuest(1)
      st.playSound("ItemSound.quest_finish")
    return htmltext

 def onTalk (self,npc,player):
   st = player.getQuestState(qn)
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   cond = st.getInt("cond")
   if st.getQuestItemsCount(MARK) == 1 :
     htmltext = "31329-mark.htm"
     st.exitQuest(1)
   elif st.getQuestItemsCount(8065) == 1 :
     htmltext = "31329-mark.htm"
     st.exitQuest(1)
   elif st.getQuestItemsCount(8067) == 1 :
     htmltext = "31329-mark.htm"
     st.exitQuest(1)
   else :
     if id == State.CREATED :
       if npcId == ELIYAH :
         if player.getLevel() > 72 :
           htmltext = "31329-02.htm"
         else :
           htmltext = "31329-01.htm"
           st.exitQuest(1)
     elif id == State.STARTED :
       if npcId == ELIYAH :
         htmltext = "31329-05.htm"
       elif npcId == FLAURON :
         if cond == 1 :
           htmltext = "32010-01.htm"
         else :
           htmltext = "32010-03.htm"
   return htmltext

QUEST       = Quest(636,qn,"Truth Beyond the Gate")

QUEST.addStartNpc(ELIYAH)

QUEST.addTalkId(ELIYAH)
QUEST.addTalkId(FLAURON)