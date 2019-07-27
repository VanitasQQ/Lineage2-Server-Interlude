# autor Snzinfo L2EmuRT Team
import sys
from ru.catssoftware.gameserver.model.quest        import State
from ru.catssoftware.gameserver.model.quest        import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "7002_NewbieGuide"

NPCS = [30598,30599,30600,30601,30602,32135]

FIGHTER = [0x00,0x12,0x1f,0x2c,0x35,0x7b,0x7c]
MAGE = [0x0a,0x19,0x26,0x31]

class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onEvent (self,event,st):
     htmltext = event
     return htmltext

 def onTalk (Self,npc,player):
    htmltext = "<html><body>test</body></html>"
    st = player.getQuestState(qn)
    if not st : return htmltext
    npcId = npc.getNpcId()
    Level = st.getPlayer().getLevel()
    ClassId = player.getClassId().getId()

    if npcId == 30598 :
       if player.getRace().ordinal() == 0 :
          if Level < 6 :
             if ClassId in FIGHTER :
                htmltext = str(npcId)+"-f1.htm"
             elif ClassId in MAGE :
                htmltext = str(npcId)+"-m.htm"
             else:
                htmltext = str(npcId)+"-lv.htm"
          elif Level < 8 :
             if ClassId in FIGHTER :
                htmltext = str(npcId)+"-1.htm"
             elif ClassId in MAGE :
                htmltext = str(npcId)+"-m.htm"
          elif Level < 11 :
             if ClassId in FIGHTER :
                htmltext = str(npcId)+"-1.htm"
             elif ClassId in MAGE :
                htmltext = str(npcId)+"-m6.htm"
          elif Level < 15 :
             if ClassId in FIGHTER :
                htmltext = str(npcId)+"-a1.htm"
             elif ClassId in MAGE :
                htmltext = str(npcId)+"-m6.htm"
          elif Level < 20 :
             if ClassId in FIGHTER :
                htmltext = str(npcId)+"-a1.htm"
             elif ClassId in MAGE :
                htmltext = str(npcId)+"-m12.htm"
          elif Level > 19 :
             htmltext = str(npcId)+"-lv.htm"
       else:
          htmltext = str(npcId)+"-00.htm"

    return htmltext

QUEST       = Quest(-1,qn,"custom")

for i in NPCS:
    QUEST.addStartNpc(i)
    QUEST.addTalkId(i)
