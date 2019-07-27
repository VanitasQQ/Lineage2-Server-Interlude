# Rate fix by Gnat

import sys
from ru.catssoftware import Config
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "385_YokeofthePast"

ANCIENT_SCROLL = 5902

CHANCE={
    21208:7,  #Hallowed Watchman 
    21209:8,  #Hallowed Seer
    21210:11, #Vault Guardian
    21211:11, #Vault Seer 
    21212:12, #Hallowed Sentinel
    21213:14, #Hallowed Monk 
    21214:19, #Vault Sentinel 
    21215:19, #Vault Monk 
    21216:22, #Overlord of the Holy Lands
    21217:24, #Hallowed Priest 
    21218:30, #Vault Overlord
    21219:30, #Vault Priest 
    21220:35, #Sepulcher Archon
    21221:37, #Sepulcher Inquisitor 
    21222:46, #Sepulcher Archon 
    21223:45, #Sepulcher Inquisitor
    21224:50, #Sepulcher Guardian 
    21225:54, #Sepulcher Sage 
    21226:66, #Sepulcher Guardian 
    21227:64, #Sepulcher Sage 
    21228:70, #Sepulcher Guard 
    21229:75, #Sepulcher Preacher 
    21230:91, #Sepulcher Guard 
    21231:86, #Sepulcher Preacher 
    21232:7, #Barrow Guardian
    21233:8, #Barrow Seer
    21234:11, #Grave Guardian
    21235:11, #Grave Seer
    21236:12, #Barrow Sentinel 
    21237:14, #Barrow Monk 
    21238:19, #Grave Sentinel 
    21239:19, #Grave Monk 
    21240:22, #Barrow Overlord 
    21241:24, #Barrow Priest 
    21242:30, #Grave Overlord
    21243:30, #Grave Priest 
    21244:34, #Crypt Archon 
    21245:37, #Crypt Inquisitor
    21246:46, #Tomb Archon 
    21247:45, #Tomb Inquisitor 
    21248:50, #Crypt Guardian 
    21249:54, #Crypt Sage
    21250:99, #Tomb Guardian
    21251:64, #Tomb Sage 	
    21252:70, #Crypt Guard 
    21253:75, #Crypt Preacher 
    21254:91, #Tomb Guard 
    21255:86  #Tomb Preacher 
}

class Quest (JQuest) :

 def __init__(self,id,name,descr): 
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = []

 def onEvent (self,event,st) :
    htmltext = event
    if event == "14.htm" :
      st.setState(State.STARTED)
      st.playSound("ItemSound.quest_accept")
      st.set("cond","1")
    elif event == "17.htm" :
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
     htmltext = "10.htm"
   elif st.getInt("cond") == 1 and st.getQuestItemsCount(ANCIENT_SCROLL) == 0 :
     htmltext = "16.htm"
   elif st.getInt("cond") == 1 and st.getQuestItemsCount(ANCIENT_SCROLL) :
     numancientscrolls = st.getQuestItemsCount(ANCIENT_SCROLL)
     st.giveItems(5965,numancientscrolls)
     st.takeItems(ANCIENT_SCROLL,-1)
     htmltext = "16.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
    partyMember = self.getRandomPartyMemberState(player, State.STARTED)
    if not partyMember : return
    st = partyMember.getQuestState(qn)
    chance = CHANCE[npc.getNpcId()]
    numItems, chance = divmod(chance*Config.RATE_DROP_QUEST,100)
    if st.getRandom(100) < chance : 
       numItems += 1
    if numItems :
      st.rewardItems(ANCIENT_SCROLL,int(numItems))
      st.playSound("ItemSound.quest_itemget")
    return

QUEST       = Quest(385,qn,"Yoke of the Past")

for npcId in range(31095,31126):
    if npcId in [31111,31112,31113]:
        continue
    QUEST.addTalkId(npcId)
    QUEST.addStartNpc(npcId)

for mobs in range(21208,21255):
    QUEST.addKillId(mobs)