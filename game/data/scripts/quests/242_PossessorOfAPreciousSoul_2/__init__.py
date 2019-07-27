# Made by disKret
import sys
import time
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "242_PossessorOfAPreciousSoul_2"

#NPC
VIRGIL = 31742
KASSANDRA = 31743
OGMAR = 31744
FALLEN_UNICORN = 31746
PURE_UNICORN = 31747
CORNERSTONE = 31748
MYSTERIOUS_KNIGHT = 31751
ANGEL_CORPSE = 31752
KALIS = 30759
MATILD = 30738

#QUEST ITEM
VIRGILS_LETTER = 7677
GOLDEN_HAIR = 7590
ORB_OF_BINDING = 7595
SORCERY_INGREDIENT = 7596
CARADINE_LETTER = 7678

#CHANCE FOR HAIR DROP
CHANCE_FOR_HAIR = 20

#MOB
RESTRAINER_OF_GLORY = 27317

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [GOLDEN_HAIR, ORB_OF_BINDING, SORCERY_INGREDIENT]

 def onAdvEvent (self,event,npc,player) :
   st = player.getQuestState(qn)
   if not st: return 
   htmltext = event
   cond = st.getInt("cond")
   if event == "31742-3.htm" :
     if cond == 0 :
       st.setState(State.STARTED)
       st.takeItems(VIRGILS_LETTER,1)
       st.set("cond","1")
       st.playSound("ItemSound.quest_accept")
   elif event == "31743-5.htm" :
     if cond == 1 :
       st.set("cond","2")
       st.setState(State.STARTED)
       st.playSound("ItemSound.quest_accept")
   elif event == "31744-2.htm" :
     if cond == 2 :
       st.set("cond","3")
       st.playSound("ItemSound.quest_middle")
   elif event == "31751-2.htm" :
     if cond == 3 :
       st.set("cond","4")
       st.playSound("ItemSound.quest_middle")
   elif event == "30759-2.htm" :
     if cond == 6 :
       st.set("cond","7")
       st.playSound("ItemSound.quest_middle")
   elif event == "30738-2.htm" :
     if cond == 7 :
       st.set("cond","8")
       st.giveItems(SORCERY_INGREDIENT,1)
       st.playSound("ItemSound.quest_middle")
   elif event == "30759-5.htm" :
     if cond == 8 :
       st.set("cond","9")
       st.set("awaitsDrops","1")
       st.takeItems(GOLDEN_HAIR,1)
       st.takeItems(SORCERY_INGREDIENT,1)
       st.playSound("ItemSound.quest_middle")
   elif event == "1" :
     npc.getSpawn().stopRespawn()
     npc.deleteMe()
     npc2 = st.addSpawn(PURE_UNICORN,85884,-76588,-3475)
     self.startQuestTimer("2",30000,npc2,player)
   elif event == "2" :
     npc.deleteMe()
     npc2 = st.addSpawn(FALLEN_UNICORN,85884,-76588,-3475)
   return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext
   npcId = npc.getNpcId()
   id = st.getState()
   if npcId != VIRGIL and id != State.STARTED : return htmltext
   cornerstones = st.getInt("cornerstones")
   if id == State.CREATED :
     st.set("cond","0")
     st.set("cornerstones","0")
   cond = st.getInt("cond")
   if player.isSubClassActive() :
     if npcId == VIRGIL :
         if cond == 0 and st.getQuestItemsCount(VIRGILS_LETTER) == 1 :
            if id == State.COMPLETED :
                htmltext = "<html><body>This quest has already been completed.</body></html>"
            elif player.getLevel() < 60 :
                htmltext = "31742-2.htm"
                st.exitQuest(1)
            elif player.getLevel() >= 60 :
                htmltext = "31742-1.htm"
         elif cond == 1 :
             htmltext = "31742-4.htm"
         elif cond == 11 :
             htmltext = "31742-6.htm"
             st.set("cond","0")
             st.set("cornerstones","0")
             st.giveItems(CARADINE_LETTER,1)
             st.addExpAndSp(455764,0)
             st.playSound("ItemSound.quest_finish")
             st.exitQuest(False)
     elif npcId == KASSANDRA :
         if cond == 1 :
             htmltext = "31743-1.htm"
         elif cond == 2 :
             htmltext = "31743-6.htm"
         elif cond == 11 :
             htmltext = "31743-7.htm"
     elif npcId == OGMAR :
         if cond == 2 :
             htmltext = "31744-1.htm"
         elif cond == 3 :
             htmltext = "31744-3.htm"
     elif npcId == MYSTERIOUS_KNIGHT :
         if cond == 3 :
             htmltext = "31751-1.htm"
         elif cond == 4 :
             htmltext = "31751-3.htm"
         elif cond == 5 and st.getQuestItemsCount(GOLDEN_HAIR) == 1 :
             htmltext = "31751-4.htm"
             st.set("cond","6")
             st.playSound("ItemSound.quest_middle")
         elif cond == 6 :
             htmltext = "31751-5.htm"
     elif npcId == ANGEL_CORPSE :
         if cond == 4 :
           npc.reduceCurrentHp(10000,npc,None)
           chance = st.getRandom(100)
           if CHANCE_FOR_HAIR < chance :
             htmltext = "31752-2.htm"
           else :
             st.set("cond","5")
             st.giveItems(GOLDEN_HAIR,1)
             st.playSound("ItemSound.quest_middle")
             htmltext = "31752-1.htm"
         elif cond == 5 :
             htmltext = "31752-2.htm"
     elif npcId == KALIS :
         if cond == 6 :
             htmltext = "30759-1.htm"
         elif cond == 7 :
             htmltext = "30759-3.htm"
         elif cond == 8 and st.getQuestItemsCount(SORCERY_INGREDIENT) == 1 :
             htmltext = "30759-4.htm"
         elif cond == 9 :
             htmltext = "30759-6.htm"
     elif npcId == MATILD :
         if cond == 7 :
             htmltext = "30738-1.htm"
         elif cond == 8 :
             htmltext = "30738-3.htm"
     elif npcId == FALLEN_UNICORN :
         if cond == 9 :
             htmltext = "31746-1.htm"
         elif cond == 10 :
             htmltext = "31746-2.htm"
             self.startQuestTimer("1",3000,npc,player)
     elif npcId == CORNERSTONE :
         if cond == 9 and st.getQuestItemsCount(ORB_OF_BINDING) == 0 :
             htmltext = "31748-1.htm"
         elif cond == 9 and st.getQuestItemsCount(ORB_OF_BINDING) >= 1 :
             htmltext = "31748-2.htm"
             st.takeItems(ORB_OF_BINDING,1)
             npc.reduceCurrentHp(10000,npc,None)
             st.set("cornerstones",str(cornerstones+1))
             st.playSound("ItemSound.quest_middle")
             if cornerstones == 3 :
                 st.set("cond","10")
                 st.playSound("ItemSound.quest_middle")
     elif npcId == PURE_UNICORN :
         if cond == 10 :
             st.set("cond","11")
             st.playSound("ItemSound.quest_middle")
             htmltext = "31747-1.htm"
         elif cond == 11 :
             htmltext = "31747-2.htm"
   else :
     htmltext = "<html><body>Quest may only be undertaken by a character of the proper sub-class.</body></html>"
   return htmltext

 def onKill(self,npc,player,isPet):
    # get a random party member that awaits for drops from this quest 
    partyMember = self.getRandomPartyMember(player,"awaitsDrops","1")
    if not partyMember : return
    st = partyMember.getQuestState(qn)
    if st.getInt("cond") == 9 and st.getQuestItemsCount(ORB_OF_BINDING) <= 4 :
      st.giveItems(ORB_OF_BINDING,1)
      st.playSound("ItemSound.quest_itemget")
      if st.getQuestItemsCount(ORB_OF_BINDING) == 5 :
          st.unset("awaitsDrops")
    return 

QUEST       = Quest(242,qn,"Possessor of a Precious Soul - 2")

QUEST.addStartNpc(VIRGIL)

QUEST.addTalkId(VIRGIL)
QUEST.addTalkId(KASSANDRA)
QUEST.addTalkId(OGMAR)
QUEST.addTalkId(MYSTERIOUS_KNIGHT)
QUEST.addTalkId(ANGEL_CORPSE)
QUEST.addTalkId(KALIS)
QUEST.addTalkId(MATILD)
QUEST.addTalkId(FALLEN_UNICORN)
QUEST.addTalkId(CORNERSTONE)
QUEST.addTalkId(PURE_UNICORN)

QUEST.addKillId(RESTRAINER_OF_GLORY)