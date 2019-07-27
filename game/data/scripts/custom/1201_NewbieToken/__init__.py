# Made by Vice
import sys
from ru.catssoftware.gameserver.model.quest import QuestMessage
from ru.catssoftware.gameserver.network.serverpackets import ExShowScreenMessage
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest
from ru.catssoftware.gameserver.model import L2Multisell

qn = "1201_NewbieToken"

#enable/disable coupon give
TOKEN_ENABLED = 1

#NPCs
NPCS = [30598,30599,30600,30601,30602,31076,31077,32135]

#Items
COUPON_ONE = 7832
COUPON_TWO = 7833

#Newbie/one time rewards section
#Any quest should rely on a unique bit, but
#it could be shared among quest that were mutually
#exclusive or race restricted.
#Bit #1 isn't used for backwards compatibility.
#This script uses 2 bits, one for newbie coupons and another for travelers
WEAPON_REWARD = 16
ARMOR_REWARD = 32

# Multisell
WEAPON_MULTISELL = 528
ARMOR_MULTISELL = 529

class Quest (JQuest) : 

  def __init__(self, id, name, descr) :
    JQuest.__init__(self, id, name, descr)

  def onAdvEvent (self, event, npc, player) :
    if not TOKEN_ENABLED : return
    st = player.getQuestState(qn)
    newbie = player.getNewbie()
    level = player.getLevel()
    occupation_level = player.getClassId().level()
    pkkills = player.getPkKills()
    if event == "newbie_give_weapon_coupon" :
       #@TODO: check if this is the very first character for this account
       #would need a bit of SQL, or a core method to determine it.
       #This condition should be stored by the core in the account_data table
       #upon character creation.
       if 6 <= level <= 39 and not pkkills and occupation_level == 0 :
          # check the player state against this quest newbie rewarding mark.
          if newbie | WEAPON_REWARD != newbie :
             player.setNewbie(newbie|WEAPON_REWARD)
             st.giveItems(COUPON_ONE, 5)
             st1 = player.getQuestState("7003_NewbieHelper")
             if not st1 : return "2.htm"
             st1.set("cond","4");
             player.sendPacket(ExShowScreenMessage(QuestMessage.Q1201_mess1.get(), 4000))
             return "2.htm" #here's the coupon you requested
          else :
             return "3.htm" #you got a coupon already!
       else :
          return "4.htm" #you're not eligible to get a coupon (level caps, pkkills or already changed class)

    elif event == "newbie_show_weapon" :
       if 6 <= level <= 39 and not pkkills and occupation_level == 0 :
          L2Multisell.getInstance().separateAndSend(WEAPON_MULTISELL, player, 0, 0);
       else :
          return "5.htm" #you're not eligible to use warehouse

    elif event == "newbie_give_armor_coupon" :
       #@TODO: check if this is the very first character for this account
       #would need a bit of SQL, or a core method to determine it.
       #This condition should be stored by the core in the account_data table
       #upon character creation.
       if 6 <= level <= 39 and not pkkills and occupation_level > 0 :
          # check the player state against this quest newbie rewarding mark.
          if newbie | ARMOR_REWARD != newbie :
             player.setNewbie(newbie|ARMOR_REWARD)
             st.giveItems(COUPON_TWO, 1)
             return "6.htm" #here's the coupon you requested
          else :
             return "7.htm" #you got a coupon already!
       else :
          return "8.htm" #you're not eligible to get a coupon (level caps, pkkills or already changed class)

    elif event == "newbie_show_armor" :
       if 6 <= level <= 39 and not pkkills and occupation_level > 0 :
          L2Multisell.getInstance().separateAndSend(ARMOR_MULTISELL, player, 0, 0);
       else :
          return "9.htm" #you're not eligible to use warehouse

  def onTalk (self,npc,player):
    st = player.getQuestState(qn)
    if not st : st = self.newQuestState(player)
    return "1.htm"

QUEST = Quest(1201, qn, "custom")

for npc in NPCS :
   QUEST.addStartNpc(npc)
   QUEST.addTalkId(npc)