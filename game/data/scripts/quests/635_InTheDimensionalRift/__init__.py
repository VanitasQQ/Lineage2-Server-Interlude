# In the Dimensional Rift v0.1 by DrLecter
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "635_InTheDimensionalRift"

DIMENSION_FRAGMENT = 7079

# Unconfirmed info:
# how many quest slots you need to have in order to enter be able to take another quests within the Rift
MAX_QUEST = 23
# Rift Posts should take you back to the place you came from
COORD={
1: [-41572,209731,-5087], #Necropolis of Sacrifice 
2: [-52872,-250283,-7908],#Catacomb of the Heretic
3: [ 45256,123906,-5411], #Pilgrim's Necropolis
4: [ 46192,170290,-4981], #Catacomb of the Branded
5: [111273,174015,-5437], #Necropolis of Worship
6: [-20604,-250789,-8165],#Catacomb of Apostate
7: [-21726, 77385,-5171], #Patriot's Necropolis
8: [140405, 79679,-5427], #Catacomb of the Witch
9: [-52366, 79097,-4741], #Necropolis of Devotion (ex Ascetics)
10:[118311,132797,-4829], #Necropolis of Martyrdom
11:[172185,-17602,-4901], #Disciple's Necropolis
12:[ 83000,209213,-5439], #Saint's Necropolis
13:[-19500, 13508,-4901], #Catacomb of Dark Omens
14:[113865, 84543,-6541]  #Catacomb of the Forbidden Path
}

class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onEvent (self,event,st) :
    htmltext = event
    id=st.getInt("id")
    count=st.getInt("count")
    if event == "5.htm" :
      if id :
         if count:
            htmltext="5a.htm"
         st.set("count",str(count+1))
         st.setState(State.STARTED)
         st.set("cond","1")
         st.getPlayer().teleToLocation(-114790,-180576,-6781)
      else :
         htmltext="What are you trying to do?"
         st.exitQuest(1)
    elif event == "6.htm" :
      st.exitQuest(1)
    return htmltext

 def onTalk (self,npc,player) :
   st = player.getQuestState(qn)
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   if st :
     npcId = npc.getNpcId()
     cond=st.getInt("cond")
     id=st.getInt("id")
     if npcId in range(31494,31508) :
        if player.getLevel() < 20 :
           st.exitQuest(1)
           htmltext="1.htm"
        elif len(player.getAllActiveQuests()) > MAX_QUEST :
           st.exitQuest(1)
           htmltext="1a.htm"
        elif not st.getQuestItemsCount(DIMENSION_FRAGMENT) :
           htmltext="3.htm"
        else :
           st.setState(State.CREATED)
           id=str(npcId-31493)
           st.set("id",id)
           htmltext="4.htm"
     elif st.getState() == State.STARTED :
        if id :
           x,y,z=COORD[id]
           player.teleToLocation(x,y,z)
           st.unset("cond")
           st.exitQuest(False)
           htmltext="7.htm"
        else :
           htmltext="Where?"
           st.exitQuest(1)
   return htmltext

QUEST       = Quest(635, qn, "In The Dimensional Rift")

for npcId in range(31494,31508):
    QUEST.addTalkId(npcId)
    QUEST.addStartNpc(npcId)

for npcId in range(31488,31494) :
    QUEST.addTalkId(npcId)