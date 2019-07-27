#Hunt of the Golden Ram Mercenary Force
# Made by Polo - Have fun!..... fix & addition by t0rm3nt0r and LEX
# Rate fix by Gnat
import sys
from ru.catssoftware import Config
from ru.catssoftware.gameserver.datatables import SkillTable
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "628_HuntGoldenRam"

#Npcs
KAHMAN = 31554
ABERCROMBIE = 31555
SELINA = 31556

#Items
CHITIN = 7248   #Splinter Stakato Chitin
CHITIN2 = 7249  #Needle Stakato Chitin
RECRUIT = 7246  #Golden Ram Badge - Recruit
SOLDIER = 7247  #Golden Ram Badge - Soldier
GOLDEN_RAM_COIN = 7251 #Golden Ram Coin

#chances
MAX=100
CHANCE={
    21508:50,
    21509:43,
    21510:52,
    21511:57,
    21512:75,
    21513:50,
    21514:43,
    21515:52,
    21516:53,
    21517:74
}

BUFF={
"1":[4404,2,2],#Focus: Requires 2 Golden Ram Chits
"2":[4405,2,2],#Death Whisper: Requires 2 Golden Ram Chits
"3":[4393,3,3],#Might: Requires 3 Golden Ram Chits
"4":[4400,2,3],#Acumen: Requires 3 Golden Ram Chits
"5":[4397,1,3],#Berserker: Requires 3 Golden Ram Chits
"6":[4399,2,3],#Vampiric Rage: Requires 3 Golden Ram Chits
"7":[4401,1,6],#Empower: Requires 6 Golden Ram Chits
"8":[4402,2,6],#Haste: Requires 6 Golden Ram Chits
}

#needed count
#count = 100

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = range(7246,7250)

 def onAdvEvent (self,event,npc,player) :
    st = player.getQuestState(qn)
    if not st: return
    htmltext = event
    cond = st.getInt("cond")
    if htmltext == "31554-03a.htm" : #Giving 100 Splinter Stakato Chitins. Getting Recruit mark
       if st.getQuestItemsCount(CHITIN)>=100 and cond == 1 :
          st.set("cond","2")
          st.takeItems(CHITIN,-1)
          st.giveItems(RECRUIT,1)
          htmltext = "31554-04.htm"
    elif event == "31554-07.htm" : #Cancelling the quest
       st.exitQuest(1)
       st.playSound("ItemSound.quest_giveup")
    elif event in BUFF.keys() and cond == 3 : #Asking for buff
        skillId,level,coins=BUFF[event]
        if st.getQuestItemsCount(GOLDEN_RAM_COIN) >= coins :
          st.takeItems(GOLDEN_RAM_COIN,coins)
          npc.setTarget(player)
          npc.doCast(SkillTable.getInstance().getInfo(skillId,level))
          htmltext = "31556-1.htm"
        else :
          htmltext = "You don't have required items"
    return htmltext

 def onTalk (self,npc,player):
   st = player.getQuestState(qn)
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   if st :
       npcId = npc.getNpcId()
       cond = st.getInt("cond")
       id = st.getState()
       if id == State.COMPLETED :
         st.setState(State.STARTED)
         st.set("cond","3")
       chitin1=st.getQuestItemsCount(CHITIN)
       chitin2=st.getQuestItemsCount(CHITIN2)
       if cond == 0 : #Starting the quest
          if player.getLevel()>= 66 : #Succesful start: Kill Splinter Stakato
             htmltext = "31554-02.htm"
             st.set("cond","1")
             st.setState(State.STARTED)
             st.playSound("ItemSound.quest_accept")
          else :
             htmltext = "31554-01.htm" #not qualified
             st.exitQuest(1)
       elif id == State.STARTED :
           if cond == 1 : #Bringin Splinter Stakato chitins
              if npcId == KAHMAN :
                 if chitin1>=100 :
                    htmltext = "31554-03.htm" #Enough. Ready to give
                 else:
                    htmltext = "31554-03a.htm" # Need more chitins
           elif cond == 2 : # Bring more chitins of Splinter and Needle Stakato
              if npcId == ABERCROMBIE : # Trader: first multisell
                 htmltext = "31555-1.htm" 
                 return htmltext
              if npcId == SELINA : # Buffer: not qualified
                 return htmltext
              elif chitin1>=100 and chitin2>=100 : #Enough chitins. Ending the quest, Soldier mark.
                 htmltext = "31554-05.htm"
                 st.takeItems(CHITIN,-1)
                 st.takeItems(CHITIN2,-1)
                 st.takeItems(RECRUIT,1)
                 st.giveItems(SOLDIER,1)
                 st.set("cond","3")
                 st.playSound("ItemSound.quest_finish")
              elif not chitin1 and not chitin2: #Have no chitins. Can stop the quest
                 htmltext = "31554-04b.htm"
              else :
                 htmltext = "31554-04a.htm" #Not enough chitins. Bring more
           elif cond == 3 : #Soldier mark - last stage
              htmltext = "31554-05a.htm" #Can stop the quest
              if npcId == ABERCROMBIE :
                 htmltext = "31555-2.htm" #Trader: second multisell
              elif npcId == SELINA :
                 htmltext = "31556-1.htm" #Buffer: buffs list
   return htmltext

 def onKill(self,npc,player,isPet):
   partyMember = self.getRandomPartyMemberState(player, State.STARTED)
   if not partyMember : return
   st = partyMember.getQuestState(qn)
   if st :
        if st.getState() == State.STARTED :
            npcId = npc.getNpcId()
            cond = st.getInt("cond")
            chance = CHANCE[npcId]
            numItems, chance = divmod(chance*Config.RATE_DROP_QUEST,100)
            if st.getRandom(100) < chance : 
               numItems += 1
            item = 0
            if cond in [1,2] and npcId in range(21508,21513): #Splinter Stakatos
               item = CHITIN       
            elif cond==2 and npcId in range(21513,21518): #Needle Stakatos
               item = CHITIN2
            if cond in [1,2] and item != 0 and numItems >= 1 :
               count = st.getQuestItemsCount(item)
	       if count < 100 :
                   if count + numItems >= 100 :
                      numItems = 100 - count
                      st.playSound("ItemSound.quest_middle")
                   else:
                      st.playSound("ItemSound.quest_itemget")
                   st.giveItems(item,int(numItems))
   return
           
QUEST       = Quest(628,qn,"Hunt of the Golden Ram Mercenary Force")

QUEST.addStartNpc(KAHMAN)

QUEST.addTalkId(KAHMAN)
QUEST.addTalkId(ABERCROMBIE)
QUEST.addTalkId(SELINA)

for mob in range(21508,21518):
    QUEST.addKillId(mob)