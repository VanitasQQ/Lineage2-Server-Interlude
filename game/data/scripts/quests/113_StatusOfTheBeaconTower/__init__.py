# Made by Kerberos v1.0 on 2008/02/09
# this script is part of the Official L2J Datapack Project.
# Visit http://forum.l2jdp.com for more details.
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "113_StatusOfTheBeaconTower"

#NPCs
Moira = 31979
Torrant = 32016

#Items
Box = 8086

class Quest (JQuest) : 

 def __init__(self,id,name,descr):
    JQuest.__init__(self,id,name,descr)
    self.questItemIds = [Box]

 def onEvent(self, event, st):
    htmltext = event
    if event == "31979-02.htm" :
      st.set("cond","1")
      st.giveItems(Box,1)
      st.setState(State.STARTED)
      st.playSound("ItemSound.quest_accept")
    elif event == "32016-02.htm" :
      st.rewardItems(57,21578)
      st.takeItems(Box,1)
      st.addExpAndSp(76665,5333)
      st.playSound("ItemSound.quest_finish")
      st.exitQuest(False)
    return htmltext

 def onTalk (self,npc,player):        
    htmltext = "<html><head><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
    st = player.getQuestState(qn)
    if not st : return htmltext
    state = st.getState()
    npcId = npc.getNpcId()
    cond = st.getInt("cond")
    if state == State.COMPLETED :
       htmltext = "<html><body>This quest has already been completed.</body></html>"
    elif npcId == Moira :
       if state == State.CREATED:
          if st.getPlayer().getLevel() >= 40 :
             htmltext = "31979-01.htm"
          else:
             htmltext = "31979-00.htm"
             st.exitQuest(1)
       elif cond == 1:
          htmltext = "31979-03.htm"
    elif npcId == Torrant and st.getQuestItemsCount(Box) == 1:
       htmltext = "32016-01.htm"
    return htmltext

QUEST = Quest(113,qn,"Status of the Beacon Tower")

QUEST.addStartNpc(Moira)

QUEST.addTalkId(Moira)
QUEST.addTalkId(Torrant)