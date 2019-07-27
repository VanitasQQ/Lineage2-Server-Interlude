# Made by mtrix
# Rate fix by Gnat
import sys
from ru.catssoftware import Config
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "354_ConquestOfAlligatorIsland"

ADENA = 57
ALLIGATOR_TOOTH = 5863
TORN_MAP_FRAGMENT = 5864
PIRATES_TREASURE_MAP = 5915
CHANCE = 45
CHANCE2 = 10
#These items are custom, since we don't have info about them. Feel free to change them as you see fit (DrLecter)
#Syntax: [itemid,max qty],
RANDOM_REWARDS=[[736,int(15)], #SoE
                [1061,int(20)],#Healing Potion
                [734,int(15)], #Haste Potion
                [735,int(15)], #Alacrity Potion
                [1878,int(35)],#Braided Hemp
                [1875,int(15)],#Stone of Purity
                [1879,int(15)],#Cokes
                [1880,int(15)],#Steel
                [956,1],  #Enchant Armor D
                [955,1],  #Enchant Weapon D
               ]

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [ALLIGATOR_TOOTH, TORN_MAP_FRAGMENT]

 def onEvent (self,event,st) :
     htmltext = event
     amount = st.getQuestItemsCount(ALLIGATOR_TOOTH)
     maps = divmod(st.getQuestItemsCount(TORN_MAP_FRAGMENT),10)
     bonus1 = 3100
     bonus2 = 0
     if event == "30895-00a.htm" :
         st.exitQuest(1)
     elif event == "1" :
         st.setState(State.STARTED)
         st.set("cond","1")
         htmltext = "30895-02.htm"
         st.playSound("ItemSound.quest_accept")
     elif event == "30895-06.htm" :
         if st.getQuestItemsCount(TORN_MAP_FRAGMENT)>=10 :
             htmltext = "30895-07.htm"
     elif event == "30895-05.htm" :
         if amount :
             if amount >= 100:
               bonus2 = 10700
             st.rewardItems(ADENA,amount*220 + bonus1 + bonus2)
             st.takeItems(ALLIGATOR_TOOTH,-1)
             st.playSound("ItemSound.quest_itemget")
             htmltext = "30895-05a.htm"
             if amount > 99 :
                htmltext = "30895-05b.htm"
                item=RANDOM_REWARDS[st.getRandom(len(RANDOM_REWARDS))]
                st.rewardItems(item[0],st.getRandom(item[1])+1)
     elif event == "30895-08.htm" :
         st.giveItems(PIRATES_TREASURE_MAP,maps[0])
         st.takeItems(TORN_MAP_FRAGMENT,maps[0]*10)
     elif event == "30895-09.htm" :
         st.exitQuest(1)
         st.playSound("ItemSound.quest_finish")
     return htmltext

 def onTalk (self,npc,player):
     htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
     st = player.getQuestState(qn)
     if not st : return htmltext

     npcId = npc.getNpcId()
     id = st.getState()
     level = player.getLevel()
     cond = st.getInt("cond")
     if id == State.CREATED :
        if level>=38 :
           htmltext = "30895-01.htm"
        else :
           htmltext = "30895-00.htm"
     elif cond==1 :
         htmltext = "30895-03.htm"
     return htmltext

 def onKill(self,npc,player,isPet):
     partyMember = self.getRandomPartyMemberState(player,State.STARTED)
     if not partyMember : return
     st = partyMember.getQuestState(qn)
     npcId = npc.getNpcId()
     cond = st.getInt("cond")
     numItems, chance = divmod(CHANCE*Config.RATE_DROP_QUEST,100)
     random = st.getRandom(100)
     if random < chance :
         numItems += 1
     if numItems :
         st.giveItems(ALLIGATOR_TOOTH,int(numItems))
         st.playSound("ItemSound.quest_itemget")
     if random<=CHANCE2 and st.getQuestItemsCount(TORN_MAP_FRAGMENT)<10 :
         st.giveItems(TORN_MAP_FRAGMENT,1)
     return

QUEST       = Quest(354,qn,"Conquest Of Alligator Island")

QUEST.addStartNpc(30895)

QUEST.addTalkId(30895)

for i in range(20804,20809)+[20991] :
    QUEST.addKillId(i)