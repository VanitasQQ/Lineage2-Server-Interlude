# Made by Kerberos - based on a L2Fortress script
# this script is part of the Official L2J Datapack Project.
# Visit http://forum.l2jdp.com for more details.
import sys
from ru.catssoftware.gameserver.ai import CtrlIntention
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest
from ru.catssoftware.gameserver.model import L2CharPosition
from ru.catssoftware.gameserver.network.serverpackets import NpcSay

qn = "21_HiddenTruth"

ROUTES={
1:[52373,-54296,-3136,0],
2:[52451,-52921,-3152,0],
3:[51909,-51725,-3125,0],
4:[52438,-51240,-3097,0],
5:[52143,-51418,-3085,0]
}

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [7140]

 def onAdvEvent (self,event,npc,player):
        st = player.getQuestState(qn)
        if not st : return
        htmltext = event
        if event == "31522-02.htm":
            st.setState(State.STARTED)
            st.playSound("ItemSound.quest_accept")
            st.set("cond","1")
        elif event == "31328-05.htm":
            st.set("cond","0")
            st.set("onlyone","1")
            st.unset("AGRIPEL")
            st.unset("DOMINIC")
            st.unset("BENEDICT")
            st.exitQuest(False)
            st.takeItems(7140,-1)
            if st.getQuestItemsCount(7141) == 0 :
                st.giveItems(7141,1)
                st.addExpAndSp(131228,11978)
            st.playSound("ItemSound.quest_finish")
            htmltext = "31328-05.htm"
        elif event == "31523-03.htm" :
            st.playSound("SkillSound5.horror_02")
            st.set("cond","2")
            ghost = st.addSpawn(31524,51432,-54570,-3136,180000)
            ghost.broadcastPacket(NpcSay(ghost.getObjectId(),0,ghost.getNpcId(),"Who awoke me?"))
        elif event == "31524-06.htm" :
            st.set("cond","3")
            st.playSound("ItemSound.quest_middle")
            ghost = self.addSpawn(31525,npc)
            ghost.broadcastPacket(NpcSay(ghost.getObjectId(),0,ghost.getNpcId(),"My master has instructed me to be your guide, "+ player.getName()))
            self.startQuestTimer("1",1,ghost,player)
            self.startQuestTimer("despawn",180000,ghost,player)
        elif event == "31526-03.htm" :
            st.playSound("ItemSound.item_drop_equip_armor_cloth")
        elif event == "31526-08.htm" :
            st.playSound("AmdSound.ed_chimes_05")
            st.set("cond","5")
            st.playSound("ItemSound.quest_middle")
        elif event == "31526-14.htm" :
            st.giveItems(7140,1)
            st.set("cond","6")
            st.playSound("ItemSound.quest_middle")
        elif event == "despawn" :
            npc.deleteMe()
            return
        elif event.isdigit() :
            loc = int(event)
            x,y,z,heading=ROUTES[loc]
            if event == "1" :
                npc.getAI().setIntention(CtrlIntention.AI_INTENTION_MOVE_TO, L2CharPosition(x,y,z,heading))
                self.startQuestTimer("2",5000,npc,player)
            elif event == "2" :
                npc.getAI().setIntention(CtrlIntention.AI_INTENTION_MOVE_TO, L2CharPosition(x,y,z,heading))
                self.startQuestTimer("3",12000,npc,player)
            elif event == "3" :
                npc.getAI().setIntention(CtrlIntention.AI_INTENTION_MOVE_TO, L2CharPosition(x,y,z,heading))
                self.startQuestTimer("4",15000,npc,player)
            elif event == "4" :
                npc.getAI().setIntention(CtrlIntention.AI_INTENTION_MOVE_TO, L2CharPosition(x,y,z,heading))
                self.startQuestTimer("5",5000,npc,player)
            elif event == "5" :
                npc.getAI().setIntention(CtrlIntention.AI_INTENTION_MOVE_TO, L2CharPosition(x,y,z,heading))
            return
        return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext
   npcId = npc.getNpcId()
   cond = st.getInt("cond")
   onlyone = st.getInt("onlyone")
   state = st.getState()
   if state == State.COMPLETED :
      htmltext = "<html><body>This quest has already been completed.</body></html>"
   elif npcId == 31522 :
     if state == State.CREATED :
        if st.getPlayer().getLevel() >= 63 :
           htmltext = "31522-01.htm"
        else:
           htmltext = "31522-03.htm"
           st.exitQuest(1)
     elif cond == 1 :
       htmltext = "31522-05.htm"
   elif npcId == 31523 :
     if cond == 1 :
       htmltext = "31523-01.htm"
     elif cond == 2 :
       htmltext = "31523-04.htm"
       st.playSound("SkillSound5.horror_02")
   elif npcId == 31524 :
     if cond == 2 :
       htmltext = "31524-01.htm"
     elif cond == 3 :
       htmltext = "31524-07b.htm"
       st.set("cond","4")
       st.playSound("ItemSound.quest_middle")
     elif cond == 4 :
       htmltext = "31524-07c.htm"
   elif npcId == 31525 :
     if cond == 3 :
       htmltext = "31525-01.htm"
     elif cond == 4 and id == 1 :
       htmltext = "31525-02.htm"
   elif npcId == 31526 :
     if cond in [3,4] :
       htmltext = "31526-01.htm"
     elif cond == 5 :
       htmltext = "31526-10.htm"
       st.playSound("AmdSound.ed_chimes_05")
     elif cond == 6 :
       htmltext = "31526-15.htm"
   elif npcId == 31348 and st.getQuestItemsCount(7140) == 1 :
     if cond == 6 :
       st.set("AGRIPEL","1")
       if st.getInt("AGRIPEL") == 1 and st.getInt("DOMINIC") == 1 and st.getInt("BENEDICT") == 1 :
         htmltext = "31348-02.htm"
         st.set("cond","7")
         st.playSound("ItemSound.quest_middle")
         return htmltext
       htmltext = "31348-0"+str(st.getRandom(3))+".htm"
     elif cond == 7 :
       htmltext = "31348-03.htm"
   elif npcId == 31350 and st.getQuestItemsCount(7140) == 1 :
     if cond == 6 :
       st.set("DOMINIC","1")
       if st.getInt("AGRIPEL") == 1 and st.getInt("DOMINIC") == 1 and st.getInt("BENEDICT") == 1 :
         htmltext = "31350-02.htm"
         st.set("cond","7")
         st.playSound("ItemSound.quest_middle")
         return htmltext
       htmltext = "31350-0"+str(st.getRandom(3))+".htm"
     elif cond == 7 :
       htmltext = "31350-03.htm"
   elif npcId == 31349 and st.getQuestItemsCount(7140) == 1 :
     if cond == 6 :
       st.set("BENEDICT","1")
       if st.getInt("AGRIPEL") == 1 and st.getInt("DOMINIC") == 1 and st.getInt("BENEDICT") == 1 :
         htmltext = "31349-02.htm"
         st.set("cond","7")
         st.playSound("ItemSound.quest_middle")
         return htmltext
       htmltext = "31349-0"+str(st.getRandom(3))+".htm"
     elif cond == 7 :
       htmltext = "31349-03.htm"
   elif npcId == 31328 :
     if cond == 7 :
       if st.getQuestItemsCount(7140) == 1 :
         htmltext = "31328-01.htm"
     elif cond == 0 and onlyone == 1 :
       htmltext = "31328-06.htm"
   return htmltext

QUEST     = Quest(21,qn,"Hidden Truth")

QUEST.addStartNpc(31522)

for NPC in [31522,31523,31524,31525,31526,31348,31349,31350,31328]:
  QUEST.addTalkId(NPC)