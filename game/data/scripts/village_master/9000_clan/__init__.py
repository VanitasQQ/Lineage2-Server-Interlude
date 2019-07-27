# Created by DraX on 2005.08.12
# minor fixes by DrLecter 2005.09.10
import sys
from ru.catssoftware.gameserver.model.quest        import State
from ru.catssoftware.gameserver.model.quest        import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "9000_clan"

NPC=[30026,30031,30037,30066,30070,30109,30115,30120,30154,30174,30175,30176,30187, \
     30191,30195,30288,30289,30290,30297,30358,30373,30462,30474,30498,30499,30500, \
     30503,30504,30505,30508,30511,30512,30513,30520,30525,30565,30594,30595,30676, \
     30677,30681,30685,30687,30689,30694,30699,30704,30845,30847,30849,30854,30857, \
     30862,30865,30894,30897,30900,30905,30910,30913,31269,31272,31276,31279,31285, \
     31288,31314,31317,31321,31324,31326,31328,31331,31334,31755,31958,31961,31965, \
     31968,31974,31977,31996,32092,32093,32094,32095,32096,32097,32098,32145,32146, \
     32147,32150,32153,32154,32157,32158,32160,32171,32191,32193,32196,32199,32202, \
     32205,32206,32209,32210,32213,32214,32217,32218,32221,32222,32225,32226,32229, \
     32230,32233,32234]

class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onEvent (self,event,st):
   htmltext = event
   if event == "9000-03.htm" :
     if st.getPlayer().getClan() == None or not st.getPlayer().isClanLeader() :
       return "9000-03-no.htm"
   elif event == "9000-04.htm" :
     if st.getPlayer().getClan() == None or not st.getPlayer().isClanLeader() :
       return "9000-04-no.htm"
   elif event == "9000-05.htm" :
     if st.getPlayer().getClan() == None or not st.getPlayer().isClanLeader() :
       return "9000-05-no.htm"
   elif event == "9000-07.htm" :
     if st.getPlayer().getClan() == None or not st.getPlayer().isClanLeader() :
       return "9000-07-no.htm"
   elif event == "9000-06a.htm" :
     if st.getPlayer().getClan() == None or not st.getPlayer().isClanLeader() :
       return "9000-07-no.htm"
   elif event == "9000-12a.htm" :
     if st.getPlayer().getClan() == None or not st.getPlayer().isClanLeader() :
       return "9000-07-no.htm"
   elif event == "9000-13a.htm" :
     if st.getPlayer().getClan() == None or not st.getPlayer().isClanLeader() :
       return "9000-07-no.htm"
   elif event == "9000-13b.htm" :
     if st.getPlayer().getClan() == None or not st.getPlayer().isClanLeader() :
       return "9000-07-no.htm"
   elif event == "9000-14a.htm" :
     if st.getPlayer().getClan() == None or not st.getPlayer().isClanLeader() :
       return "9000-07-no.htm"
   elif event == "9000-15.htm" :
     if st.getPlayer().getClan() == None or not st.getPlayer().isClanLeader() :
       return "9000-07-no.htm"
   return htmltext

 def onTalk (Self,npc,player):
   st = player.getQuestState(qn)
   npcId = npc.getNpcId()
   if npcId in NPC:
     st.set("cond","0")
     st.setState(State.STARTED)
     return "9000-01.htm"

QUEST = Quest(9000,qn,"village_master")

for item in NPC:
   QUEST.addStartNpc(item)
   QUEST.addTalkId(item)