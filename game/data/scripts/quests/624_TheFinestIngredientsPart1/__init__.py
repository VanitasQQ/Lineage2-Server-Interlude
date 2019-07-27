# by disKret
# quest rate fix by M-095
import sys
from ru.catssoftware import Config
from ru.catssoftware.tools.random import Rnd
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "624_TheFinestIngredientsPart1"

#NPC
JEREMY = 31521

#ITEMS
TRUNK_OF_NEPENTHES,FOOT_OF_BANDERSNATCHLING,SECRET_SPICE,SAUCE=range(7202,7206)
CRYOLITE=7080

#MOBS
MOBS = HOT_SPRINGS_ATROX,HOT_SPRINGS_ATROXSPAWN,HOT_SPRINGS_BANDERSNATCHLING,HOT_SPRINGS_NEPENTHES = 21321,21317,21314,21319
ITEMS={
    HOT_SPRINGS_ATROX:SECRET_SPICE,
    HOT_SPRINGS_ATROXSPAWN:SECRET_SPICE,
    HOT_SPRINGS_BANDERSNATCHLING:FOOT_OF_BANDERSNATCHLING,
    HOT_SPRINGS_NEPENTHES:TRUNK_OF_NEPENTHES
}

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [TRUNK_OF_NEPENTHES, FOOT_OF_BANDERSNATCHLING, SECRET_SPICE]

 def onEvent (self,event,st) :
   cond = st.getInt("cond")
   htmltext = event
   trunk = st.getQuestItemsCount(TRUNK_OF_NEPENTHES)
   foot = st.getQuestItemsCount(FOOT_OF_BANDERSNATCHLING)
   spice = st.getQuestItemsCount(SECRET_SPICE)
   if event == "31521-1.htm" :
     if st.getPlayer().getLevel() >= 73 : 
        st.set("cond","1")
        st.setState(State.STARTED)
        st.playSound("ItemSound.quest_accept")       
     else:
        htmltext = "31521-0a.htm"
        st.exitQuest(1)
   elif event == "31521-4.htm" :
     if trunk==foot==spice==50 :
       st.takeItems(TRUNK_OF_NEPENTHES,-1)
       st.takeItems(FOOT_OF_BANDERSNATCHLING,-1)
       st.takeItems(SECRET_SPICE,-1)
       st.playSound("ItemSound.quest_finish")
       st.giveItems(SAUCE,1)
       st.giveItems(CRYOLITE,1)
       htmltext = "31521-4.htm"
       st.exitQuest(1)
     else:
       htmltext="31521-5.htm"
       st.set("cond","1")
   return htmltext

 def onTalk (self,npc,player):
   st = player.getQuestState(qn)
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   if st :
       npcId = npc.getNpcId()
       cond = st.getInt("cond")
       if cond == 0 :
          htmltext = "31521-0.htm"
       elif st.getState() == State.STARTED:
           if cond != 3 :
              htmltext = "31521-2.htm"
           else :
              htmltext = "31521-3.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   partyMember1 = self.getRandomPartyMember(player,"1")
   partyMember2 = self.getRandomPartyMemberState(player, State.COMPLETED)
   if not partyMember1 and not partyMember2 : return
   partyMember = partyMember1
   numItems,chance = divmod(100*Config.RATE_DROP_QUEST,100)
   dropchance = Rnd.get(100)
   if dropchance  < chance:
    # player who has State.COMPLETED up to 2 out of 3 item collections may consume the party drop
    if partyMember2 :
      if Rnd.get(100) <= 66:
         return
      else :
         partyMember = partyMember1
   st = partyMember.getQuestState(qn)
   if st :
        if st.getState() == State.STARTED :
            npcId = npc.getNpcId()
            if st.getInt("cond") == 1:
             if dropchance < chance :
               numItems = numItems + 1
             numItems = int(numItems)
             item = ITEMS[npcId]
             count = st.getQuestItemsCount(item)
             if count < 50 :
               if count + numItems > 50 :
                 numItems = 50 - count
               st.giveItems(item,numItems)
               count_trunk = st.getQuestItemsCount(TRUNK_OF_NEPENTHES)
               count_foot = st.getQuestItemsCount(FOOT_OF_BANDERSNATCHLING)
               count_spice = st.getQuestItemsCount(SECRET_SPICE)
               if count_trunk == count_foot == count_spice == 50 :
                 st.set("cond","3")
                 st.playSound("ItemSound.quest_middle")
               else:
                 st.playSound("ItemSound.quest_itemget")  
   return

QUEST       = Quest(624,qn,"The Finest Ingredients - Part 1")

QUEST.addStartNpc(JEREMY)
QUEST.addTalkId(JEREMY)

for i in MOBS :
  QUEST.addKillId(i)