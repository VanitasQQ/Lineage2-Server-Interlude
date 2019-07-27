# Script for Pagan Temple Teleporters
# Needed for Quests 636 and 637
# v1.1 Done by BiTi
import sys
from ru.catssoftware.gameserver.datatables.xml     import DoorTable
from ru.catssoftware.gameserver.model.quest        import State
from ru.catssoftware.gameserver.model.quest        import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "1630_PaganTeleporters"

NPCS = [32034,32035,32036,32037]

class Quest (JQuest):

  def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

  def onAdvEvent (self,event,npc,pc):
    if event == "Close_Door1" :
       DoorTable.getInstance().getDoor(19160001).closeMe()
    elif event == "Close_Door2" :
       DoorTable.getInstance().getDoor(19160010).closeMe()
       DoorTable.getInstance().getDoor(19160011).closeMe()
    return

  def onFirstTalk (self,npc,player):
    st = player.getQuestState(qn)
    if not st :
      st = self.newQuestState(player)
    npcId = npc.getNpcId()
    if npcId == 32039 :
      player.teleToLocation(-12766,-35840,-10856)
    elif npcId == 32040 :
      player.teleToLocation(34962,-49758,-763)
    st.exitQuest(1)
    return ""

  def onTalk (self,npc,player):
    st = player.getQuestState(qn)
    npcId = npc.getNpcId()
    htmltext = None
    if npcId == 32034 :
      if st.getQuestItemsCount(8064) == 0 and st.getQuestItemsCount(8065) == 0 and st.getQuestItemsCount(8067) == 0:
	htmltext = "Mark1.htm"        
	return htmltext
      else:
      	htmltext = "FadedMark.htm"
      	DoorTable.getInstance().getDoor(19160001).openMe()
      	self.startQuestTimer("Close_Door1",10000,None,None)
    elif npcId == 32035:
      DoorTable.getInstance().getDoor(19160001).openMe()
      self.startQuestTimer("Close_Door1",10000,None,None)
      htmltext = "FadedMark.htm"
    elif npcId == 32036:
      if not st.getQuestItemsCount(8067) :
	htmltext = "Mark2.htm"        
	return htmltext
      else:
        htmltext = "Mark3.htm"
        self.startQuestTimer("Close_Door2",10000,None,None)
        DoorTable.getInstance().getDoor(19160010).openMe()
        DoorTable.getInstance().getDoor(19160011).openMe()
    elif npcId == 32037:
      DoorTable.getInstance().getDoor(19160010).openMe()
      DoorTable.getInstance().getDoor(19160011).openMe()
      self.startQuestTimer("Close_Door2",10000,None,None)
      htmltext = "FadedMark.htm"
    st.exitQuest(1)
    return htmltext

QUEST       = Quest(1630, qn, "Teleports")

for npc in NPCS :
    QUEST.addStartNpc(npc)
    QUEST.addTalkId(npc)

for i in [32039,32040] :
    QUEST.addStartNpc(i)
    QUEST.addFirstTalkId(i)