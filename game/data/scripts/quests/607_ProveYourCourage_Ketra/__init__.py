#Made by Emperorc
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.network.serverpackets import SocialAction
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "607_ProveYourCourage_Ketra"

#NPC
Kadun = 31370
Shadith = 25309

#Quest Items
Shadith_Head = 7235
Valor_Totem = 7219
Ketra_Alliance_Three = 7213

def giveReward(st,npc):
    if st.getState() == State.STARTED :
        npcId = npc.getNpcId()
        cond = st.getInt("cond")
        if npcId == Shadith :
            if st.getPlayer().isAlliedWithKetra() :
                if cond == 1:
                    if st.getPlayer().getAllianceWithVarkaKetra() == 3 and st.getQuestItemsCount(Ketra_Alliance_Three) :
                        st.giveItems(Shadith_Head,1)
                        st.set("cond","2")

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [Shadith_Head]

 def onEvent (self,event,st) :
   htmltext = event
   if event == "31370-04.htm" :
       if st.getPlayer().getAllianceWithVarkaKetra() == 3 and st.getQuestItemsCount(Ketra_Alliance_Three) :
            if st.getPlayer().getLevel() >= 75 :
                    st.set("cond","1")
                    st.setState(State.STARTED)
                    st.playSound("ItemSound.quest_accept")
                    htmltext = "31370-04.htm"
            else :
                htmltext = "31370-03.htm"
                st.exitQuest(1)
       else :
            htmltext = "31370-02.htm"
            st.exitQuest(1)
   elif event == "31370-07.htm" :
       st.takeItems(Shadith_Head,-1)
       st.giveItems(Valor_Totem,1)
       st.addExpAndSp(10000,0)
       ObjectId=st.getPlayer().getObjectId()
       st.getPlayer().broadcastPacket(SocialAction(ObjectId,3))
       st.playSound("ItemSound.quest_finish")
       htmltext = "31370-07.htm"
       st.exitQuest(1)
   return htmltext

 def onTalk (self,npc,player):
    htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
    st = player.getQuestState(qn)
    if st :
      npcId = npc.getNpcId()
      cond = st.getInt("cond")
      Head = st.getQuestItemsCount(Shadith_Head)
      Valor = st.getQuestItemsCount(Valor_Totem)
      if npcId == Kadun :
          if Valor == 0 :
              if Head == 0:
                  if cond != 1 :
                      htmltext = "31370-01.htm"
                  else:
                      htmltext = "31370-06.htm"
              else :
                  htmltext = "31370-05.htm"
    return htmltext

 def onKill(self,npc,player,isPet):
    partyMembers = [player]
    party = player.getParty()
    if party :
       partyMembers = party.getPartyMembers().toArray()
       for player in partyMembers :
           pst = player.getQuestState(qn)
           if pst :
              giveReward(pst,npc)
    else :
       pst = player.getQuestState(qn)
       if pst :
          giveReward(pst,npc)
    return

QUEST       = Quest(607,qn,"Prove Your Courage!")

QUEST.addStartNpc(Kadun)

QUEST.addTalkId(Kadun)

QUEST.addKillId(Shadith)