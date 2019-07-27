# Made by Mr. Have fun! Version 0.3 by Censor for www.l2jdp.com 
# quest rate fix by M-095
import sys
from ru.catssoftware import Config 
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "108_JumbleTumbleDiamondFuss" 

GOUPHS_CONTRACT = 1559 
REEPS_CONTRACT = 1560 
ELVEN_WINE = 1561 
BRONPS_DICE = 1562 
BRONPS_CONTRACT = 1563 
AQUAMARINE = 1564 
CHRYSOBERYL = 1565 
GEM_BOX1 = 1566 
COAL_PIECE = 1567 
BRONPS_LETTER = 1568 
BERRY_TART = 1569 
BAT_DIAGRAM = 1570 
STAR_DIAMOND = 1571 
SILVERSMITH_HAMMER = 1511
#Newbie/one time rewards section
#Any quest should rely on a unique bit, but
#it could be shared among quest that were mutually
#exclusive or race restricted.
#Bit #1 isn't used for backwards compatibility.
NEWBIE_REWARD = 2
SOULSHOT_NO_GRADE_FOR_BEGINNERS = 5789
SPIRITSHOT_NO_GRADE_FOR_BEGINNERS = 5790


class Quest (JQuest) : 

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = [GEM_BOX1, STAR_DIAMOND, GOUPHS_CONTRACT, REEPS_CONTRACT, ELVEN_WINE, BRONPS_CONTRACT, AQUAMARINE, CHRYSOBERYL, COAL_PIECE, BRONPS_DICE, BRONPS_LETTER, BERRY_TART, BAT_DIAGRAM]

 def onEvent (self,event,st) : 
    htmltext = event 
    if event == "1" : 
          htmltext = "30523-03.htm" 
          st.giveItems(GOUPHS_CONTRACT,1) 
          st.set("cond","1") 
          st.setState(State.STARTED) 
          st.playSound("ItemSound.quest_accept") 
    elif event == "30555_1" : 
          htmltext = "30555-02.htm" 
          st.takeItems(REEPS_CONTRACT,1) 
          st.giveItems(ELVEN_WINE,1) 
    elif event == "30526_1" : 
          htmltext = "30526-02.htm" 
          st.takeItems(BRONPS_DICE,1) 
          st.giveItems(BRONPS_CONTRACT,1) 
    return htmltext 


 def onTalk (self,npc,player): 

   npcId = npc.getNpcId() 
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>" 
   st = player.getQuestState(qn) 
   if not st : return htmltext 

   id = st.getState() 
   if id == State.CREATED : 
     st.set("cond","0") 
   if npcId == 30523 and id == State.COMPLETED : 
      htmltext = "<html><body>This quest has already been completed.</body></html>" 
   elif npcId == 30523 and st.getInt("cond")==0 : 
          if player.getRace().ordinal() != 4 : 
            htmltext = "30523-00.htm" 
            st.exitQuest(1) 
          elif player.getLevel() >= 10 : 
            htmltext = "30523-02.htm" 
            return htmltext 
          else: 
            htmltext = "30523-01.htm" 
            st.exitQuest(1) 
   elif npcId == 30523 and st.getInt("cond")==1 and st.getQuestItemsCount(GOUPHS_CONTRACT) : 
          htmltext = "30523-04.htm" 
   elif npcId == 30523 and st.getInt("cond")==1 and (st.getQuestItemsCount(REEPS_CONTRACT) or st.getQuestItemsCount(ELVEN_WINE) or st.getQuestItemsCount(BRONPS_DICE) or st.getQuestItemsCount(BRONPS_CONTRACT)) : 
          htmltext = "30523-05.htm" 
   elif npcId == 30523 and st.getInt("cond")==1 and st.getQuestItemsCount(GEM_BOX1) : 
          htmltext = "30523-06.htm" 
          st.takeItems(GEM_BOX1,1) 
          st.giveItems(COAL_PIECE,1) 
   elif npcId == 30523 and st.getInt("cond")==1 and (st.getQuestItemsCount(BRONPS_LETTER) or st.getQuestItemsCount(COAL_PIECE) or st.getQuestItemsCount(BERRY_TART) or st.getQuestItemsCount(BAT_DIAGRAM)) : 
          htmltext = "30523-07.htm" 
   elif npcId == 30523 and st.getInt("cond")==1 and st.getQuestItemsCount(STAR_DIAMOND) : 
          htmltext = "30523-08.htm"
          # check the player state against this quest newbie rewarding mark.
          st.giveItems(57,14666)
          newbie = player.getNewbie()
          if newbie | NEWBIE_REWARD != newbie :
             player.setNewbie(newbie|NEWBIE_REWARD)
             if player.getClassId().isMage() :
                st.giveItems(SPIRITSHOT_NO_GRADE_FOR_BEGINNERS,3000)
                st.playTutorialVoice("tutorial_voice_027")
             else :
                st.giveItems(SOULSHOT_NO_GRADE_FOR_BEGINNERS,7000)
                st.playTutorialVoice("tutorial_voice_026")
          st.giveItems(1060,int(100*Config.RATE_QUESTS_REWARD_ITEMS))
          st.giveItems(SILVERSMITH_HAMMER,1) 
          for item in range(4412,4417) :
              st.giveItems(item,int(10*Config.RATE_QUESTS_REWARD_ITEMS))
          st.takeItems(STAR_DIAMOND,-1) 
          st.addExpAndSp(34565,2962)
          st.set("cond","0") 
          st.exitQuest(False) 
          st.playSound("ItemSound.quest_finish") 
   elif id == State.STARTED : 
       if npcId == 30516 and st.getInt("cond")==1 and st.getQuestItemsCount(GOUPHS_CONTRACT) and st.getQuestItemsCount(REEPS_CONTRACT)==0 : 
              htmltext = "30516-01.htm" 
              st.giveItems(REEPS_CONTRACT,1) 
              st.takeItems(GOUPHS_CONTRACT,1) 
       elif npcId == 30516 and st.getInt("cond")==1 and st.getQuestItemsCount(GOUPHS_CONTRACT)==0 and st.getQuestItemsCount(REEPS_CONTRACT) : 
              htmltext = "30516-02.htm" 
       elif npcId == 30516 and st.getInt("cond")==1 and st.getQuestItemsCount(GOUPHS_CONTRACT)==0 and st.getQuestItemsCount(REEPS_CONTRACT)==0 : 
              htmltext = "30516-03.htm" 
       elif npcId == 30555 and st.getInt("cond")==1 and st.getQuestItemsCount(REEPS_CONTRACT)==0 and st.getQuestItemsCount(ELVEN_WINE)==0 : 
              htmltext = "30555-01.htm" 
       elif npcId == 30555 and st.getInt("cond")==1 and st.getQuestItemsCount(REEPS_CONTRACT) and st.getQuestItemsCount(ELVEN_WINE)==0 : 
              htmltext = "30555-02.htm" 
              st.giveItems(ELVEN_WINE,1) 
              st.takeItems(REEPS_CONTRACT,1) 
       elif npcId == 30555 and st.getInt("cond")==1 and st.getQuestItemsCount(REEPS_CONTRACT)==0 and st.getQuestItemsCount(ELVEN_WINE) : 
              htmltext = "30555-03.htm" 
       elif npcId == 30555 and st.getInt("cond")==1 and st.getQuestItemsCount(GEM_BOX1)==1 : 
              htmltext = "30555-04.htm" 
       elif npcId == 30555 and st.getInt("cond")==1 and st.getQuestItemsCount(GEM_BOX1)==0 and st.getQuestItemsCount(REEPS_CONTRACT)==0 and st.getQuestItemsCount(ELVEN_WINE)==0 : 
              htmltext = "30555-05.htm" 
       elif npcId == 30529 and st.getInt("cond")==1 and st.getQuestItemsCount(ELVEN_WINE) and st.getQuestItemsCount(BRONPS_DICE)==0 : 
              htmltext = "30529-01.htm" 
              st.giveItems(BRONPS_DICE,1) 
              st.takeItems(ELVEN_WINE,1) 
       elif npcId == 30529 and st.getInt("cond")==1 and st.getQuestItemsCount(ELVEN_WINE)==0 and st.getQuestItemsCount(BRONPS_DICE) : 
              htmltext = "30529-02.htm" 
       elif npcId == 30529 and st.getInt("cond")==1 and st.getQuestItemsCount(ELVEN_WINE)==0 and st.getQuestItemsCount(BRONPS_DICE)==0 : 
              htmltext = "30529-03.htm" 
       elif npcId == 30526 and st.getInt("cond")==1 and st.getQuestItemsCount(BRONPS_DICE) : 
              htmltext = "30526-01.htm" 
       elif npcId == 30526 and st.getInt("cond")==1 and st.getQuestItemsCount(BRONPS_CONTRACT) and (st.getQuestItemsCount(AQUAMARINE)+st.getQuestItemsCount(CHRYSOBERYL)<20) : 
              htmltext = "30526-03.htm" 
       elif npcId == 30526 and st.getInt("cond")==1 and st.getQuestItemsCount(BRONPS_CONTRACT) and (st.getQuestItemsCount(AQUAMARINE)+st.getQuestItemsCount(CHRYSOBERYL)>=20) : 
              htmltext = "30526-04.htm" 
              st.takeItems(BRONPS_CONTRACT,1) 
              st.takeItems(AQUAMARINE,st.getQuestItemsCount(AQUAMARINE)) 
              st.takeItems(CHRYSOBERYL,st.getQuestItemsCount(CHRYSOBERYL)) 
              st.giveItems(GEM_BOX1,1) 
       elif npcId == 30526 and st.getInt("cond")==1 and st.getQuestItemsCount(GEM_BOX1) : 
              htmltext = "30526-05.htm" 
       elif npcId == 30526 and st.getInt("cond")==1 and st.getQuestItemsCount(COAL_PIECE) : 
              htmltext = "30526-06.htm" 
              st.takeItems(COAL_PIECE,1) 
              st.giveItems(BRONPS_LETTER,1) 
       elif npcId == 30526 and st.getInt("cond")==1 and st.getQuestItemsCount(BRONPS_LETTER) : 
              htmltext = "30526-07.htm" 
       elif npcId == 30526 and st.getInt("cond")==1 and st.getQuestItemsCount(BERRY_TART) or st.getQuestItemsCount(BAT_DIAGRAM) or st.getQuestItemsCount(STAR_DIAMOND) : 
              htmltext = "30526-08.htm" 
       elif npcId == 30521 and st.getInt("cond")==1 and st.getQuestItemsCount(BRONPS_LETTER) and st.getQuestItemsCount(BERRY_TART)==0 : 
              htmltext = "30521-01.htm" 
              st.giveItems(BERRY_TART,1) 
              st.takeItems(BRONPS_LETTER,1) 
       elif npcId == 30521 and st.getInt("cond")==1 and st.getQuestItemsCount(BRONPS_LETTER)==0 and st.getQuestItemsCount(BERRY_TART) : 
              htmltext = "30521-02.htm" 
       elif npcId == 30521 and st.getInt("cond")==1 and st.getQuestItemsCount(BRONPS_LETTER)==0 and st.getQuestItemsCount(BERRY_TART)==0 : 
              htmltext = "30521-03.htm" 
       elif npcId == 30522 and st.getInt("cond")==1 and st.getQuestItemsCount(BAT_DIAGRAM)==0 and st.getQuestItemsCount(BERRY_TART) and st.getQuestItemsCount(STAR_DIAMOND)==0 : 
              htmltext = "30522-01.htm" 
              st.giveItems(BAT_DIAGRAM,1) 
              st.takeItems(BERRY_TART,1) 
       elif npcId == 30522 and st.getInt("cond")==1 and st.getQuestItemsCount(BAT_DIAGRAM) and st.getQuestItemsCount(BERRY_TART)==0 and st.getQuestItemsCount(STAR_DIAMOND)==0 : 
              htmltext = "30522-02.htm" 
       elif npcId == 30522 and st.getInt("cond")==1 and st.getQuestItemsCount(BAT_DIAGRAM)==0 and st.getQuestItemsCount(BERRY_TART)==0 and st.getQuestItemsCount(STAR_DIAMOND) : 
              htmltext = "30522-03.htm" 
       elif npcId == 30522 and st.getInt("cond")==1 and st.getQuestItemsCount(BAT_DIAGRAM)==0 and st.getQuestItemsCount(BERRY_TART)==0 and st.getQuestItemsCount(STAR_DIAMOND)==0 : 
              htmltext = "30522-04.htm" 
   return htmltext 

 def onKill(self,npc,player,isPet): 
   st = player.getQuestState(qn) 
   if not st : return 
   if st.getState() != State.STARTED : return 

   npcId = npc.getNpcId() 
   if npcId == 20323 : 
        if st.getInt("cond") == 1 and st.getQuestItemsCount(BRONPS_CONTRACT) : 
          if st.getRandom(10) < 8 : 
            st.giveItems(AQUAMARINE,1) 
            if st.getQuestItemsCount(AQUAMARINE)+st.getQuestItemsCount(CHRYSOBERYL) == 19 : 
              if st.getQuestItemsCount(AQUAMARINE) < 10 : 
                st.playSound("ItemSound.quest_itemget") 
              else :
                st.playSound("ItemSound.quest_middle") 
            else: 
              if st.getQuestItemsCount(AQUAMARINE) < 10 : 
                st.playSound("ItemSound.quest_itemget") 
              else :
                st.playSound("ItemSound.quest_middle") 
          if st.getRandom(10) < 8 : 
            if st.getQuestItemsCount(AQUAMARINE)+st.getQuestItemsCount(CHRYSOBERYL) == 19 : 
              if st.getQuestItemsCount(CHRYSOBERYL) < 10 : 
                st.giveItems(CHRYSOBERYL,1) 
                st.playSound("ItemSound.quest_middle") 
            elif st.getQuestItemsCount(AQUAMARINE)+st.getQuestItemsCount(CHRYSOBERYL) < 20 : 
                if st.getQuestItemsCount(CHRYSOBERYL) < 10 : 
                  st.giveItems(CHRYSOBERYL,1) 
                  st.playSound("ItemSound.quest_itemget") 
   elif npcId == 20324 : 
        if st.getInt("cond") == 1 and st.getQuestItemsCount(BRONPS_CONTRACT) : 
          if st.getRandom(10) < 6 : 
            if st.getQuestItemsCount(AQUAMARINE)+st.getQuestItemsCount(CHRYSOBERYL) == 19 : 
              if st.getQuestItemsCount(AQUAMARINE) < 10 : 
                st.giveItems(AQUAMARINE,1) 
                st.playSound("ItemSound.quest_middle") 
            else: 
              if st.getQuestItemsCount(AQUAMARINE) < 10 : 
                st.giveItems(AQUAMARINE,1) 
                st.playSound("ItemSound.quest_itemget") 
          if st.getRandom(10) < 6 : 
            if st.getQuestItemsCount(AQUAMARINE)+st.getQuestItemsCount(CHRYSOBERYL) == 19 : 
              if st.getQuestItemsCount(CHRYSOBERYL) < 10 : 
                st.giveItems(CHRYSOBERYL,1) 
                st.playSound("ItemSound.quest_middle") 
            elif st.getQuestItemsCount(AQUAMARINE)+st.getQuestItemsCount(CHRYSOBERYL) < 20 : 
                if st.getQuestItemsCount(CHRYSOBERYL) < 10 : 
                  st.giveItems(CHRYSOBERYL,1) 
                  st.playSound("ItemSound.quest_itemget") 
   elif npcId == 20480 : 
        if st.getInt("cond") == 1 and st.getQuestItemsCount(BAT_DIAGRAM) and st.getQuestItemsCount(STAR_DIAMOND) == 0 : 
          if st.getRandom(10) < 2 : 
            st.giveItems(STAR_DIAMOND,1) 
            st.takeItems(BAT_DIAGRAM,1) 
            st.playSound("ItemSound.quest_middle") 
   return 

QUEST       = Quest(108,qn,"Jumble Tumble Diamond Fuss") 

QUEST.addStartNpc(30523) 

QUEST.addTalkId(30523) 

QUEST.addTalkId(30516) 
QUEST.addTalkId(30521) 
QUEST.addTalkId(30522) 
QUEST.addTalkId(30523) 
QUEST.addTalkId(30526) 
QUEST.addTalkId(30529) 
QUEST.addTalkId(30555) 

QUEST.addKillId(20323) 
QUEST.addKillId(20324) 
QUEST.addKillId(20480) 
