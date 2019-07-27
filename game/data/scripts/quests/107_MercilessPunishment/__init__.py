# Made by Mr. Have fun! Version 0.3 updated by Censor for www.l2jdp.com 
# quest rate fix by M-095
import sys
from ru.catssoftware import Config 
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest
from ru.catssoftware.gameserver.network.serverpackets      import SocialAction

qn = "107_MercilessPunishment" 

HATOSS_ORDER1_ID = 1553 
HATOSS_ORDER2_ID = 1554 
HATOSS_ORDER3_ID = 1555 
LETTER_TO_HUMAN_ID = 1557 
LETTER_TO_DARKELF_ID = 1556 
LETTER_TO_ELF_ID = 1558 
BUTCHER_ID = 1510 
LESSER_HEALING_ID = 1060 
CRYSTAL_BATTLE = 4412 
CRYSTAL_LOVE = 4413 
CRYSTAL_SOLITUDE = 4414 
CRYSTAL_FEAST = 4415 
CRYSTAL_CELEBRATION = 4416 
#Newbie/one time rewards section
#Any quest should rely on a unique bit, but
#it could be shared among quest that were mutually
#exclusive or race restricted.
#Bit #1 isn't used for backwards compatibility.
NEWBIE_REWARD = 2
SPIRITSHOT_NO_GRADE_FOR_BEGINNERS = 5790 
SOULSHOT_NO_GRADE_FOR_BEGINNERS = 5789

class Quest (JQuest) : 

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [HATOSS_ORDER2_ID, LETTER_TO_DARKELF_ID, LETTER_TO_HUMAN_ID, LETTER_TO_ELF_ID, HATOSS_ORDER1_ID, HATOSS_ORDER3_ID]

 def onEvent (self,event,st) : 
    htmltext = event 
    if event == "1" : 
          st.set("id","0") 
          htmltext = "30568-03.htm" 
          st.giveItems(HATOSS_ORDER1_ID,1) 
          st.set("cond","1") 
          st.setState(State.STARTED) 
          st.playSound("ItemSound.quest_accept") 
    elif event == "30568_1" : 
            htmltext = "30568-06.htm" 
            st.exitQuest(1)
            st.playSound("ItemSound.quest_giveup") 
    elif event == "30568_2" : 
            htmltext = "30568-07.htm" 
            st.takeItems(HATOSS_ORDER1_ID,1) 
            if st.getQuestItemsCount(HATOSS_ORDER2_ID) == 0 : 
              st.giveItems(HATOSS_ORDER2_ID,1) 
    elif event == "30568_3" : 
            htmltext = "30568-06.htm" 
            st.exitQuest(1)
            st.playSound("ItemSound.quest_giveup") 
    elif event == "30568_4" : 
            htmltext = "30568-09.htm" 
            st.takeItems(HATOSS_ORDER2_ID,1) 
            if st.getQuestItemsCount(HATOSS_ORDER3_ID) == 0 : 
              st.giveItems(HATOSS_ORDER3_ID,1) 
    return htmltext 


 def onTalk (self,npc,player): 

   npcId = npc.getNpcId() 
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>" 
   st = player.getQuestState(qn) 
   if not st : return htmltext 

   id = st.getState() 
   if npcId == 30568 and id == State.COMPLETED : 
      htmltext = "<html><body>This quest has already been completed.</body></html>" 
   elif npcId == 30568 and id == State.CREATED : 
      if player.getRace().ordinal() != 3 : 
        htmltext = "30568-00.htm" 
        st.exitQuest(1) 
      elif player.getLevel() >= 10 : 
        htmltext = "30568-02.htm" 
        return htmltext 
      else: 
        htmltext = "30568-01.htm" 
        st.exitQuest(1) 
   elif npcId == 30568 and st.getInt("cond")==1 and (st.getQuestItemsCount(HATOSS_ORDER1_ID) or st.getQuestItemsCount(HATOSS_ORDER2_ID) or st.getQuestItemsCount(HATOSS_ORDER3_ID)) and ((st.getQuestItemsCount(LETTER_TO_ELF_ID)+st.getQuestItemsCount(LETTER_TO_HUMAN_ID)+st.getQuestItemsCount(LETTER_TO_DARKELF_ID))==0) : 
          htmltext = "30568-04.htm" 
   elif npcId == 30568 and st.getInt("cond")==1 and (st.getQuestItemsCount(HATOSS_ORDER1_ID) or st.getQuestItemsCount(HATOSS_ORDER2_ID) or st.getQuestItemsCount(HATOSS_ORDER3_ID)) and ((st.getQuestItemsCount(LETTER_TO_ELF_ID)+st.getQuestItemsCount(LETTER_TO_HUMAN_ID)+st.getQuestItemsCount(LETTER_TO_DARKELF_ID))==1) : 
          htmltext = "30568-05.htm" 
   elif npcId == 30568 and st.getInt("cond")==1 and (st.getQuestItemsCount(HATOSS_ORDER1_ID) or st.getQuestItemsCount(HATOSS_ORDER2_ID) or st.getQuestItemsCount(HATOSS_ORDER3_ID)) and ((st.getQuestItemsCount(LETTER_TO_ELF_ID)+st.getQuestItemsCount(LETTER_TO_HUMAN_ID)+st.getQuestItemsCount(LETTER_TO_DARKELF_ID))==2) : 
          htmltext = "30568-08.htm" 
   elif npcId == 30568 and st.getInt("cond")==1 and (st.getQuestItemsCount(HATOSS_ORDER1_ID) or st.getQuestItemsCount(HATOSS_ORDER2_ID) or st.getQuestItemsCount(HATOSS_ORDER3_ID)) and ((st.getQuestItemsCount(LETTER_TO_ELF_ID)+st.getQuestItemsCount(LETTER_TO_HUMAN_ID)+st.getQuestItemsCount(LETTER_TO_DARKELF_ID))==3) : 
          if st.getInt("id") != 107 : 
            st.set("id","107") 
            htmltext = "30568-10.htm" 
            st.takeItems(LETTER_TO_DARKELF_ID,1) 
            st.takeItems(LETTER_TO_HUMAN_ID,1) 
            st.takeItems(LETTER_TO_ELF_ID,1) 
            st.takeItems(HATOSS_ORDER3_ID,1)
            st.giveItems(57,14666)
            st.giveItems(LESSER_HEALING_ID,int(100*Config.RATE_QUESTS_REWARD_ITEMS))
            st.giveItems(BUTCHER_ID,1)
            st.giveItems(CRYSTAL_BATTLE,int(10*Config.RATE_QUESTS_REWARD_ITEMS))
            st.giveItems(CRYSTAL_LOVE,int(10*Config.RATE_QUESTS_REWARD_ITEMS))
            st.giveItems(CRYSTAL_SOLITUDE,int(10*Config.RATE_QUESTS_REWARD_ITEMS))
            st.giveItems(CRYSTAL_FEAST,int(10*Config.RATE_QUESTS_REWARD_ITEMS))
            st.giveItems(CRYSTAL_CELEBRATION,int(10*Config.RATE_QUESTS_REWARD_ITEMS))
            # check the player state against this quest newbie rewarding mark.
            newbie = player.getNewbie()
            if newbie | NEWBIE_REWARD != newbie :
               player.setNewbie(newbie|NEWBIE_REWARD)
               if player.getClassId().isMage() :
                  st.giveItems(SPIRITSHOT_NO_GRADE_FOR_BEGINNERS,3000)
                  st.playTutorialVoice("tutorial_voice_027")
               else :
                  st.giveItems(SOULSHOT_NO_GRADE_FOR_BEGINNERS,7000)
                  st.playTutorialVoice("tutorial_voice_026")
            st.unset("cond") 
            st.addExpAndSp(34565,2962)
            player.sendPacket(SocialAction(player.getObjectId(),3))
            st.exitQuest(False) 
            st.playSound("ItemSound.quest_finish") 
   elif npcId == 30580 and st.getInt("cond")==1 and id == State.STARTED and (st.getQuestItemsCount(HATOSS_ORDER1_ID) or st.getQuestItemsCount(HATOSS_ORDER2_ID) or st.getQuestItemsCount(HATOSS_ORDER3_ID)) : 
          htmltext = "30580-01.htm" 
   return htmltext 

 def onKill(self,npc,player,isPet): 
   st = player.getQuestState(qn) 
   if not st : return 
   if st.getState() != State.STARTED : return 
    
   npcId = npc.getNpcId() 
   if npcId == 27041 : 
        st.set("id","0") 
        if st.getInt("cond") == 1 : 
          if st.getQuestItemsCount(HATOSS_ORDER1_ID) and st.getQuestItemsCount(LETTER_TO_HUMAN_ID) == 0 : 
            st.giveItems(LETTER_TO_HUMAN_ID,1) 
            st.playSound("ItemSound.quest_itemget") 
          if st.getQuestItemsCount(HATOSS_ORDER2_ID) and st.getQuestItemsCount(LETTER_TO_DARKELF_ID) == 0 : 
            st.giveItems(LETTER_TO_DARKELF_ID,1) 
            st.playSound("ItemSound.quest_itemget") 
          if st.getQuestItemsCount(HATOSS_ORDER3_ID) and st.getQuestItemsCount(LETTER_TO_ELF_ID) == 0 : 
            st.giveItems(LETTER_TO_ELF_ID,1) 
            st.playSound("ItemSound.quest_itemget") 
   return 

QUEST       = Quest(107,qn,"Merciless Punishment") 

QUEST.addStartNpc(30568) 

QUEST.addTalkId(30568) 

QUEST.addTalkId(30580) 

QUEST.addKillId(27041) 
