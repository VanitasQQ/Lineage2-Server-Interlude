# Made by Mr. - Version 0.3 by DrLecter
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "320_BonesTellFuture"

BONE_FRAGMENT = 809
ADENA = 57

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [BONE_FRAGMENT]

 def onEvent (self,event,st) :
    htmltext = event
    if event == "30359-04.htm" :
      st.set("cond","1")
      st.setState(State.STARTED)
      st.playSound("ItemSound.quest_accept")
    return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if st.getInt("cond")==0 :
     if player.getRace().ordinal() != 2 :
       htmltext = "30359-00.htm"
       st.exitQuest(1)
     elif player.getLevel() >= 10 :
       htmltext = "30359-03.htm"
     else:
       htmltext = "30359-02.htm"
       st.exitQuest(1)
   else :
     if st.getQuestItemsCount(BONE_FRAGMENT)<10 :
       htmltext = "30359-05.htm"
     else :
       htmltext = "30359-06.htm"
       st.rewardItems(ADENA,8470)
       st.takeItems(BONE_FRAGMENT,-1)
       st.exitQuest(1)
       st.playSound("ItemSound.quest_finish")
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return 
   if st.getState() != State.STARTED : return 
   
   count=st.getQuestItemsCount(BONE_FRAGMENT)
   if count<10 and st.getRandom(10)>7 :
      st.giveItems(BONE_FRAGMENT,1)
      if count == 9 :
        st.playSound("ItemSound.quest_middle")
        st.set("cond","2")
      else :
        st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(320,qn,"Bones Tell Future")

QUEST.addStartNpc(30359)

QUEST.addTalkId(30359)

QUEST.addKillId(20517)
QUEST.addKillId(20518)