# Made by Mr. - Version 0.3 by DrLecter
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.network.serverpackets import SocialAction
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "156_MillenniumLove"

RYLITHS_LETTER_ID = 1022
THEONS_DIARY_ID = 1023

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [RYLITHS_LETTER_ID, THEONS_DIARY_ID]

 def onEvent (self,event,st) :
    htmltext = event
    if event == "1" :
       if st.getPlayer().getLevel() >= 15 :
          htmltext = "30368-06.htm"
          st.giveItems(RYLITHS_LETTER_ID,1)
          st.set("cond","1")
          st.setState(State.STARTED)
          st.playSound("ItemSound.quest_accept")
       else:
          htmltext = "30368-05.htm"
          st.exitQuest(1)
    elif event == "156_1" :
       st.takeItems(RYLITHS_LETTER_ID,-1)
       if not st.getQuestItemsCount(THEONS_DIARY_ID) :
          st.giveItems(THEONS_DIARY_ID,1)
       htmltext = "30369-03.htm"
    elif event == "156_2" :
       st.takeItems(RYLITHS_LETTER_ID,-1)
       st.unset("cond")
       st.exitQuest(False)
       st.playSound("ItemSound.quest_finish")
       st.giveItems(5250,1)
       st.addExpAndSp(3000,0)
       ObjectId=st.getPlayer().getObjectId()
       st.getPlayer().broadcastPacket(SocialAction(ObjectId,3))
       htmltext = "30369-04.htm"
    return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if id == State.COMPLETED :
      htmltext = "<html><body>This quest has already been completed.</body></html>"
   elif npcId == 30368 :
      if not st.getInt("cond") :
         htmltext = "30368-04.htm"
      elif st.getInt("cond") :
        if st.getQuestItemsCount(RYLITHS_LETTER_ID) :
           htmltext = "30368-07.htm"
        elif st.getQuestItemsCount(THEONS_DIARY_ID) :
           st.takeItems(THEONS_DIARY_ID,-1)
           st.unset("cond")
           st.exitQuest(False)
           st.playSound("ItemSound.quest_finish")
           st.addExpAndSp(3000,0)
           ObjectId=player.getObjectId()
           player.broadcastPacket(SocialAction(ObjectId,3))
           st.rewardItems(5250,1)
           htmltext = "30368-08.htm"
   elif npcId == 30369 and id == State.STARTED:
      if st.getQuestItemsCount(RYLITHS_LETTER_ID) :
         htmltext = "30369-02.htm"
      elif st.getQuestItemsCount(THEONS_DIARY_ID) :
         htmltext = "30369-05.htm"
   return htmltext

QUEST       = Quest(156,qn,"Millennium Love")

QUEST.addStartNpc(30368)

QUEST.addTalkId(30368)
QUEST.addTalkId(30369)