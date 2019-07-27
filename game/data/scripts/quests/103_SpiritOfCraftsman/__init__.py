# Made by Mr. Have fun! - Version 0.3 by DrLecter
# quest rate fix by M-095
import sys
from ru.catssoftware import Config 
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "103_SpiritOfCraftsman"

KAROYDS_LETTER_ID = 968
CECKTINONS_VOUCHER1_ID = 969
CECKTINONS_VOUCHER2_ID = 970
BONE_FRAGMENT1_ID = 1107
SOUL_CATCHER_ID = 971
PRESERVE_OIL_ID = 972
ZOMBIE_HEAD_ID = 973
STEELBENDERS_HEAD_ID = 974
BLOODSABER_ID = 975
#Newbie/one time rewards section
#Any quest should rely on a unique bit, but
#it could be shared among quest that were mutually
#exclusive or race restricted.
#Bit #1 isn't used for backwards compatibility.
NEWBIE_REWARD = 8
SOULSHOT_FOR_BEGINNERS = 5789
SOULSHOT_NO_GRADE = 1835
SPIRITSHOT_NO_GRADE = 2509

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [KAROYDS_LETTER_ID, CECKTINONS_VOUCHER1_ID, CECKTINONS_VOUCHER2_ID, BONE_FRAGMENT1_ID, SOUL_CATCHER_ID, PRESERVE_OIL_ID, ZOMBIE_HEAD_ID, STEELBENDERS_HEAD_ID]

 def onEvent (self,event,st) :
    htmltext = event
    if event == "30307-05.htm" :
        st.giveItems(KAROYDS_LETTER_ID,1)
        st.set("cond","1")
        st.setState(State.STARTED)
        st.playSound("ItemSound.quest_accept")
    return htmltext


 def onTalk (self,npc,player) :
   npcId = npc.getNpcId()
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st: return htmltext
   id = st.getState()
   if id == State.COMPLETED :
        htmltext = "<html><body>This quest has already been completed.</body></html>"
   elif npcId == 30307 and id == State.CREATED :
     if player.getRace().ordinal() != 2 :
        htmltext = "30307-00.htm"
     elif player.getLevel() >= 10 :
        htmltext = "30307-03.htm"
        return htmltext
     else:
        htmltext = "30307-02.htm"
        st.exitQuest(1)
   elif id == State.STARTED : 
       if npcId == 30307 and st.getInt("cond")>=1 and (st.getQuestItemsCount(KAROYDS_LETTER_ID)>=1 or st.getQuestItemsCount(CECKTINONS_VOUCHER1_ID)>=1 or st.getQuestItemsCount(CECKTINONS_VOUCHER2_ID)>=1) :
            htmltext = "30307-06.htm"
       elif npcId == 30132 and st.getInt("cond")==1 and st.getQuestItemsCount(KAROYDS_LETTER_ID)==1 :
            htmltext = "30132-01.htm"
            st.set("cond","2")
            st.playSound("ItemSound.quest_middle") 
            st.takeItems(KAROYDS_LETTER_ID,1)
            st.giveItems(CECKTINONS_VOUCHER1_ID,1)
       elif npcId == 30132 and st.getInt("cond")>=2 and (st.getQuestItemsCount(CECKTINONS_VOUCHER1_ID)>=1 or st.getQuestItemsCount(CECKTINONS_VOUCHER2_ID)>=1) :
            htmltext = "30132-02.htm"
       elif npcId == 30144 and st.getInt("cond")==2 and st.getQuestItemsCount(CECKTINONS_VOUCHER1_ID)>=1 :
            htmltext = "30144-01.htm"
            st.set("cond","3")
            st.playSound("ItemSound.quest_middle") 
            st.takeItems(CECKTINONS_VOUCHER1_ID,1)
            st.giveItems(CECKTINONS_VOUCHER2_ID,1)
       elif npcId == 30144 and st.getInt("cond")==3 and st.getQuestItemsCount(CECKTINONS_VOUCHER2_ID)>=1 and st.getQuestItemsCount(BONE_FRAGMENT1_ID)<10 :
            htmltext = "30144-02.htm"
       elif npcId == 30144 and st.getInt("cond")==4 and st.getQuestItemsCount(CECKTINONS_VOUCHER2_ID)==1 and st.getQuestItemsCount(BONE_FRAGMENT1_ID)>=10 :
            htmltext = "30144-03.htm"
            st.set("cond","5")
            st.playSound("ItemSound.quest_middle") 
            st.takeItems(CECKTINONS_VOUCHER2_ID,1)
            st.takeItems(BONE_FRAGMENT1_ID,10)
            st.giveItems(SOUL_CATCHER_ID,1)
       elif npcId == 30144 and st.getInt("cond")==5 and st.getQuestItemsCount(SOUL_CATCHER_ID)==1 :
            htmltext = "30144-04.htm"
       elif npcId == 30132 and st.getInt("cond")==5 and st.getQuestItemsCount(SOUL_CATCHER_ID)==1 :
            htmltext = "30132-03.htm"
            st.set("cond","6")
            st.playSound("ItemSound.quest_middle") 
            st.takeItems(SOUL_CATCHER_ID,1)
            st.giveItems(PRESERVE_OIL_ID,1)
       elif npcId == 30132 and st.getInt("cond")==6 and st.getQuestItemsCount(PRESERVE_OIL_ID)==1 and st.getQuestItemsCount(ZOMBIE_HEAD_ID)==0 and st.getQuestItemsCount(STEELBENDERS_HEAD_ID)==0 :
            htmltext = "30132-04.htm"
       elif npcId == 30132 and st.getInt("cond")==7 and st.getQuestItemsCount(ZOMBIE_HEAD_ID)==1 :
            htmltext = "30132-05.htm"
            st.set("cond","8")
            st.playSound("ItemSound.quest_middle") 
            st.takeItems(ZOMBIE_HEAD_ID,1)
            st.giveItems(STEELBENDERS_HEAD_ID,1)
       elif npcId == 30132 and st.getInt("cond")==8 and st.getQuestItemsCount(STEELBENDERS_HEAD_ID)==1 :
            htmltext = "30132-06.htm"
       elif npcId == 30307 and st.getInt("cond")==8 and st.getQuestItemsCount(STEELBENDERS_HEAD_ID)==1 :
            htmltext = "30307-07.htm"
            st.giveItems(57,19799)
            st.takeItems(STEELBENDERS_HEAD_ID,1)
            st.giveItems(BLOODSABER_ID,1)
            st.giveItems(1060,int(100*Config.RATE_QUESTS_REWARD_ITEMS))
            mage = player.getClassId().isMage()
            if mage :
               st.giveItems(SPIRITSHOT_NO_GRADE,500)
            else : 
               st.giveItems(SOULSHOT_NO_GRADE,1000)
            for item in range(4412,4417) : 
               st.giveItems(item,int(10*Config.RATE_QUESTS_REWARD_ITEMS))
            st.unset("cond")
            st.exitQuest(False)
            st.playSound("ItemSound.quest_finish")
            # check the player state against this quest newbie rewarding mark.
            newbie = player.getNewbie()
            if newbie | NEWBIE_REWARD != newbie :
               player.setNewbie(newbie|NEWBIE_REWARD)
               if not player.getClassId().isMage() :
                  st.giveItems(SOULSHOT_FOR_BEGINNERS,7000)
                  st.playTutorialVoice("tutorial_voice_026")
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st: return
   if st.getState() != State.STARTED : return 
   npcId = npc.getNpcId()
   if npcId in [20517,20518,20455] :
      bones = st.getQuestItemsCount(BONE_FRAGMENT1_ID)
      if st.getQuestItemsCount(CECKTINONS_VOUCHER2_ID) == 1 and bones < 10 :
         numItems, chance = divmod(30*Config.RATE_DROP_QUEST,100)
         if st.getRandom(100) <= chance :
            numItems += 1
         numItems = int(numItems)
         if numItems != 0 :
            if 10 <= (bones + numItems) :
               numItems = 10 - bones
               st.playSound("ItemSound.quest_middle")
               st.set("cond","4")
            else:
               st.playSound("ItemSound.quest_itemget")
            st.giveItems(BONE_FRAGMENT1_ID,numItems)
   elif npcId in [20015,20020] :
      if st.getQuestItemsCount(PRESERVE_OIL_ID) == 1 :
         if st.getRandom(10)<3*Config.RATE_DROP_QUEST :
            st.set("cond","7")
            st.giveItems(ZOMBIE_HEAD_ID,1)
            st.playSound("ItemSound.quest_middle")
            st.takeItems(PRESERVE_OIL_ID,1)
   return

QUEST       = Quest(103,qn,"Spirit Of Craftsman")

QUEST.addStartNpc(30307)

QUEST.addTalkId(30307)

QUEST.addTalkId(30132)
QUEST.addTalkId(30144)

QUEST.addKillId(20015)
QUEST.addKillId(20020)
QUEST.addKillId(20455)
QUEST.addKillId(20517)
QUEST.addKillId(20518)
