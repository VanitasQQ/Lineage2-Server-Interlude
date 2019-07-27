# Made by Next - cleanup by Kerberos
# this script is part of the Official L2J Datapack Project.
# Visit http://forum.l2jdp.com for more details.
# Rate fix by Gnat
import sys
from ru.catssoftware import Config
from ru.catssoftware.gameserver.model.quest import State
from ru.catssoftware.gameserver.model.quest import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "632_NecromancersRequest"
#NPC
WIZARD = 31522

#ITEMS
V_HEART = 7542
Z_BRAIN = 7543

#DROP CHANCES
V_HEART_CHANCE = 50 # in percents
Z_BRAIN_CHANCE = 33 # in percents

#REWARDS
ADENA = 57
ADENA_AMOUNT = 120000

#MOBS
VAMPIRES = [ 21568, 21573, 21582, 21585, 21586, 21587, 21588, 21589, 21590, 21591, 21592, 21593, 21594, 21595 ]
UNDEADS = [ 21547, 21548, 21549, 21551, 21552, 21555, 21556, 21562, 21571, 21576, 21577, 21579 ]

class Quest (JQuest):

    def __init__(self,id,name,descr): 
        JQuest.__init__(self,id,name,descr)
        self.questItemIds = [V_HEART, Z_BRAIN]

    def onEvent (self,event,st):
        if event == "0":
           st.playSound("ItemSound.quest_finish")
           htmltext = "31522-3.htm"
           st.exitQuest(1)
        elif event == "1":
           htmltext = "31522-0.htm"
        elif event == "2":
           if st.getInt("cond") == 2:
              if st.getQuestItemsCount(V_HEART) == 200:
                 st.takeItems(V_HEART, 200)
                 st.rewardItems(ADENA, ADENA_AMOUNT)
                 st.playSound("ItemSound.quest_finish")
                 st.set("cond","1")
                 htmltext = "31522-1.htm"
        elif event == "start":
           if st.getPlayer().getLevel() > 62 :
              htmltext = "31522-0.htm"
              st.set("cond","1")
              st.setState(State.STARTED)
              st.playSound("ItemSound.quest_accept")
           else:
              htmltext = "<html><body>Mysterious Wizard:<br>This quest can only be taken by characters that have a minimum level of <font color=\"LEVEL\">63</font>. Return when you are more experienced.</body></html>"
              st.exitQuest(1)
        return htmltext

    def onKill (self,npc,player,isPet):
        npcId = npc.getNpcId()
        if npcId in UNDEADS:
           partyMember = self.getRandomPartyMemberState(player, State.STARTED)
           if not partyMember: return
           st = partyMember.getQuestState(qn)
           if not st: return
           numItems, chance = divmod(Z_BRAIN_CHANCE*Config.RATE_DROP_QUEST,100)
           if st.getRandom(100) < chance:
              numItems += 1
           if numItems :
              st.giveItems(Z_BRAIN,int(numItems))
              st.playSound("ItemSound.quest_itemget")
        elif npcId in VAMPIRES:
           partyMember = self.getRandomPartyMember(player, "cond", "1")
           if not partyMember: return                
           st = partyMember.getQuestState(qn)
           if not st: return
           numItems, chance = divmod(V_HEART_CHANCE*Config.RATE_DROP_QUEST,100)
           count = st.getQuestItemsCount(V_HEART)
           if st.getRandom(100) < chance:
              numItems += 1
           if numItems :
              if count + numItems >= 200 :
                 numItems = 200 - count
                 st.playSound("ItemSound.quest_middle")
                 st.set("cond","2")
              else:
                 st.playSound("ItemSound.quest_itemget")
              st.giveItems(V_HEART, int(numItems))
        return

    def onTalk (self,npc,player):
        htmltext = "<html><body>You are either not on a quest that involves this NPC, or you don't meet this NPC's minimum quest requirements.</body></html>"
        st = player.getQuestState(qn)
        if st:
           npcId = npc.getNpcId()
           id = st.getState()
           cond = st.getInt("cond")
           if cond == 0 and id == State.CREATED:
              if npcId == WIZARD:
                 htmltext = "31522.htm"
           if cond == 1 and id == State.STARTED:
              htmltext = "31522-1.htm"
           if cond == 2 and id == State.STARTED:
              if st.getQuestItemsCount(V_HEART) == 200:
                 htmltext = "31522-2.htm"
        return htmltext

QUEST       = Quest(632, qn, "Necromancer's Request")

QUEST.addStartNpc(WIZARD)

QUEST.addTalkId(WIZARD)

for i in VAMPIRES:
    QUEST.addKillId(i)
for i in UNDEADS:
    QUEST.addKillId(i)