# Made by Mr. Have fun! Version 0.3
# Shadow Weapon Coupons contributed by BiTi for the Official L2J Datapack Project
# Visit http://forum.l2jdp.com for more details
import sys
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest
from ru.catssoftware.gameserver.network.serverpackets import NpcSay
from ru.catssoftware.gameserver.network.serverpackets import SocialAction

qn = "416_PathToOrcShaman"

FIRE_CHARM = 1616
KASHA_BEAR_PELT = 1617
KASHA_BSPIDER_HUSK = 1618
KASHA_BSPIDER_HUSK = 1618
FIERY_EGG1 = 1619
FIERY_EGG1 = 1619
HESTUI_MASK = 1620
HESTUI_MASK = 1620
FIERY_EGG2 = 1621
TOTEM_SPIRIT_CLAW = 1622
TATARUS_LETTER = 1623
FLAME_CHARM = 1624
GRIZZLY_BLOOD = 1625
BLOOD_CAULDRON = 1626
SPIRIT_NET = 1627
BOUND_DURKA_SPIRIT = 1628
DURKA_PARASITE = 1629
TOTEM_SPIRIT_BLOOD = 1630
MASK_OF_MEDIUM = 1631

class Quest (JQuest) :

 def __init__(self,id,name,descr):
     JQuest.__init__(self,id,name,descr)
     self.questItemIds = range(1616,1631)

 def onEvent (self,event,st) :
    htmltext = event
    player = st.getPlayer()
    if event == "1" :
        st.set("id","0")
        st.set("cond","1")
        st.setState(State.STARTED)
        st.playSound("ItemSound.quest_accept")
        htmltext = "30585-06.htm"
        st.giveItems(FIRE_CHARM,1)
    elif event == "32057_1" :
        htmltext = "32057-02.htm"
        st.playSound("ItemSound.quest_middle")
        st.set("cond","14")
    elif event == "32057_2" :
        htmltext = "32057-05.htm"
        st.playSound("ItemSound.quest_middle")
        st.set("cond","21")
    elif event == "32090_1" :
        htmltext = "32090-04.htm"
        st.playSound("ItemSound.quest_middle")
        st.set("cond","18")
    elif event == "30585_1" :
          if player.getClassId().getId() != 0x31 :
            if player.getClassId().getId() == 0x32 :
              htmltext = "30585-02a.htm"
            else:
              htmltext = "30585-02.htm"
          else:
            if player.getLevel() < 18 :
              htmltext = "30585-03.htm"
            else:
              if st.getQuestItemsCount(MASK_OF_MEDIUM) != 0 :
                htmltext = "30585-04.htm"
              else:
                htmltext = "30585-05.htm"
                return htmltext
    elif event == "30585_1a" :
          htmltext = "30585-10a.htm"
    elif event == "30585_2" :
          htmltext = "30585-11.htm"
          st.takeItems(TOTEM_SPIRIT_CLAW,1)
          st.giveItems(TATARUS_LETTER,1)
          st.set("cond","5")
          st.playSound("ItemSound.quest_middle")
    elif event == "30585_3" :
          htmltext = "30585-11a.htm"
          st.takeItems(TOTEM_SPIRIT_CLAW,1)
          st.playSound("ItemSound.quest_middle")
          st.set("cond","12")
    elif event == "30592_1" :
          htmltext = "30592-02.htm"
    elif event == "30592_2" :
          htmltext = "30592-03.htm"
          st.takeItems(HESTUI_MASK,1)
          st.takeItems(FIERY_EGG2,1)
          st.giveItems(TOTEM_SPIRIT_CLAW,1)
          st.set("cond","4")
          st.playSound("ItemSound.quest_middle")
    elif event == "30502_2" :
          htmltext = "30502-07.htm"
          st.rewardItems(57,81900)
          st.takeItems(TOTEM_SPIRIT_BLOOD,st.getQuestItemsCount(TOTEM_SPIRIT_BLOOD))
          st.giveItems(MASK_OF_MEDIUM,1)
          st.addExpAndSp(295862,18194)
          player.sendPacket(SocialAction(player.getObjectId(),3))
          player.sendPacket(SocialAction(player.getObjectId(),15))
          st.set("cond","0")
          st.exitQuest(False)
          st.playSound("ItemSound.quest_finish")
    elif event == "30593_1" :
          htmltext = "30593-02.htm"
    elif event == "30593_2" :
          htmltext = "30593-03.htm"
          st.takeItems(BLOOD_CAULDRON,1)
          st.giveItems(SPIRIT_NET,1)
          st.set("cond","9")
          st.playSound("ItemSound.quest_middle")
    return htmltext

 def onTalk (self,npc,player):
   htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
   st = player.getQuestState(qn)
   if not st : return htmltext

   npcId = npc.getNpcId()
   id = st.getState()
   if npcId != 30585 and id != State.STARTED : return htmltext

   if npcId == 30585 and st.getInt("cond")==0 :
        htmltext = "30585-01.htm"
   elif npcId == 30585 and st.getInt("cond") == 12:
        htmltext = "30585-11a.htm"
   elif npcId == 31979 and st.getInt("cond") == 12:
        htmltext = "31979-01.htm"
        st.playSound("ItemSound.quest_middle")
        st.set("cond","13")
   elif npcId == 31979 and st.getInt("cond") == 21:
        htmltext = "31979-03.htm"
        st.giveItems(MASK_OF_MEDIUM,1)
        st.rewardItems(57,81900)
        st.addExpAndSp(295862,18194)
        player.sendPacket(SocialAction(player.getObjectId(),3))
        player.sendPacket(SocialAction(player.getObjectId(),15))
        st.set("cond","0")
        st.exitQuest(False)
        st.playSound("ItemSound.quest_finish")
   elif npcId == 31979 and st.getInt("cond") == 13:
        htmltext = "31979-02.htm"
   elif npcId == 32057 and st.getInt("cond") == 13:
        htmltext = "32057-01.htm"
   elif npcId == 32057 and st.getInt("cond") == 14:
        htmltext = "32057-03.htm"
   elif npcId == 32057 and st.getInt("cond") == 20:
        htmltext = "32057-04.htm"
   elif npcId == 32057 and st.getInt("cond") == 21:
        htmltext = "32057-05.htm"
   elif npcId == 32090 and st.getInt("cond") == 15:
        htmltext = "32090-01.htm"
        st.playSound("ItemSound.quest_middle")
        st.set("cond","16")
   elif npcId == 32090 and st.getInt("cond") == 16:
        htmltext = "32090-01.htm"
   elif npcId == 32090 and st.getInt("cond") == 17:
        htmltext = "32090-02.htm"
   elif npcId == 32090 and st.getInt("cond") == 18:
        htmltext = "32090-05.htm"
   elif npcId == 32090 and st.getInt("cond") == 19:
        htmltext = "32090-06.htm"
        st.playSound("ItemSound.quest_middle")
        st.set("cond","20")
   elif npcId == 32090 and st.getInt("cond") == 20:
        htmltext = "32090-06.htm"
   elif npcId == 30585 and st.getInt("cond") and st.getQuestItemsCount(FIRE_CHARM)==1 and ((st.getQuestItemsCount(KASHA_BEAR_PELT)+st.getQuestItemsCount(KASHA_BSPIDER_HUSK)+st.getQuestItemsCount(FIERY_EGG1))<3) :
        htmltext = "30585-07.htm"
   elif npcId == 30585 and st.getInt("cond") and st.getQuestItemsCount(FIRE_CHARM)==1 and ((st.getQuestItemsCount(KASHA_BEAR_PELT)+st.getQuestItemsCount(KASHA_BSPIDER_HUSK)+st.getQuestItemsCount(FIERY_EGG1))>=3) :
        htmltext = "30585-08.htm"
        st.takeItems(FIRE_CHARM,1)
        st.takeItems(KASHA_BEAR_PELT,1)
        st.takeItems(KASHA_BSPIDER_HUSK,1)
        st.takeItems(FIERY_EGG1,1)
        st.giveItems(HESTUI_MASK,1)
        st.giveItems(FIERY_EGG2,1)
        st.set("cond","3")
        st.playSound("ItemSound.quest_middle")
   elif npcId == 30585 and st.getInt("cond") and st.getQuestItemsCount(HESTUI_MASK)==1 and st.getQuestItemsCount(FIERY_EGG2)==1 :
        htmltext = "30585-09.htm"
   elif npcId == 30585 and st.getInt("cond") and st.getQuestItemsCount(TOTEM_SPIRIT_CLAW)==1 :
        htmltext = "30585-10.htm"
   elif npcId == 30585 and st.getInt("cond") and st.getQuestItemsCount(TATARUS_LETTER)==1 :
        htmltext = "30585-12.htm"
   elif npcId == 30585 and st.getInt("cond") and (st.getQuestItemsCount(GRIZZLY_BLOOD) or st.getQuestItemsCount(FLAME_CHARM) or st.getQuestItemsCount(BLOOD_CAULDRON) or st.getQuestItemsCount(SPIRIT_NET) or st.getQuestItemsCount(BOUND_DURKA_SPIRIT) or st.getQuestItemsCount(TOTEM_SPIRIT_BLOOD)) :
        htmltext = "30585-13.htm"
   elif npcId == 30592 and st.getInt("cond") and st.getQuestItemsCount(HESTUI_MASK) and st.getQuestItemsCount(FIERY_EGG2) :
        htmltext = "30592-01.htm"
   elif npcId == 30592 and st.getInt("cond") and st.getQuestItemsCount(TOTEM_SPIRIT_CLAW) :
        htmltext = "30592-04.htm"
   elif npcId == 30592 and st.getInt("cond") and (st.getQuestItemsCount(GRIZZLY_BLOOD) or st.getQuestItemsCount(FLAME_CHARM) or st.getQuestItemsCount(BLOOD_CAULDRON) or st.getQuestItemsCount(SPIRIT_NET) or st.getQuestItemsCount(BOUND_DURKA_SPIRIT) or st.getQuestItemsCount(TOTEM_SPIRIT_BLOOD) or st.getQuestItemsCount(TATARUS_LETTER)) :
        htmltext = "30592-05.htm"
   elif npcId == 30502 and st.getInt("cond") and st.getQuestItemsCount(TATARUS_LETTER) :
        htmltext = "30502-01.htm"
        st.giveItems(FLAME_CHARM,1)
        st.takeItems(TATARUS_LETTER,1)
        st.set("cond","6")
        st.playSound("ItemSound.quest_middle")
   elif npcId == 30502 and st.getInt("cond") and st.getQuestItemsCount(FLAME_CHARM)==1 and st.getQuestItemsCount(GRIZZLY_BLOOD)<3 :
        htmltext = "30502-02.htm"
   elif npcId == 30502 and st.getInt("cond") and st.getQuestItemsCount(FLAME_CHARM)==1 and st.getQuestItemsCount(GRIZZLY_BLOOD)>=3 :
        htmltext = "30502-03.htm"
        st.takeItems(FLAME_CHARM,1)
        st.takeItems(GRIZZLY_BLOOD,st.getQuestItemsCount(GRIZZLY_BLOOD))
        st.giveItems(BLOOD_CAULDRON,1)
        st.set("cond","8")
        st.playSound("ItemSound.quest_middle")
   elif npcId == 30502 and st.getInt("cond") and st.getQuestItemsCount(BLOOD_CAULDRON)==1 :
        htmltext = "30502-04.htm"
   elif npcId == 30502 and st.getInt("cond") and (st.getQuestItemsCount(BOUND_DURKA_SPIRIT)==1 or st.getQuestItemsCount(SPIRIT_NET)==1) :
        htmltext = "30502-05.htm"
   elif npcId == 30502 and st.getInt("cond") and st.getQuestItemsCount(TOTEM_SPIRIT_BLOOD)==1 :
        htmltext = "30502-06.htm"
   elif npcId == 30593 and st.getInt("cond") and st.getQuestItemsCount(BLOOD_CAULDRON) :
        htmltext = "30593-01.htm"
   elif npcId == 30593 and st.getInt("cond") and st.getQuestItemsCount(SPIRIT_NET) and st.getQuestItemsCount(BOUND_DURKA_SPIRIT)==0 :
        htmltext = "30593-04.htm"
   elif npcId == 30593 and st.getInt("cond") and st.getQuestItemsCount(SPIRIT_NET)==0 and st.getQuestItemsCount(BOUND_DURKA_SPIRIT) :
        htmltext = "30593-05.htm"
        st.takeItems(BOUND_DURKA_SPIRIT,1)
        st.giveItems(TOTEM_SPIRIT_BLOOD,1)
        st.set("cond","11")
        st.playSound("ItemSound.quest_middle")
   elif npcId == 30593 and st.getInt("cond")==1 and st.getQuestItemsCount(TOTEM_SPIRIT_BLOOD) :
        htmltext = "30593-06.htm"
   return htmltext

 def onKill(self,npc,player,isPet):
   st = player.getQuestState(qn)
   if not st : return
   if st.getState() != State.STARTED : return
   
   npcId = npc.getNpcId()
   if npcId == 20479 :
        st.set("id","0")
        if st.getInt("cond") and st.getQuestItemsCount(FIRE_CHARM) == 1 and st.getQuestItemsCount(KASHA_BEAR_PELT)<1 :
          if st.getQuestItemsCount(KASHA_BEAR_PELT)+st.getQuestItemsCount(KASHA_BSPIDER_HUSK)+st.getQuestItemsCount(FIERY_EGG1) == 2 :
            st.giveItems(KASHA_BEAR_PELT,1)
            st.playSound("ItemSound.quest_middle")
            st.set("cond","2")
          else:
            st.giveItems(KASHA_BEAR_PELT,1)
            st.playSound("ItemSound.quest_itemget")
   elif npcId == 27319 :
        if st.getInt("cond") == 14:
            st.set("cond","15")
            st.playSound("ItemSound.quest_middle")
            npc.broadcastPacket(NpcSay(npc.getObjectId(),0,npc.getNpcId(),"My dear friend of "+player.getName()+", who has gone on ahead of me!"))
        elif st.getInt("cond") == 16:
            st.set("cond","17")
            st.playSound("ItemSound.quest_middle")
            npc.broadcastPacket(NpcSay(npc.getObjectId(),0,npc.getNpcId(),"Listen to Tejakar Gandi, young Oroka! The spirit of the slain leopard is calling you, "+player.getName()+"!"))
        elif st.getInt("cond") == 18:
            st.set("cond","19")
            st.playSound("ItemSound.quest_middle")
   elif npcId == 20478 :
        st.set("id","0")
        if st.getInt("cond") and st.getQuestItemsCount(FIRE_CHARM) == 1 and st.getQuestItemsCount(KASHA_BSPIDER_HUSK)<1 :
          if st.getQuestItemsCount(KASHA_BEAR_PELT)+st.getQuestItemsCount(KASHA_BSPIDER_HUSK)+st.getQuestItemsCount(FIERY_EGG1) == 2 :
            st.giveItems(KASHA_BSPIDER_HUSK,1)
            st.playSound("ItemSound.quest_middle")
            st.set("cond","2")
          else:
            st.giveItems(KASHA_BSPIDER_HUSK,1)
            st.playSound("ItemSound.quest_itemget")
   elif npcId == 20415 :
        st.set("id","0")
        if st.getInt("cond") and st.getQuestItemsCount(FIRE_CHARM) == 1 and st.getQuestItemsCount(FIERY_EGG1)<1 :
          if st.getQuestItemsCount(KASHA_BEAR_PELT)+st.getQuestItemsCount(KASHA_BSPIDER_HUSK)+st.getQuestItemsCount(FIERY_EGG1) == 2 :
            st.giveItems(FIERY_EGG1,1)
            st.playSound("ItemSound.quest_middle")
            st.set("cond","2")
          else:
            st.giveItems(FIERY_EGG1,1)
            st.playSound("ItemSound.quest_itemget")
   elif npcId == 20335 :
        st.set("id","0")
        if st.getInt("cond") and st.getQuestItemsCount(FLAME_CHARM) == 1 and st.getQuestItemsCount(GRIZZLY_BLOOD)<3 :
          if st.getQuestItemsCount(GRIZZLY_BLOOD) == 2 :
            st.giveItems(GRIZZLY_BLOOD,1)
            st.playSound("ItemSound.quest_middle")
            st.set("cond","7")
          else:
            st.giveItems(GRIZZLY_BLOOD,1)
            st.playSound("ItemSound.quest_itemget")
   elif npcId == 20038 :
        st.set("id","0")
        if st.getInt("cond") and st.getQuestItemsCount(SPIRIT_NET) == 1 and st.getQuestItemsCount(BOUND_DURKA_SPIRIT) == 0 and st.getQuestItemsCount(DURKA_PARASITE)<8 :
          n = st.getRandom(10)
          if st.getQuestItemsCount(DURKA_PARASITE) == 5 and n<1 :
            st.takeItems(DURKA_PARASITE,st.getQuestItemsCount(DURKA_PARASITE))
            st.addSpawn(27056)
            st.playSound("ItemSound.quest_itemget")
          elif st.getQuestItemsCount(DURKA_PARASITE) == 6 and n<2 :
            st.takeItems(DURKA_PARASITE,st.getQuestItemsCount(DURKA_PARASITE))
            st.playSound("ItemSound.quest_itemget")
            st.addSpawn(27056)
          elif st.getQuestItemsCount(DURKA_PARASITE) == 7 and n<2 :
            st.takeItems(DURKA_PARASITE,st.getQuestItemsCount(DURKA_PARASITE))
            st.playSound("ItemSound.quest_itemget")
            st.addSpawn(27056)
          elif st.getQuestItemsCount(DURKA_PARASITE) >= 7 :
            st.addSpawn(27056)
            st.playSound("ItemSound.quest_itemget")
            st.takeItems(DURKA_PARASITE,st.getQuestItemsCount(DURKA_PARASITE))
          else:
            st.giveItems(DURKA_PARASITE,1)
            st.playSound("ItemSound.quest_itemget")
   elif npcId == 20043 :
        st.set("id","0")
        if st.getInt("cond") and st.getQuestItemsCount(SPIRIT_NET) == 1 and st.getQuestItemsCount(BOUND_DURKA_SPIRIT) == 0 and st.getQuestItemsCount(DURKA_PARASITE)<8 :
          n = st.getRandom(10)
          if st.getQuestItemsCount(DURKA_PARASITE) == 5 and n<1 :
            st.takeItems(DURKA_PARASITE,st.getQuestItemsCount(DURKA_PARASITE))
            st.addSpawn(27056)
            st.playSound("ItemSound.quest_itemget")
          elif st.getQuestItemsCount(DURKA_PARASITE) == 6 and n<2 :
            st.takeItems(DURKA_PARASITE,st.getQuestItemsCount(DURKA_PARASITE))
            st.playSound("ItemSound.quest_itemget")
            st.addSpawn(27056)
          elif st.getQuestItemsCount(DURKA_PARASITE) == 7 and n<2 :
            st.takeItems(DURKA_PARASITE,st.getQuestItemsCount(DURKA_PARASITE))
            st.playSound("ItemSound.quest_itemget")
            st.addSpawn(27056)
          elif st.getQuestItemsCount(DURKA_PARASITE) >= 7 :
            st.addSpawn(27056)
            st.playSound("ItemSound.quest_itemget")
            st.takeItems(DURKA_PARASITE,st.getQuestItemsCount(DURKA_PARASITE))
          else:
            st.giveItems(DURKA_PARASITE,1)
            st.playSound("ItemSound.quest_itemget")
   elif npcId == 27056 :
        st.set("id","0")
        if st.getInt("cond") and st.getQuestItemsCount(SPIRIT_NET) == 1 and st.getQuestItemsCount(BOUND_DURKA_SPIRIT) == 0 :
          st.giveItems(BOUND_DURKA_SPIRIT,1)
          st.takeItems(SPIRIT_NET,1)
          st.takeItems(DURKA_PARASITE,st.getQuestItemsCount(DURKA_PARASITE))
          st.playSound("ItemSound.quest_middle")
          st.set("cond","10")
   return

QUEST       = Quest(416,qn,"Path of the Orc Shama")

QUEST.addStartNpc(30585)

QUEST.addTalkId(30585)
QUEST.addTalkId(30502)
QUEST.addTalkId(30592)
QUEST.addTalkId(30593)
QUEST.addTalkId(31979)
QUEST.addTalkId(32057)
QUEST.addTalkId(32090)

QUEST.addKillId(20335)
QUEST.addKillId(20038)
QUEST.addKillId(20415)
QUEST.addKillId(20043)
QUEST.addKillId(20478)
QUEST.addKillId(20479)
QUEST.addKillId(27056)
QUEST.addKillId(27319)