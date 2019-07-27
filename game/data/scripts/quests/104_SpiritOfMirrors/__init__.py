# Made by Mr. Have fun! - Version 0.5 updated by Censor for www.l2jdp.com 
# quest rate fix by M-095
import sys
from ru.catssoftware import Config 
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "104_SpiritOfMirrors" 

GALLINS_OAK_WAND = 748 
WAND_SPIRITBOUND1 = 1135 
WAND_SPIRITBOUND2 = 1136 
WAND_SPIRITBOUND3 = 1137 
WAND_OF_ADEPT = 747
#Newbie/one time rewards section
#Any quest should rely on a unique bit, but
#it could be shared among quest that were mutually
#exclusive or race restricted.
#Bit #1 isn't used for backwards compatibility.
NEWBIE_REWARD = 2
SPIRITSHOT_NO_GRADE_FOR_BEGINNERS = 5790 
SPIRITSHOT_NO_GRADE = 2509 
SOULSHOT_NO_GRADE = 1835

DROPLIST = { 
27003: (WAND_SPIRITBOUND1), 
27004: (WAND_SPIRITBOUND2), 
27005: (WAND_SPIRITBOUND3) 
} 

# Helper function - If player have all quest items returns 1, otherwise 0 
def HaveAllQuestItems (st) : 
  for mobId in DROPLIST.keys() : 
    if st.getQuestItemsCount(DROPLIST[mobId]) == 0 : 
      return 0 
  return 1 

# Main Quest code 
class Quest (JQuest) : 

 def __init__(self,id,name,descr):
   JQuest.__init__(self,id,name,descr)
   self.questItemIds = [GALLINS_OAK_WAND, WAND_SPIRITBOUND1, WAND_SPIRITBOUND2, WAND_SPIRITBOUND3]

 def onEvent (self,event,st) : 
    htmltext = event 
    if event == "30017-03.htm" : 
      st.set("cond","1") 
      st.setState(State.STARTED)
      st.playSound("ItemSound.quest_accept") 
      st.giveItems(GALLINS_OAK_WAND,1) 
      st.giveItems(GALLINS_OAK_WAND,1) 
      st.giveItems(GALLINS_OAK_WAND,1) 
    return htmltext 

 def onTalk (self,npc,player): 
   npcId = npc.getNpcId() 
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>" 
   st = player.getQuestState(qn) 
   if not st: return htmltext 
   id = st.getState() 
   if id == State.COMPLETED : 
      htmltext = "<html><body>This quest has already been completed</body></html>" 
   elif npcId == 30017 and id == State.CREATED :
     if player.getRace().ordinal() != 0 : 
        htmltext = "30017-00.htm"
        st.exitQuest(1)
     elif player.getLevel() >= 10 : 
        htmltext = "30017-02.htm" 
        return htmltext 
     else: 
        htmltext = "30017-06.htm" 
        st.exitQuest(1) 
   elif id == State.STARTED : 
     if npcId == 30017 and st.getInt("cond") and st.getQuestItemsCount(GALLINS_OAK_WAND)>=1 and not HaveAllQuestItems(st) : 
        htmltext = "30017-04.htm" 
     elif npcId == 30017 and st.getInt("cond")==3 and HaveAllQuestItems(st) : 
        for mobId in DROPLIST.keys() :
            st.takeItems(DROPLIST[mobId],-1)
        if player.getClassId().isMage() :
          st.giveItems(SPIRITSHOT_NO_GRADE,500)
        else :
          st.giveItems(SOULSHOT_NO_GRADE,1000)
        # check the player state against this quest newbie rewarding mark.
        newbie = player.getNewbie()
        if newbie | NEWBIE_REWARD != newbie :
           player.setNewbie(newbie|NEWBIE_REWARD)
           if player.getClassId().isMage() :
              st.giveItems(SPIRITSHOT_NO_GRADE_FOR_BEGINNERS,3000)
              st.playTutorialVoice("tutorial_voice_027")
        st.giveItems(1060,int(100*Config.RATE_QUESTS_REWARD_ITEMS))
        st.giveItems(WAND_OF_ADEPT,1)
        for item in range(4412,4417) :
            st.giveItems(item,int(10*Config.RATE_QUESTS_REWARD_ITEMS))
        st.addExpAndSp(39750,3407)
        htmltext = "30017-05.htm" 
        st.unset("cond") 
        st.exitQuest(False) 
        st.playSound("ItemSound.quest_finish") 
     elif npcId == 30045 and st.getInt("cond") : 
        htmltext = "30045-01.htm" 
        st.set("cond","2") 
        st.playSound("ItemSound.quest_middle") 
     elif npcId == 30043 and st.getInt("cond") : 
        htmltext = "30043-01.htm" 
        st.set("cond","2") 
        st.playSound("ItemSound.quest_middle") 
     elif npcId == 30041 and st.getInt("cond") : 
        htmltext = "30041-01.htm" 
        st.set("cond","2") 
        st.playSound("ItemSound.quest_middle") 
   return htmltext 

 def onKill(self,npc,player,isPet): 
   st = player.getQuestState(qn) 
   if not st: return 
   if st.getState() != State.STARTED : return 
   npcId = npc.getNpcId() 
   if st.getInt("cond") >= 1 and st.getItemEquipped(9) == GALLINS_OAK_WAND and not st.getQuestItemsCount(DROPLIST[npcId]) : # (7) means weapon slot 
     st.takeItems(GALLINS_OAK_WAND,1) 
     st.giveItems(DROPLIST[npcId],1) 
     if HaveAllQuestItems(st) : 
       st.set("cond","3") 
       st.playSound("ItemSound.quest_middle")
     else:
       st.playSound("ItemSound.quest_itemget") 
   return 

QUEST       = Quest(104,qn,"Spirit Of Mirrors") 

 
QUEST.addStartNpc(30017) 

QUEST.addTalkId(30017) 

QUEST.addTalkId(30041) 
QUEST.addTalkId(30043) 
QUEST.addTalkId(30045) 

for mobId in DROPLIST.keys(): 
  QUEST.addKillId(mobId)
