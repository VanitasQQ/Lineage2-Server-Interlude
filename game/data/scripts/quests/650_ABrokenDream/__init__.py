#made by ethernaly
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "650_ABrokenDream"

#NPC
GHOST = 32054

#MOBS
CREWMAN = 22027
VAGABOND = 22028

#DROP
DREAM_FRAGMENT_ID = 8514

CHANCE = 68

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [DREAM_FRAGMENT_ID]

 def onEvent (self,event,st) :
    htmltext = event
    if event == "2a.htm" :
      st.setState(State.STARTED)
      st.playSound("ItemSound.quest_accept")
      st.set("cond","1")
    elif event == "500.htm" :
      st.playSound("ItemSound.quest_finish")
      st.exitQuest(1)
    return htmltext

 def onTalk (self,npc,player):
   st = player.getQuestState(qn)
   if st :
        npcId = npc.getNpcId()
        htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
        id = st.getState()
        if id == State.CREATED :
            Ocean = player.getQuestState("117_OceanOfDistantStar")
            if st.getPlayer().getLevel() < 39:
                htmltext="100.htm"
                st.exitQuest(1)
            elif Ocean:
                if Ocean.getState() == State.COMPLETED :
                    htmltext="200.htm"
                else :
                    htmltext = "600.htm"
                    st.exitQuest(1)
            else :
            	htmltext = "600.htm"
                st.exitQuest(1)
        elif id == State.STARTED :
            if st.getQuestItemsCount(DREAM_FRAGMENT_ID):
               htmltext = "2a.htm"
            else :
               htmltext = "400.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   partyMember = self.getRandomPartyMember(player,"1")
   if not partyMember : return
   st = partyMember.getQuestState(qn)
   if st :
        if st.getState() == State.STARTED :
            if st.getRandom(100)<CHANCE :
                st.giveItems(DREAM_FRAGMENT_ID,1)
                st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(650, qn, "A Broken Dream")

QUEST.addStartNpc(GHOST)

QUEST.addTalkId(GHOST)

QUEST.addKillId(CREWMAN)
QUEST.addKillId(VAGABOND)