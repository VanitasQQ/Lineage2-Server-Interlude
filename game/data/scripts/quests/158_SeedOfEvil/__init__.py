# Made by Mr. Have fun! Version 0.2
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "158_SeedOfEvil"

CLAY_TABLET_ID = 1025
ENCHANT_ARMOR_D = 956

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [CLAY_TABLET_ID]

 def onEvent (self,event,st) :
    htmltext = event
    if event == "1" :
        st.set("id","0")
        st.set("cond","1")
        st.setState(State.STARTED)
        st.playSound("ItemSound.quest_accept")
        htmltext = "30031-04.htm"
    return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if npcId == 30031 and st.getInt("cond")==0 and st.getInt("onlyone")==0 :
     if player.getLevel() >= 21 :
       htmltext = "30031-03.htm"
       return htmltext
     else:
       htmltext = "30031-02.htm"
       st.exitQuest(1)
   elif npcId == 30031 and st.getInt("cond")==0 and st.getInt("onlyone")==1 :
      htmltext = "<html><body>This quest has already been completed.</body></html>"
   elif npcId == 30031 and st.getInt("cond")!=0 and st.getQuestItemsCount(CLAY_TABLET_ID)==0 :
        htmltext = "30031-05.htm"
   elif npcId == 30031 and st.getInt("cond")!=0 and st.getQuestItemsCount(CLAY_TABLET_ID)!=0 and st.getInt("onlyone")==0 :
        if st.getInt("id") != 158 :
          st.set("id","158")
          st.rewardItems(57,1495)
          st.giveItems(ENCHANT_ARMOR_D,1)
          st.takeItems(CLAY_TABLET_ID,-1)
          st.addExpAndSp(17818,927)
          st.set("cond","0")
          st.exitQuest(False)
          st.playSound("ItemSound.quest_finish")
          st.set("onlyone","1")
          htmltext = "30031-06.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return
   if st.getState() != State.STARTED : return

   npcId = npc.getNpcId()
   if npcId == 27016 :
        st.set("id","0")
        if st.getInt("cond") != 0 and st.getQuestItemsCount(CLAY_TABLET_ID) == 0 :
          st.giveItems(CLAY_TABLET_ID,1)
          st.playSound("ItemSound.quest_middle")
   return

QUEST       = Quest(158,qn,"Seed of Evil")

QUEST.addStartNpc(30031)

QUEST.addTalkId(30031)

QUEST.addKillId(27016)