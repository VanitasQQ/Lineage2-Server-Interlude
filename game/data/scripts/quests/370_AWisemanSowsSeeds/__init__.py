# Made by disKret
import sys
from ru.catssoftware.gameserver.model.quest import QuestMessage
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest
qn = "370_AWisemanSowsSeeds"

#NPC
CASIAN = 30612

#MOBS
MOBS = [20082,20084,20086,20089,20090]

#ITEMS
SPELLBOOK_PAGE = 5916
CHAPTER_OF_FIRE,CHAPTER_OF_WATER,CHAPTER_OF_WIND,CHAPTER_OF_EARTH = range(5917,5921)

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = range(5917,5921)

 def onEvent (self,event,st) :
   htmltext = event
   if event == "30612-3.htm" :
     st.set("cond","1")
     st.setState(State.STARTED)
     st.set("awaitsPartyDrop","1")
     st.playSound("ItemSound.quest_accept")
   elif event == "30612-6.htm" :
     if st.getQuestItemsCount(CHAPTER_OF_FIRE) and st.getQuestItemsCount(CHAPTER_OF_WATER) and st.getQuestItemsCount(CHAPTER_OF_WIND) and st.getQuestItemsCount(CHAPTER_OF_EARTH) :
       st.rewardItems(57,3600)
       st.takeItems(CHAPTER_OF_FIRE,1)
       st.takeItems(CHAPTER_OF_WATER,1)
       st.takeItems(CHAPTER_OF_WIND,1)
       st.takeItems(CHAPTER_OF_EARTH,1)
       htmltext = "30612-8.htm"
   elif event == "30612-9.htm" :
     st.playSound("ItemSound.quest_finish")
     st.exitQuest(1)
   return htmltext

 def onTalk (self,npc,player):
   htmltext = QuestMessage.QDefault.get()
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   cond=st.getInt("cond")
   if cond == 0 :
     if player.getLevel() >= 28 :
       htmltext = "30612-0.htm"
     else:
       htmltext = "30612-0a.htm"
       st.exitQuest(1)
   elif cond :
     htmltext = "30612-4.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   partyMember = self.getRandomPartyMember(player,"awaitsPartyDrop","1")
   if not partyMember : return
   st = partyMember.getQuestState(qn)

   chance = st.getRandom(100)
   if chance in range(1,30):
     st.giveItems(SPELLBOOK_PAGE,1)
     st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(370,qn,"A Wiseman Sows Seeds")

QUEST.addStartNpc(CASIAN)

QUEST.addTalkId(CASIAN)

for i in MOBS :
  QUEST.addKillId(i)