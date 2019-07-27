# Made by Mr. - Version 0.3 by DrLecter
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.network.serverpackets import SocialAction
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "166_DarkMass"

UNDRES_LETTER_ID = 1088
CEREMONIAL_DAGGER_ID = 1089
DREVIANT_WINE_ID = 1090
GARMIELS_SCRIPTURE_ID = 1091
ADENA_ID = 57

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [CEREMONIAL_DAGGER_ID, DREVIANT_WINE_ID, GARMIELS_SCRIPTURE_ID, UNDRES_LETTER_ID]

 def onEvent (self,event,st) :
    htmltext = event
    if event == "30130-04.htm" :
       st.giveItems(UNDRES_LETTER_ID,1)
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
   if id == State.CREATED :
     st.set("cond","0")
     if player.getRace().ordinal() == 2 :
        if player.getLevel() >= 2 :
           htmltext = "30130-03.htm"
           return htmltext
        else :
           htmltext = "30130-00.htm"
           st.exitQuest(1)
     else:
        htmltext = "30130-02.htm"
        st.exitQuest(1)
   elif id == State.COMPLETED :
      htmltext = "<html><body>This quest has already been completed.</body></html>"
   elif npcId == 30130 :
      if st.getInt("cond") and st.getQuestItemsCount(UNDRES_LETTER_ID):
         if (st.getQuestItemsCount(GARMIELS_SCRIPTURE_ID)+st.getQuestItemsCount(DREVIANT_WINE_ID)+st.getQuestItemsCount(CEREMONIAL_DAGGER_ID)==0) :
            htmltext = "30130-05.htm"
         elif st.getQuestItemsCount(CEREMONIAL_DAGGER_ID)==st.getQuestItemsCount(DREVIANT_WINE_ID)==st.getQuestItemsCount(GARMIELS_SCRIPTURE_ID)==1 :
            htmltext = "30130-06.htm"
            st.takeItems(CEREMONIAL_DAGGER_ID,1)
            st.takeItems(DREVIANT_WINE_ID,1)
            st.takeItems(GARMIELS_SCRIPTURE_ID,1)
            st.takeItems(UNDRES_LETTER_ID,1)
            st.rewardItems(ADENA_ID,2966)
            st.addExpAndSp(5672,446)
            ObjectId=player.getObjectId()
            player.broadcastPacket(SocialAction(ObjectId,3))
            st.set("cond","0")
            st.exitQuest(False)
            st.playSound("ItemSound.quest_finish")
   elif id == State.STARTED:
       if npcId == 30135 :
          if st.getQuestItemsCount(UNDRES_LETTER_ID) :
             if not st.getQuestItemsCount(CEREMONIAL_DAGGER_ID) :
                st.giveItems(CEREMONIAL_DAGGER_ID,1)
                htmltext = "30135-01.htm"
             else :
                htmltext = "30135-02.htm"
       elif npcId == 30139 :
          if st.getQuestItemsCount(UNDRES_LETTER_ID) :
             if not st.getQuestItemsCount(DREVIANT_WINE_ID) :
                st.giveItems(DREVIANT_WINE_ID,1)
                htmltext = "30139-01.htm"
             else :
                htmltext = "30139-02.htm"
       elif npcId == 30143 :
          if st.getQuestItemsCount(UNDRES_LETTER_ID) :
             if not st.getQuestItemsCount(GARMIELS_SCRIPTURE_ID) :
                st.giveItems(GARMIELS_SCRIPTURE_ID,1)
                htmltext = "30143-01.htm"
             else :
                htmltext = "30143-02.htm"
       if st.getQuestItemsCount(UNDRES_LETTER_ID) and (st.getQuestItemsCount(CEREMONIAL_DAGGER_ID) + st.getQuestItemsCount(DREVIANT_WINE_ID) + st.getQuestItemsCount(GARMIELS_SCRIPTURE_ID) >= 3) :
         st.set("cond","2")
         st.playSound("ItemSound.quest_middle")
   return htmltext

QUEST       = Quest(166,qn,"Mass of Darkness")

QUEST.addStartNpc(30130)

QUEST.addTalkId(30130)
QUEST.addTalkId(30135)
QUEST.addTalkId(30139)
QUEST.addTalkId(30143)