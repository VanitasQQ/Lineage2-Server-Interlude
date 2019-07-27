# Made by disKret, Ancient Legion Server
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.network.serverpackets import SocialAction
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "16_TheComingDarkness"

#NPC
HIERARCH = 31517
EVIL_ALTAR_1 = 31512
EVIL_ALTAR_2 = 31513
EVIL_ALTAR_3 = 31514
EVIL_ALTAR_4 = 31515
EVIL_ALTAR_5 = 31516

#ITEMS
CRYSTAL_OF_SEAL = 7167

class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onEvent (self,event,st) :
   htmltext = event
   cond = st.getInt("cond")
   if event == "31517-1.htm" :
     return htmltext
   if event == "31517-2.htm" :
     st.giveItems(CRYSTAL_OF_SEAL,5)
     st.set("cond","1")
     st.setState(State.STARTED)
     st.playSound("ItemSound.quest_accept")
   if event == "31512-1.htm" :
     if cond == 1 :
       st.takeItems(CRYSTAL_OF_SEAL,1)
       st.set("cond","2")
       st.playSound("ItemSound.quest_middle")
   if event == "31513-1.htm" :
     if cond == 2 :
       st.takeItems(CRYSTAL_OF_SEAL,1)
       st.set("cond","3")
       st.playSound("ItemSound.quest_middle")
   if event == "31514-1.htm" :
     if cond == 3 :
       st.takeItems(CRYSTAL_OF_SEAL,1)
       st.set("cond","4")
       st.playSound("ItemSound.quest_middle")
   if event == "31515-1.htm" :
     if cond == 4 :
       st.takeItems(CRYSTAL_OF_SEAL,1)
       st.set("cond","5")
       st.playSound("ItemSound.quest_middle")
   if event == "31516-1.htm" :
     if cond == 5 :
       st.takeItems(CRYSTAL_OF_SEAL,1)
       st.set("cond","6")
       st.playSound("ItemSound.quest_middle")
   return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   cond = st.getInt("cond")
   id = st.getState()
   if id == State.COMPLETED :
     htmltext = "<html><body>This quest has already been completed.</body></html>"
   elif id == State.CREATED and npcId == HIERARCH:
     st2 = player.getQuestState("17_LightAndDarkness")
     if st2 and st2.getState() == State.COMPLETED :
       if player.getLevel() >= 62 :
         htmltext = "31517-0.htm"
       else :
         htmltext = "<html><body>(Only characters level 62 and above are permitted to undertake this quest.) </body></html>"
         st.exitQuest(1)
     else:
       htmltext = "<html><body>Quest Light and Darkness need to be finished first.</body></html>"
       st.exitQuest(1)
   elif id == State.STARTED :
       if npcId == EVIL_ALTAR_1 and cond == 1 :
         htmltext = "31512-0.htm"
       if npcId == EVIL_ALTAR_2 and cond == 2 :
         htmltext = "31513-0.htm"
       if npcId == EVIL_ALTAR_3 and cond == 3 :
         htmltext = "31514-0.htm"
       if npcId == EVIL_ALTAR_4 and cond== 4 :
         htmltext = "31515-0.htm"
       if npcId == EVIL_ALTAR_5 and cond == 5 :
         htmltext = "31516-0.htm"
       if npcId == HIERARCH and cond == 6 :
         st.addExpAndSp(865187,69172)
         ObjectId=player.getObjectId()
         player.broadcastPacket(SocialAction(ObjectId,3))
         st.set("cond","0")
         st.exitQuest(False)
         st.playSound("ItemSound.quest_finish")
         htmltext = "31517-3.htm"
   return htmltext

QUEST       = Quest(16,qn,"The Coming Darkness")

QUEST.addStartNpc(HIERARCH)

QUEST.addTalkId(HIERARCH)

for altars in range(31512,31517):
  QUEST.addTalkId(altars)