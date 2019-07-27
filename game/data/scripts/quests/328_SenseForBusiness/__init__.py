# Made by Mr. Have fun! - Version 0.3 by Drlecter
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "328_SenseForBusiness"

MONSTER_EYE_CARCASS = 1347
MONSTER_EYE_LENS = 1366
BASILISK_GIZZARD = 1348
ADENA = 57

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [MONSTER_EYE_CARCASS, MONSTER_EYE_LENS, BASILISK_GIZZARD]

 def onEvent (self,event,st) :
    htmltext = event
    if event == "30436-03.htm" :
        st.set("cond","1")
        st.setState(State.STARTED)
        st.playSound("ItemSound.quest_accept")
    elif event == "30436-06.htm" :
        st.playSound("ItemSound.quest_finish")
        st.exitQuest(1)
    return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if id == State.CREATED :
     st.set("cond","0")
   if st.getInt("cond")==0 :
     if player.getLevel() >= 21 :
        htmltext = "30436-02.htm"
        return htmltext
     else:
        htmltext = "30436-01.htm"
        st.exitQuest(1)
   else :
     carcass=st.getQuestItemsCount(MONSTER_EYE_CARCASS)
     lenses=st.getQuestItemsCount(MONSTER_EYE_LENS)
     gizzard=st.getQuestItemsCount(BASILISK_GIZZARD)
     if carcass+lenses+gizzard >= 10 :
       bonus = 618
     else :
       bonus = 0
     if carcass+lenses+gizzard > 0 :
        st.rewardItems(ADENA,25*carcass+1000*lenses+60*gizzard+bonus)
        st.takeItems(MONSTER_EYE_CARCASS,-1)
        st.takeItems(MONSTER_EYE_LENS,-1)
        st.takeItems(BASILISK_GIZZARD,-1)
        htmltext = "30436-05.htm"
     else:
        htmltext = "30436-04.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return 
   if st.getState() != State.STARTED : return 
   
   npcId = npc.getNpcId()
   n = st.getRandom(100)
   if npcId == 20055 :
     if n<51 :
      st.playSound("ItemSound.quest_itemget")
      if n<50 :
         st.giveItems(MONSTER_EYE_CARCASS,1)
      else :
         st.giveItems(MONSTER_EYE_LENS,1)
   elif npcId == 20059 :
     if n<55 :
      st.playSound("ItemSound.quest_itemget")
      if n<54 :
         st.giveItems(MONSTER_EYE_CARCASS,1)
      else :
         st.giveItems(MONSTER_EYE_LENS,1)
   elif npcId == 20067 :
     if n<69 :
      st.playSound("ItemSound.quest_itemget")
      if n<67 :
         st.giveItems(MONSTER_EYE_CARCASS,1)
      else :
         st.giveItems(MONSTER_EYE_LENS,1)
   elif npcId == 20068 :
     if n<74 :
      st.playSound("ItemSound.quest_itemget")
      if n<72 :
         st.giveItems(MONSTER_EYE_CARCASS,1)
      else :
         st.giveItems(MONSTER_EYE_LENS,1)
   elif npcId == 20070 :
      if n<50 :
         st.giveItems(BASILISK_GIZZARD,1)
         st.playSound("ItemSound.quest_itemget")
   elif npcId == 20072 :
      if n<53 :
         st.giveItems(BASILISK_GIZZARD,1)
         st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(328,qn,"Sense For Business")

QUEST.addStartNpc(30436)

QUEST.addTalkId(30436)

for i in [ 20055,20059,20067,20068,20070,20072 ] :
    QUEST.addKillId(i)