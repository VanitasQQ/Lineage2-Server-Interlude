#Made by Kerb
# quest rate fix by M-095
import sys
from java.lang import System
from ru.catssoftware import Config 
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest
from ru.catssoftware.gameserver.network.serverpackets import NpcSay
from ru.catssoftware.tools.random import Rnd
from ru.catssoftware.gameserver.model.entity import GrandBossState
from ru.catssoftware.gameserver.model.entity.GrandBossState import StateEnum

qn = "625_TheFinestIngredientsPart2"
#Npcs
JEREMY = 31521
TABLE = 31542
#RaidBoss
BUMPALUMP = 25296
#Items
SAUCE = 7205
FOOD = 7209
MEAT = 7210
#Rewards dye +2str-2con/+2str-2dex/+2con-2str/+2con-2dex/+2dex-2str/+2dex-2con
REWARDS = range (4589,4595)

def AutoChat(npc,text) :
    chars = npc.getKnownList().getKnownPlayers().values().toArray()
    if chars != None:
       for pc in chars :
          sm = NpcSay(npc.getObjectId(), 0, npc.getNpcId(), text)
          pc.sendPacket(sm)

class Quest (JQuest) :
 def __init__(self,id,name,descr):
 	JQuest.__init__(self,id,name,descr)
 	self.questItemIds = [FOOD, MEAT]
	self.gstate = GrandBossState(BUMPALUMP)
 	test = self.loadGlobalQuestVar("625_respawn")
 	if test.isdigit() :
 	   remain = long(test) - System.currentTimeMillis()
 	   if remain <= 0 :
 	      self.addSpawn(31542,157136,-121456,-2363,40000, False, 0, True)
 	   else :
 	      self.startQuestTimer("spawn_npc", remain, None, None)
 	else:
 	   self.addSpawn(31542,157136,-121456,-2363,40000, False, 0, True)

 def onAdvEvent (self, event, npc, player) :
   if event == "Icicle Emperor Bumbalump has despawned" :
      npc.reduceCurrentHp(9999999,npc,None)
      self.addSpawn(31542,157136,-121456,-2363,40000, False, 0, True)
      AutoChat(npc,"The good fragrant flavor...")
      return
   elif event == "spawn_npc" :
      self.addSpawn(31542,157136,-121456,-2363,40000, False, 0, True)
      return
   st = player.getQuestState(qn)
   if not st: return
   cond = st.getInt("cond")
   htmltext = event
   if event == "31521-02.htm" :
      if st.getPlayer().getLevel() < 73 : 
         htmltext = "31521-00b.htm"
         st.exitQuest(1)
      else:
         st.set("cond","1")
         st.setState(State.STARTED)
         st.takeItems(SAUCE,1)
         st.giveItems(FOOD,1)
         st.playSound("ItemSound.quest_accept")
   elif event == "31542-02.htm" :
       if st.getQuestItemsCount(FOOD) == 0 :
           htmltext = "31542-04.htm"
       else:
	   if self.gstate.getState() == StateEnum.INTERVAL :
              if System.currentTimeMillis() < self.gstate.getRespawnDate() :
                    return "<html><body><center><br>No time to call</body></html>"
           spawnId = st.addSpawn(BUMPALUMP,158240,-121536,-2253)
           st.takeItems(FOOD,1)
           npc.deleteMe()
           st.set("cond","2")
           self.startQuestTimer("Icicle Emperor Bumbalump has despawned",1200000,spawnId,None)
           AutoChat(spawnId,"not!")
   elif event == "31521-04.htm" :
      if st.getQuestItemsCount(MEAT) >= 1 :
         st.takeItems(MEAT,1)
         st.giveItems(REWARDS[st.getRandom(len(REWARDS))],5)
         st.exitQuest(1)
         htmltext = "31521-04.htm"
      else:
         htmltext = "31521-05.htm"
         st.exitQuest(1)
   return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if st :
     npcId = npc.getNpcId()
     id = st.getState()
     cond = st.getInt("cond")
     if cond == 0 :
       if npcId == JEREMY :
         if st.getQuestItemsCount(SAUCE) >= 1 :
           htmltext = "31521-01.htm"
         else:
           htmltext = "31521-00a.htm"
     elif cond == 1 :
       if npcId == JEREMY :
         htmltext = "31521-02a.htm"
       if npcId == TABLE :
         htmltext = "31542-01.htm"
     elif cond == 2 :
       if npcId == JEREMY :
         htmltext = "31521-03a.htm"
       if npcId == TABLE :
         htmltext = "31542-01.htm"
     elif cond == 3 :
       if npcId == JEREMY :
         htmltext = "31521-03.htm"
       if npcId == TABLE :
         htmltext = "31542-05.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
    npcId = npc.getNpcId()
    if npcId == BUMPALUMP :
        respawnMinDelay = 43200000  * int(Config.RAID_MIN_RESPAWN_MULTIPLIER)
        respawnMaxDelay = 129600000 * int(Config.RAID_MAX_RESPAWN_MULTIPLIER)
        respawn_delay = Rnd.get(respawnMinDelay,respawnMaxDelay)
        self.gstate.setRespawnDate(24*60*60000) 
        self.gstate.setState(StateEnum.INTERVAL)
        self.saveGlobalQuestVar("625_respawn", str(System.currentTimeMillis()+respawn_delay))
        self.startQuestTimer("spawn_npc", respawn_delay, None, None)
        self.cancelQuestTimer("Icicle Emperor Bumbalump has despawned",npc,None)
        party = player.getParty()
        if party :
            PartyQuestMembers = []
            for player1 in party.getPartyMembers().toArray() :
                st1 = player1.getQuestState(qn)
                if st1 :
                    if st1.getState() == State.STARTED and (st1.getInt("cond") == 1 or st1.getInt("cond") == 2) :
                        PartyQuestMembers.append(st1)
            if len(PartyQuestMembers) == 0 : return
            st = PartyQuestMembers[Rnd.get(len(PartyQuestMembers))]
            if st.getQuestItemsCount(FOOD) > 0 :
                st.takeItems(FOOD,1)
            st.giveItems(MEAT,1)
            st.set("cond","3")
            st.playSound("ItemSound.quest_middle")
        else :
            st = player.getQuestState(qn)
            if not st : return
            if st.getState() == State.STARTED and (st.getInt("cond") == 1 or st.getInt("cond") == 2) :
                if st.getQuestItemsCount(FOOD) > 0 :
                    st.takeItems(FOOD,1)
                st.giveItems(MEAT,1)
                st.set("cond","3")
                st.playSound("ItemSound.quest_middle")
    return

QUEST = Quest(625,qn,"The Finest Ingredients - Part 2")

QUEST.addStartNpc(JEREMY)

QUEST.addTalkId(JEREMY)
QUEST.addTalkId(TABLE)

QUEST.addKillId(BUMPALUMP)