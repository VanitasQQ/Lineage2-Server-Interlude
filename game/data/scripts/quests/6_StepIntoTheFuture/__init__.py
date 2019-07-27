# Created by CubicVirtuoso
# Any problems feel free to drop by #l2j-datapack on irc.freenode.net
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "6_StepIntoTheFuture"

#NPCs
ROXXY      = 30006
BAULRO     = 30033
SIR_COLLIN = 30311

#ITEM
BAULRO_LETTER = 7571

#REWARDS
SCROLL_OF_ESCAPE_GIRAN = 7559
MARK_OF_TRAVELER       = 7570

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [BAULRO_LETTER]

 def onEvent (self,event,st) :
   htmltext = event
   if event == "30006-03.htm" :
     st.set("cond","1")
     st.set("id","1")
     st.setState(State.STARTED)
     st.playSound("ItemSound.quest_accept")
   elif event == "30033-02.htm" :
     st.giveItems(BAULRO_LETTER,1)
     st.set("cond","2")
     st.set("id","2")
     st.playSound("ItemSound.quest_middle")
   elif event == "30311-03.htm" :
     st.takeItems(BAULRO_LETTER,-1)
     st.set("cond","3")
     st.set("id","3")
     st.playSound("ItemSound.quest_middle")
   elif event == "30006-06.htm" :
     st.giveItems(SCROLL_OF_ESCAPE_GIRAN,1)
     st.giveItems(MARK_OF_TRAVELER,1)
     st.unset("cond")
     st.exitQuest(False)
     st.playSound("ItemSound.quest_finish")
   return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   cond  = st.getInt("cond")
   id    = st.getState()
   if id == State.CREATED :
     st.set("cond","0")
     st.set("id","0")
     if player.getRace().ordinal() == 0 :
       if player.getLevel() >= 3 :
         htmltext = "30006-02.htm"
       else :
         htmltext = "<html><body>Quest for characters level 3 and above.</body></html>"
         st.exitQuest(1)
     else :
       htmltext = "30006-01.htm"
       st.exitQuest(1)
   elif npcId == ROXXY and id == State.COMPLETED :
     htmltext = "<html><body>I can't supply you with another Giran Scroll of Escape. Sorry traveller.</body></html>"
   elif npcId == ROXXY and cond == 1 :
     htmltext = "30006-04.htm"
   elif id == State.STARTED :
       if npcId == BAULRO :
         if cond == 1:
           htmltext = "30033-01.htm"
         elif cond == 2 and st.getQuestItemsCount(BAULRO_LETTER):
           htmltext = "30033-03.htm"
       elif npcId == SIR_COLLIN and cond == 2 and st.getQuestItemsCount(BAULRO_LETTER) :
           htmltext = "30311-02.htm"
       elif npcId == ROXXY and cond == 3 :
         htmltext = "30006-05.htm"
   return htmltext

QUEST     = Quest(6,qn,"Step into the Future")

QUEST.addStartNpc(ROXXY)

QUEST.addTalkId(ROXXY)
QUEST.addTalkId(BAULRO)
QUEST.addTalkId(SIR_COLLIN)