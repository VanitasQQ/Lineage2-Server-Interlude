# Created by DrLecter
import sys
from ru.catssoftware.gameserver.model              import L2Multisell
from ru.catssoftware.gameserver.model.quest        import State
from ru.catssoftware.gameserver.model.quest        import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "4000_ShadowWeapons"

NPC = [30037,30066,30070,30109,30115,30120,30174,30175,30176,30187,30191,30195, \
       30288,30289,30290,30297,30373,30462,30474,30498,30499,30500,30503,30504, \
       30505,30508,30511,30512,30513,30594,30595,30676,30677,30681,30685,30687, \
       30689,30694,30699,30704,30845,30847,30849,30854,30857,30862,30865,30894, \
       30897,30900,30905,30910,30913,31269,31272,31276,31279,31285,31288,31314, \
       31317,31321,31324,31326,31328,31331,31334,31336,31958,31961,31965,31968, \
       31974,31977,31996,32092,32093,32094,32095,32096,32097,32098,32193,32196, \
       32199,32202,32205,32206,32209,32210,32213,32214,32217,32218,32221,32222, \
       32225,32226,32229,32230,32233,32234]

D_COUPON,C_COUPON = [8869,8870]

class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onAdvEvent (self, event, npc, player) :
    st = player.getQuestState(qn)
    has_d = st.getQuestItemsCount(D_COUPON)
    has_c = st.getQuestItemsCount(C_COUPON)
    if has_d or has_c :
      multisell = 306893003
      if not has_d :
        multisell = 306893002
      elif not has_c :
        multisell = 306893001
      L2Multisell.getInstance().separateAndSend(multisell, player, 0, 0)
      st.exitQuest(1)
      return
    else :
      htmltext = "exchange-no.htm"
      st.exitQuest(1)
    return htmltext

 def onTalk (self, npc, player) :
   st = player.getQuestState(qn)
   if not st: return

   htmltext = "exchange.htm"
   return htmltext

QUEST       = Quest(4000,qn,"Custom")

for item in NPC:
   QUEST.addStartNpc(item)
   QUEST.addTalkId(item)