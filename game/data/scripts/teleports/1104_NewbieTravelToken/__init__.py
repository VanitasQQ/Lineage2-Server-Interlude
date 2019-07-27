# Newbie Travel Token Teleport - by DrLecter
import sys
from ru.catssoftware.gameserver.model.quest        import State
from ru.catssoftware.gameserver.model.quest        import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "1104_NewbieTravelToken"

TOKEN = 8542

DATA={
      30600:[ 12111,  16686,-4584], #DE
      30601:[115632,-177996, -896], #DW
      30599:[ 45475,  48359,-3056], #EV
      30602:[-45032,-113598, -192], #OV
      30598:[-84081, 243227,-3728]  #TI
}

class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onEvent (self,event,st):
   if event.isdigit() :
     dest = int(event)
     if dest in DATA.keys() :
       x,y,z = DATA[dest]
       if x and y and z :
         if st.getQuestItemsCount(TOKEN):
           st.takeItems(TOKEN,1)
           st.getPlayer().teleToLocation(x,y,z)
           st.exitQuest(1)
         else:
           st.exitQuest(1)
           return "Incorrect item count"
   return

 def onTalk (Self,npc,player):
   st = player.getQuestState(qn)
   npcId = npc.getNpcId()
   if player.getLevel() >= 20 :
     htmltext = "1.htm"
     st.exitQuest(1)
   else:
     htmltext = str(npcId)+".htm"
   return htmltext

QUEST = Quest(1104,qn,"Teleports")

for i in DATA.keys() :
    QUEST.addStartNpc(i)
    QUEST.addTalkId(i)