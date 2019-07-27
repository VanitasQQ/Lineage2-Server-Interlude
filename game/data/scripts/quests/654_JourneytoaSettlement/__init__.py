# By L2J_JP SANDMAN
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "654_JourneytoaSettlement"

#NPC
SPIRIT      = 31453     #Nameless Spirit

#TARGET
TARGET_1    = 21294     #Canyon Antelope
TARGET_2    = 21295     #Canyon Antelope Slave

#ITEM
ITEM        = 8072      #Antelope Skin

#REWARD
SCROLL      = 8073      #Frintezza's Magic Force Field Removal Scroll

class Quest (JQuest) :

  def __init__(self,id,name,descr): 
      JQuest.__init__(self,id,name,descr)
      self.questItemIds = [ITEM]

  def onEvent (self,event,st) :
    htmltext = event
    if event == "31453-2.htm" :
       st.set("cond","1")
       st.setState(State.STARTED)
       st.playSound("ItemSound.quest_accept")
    elif event == "31453-3.htm" :
       st.set("cond","2")
       st.playSound("ItemSound.quest_middle")
    elif event == "31453-5.htm" :
       st.giveItems(SCROLL,1)
       st.takeItems(ITEM,1)
       st.playSound("ItemSound.quest_finish")
       st.unset("cond")
       st.exitQuest(1)
    return htmltext

  def onTalk (Self,npc,player):
    htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
    st = player.getQuestState(qn)
    if not st: return htmltext
    cond = st.getInt("cond")
    npcId = npc.getNpcId()
    id = st.getState()
    if id == State.CREATED :
       preSt = player.getQuestState("119_LastImperialPrince")
       if preSt: preId = preSt.getState()
       if player.getLevel() < 74 :
          htmltext = "<html><body>Quest for characters level 74 and above.</body></html>"
          st.exitQuest(1)
       elif not preSt:
          htmltext = "<html><body>Quest <font color=\"LEVEL\">Last Imperial Prince</font> is not accomplished or the condition is not suitable.</body></html>"
          st.exitQuest(1)
       elif preId != State.COMPLETED :
          htmltext = "<html><body>Quest <font color=\"LEVEL\">Last Imperial Prince</font> is not accomplished or the condition is not suitable.</body></html>"
          st.exitQuest(1)
       else :
          htmltext = "31453-1.htm"
    elif npcId == SPIRIT :
       if cond == 1 :
          htmltext = "31453-2.htm"
       elif cond == 3 :
          htmltext = "31453-4.htm"
    return htmltext

  def onKill (self,npc,player,isPet) :
    st = player.getQuestState(qn)
    if not st: return
    npcId = npc.getNpcId()
    if st.getInt("cond") == 2 and  st.getRandom(100) < 5 :
       st.set("cond","3")
       st.giveItems(ITEM,1)
       st.playSound("ItemSound.quest_middle")
    return

QUEST = Quest(654,qn,"Journey to a Settlement")

QUEST.addStartNpc(SPIRIT)

QUEST.addTalkId(SPIRIT)

QUEST.addKillId(TARGET_1)
QUEST.addKillId(TARGET_2)