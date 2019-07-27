# Made by Vice [L2JOneo]
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "641_AttackSailren"

#NPC
STATUE = 32109

#MOBS
VEL1 = 22196
VEL2 = 22197
VEL3 = 22198
VEL4 = 22218
VEL5 = 22223
PTE = 22199

#ITEMS
FRAGMENTS = 8782
GAZKH = 8784

class Quest (JQuest):

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [FRAGMENTS]

 def onEvent (self,event,st):
   htmltext = event
   if event == "32109-03.htm" :
     st.set("cond","1")
     st.setState(State.STARTED)
     st.playSound("ItemSound.quest_accept")
   if event == "32109-05.htm" :
     st.takeItems(FRAGMENTS,30)
     st.giveItems(GAZKH,1)
     st.exitQuest(1)
     st.playSound("ItemSound.quest_finish")
     st.unset("cond")
   return htmltext

 def onTalk (self,npc,player):
   st = player.getQuestState(qn)
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   if not st : return htmltext
   npcId = npc.getNpcId()
   id = st.getState()
   cond = st.getInt("cond")
   if npcId == STATUE :
     st125 = player.getQuestState("125_TheNameOfEvil-1")
     st126 = player.getQuestState("126_TheNameOfEvil-2")
     if id == State.CREATED :
       if player.getLevel() < 77 :
         htmltext = "32109-06.htm"
       elif (st125 and st125.getState() == State.COMPLETED and st126 and st126.getState() == State.COMPLETED) :
         htmltext = "32109-01.htm"
       else :
         htmltext = "32109-07.htm"
     elif cond == 1 :
       htmltext = "32109-08.htm"
     elif cond == 2 :
       htmltext = "32109-04.htm"
   return htmltext

 def onKill (self,npc,player,isPet):
   #partyMember = self.getRandomPartyMember(player,"1")
   #if not partyMember: return
   #st = partyMember.getQuestState(qn)
   st = player.getQuestState(qn)
   if not st : return
   if st.getState() == State.STARTED :
     npcId = npc.getNpcId()
     if npcId in [VEL1,VEL2,VEL3,VEL4,VEL5,PTE] :
       if st.getQuestItemsCount(FRAGMENTS) < 30 :
         st.giveItems(FRAGMENTS,1)
         if st.getQuestItemsCount(FRAGMENTS) == 30 :
           st.playSound("ItemSound.quest_middle")
           st.set("cond","2")
         else:
           st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(641,qn,"Attack Sailren!")

QUEST.addStartNpc(STATUE)

QUEST.addTalkId(STATUE)

QUEST.addKillId(VEL1)
QUEST.addKillId(VEL2)
QUEST.addKillId(VEL3)
QUEST.addKillId(VEL4)
QUEST.addKillId(VEL5)
QUEST.addKillId(PTE)