# Made by Mr. - Version 0.3 by DrLecter
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "316_DestroyPlaguebringers"

WERERAT_FANG = 1042
VAROOL_FOULCLAWS_FANG = 1043
ADENA = 57

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [WERERAT_FANG, VAROOL_FOULCLAWS_FANG]

 def onEvent (self,event,st) :
    htmltext = event
    if event == "30155-04.htm" :
        st.set("cond","1")
        st.setState(State.STARTED)
        st.playSound("ItemSound.quest_accept")
    elif event == "30155-08.htm" :
        st.exitQuest(1)
        st.playSound("ItemSound.quest_finish")
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
     if player.getRace().ordinal() != 1 :
       htmltext = "30155-00.htm"
       st.exitQuest(1)
     elif player.getLevel() >= 18 :
       htmltext = "30155-03.htm"
     else:
       htmltext = "30155-02.htm"
       st.exitQuest(1)
   else :
     rats=st.getQuestItemsCount(WERERAT_FANG)
     varool=st.getQuestItemsCount(VAROOL_FOULCLAWS_FANG)
     if rats or varool :
       htmltext = "30155-07.htm"
       amount=rats*30+varool*10000
       if rats+varool > 9 :
          amount += 5000
       st.rewardItems(ADENA,amount)
       st.takeItems(WERERAT_FANG,-1)
       st.takeItems(VAROOL_FOULCLAWS_FANG,-1)
     else:
       htmltext = "30155-05.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return 
   if st.getState() != State.STARTED : return 
   
   npcId = npc.getNpcId()
   if npcId == 27020 :
     if st.getQuestItemsCount(VAROOL_FOULCLAWS_FANG) == 0 and st.getRandom(10)>7:
       st.giveItems(VAROOL_FOULCLAWS_FANG,1)
       st.playSound("ItemSound.quest_middle")
   elif st.getRandom(10)>5 :
     st.giveItems(WERERAT_FANG,1)
     st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(316,qn,"Destroy Plaguebringers")

QUEST.addStartNpc(30155)

QUEST.addTalkId(30155)

QUEST.addKillId(20040)
QUEST.addKillId(20047)
QUEST.addKillId(27020)