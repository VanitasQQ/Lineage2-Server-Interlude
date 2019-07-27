# Made by Mr. Have fun! - Version 0.3 by DrLecter
# quest rate fix by M-095
import sys
from ru.catssoftware import Config 
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "101_SwordOfSolidarity"

ROIENS_LETTER = 796
HOWTOGO_RUINS = 937
BROKEN_SWORD_HANDLE = 739
BROKEN_BLADE_BOTTOM = 740
BROKEN_BLADE_TOP = 741
ALLTRANS_NOTE = 742
SWORD_OF_SOLIDARITY = 738
#Newbie/one time rewards section
#Any quest should rely on a unique bit, but
#it could be shared among quest that were mutually
#exclusive or race restricted.
#Bit #1 isn't used for backwards compatibility.
NEWBIE_REWARD = 8
SOULSHOT_FOR_BEGINNERS = 5789

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [ALLTRANS_NOTE, HOWTOGO_RUINS, BROKEN_BLADE_TOP, BROKEN_BLADE_BOTTOM, ROIENS_LETTER, BROKEN_SWORD_HANDLE]

 def onEvent (self,event,st) :
    htmltext = event
    if event == "30008-04.htm" :
        st.set("cond","1")
        st.setState(State.STARTED)
        st.playSound("ItemSound.quest_accept")
        st.giveItems(ROIENS_LETTER,1)
    elif event == "30283-02.htm" :
        st.set("cond","2")
        st.playSound("ItemSound.quest_middle")
        st.takeItems(ROIENS_LETTER,st.getQuestItemsCount(ROIENS_LETTER))
        st.giveItems(HOWTOGO_RUINS,1)
    elif event == "30283-07.htm" :
        st.giveItems(57,10981)
        st.takeItems(BROKEN_SWORD_HANDLE,-1)
        st.giveItems(SWORD_OF_SOLIDARITY,1)
        st.giveItems(1060,int(100*Config.RATE_QUESTS_REWARD_ITEMS))
        for item in range(4412,4417) :
           st.giveItems(item,int(10*Config.RATE_QUESTS_REWARD_ITEMS))
        st.addExpAndSp(25747,2171)
        st.unset("cond")
        st.exitQuest(False)
        st.playSound("ItemSound.quest_finish")
        # check the player state against this quest newbie rewarding mark.
        player = st.getPlayer()
        newbie = player.getNewbie()
        if newbie | NEWBIE_REWARD != newbie :
           player.setNewbie(newbie|NEWBIE_REWARD)
           if not player.getClassId().isMage() :
              st.giveItems(SOULSHOT_FOR_BEGINNERS,7000)
              st.playTutorialVoice("tutorial_voice_026")
    return htmltext


 def onTalk (self,npc,player) :
   npcId = npc.getNpcId()
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>" 
   st = player.getQuestState(qn)
   if not st: return htmltext
   id = st.getState()
   if id == State.COMPLETED : 
        htmltext = "<html><body>This quest has already been completed.</body></html>"
   elif npcId == 30008 and id == State.CREATED :
      if player.getRace().ordinal() != 0 :
        htmltext = "30008-00.htm"
      elif player.getLevel() >= 9 :
        htmltext = "30008-02.htm"
        return htmltext
      else:
        htmltext = "30008-08.htm"
        st.exitQuest(1)
   elif id == State.STARTED: 
       if npcId == 30008 and st.getInt("cond")==1 and (st.getQuestItemsCount(ROIENS_LETTER)==1) :
            htmltext = "30008-05.htm"
       elif npcId == 30008 and st.getInt("cond")>=2 and st.getQuestItemsCount(ROIENS_LETTER)==0 and st.getQuestItemsCount(ALLTRANS_NOTE)==0 :
            if st.getQuestItemsCount(BROKEN_BLADE_TOP) and st.getQuestItemsCount(BROKEN_BLADE_BOTTOM) :
              htmltext = "30008-12.htm"
            if (st.getQuestItemsCount(BROKEN_BLADE_TOP) + st.getQuestItemsCount(BROKEN_BLADE_BOTTOM)) <= 1 :
              htmltext = "30008-11.htm"
            if st.getQuestItemsCount(BROKEN_SWORD_HANDLE) > 0 :
              htmltext = "30008-07.htm"
            if st.getQuestItemsCount(HOWTOGO_RUINS) == 1 :
              htmltext = "30008-10.htm"
       elif npcId == 30008 and st.getInt("cond")==4 and st.getQuestItemsCount(ROIENS_LETTER)==0 and st.getQuestItemsCount(ALLTRANS_NOTE) :
            htmltext = "30008-06.htm"
            st.set("cond","5")
            st.playSound("ItemSound.quest_middle")
            st.takeItems(ALLTRANS_NOTE,st.getQuestItemsCount(ALLTRANS_NOTE))
            st.giveItems(BROKEN_SWORD_HANDLE,1)
       elif npcId == 30283 and st.getInt("cond")==1 and st.getQuestItemsCount(ROIENS_LETTER)>0 :
            htmltext = "30283-01.htm"
       elif npcId == 30283 and st.getInt("cond")>=2 and st.getQuestItemsCount(ROIENS_LETTER)==0 and st.getQuestItemsCount(HOWTOGO_RUINS)>0 :
            if (st.getQuestItemsCount(BROKEN_BLADE_TOP) + st.getQuestItemsCount(BROKEN_BLADE_BOTTOM)) == 1 :
              htmltext = "30283-08.htm"
            if (st.getQuestItemsCount(BROKEN_BLADE_TOP) + st.getQuestItemsCount(BROKEN_BLADE_BOTTOM)) == 0 :
              htmltext = "30283-03.htm"
            if st.getQuestItemsCount(BROKEN_BLADE_TOP) and st.getQuestItemsCount(BROKEN_BLADE_BOTTOM) :
              htmltext = "30283-04.htm"
              st.set("cond","4")
              st.playSound("ItemSound.quest_middle")
              st.takeItems(HOWTOGO_RUINS,st.getQuestItemsCount(HOWTOGO_RUINS))
              st.takeItems(BROKEN_BLADE_TOP,st.getQuestItemsCount(BROKEN_BLADE_TOP))
              st.takeItems(BROKEN_BLADE_BOTTOM,st.getQuestItemsCount(BROKEN_BLADE_BOTTOM))
              st.giveItems(ALLTRANS_NOTE,1)
       elif npcId == 30283 and st.getInt("cond")==4 and st.getQuestItemsCount(ALLTRANS_NOTE) :
            htmltext = "30283-05.htm"
       elif npcId == 30283 and st.getInt("cond")==5 and st.getQuestItemsCount(BROKEN_SWORD_HANDLE) :
            htmltext = "30283-06.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st: return   
   if st.getState() == State.STARTED :
       npcId = npc.getNpcId()
       if npcId in [20361,20362] :
          if st.getQuestItemsCount(HOWTOGO_RUINS) :
             if st.getQuestItemsCount(BROKEN_BLADE_TOP) == 0 :
                if st.getRandom(5) == 0 :
                   st.giveItems(BROKEN_BLADE_TOP,1)
             elif st.getQuestItemsCount(BROKEN_BLADE_BOTTOM) == 0 :
                if st.getRandom(5) == 0 :
                   st.giveItems(BROKEN_BLADE_BOTTOM,1)
          if st.getQuestItemsCount(BROKEN_BLADE_TOP) and st.getQuestItemsCount(BROKEN_BLADE_BOTTOM) :
             st.set("cond","3")
             st.playSound("ItemSound.quest_middle")
          else :
             st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(101,qn,"Sword Of Solidarity")

QUEST.addStartNpc(30008)

QUEST.addTalkId(30008)

QUEST.addTalkId(30283)

QUEST.addKillId(20361)
QUEST.addKillId(20362)
