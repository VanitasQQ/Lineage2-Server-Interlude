# Made by Mr. Have fun! Version 0.2
# Shadow Weapon Coupons contributed by BiTi for the Official L2J Datapack Project
# Visit http://forum.l2jdp.com for more details
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest
from ru.catssoftware.gameserver.network.serverpackets import SocialAction

qn = "414_PathToOrcRaider"

#NPCs
KARUKIA = 30570
KASMAN  = 30501
TAZEER = 31978

#MOBS 
GOBLIN_TOMB_RAIDER_LEADER = 20320
KURUKA_RATMAN_LEADER      = 27045
UMBAR_ORC                 = 27054
TIMORA_ORC                = 27320
 
#ITEMS
GREEN_BLOOD           = 1578
GOBLIN_DWELLING_MAP   = 1579
KURUKA_RATMAN_TOOTH   = 1580
BETRAYER_UMBAR_REPORT = 1589
HEAD_OF_BETRAYER      = 1591
TIMORA_ORC_HEAD       = 8544
 
#REWARD 
MARK_OF_RAIDER = 1592 
 
class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [GREEN_BLOOD, GOBLIN_DWELLING_MAP, KURUKA_RATMAN_TOOTH, BETRAYER_UMBAR_REPORT, HEAD_OF_BETRAYER, TIMORA_ORC_HEAD]

 def onEvent (self,event,st) :
   htmltext = event
   if event == "30570-05.htm" :
     st.set("id","1")
     st.set("cond","1")
     st.setState(State.STARTED)
     st.giveItems(GOBLIN_DWELLING_MAP,1)
     st.playSound("ItemSound.quest_accept")
   elif event == "30570-07a.htm" :
     st.takeItems(KURUKA_RATMAN_TOOTH,-1)
     st.takeItems(GOBLIN_DWELLING_MAP,-1)
     st.takeItems(GREEN_BLOOD,-1)
     st.giveItems(BETRAYER_UMBAR_REPORT,1)
     st.set("id","3")
     st.set("cond","3")
     st.playSound("ItemSound.quest_middle")
   elif event == "30570-07b.htm" :
     st.takeItems(KURUKA_RATMAN_TOOTH,-1)
     st.takeItems(GOBLIN_DWELLING_MAP,-1)
     st.takeItems(GREEN_BLOOD,-1)
     st.set("cond","5")
     st.playSound("ItemSound.quest_middle")
   elif event == "31978-03.htm" :
     st.set("cond","6")
     st.playSound("ItemSound.quest_middle")
   return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if npcId != KARUKIA and id != State.STARTED : return htmltext

   playerClassID = player.getClassId().getId() 
   playerLvl     = player.getLevel() 
   cond = st.getInt("cond") 
 
   if npcId == KARUKIA and cond == 0 : 
     if playerLvl >= 18 and playerClassID == 0x2c and st.getQuestItemsCount(MARK_OF_RAIDER) == 0 and st.getQuestItemsCount(GOBLIN_DWELLING_MAP) == 0 : 
       htmltext = "30570-01.htm" 
     elif playerClassID != 0x2c : 
       if playerClassID == 0x2d : 
         htmltext = "30570-02a.htm" 
       else: 
         htmltext = "30570-03.htm" 
     elif playerLvl < 18 and playerClassID == 0x2c : 
       htmltext = "30570-02.htm" 
     elif playerLvl >= 18 and playerClassID == 0x2c and st.getQuestItemsCount(MARK_OF_RAIDER) == 1 : 
       htmltext = "30570-04.htm" 
     else: 
       htmltext = "30570-02.htm" 
   elif npcId == KARUKIA and cond and st.getQuestItemsCount(GOBLIN_DWELLING_MAP) == 1 and st.getQuestItemsCount(KURUKA_RATMAN_TOOTH) < 10 : 
     htmltext = "30570-06.htm" 
   elif npcId == KARUKIA and cond and st.getQuestItemsCount(GOBLIN_DWELLING_MAP) == 1 and st.getQuestItemsCount(KURUKA_RATMAN_TOOTH) >= 10 and st.getQuestItemsCount(BETRAYER_UMBAR_REPORT) == 0 : 
     htmltext = "30570-07.htm" 
   elif npcId == KARUKIA and cond >5 :
     htmltext = "30570-07b.htm" 
   elif npcId == KARUKIA and cond and st.getQuestItemsCount(BETRAYER_UMBAR_REPORT) and st.getQuestItemsCount(HEAD_OF_BETRAYER) < 2 : 
     htmltext = "30570-08.htm" 
   elif npcId == KARUKIA and cond and st.getQuestItemsCount(BETRAYER_UMBAR_REPORT) and st.getQuestItemsCount(HEAD_OF_BETRAYER) == 2 : 
     htmltext = "30570-09.htm" 
   elif npcId == KASMAN and cond and st.getQuestItemsCount(BETRAYER_UMBAR_REPORT) and st.getQuestItemsCount(HEAD_OF_BETRAYER) == 0 : 
     htmltext = "30501-01.htm" 
   elif npcId == KASMAN and cond and st.getQuestItemsCount(HEAD_OF_BETRAYER) > 0 and st.getQuestItemsCount(HEAD_OF_BETRAYER) < 2 : 
     htmltext = "30501-02.htm" 
   elif npcId == KASMAN and cond and st.getQuestItemsCount(HEAD_OF_BETRAYER) == 2 : 
     htmltext = "30501-03.htm" 
     st.rewardItems(57,81900)
     st.takeItems(HEAD_OF_BETRAYER,-1) 
     st.takeItems(BETRAYER_UMBAR_REPORT,-1) 
     st.giveItems(MARK_OF_RAIDER,1)
     st.addExpAndSp(295862,17354)
     player.sendPacket(SocialAction(player.getObjectId(),3))
     st.unset("cond") 
     st.exitQuest(False) 
     st.playSound("ItemSound.quest_finish")
   elif npcId == TAZEER:
     if cond == 5:
        htmltext = "31978-01.htm" 
     elif cond == 6:
        htmltext = "31978-04.htm" 
     elif cond == 7:
        htmltext = "31978-05.htm"
        st.takeItems(TIMORA_ORC_HEAD,-1)
        st.giveItems(MARK_OF_RAIDER,1)
        st.rewardItems(57,81900)
        st.addExpAndSp(160267,10656)
        player.sendPacket(SocialAction(player.getObjectId(),3))
        st.unset("cond")
        st.exitQuest(False)
        st.playSound("ItemSound.quest_finish")
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return 
   if st.getState() != State.STARTED : return 
   
   cond = st.getInt("cond") 
   npcId = npc.getNpcId()
   xx = int(player.getX())
   yy = int(player.getY())
   zz = int(player.getZ())
   if npcId == GOBLIN_TOMB_RAIDER_LEADER : 
     if cond and st.getQuestItemsCount(GOBLIN_DWELLING_MAP) == 1 and st.getQuestItemsCount(KURUKA_RATMAN_TOOTH) < 10 and st.getQuestItemsCount(GREEN_BLOOD) < 40 : 
       if st.getQuestItemsCount(GREEN_BLOOD) > 1 : 
         if st.getRandom(100) < ((st.getQuestItemsCount(GREEN_BLOOD))*10) : 
           st.takeItems(GREEN_BLOOD,-1) 
           st.addSpawn(KURUKA_RATMAN_LEADER,xx,yy,zz) 
         else: 
           st.giveItems(GREEN_BLOOD,1) 
           st.playSound("ItemSound.quest_itemget") 
       else: 
         st.giveItems(GREEN_BLOOD,1) 
         st.playSound("ItemSound.quest_itemget") 
   elif npcId == KURUKA_RATMAN_LEADER : 
     if cond and st.getQuestItemsCount(GOBLIN_DWELLING_MAP) == 1 and st.getQuestItemsCount(KURUKA_RATMAN_TOOTH) < 10 : 
       st.takeItems(GREEN_BLOOD,-1) 
       if st.getQuestItemsCount(KURUKA_RATMAN_TOOTH) == 9 : 
         st.giveItems(KURUKA_RATMAN_TOOTH,1) 
         st.set("id","2") 
         st.set("cond","2") 
         st.playSound("ItemSound.quest_middle") 
       else: 
         st.giveItems(KURUKA_RATMAN_TOOTH,1) 
         st.playSound("ItemSound.quest_itemget") 
   elif npcId == UMBAR_ORC :
     if cond and st.getQuestItemsCount(BETRAYER_UMBAR_REPORT) > 0 and st.getQuestItemsCount(HEAD_OF_BETRAYER) < 2 : 
       st.giveItems(HEAD_OF_BETRAYER,1) 
       if st.getQuestItemsCount(HEAD_OF_BETRAYER) > 1 : 
         st.set("id","4") 
         st.set("cond","4") 
         st.playSound("ItemSound.quest_middle") 
       else: 
         st.playSound("ItemSound.quest_itemget") 
   elif npcId == TIMORA_ORC :
     if cond == 6:
         st.set("cond","7") 
         st.playSound("ItemSound.quest_middle")
         st.giveItems(TIMORA_ORC_HEAD,1) 
   return

QUEST     = Quest(414,qn,"Path of the Orc Raider")

QUEST.addStartNpc(KARUKIA)

QUEST.addTalkId(KARUKIA)
QUEST.addTalkId(KASMAN)
QUEST.addTalkId(TAZEER)

QUEST.addKillId(GOBLIN_TOMB_RAIDER_LEADER)
QUEST.addKillId(KURUKA_RATMAN_LEADER)
QUEST.addKillId(UMBAR_ORC)
QUEST.addKillId(TIMORA_ORC)