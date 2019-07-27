# Created by CubicVirtuoso
# Any problems feel free to drop by #l2j-datapack on irc.freenode.net
# quest rate fix by M-095
import sys
from ru.catssoftware import Config 
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "431_WeddingMarch"

MELODY_MAESTRO_KANTABILON_ID = 31042
SILVER_CRYSTAL_ID = 7540
LIENRIKS_ID = 20786
LIENRIKS_LAD_ID = 20787
WEDDING_ECHO_CRYSTAL_ID = 7062

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [SILVER_CRYSTAL_ID]
 
 def onEvent (self,event,st) :
     htmltext = event
     cond = st.getInt("cond")
     if event == "1" and cond == 0 :
         htmltext = "31042-02.htm"
         st.set("cond","1")
         st.setState(State.STARTED)
         st.playSound("ItemSound.quest_accept")
     elif event == "3" and st.getQuestItemsCount(SILVER_CRYSTAL_ID) == 50 :
         st.giveItems(WEDDING_ECHO_CRYSTAL_ID,25)
         st.takeItems(SILVER_CRYSTAL_ID,50)
         htmltext = "31042-05.htm"
         st.playSound("ItemSound.quest_finish")
         st.exitQuest(1)
     return htmltext
 
 def onTalk (self,npc,player):
     htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
     st = player.getQuestState(qn)
     if not st : return htmltext

     npcId = npc.getNpcId()
     id = st.getState()
     cond = st.getInt("cond")
     id = st.getState()
     if id == State.CREATED :
         htmltext = "31042-01.htm"
     elif cond == 1 :
         htmltext = "31042-03.htm"
     elif cond == 2 :
         htmltext = "31042-04.htm"
     return htmltext
 
 def onKill(self,npc,player,isPet):
     partyMember = self.getRandomPartyMember(player,"1")
     if not partyMember : return
     st = partyMember.getQuestState(qn) 
     count = st.getQuestItemsCount(SILVER_CRYSTAL_ID)
     if st.getInt("cond") == 1 and count < 50 :
        chance = 100 * Config.RATE_DROP_QUEST
        numItems, chance = divmod(chance,100)
        if st.getRandom(100) < chance : 
           numItems += 1
        if numItems :
           if count + numItems >= 50 :
              numItems = 50 - count
              st.playSound("ItemSound.quest_middle")
              st.set("cond","2")
           else:
              st.playSound("ItemSound.quest_itemget")
           st.giveItems(SILVER_CRYSTAL_ID,int(numItems))
     return
 
QUEST       = Quest(431,qn,"Wedding March")

QUEST.addStartNpc(31042)

QUEST.addTalkId(31042)

QUEST.addKillId(20786)
QUEST.addKillId(20787)