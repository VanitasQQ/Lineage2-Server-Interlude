# Rate fix by Gnat

import sys
from ru.catssoftware import Config
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "634_InSearchofDimensionalFragments"

DIMENSION_FRAGMENT_ID = 7079

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [DIMENSION_FRAGMENT_ID]

 def onEvent (self,event,st) :
    htmltext = event
    if event == "2a.htm" :
      st.setState(State.STARTED)
      st.playSound("ItemSound.quest_accept")
      st.set("cond","1")
    elif event == "5.htm" :
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
            if player.getLevel() < 20 :
                st.exitQuest(1)
                htmltext="1.htm"
            else:
                htmltext="2.htm"
        elif id == State.STARTED :
            htmltext = "4.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
    partyMember = self.getRandomPartyMemberState(player, State.STARTED)
    if not partyMember : return
    st = partyMember.getQuestState(qn)
    if st :
        if st.getState() == State.STARTED :
            itemMultiplier,chance = divmod(80*Config.RATE_DROP_QUEST,1000)
            if st.getRandom(1000) < chance :
                itemMultiplier += 1
            numItems = int(itemMultiplier * (npc.getLevel() * 0.15 +1.6))
            if numItems > 0 :
                st.giveItems(DIMENSION_FRAGMENT_ID,int(numItems))
    return

QUEST       = Quest(634, qn, "In Search of Dimensional Fragments")

for npcId in range(31494,31508):
  QUEST.addTalkId(npcId)
  QUEST.addStartNpc(npcId)

for mobs in range(21208,21256):
  QUEST.addKillId(mobs)