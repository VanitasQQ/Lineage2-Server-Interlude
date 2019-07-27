# Made by Mr. Have fun! Version 0.2
# Shadow Weapon Coupons contributed by BiTi for the Official L2J Datapack Project
# Visit http://forum.l2jdp.com for more details
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "226_TestOfHealer"

REPORT_OF_PERRIN = 2810
CRISTINAS_LETTER = 2811
PICTURE_OF_WINDY = 2812
GOLDEN_STATUE = 2813
WINDYS_PEBBLES = 2814
ORDER_OF_SORIUS = 2815
SECRET_LETTER1 = 2816
SECRET_LETTER2 = 2817
SECRET_LETTER3 = 2818
SECRET_LETTER4 = 2819
MARK_OF_HEALER = 2820
ADENA = 57
SHADOW_WEAPON_COUPON_CGRADE = 8870

#NPCs
BANDELLOS = 30473
PERRIN = 30428
ALLANA = 30424
GUPU = 30658
ORPHAN = 30659
WINDY = 30660
SORIUS = 30327
MYSTERIOUS = 30661
PIPER = 30662
SLEIN = 30663
KEIN = 30664
KRISTINA = 30665
DAURIN = 30674

#MOBs
TATOMA = 27134
LETO_LEADER = 27123
LETO_ASSASSIN = 27124
LETO_SNIPER = 27125
LETO_WIZARD = 27126
LETO_LORD = 27127

#this handles all dropdata, npcId:[condition,maxcount,item,next condition]
DROPLIST={
TATOMA:[2,1,0,"3"],
LETO_LEADER:[11,1,SECRET_LETTER1,"12"],
LETO_ASSASSIN:[14,1,SECRET_LETTER2,"15"],
LETO_SNIPER:[16,1,SECRET_LETTER3,"17"],
LETO_LORD:[18,1,SECRET_LETTER4,"19"]
}

#this handles 3 groups of mobs spawned by Dark Elves, npcId:[html1,html2,html3,html4]
ELVES={
PIPER:["30662-01.htm","30662-02.htm","30662-03.htm","30662-04.htm"],
SLEIN:["30663-01.htm","30663-02.htm","30663-03.htm","30663-04.htm"],
KEIN:["30664-01.htm","30664-02.htm","30664-03.htm","30664-04.htm"]
}

class Quest (JQuest) :

 def __init__(self,id,name,descr):
   JQuest.__init__(self,id,name,descr)
   self.questItemIds = range(2810,2820)

 def onAdvEvent (self,event,npc, player) :
    htmltext = event
    st = player.getQuestState(qn)
    if not st : return
    if event == "1" :
      htmltext = "30473-04.htm"
      st.set("cond","1")
      st.setState(State.STARTED)
      st.playSound("ItemSound.quest_accept")
      st.giveItems(REPORT_OF_PERRIN,1)
    elif event == "30473_1" :
          htmltext = "30473-08.htm"
    elif event == "30473_2" :
          htmltext = "30473-09.htm"
          if st.getQuestItemsCount(GOLDEN_STATUE):
            st.addExpAndSp(738283,50662)
          else:
            st.addExpAndSp(118304,26250)
          st.giveItems(MARK_OF_HEALER,1)
          st.giveItems(ADENA,233490)
          st.giveItems(7562,60)
          st.giveItems(SHADOW_WEAPON_COUPON_CGRADE,15)
          st.takeItems(GOLDEN_STATUE,1)
          st.set("cond","0")
          st.exitQuest(False)
          st.playSound("ItemSound.quest_finish")
          st.set("onlyone","1")
    elif event == "30428_1" :
          htmltext = "30428-02.htm"
          st.addSpawn(TATOMA)
          st.set("cond","2")
    elif event == "30658_1" :
          if st.getQuestItemsCount(ADENA) >= 100000 :
            htmltext = "30658-02.htm"
            st.takeItems(ADENA,100000)
            st.giveItems(PICTURE_OF_WINDY,1)
            st.set("cond","7")
          else:
            htmltext = "30658-05.htm"
    elif event == "30658_2" :
          htmltext = "30658-03.htm"
          st.set("cond","6")
    elif event == "30658_06" :
          htmltext = "30658-07.htm"
          st.set("cond","9")
    elif event == "30660_1" :
          htmltext = "30660-02.htm"
    elif event == "30660_2" :
          htmltext = "30660-03.htm"
          st.takeItems(PICTURE_OF_WINDY,1)
          st.giveItems(WINDYS_PEBBLES,1)
          st.set("cond","8")
    elif event == "30674_1" :
          htmltext = "30674-02.htm"
          st.takeItems(ORDER_OF_SORIUS,1)
          st.addSpawn(27122)
          st.addSpawn(27122)
          st.addSpawn(LETO_LEADER)
          st.set("cond","11")
          st.playSound("Itemsound.quest_before_battle")
    elif event == "30665_1" :
          htmltext = "30665-02.htm"
          st.takeItems(SECRET_LETTER1,1)
          st.takeItems(SECRET_LETTER2,1)
          st.takeItems(SECRET_LETTER3,1)
          st.takeItems(SECRET_LETTER4,1)
          st.giveItems(CRISTINAS_LETTER,1)
          st.set("cond","22")
    return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if npcId != BANDELLOS and id != State.STARTED : return htmltext

   if npcId == BANDELLOS :
     if st.getInt("cond")==0 and st.getInt("onlyone")==0 :
        if (player.getClassId().getId() in [0x04, 0x0f, 0x1d, 0x13]) and player.getLevel() > 38 :
          htmltext = "30473-03.htm"
        elif player.getClassId().getId() in [0x04, 0x0f, 0x1d, 0x13] :
          htmltext = "30473-01.htm"
        else:
          htmltext = "30473-02.htm"
          st.exitQuest(1)
     elif st.getInt("cond")==0 and st.getInt("onlyone")==1 :
      htmltext = "<html><body>This quest has already been completed.</body></html>"
     elif st.getInt("cond")<23 and st.getInt("cond")>0 :
      htmltext = "30473-05.htm"
     elif st.getInt("cond")==23 and st.getQuestItemsCount(GOLDEN_STATUE)==0 :
      htmltext = "30473-06.htm"
      st.addExpAndSp(32000,4100)
      st.giveItems(MARK_OF_HEALER,1)
      st.set("cond","0")
      st.exitQuest(False)
      st.playSound("ItemSound.quest_finish")
      st.set("onlyone","1")
     elif st.getInt("cond")==23 and st.getQuestItemsCount(GOLDEN_STATUE) :
      htmltext = "30473-07.htm"
   elif npcId == PERRIN:
     if st.getInt("cond")==1 :
      htmltext = "30428-01.htm"
     elif st.getInt("cond")==3 :
      htmltext = "30428-03.htm"
      st.set("cond","4")
      st.takeItems(REPORT_OF_PERRIN,1)
     elif st.getInt("cond")==4 :
      htmltext = "30428-04.htm"
   elif npcId == ORPHAN and st.getInt("cond")==4 :
        n = st.getRandom(5)
        if n == 0:
          htmltext = "30659-01.htm"
          htmltext = "30659-02.htm"
        elif n == 2:
          htmltext = "30659-03.htm"
        elif n == 3:
          htmltext = "30659-04.htm"
        elif n == 4:
          htmltext = "30659-05.htm"
   elif npcId == ALLANA:
     if st.getInt("cond")==4 :
      htmltext = "30424-01.htm"
      st.set("cond","5")
     elif st.getInt("cond")==5 :
      htmltext = "30424-02.htm"
   elif npcId == GUPU :
     if st.getInt("cond")==5 :
      htmltext = "30658-01.htm"
      st.set("cond","6")
     elif st.getInt("cond")==6 :
      htmltext = "30658-01.htm"
     elif st.getInt("cond")==7 :
      htmltext = "30658-04.htm"
     elif st.getInt("cond")==8 and st.getQuestItemsCount(WINDYS_PEBBLES) > 0 :
      htmltext = "30658-06.htm"
      st.giveItems(GOLDEN_STATUE,1)
      st.takeItems(WINDYS_PEBBLES,1)
     elif st.getInt("cond")==8 :
      htmltext = "30658-06.htm"
     elif st.getInt("cond")==9 :
      htmltext = "30658-07.htm"
   elif npcId == WINDY:
     if st.getInt("cond")==7:
      htmltext = "30660-01.htm"
     elif st.getInt("cond")==8 :
      htmltext = "30660-04.htm"
   elif npcId == SORIUS :
     if st.getInt("cond")==9 :
      htmltext = "30327-01.htm"
      st.giveItems(ORDER_OF_SORIUS,1)
      st.set("cond","10")
     elif st.getInt("cond")>9 and st.getInt("cond")<22 :
      htmltext = "30327-02.htm"
     elif st.getInt("cond")==22 :
      htmltext = "30327-03.htm"
      st.takeItems(CRISTINAS_LETTER,1)
      st.set("cond","23")
   elif npcId == DAURIN:
     if st.getInt("cond")==10 and st.getQuestItemsCount(ORDER_OF_SORIUS) :
      htmltext = "30674-01.htm"
     elif st.getInt("cond")==12 and st.getQuestItemsCount(SECRET_LETTER1) :
      htmltext = "30674-03.htm"
      st.set("cond","13")
   elif npcId == MYSTERIOUS:
     if st.getInt("cond")==13 or st.getInt("cond")==14 :
      htmltext = "30661-01.htm"
      st.addSpawn(LETO_ASSASSIN)
      st.addSpawn(LETO_ASSASSIN)
      st.addSpawn(LETO_ASSASSIN)
      st.playSound("Itemsound.quest_before_battle")
      st.set("cond","14")
     elif st.getInt("cond")==15 or st.getInt("cond")==16:
      htmltext = "30661-02.htm"
      st.addSpawn(LETO_SNIPER)
      st.addSpawn(LETO_SNIPER)
      st.addSpawn(LETO_SNIPER)
      st.playSound("Itemsound.quest_before_battle")
      st.set("cond","16")
     elif st.getInt("cond")==17 or st.getInt("cond")==18:
      htmltext = "30661-03.htm"
      st.addSpawn(LETO_WIZARD)
      st.addSpawn(LETO_WIZARD)
      st.addSpawn(LETO_LORD)
      st.playSound("Itemsound.quest_before_battle")
      st.set("cond","18")
     elif st.getInt("cond") == 19 :
      htmltext = "30661-04.htm"
      st.set("cond","20")
   elif npcId in ELVES.keys() :
     if st.getInt("cond") == 20:
      htmltext = ELVES[npcId][2]
      st.set("cond","21")
     elif st.getInt("cond") == 21:
      htmltext = ELVES[npcId][3]
   elif npcId == KRISTINA :
     if st.getInt("cond")==21 :
      htmltext = "30665-01.htm"
     elif st.getInt("cond")<21 :
      htmltext = "30665-03.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return
   if st.getState() != State.STARTED : return
   npcId = npc.getNpcId()
   if not npcId in DROPLIST.keys() : return
   condition,maxcount,item,next_condition=DROPLIST[npcId]
   if st.getInt("cond")==condition and st.getQuestItemsCount(item)<maxcount:
     if item != 0:
       st.giveItems(item,1)
     if next_condition != 0:
       st.set("cond",next_condition)
     st.playSound("Itemsound.quest_middle")
   return

QUEST       = Quest(226,qn,"Test of the Healer")

QUEST.addStartNpc(BANDELLOS)

QUEST.addTalkId(BANDELLOS)

for npcId in [SORIUS,ALLANA,PERRIN,GUPU,ORPHAN,WINDY,MYSTERIOUS,PIPER,SLEIN,KEIN,KRISTINA,DAURIN]:
  QUEST.addTalkId(npcId)

for mobId in DROPLIST.keys():
  QUEST.addKillId(mobId)