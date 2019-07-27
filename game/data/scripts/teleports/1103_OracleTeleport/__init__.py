# Originally Created by Ham Wong on 2007.03.07
# updated by Kerberos on 2008.01.13
# fixed by Emperorc on 2008.02.28
import sys
from ru.catssoftware.gameserver.model.quest          import State
from ru.catssoftware.gameserver.model.quest          import QuestState
from ru.catssoftware.gameserver.model.quest.jython   import QuestJython as JQuest
from ru.catssoftware.gameserver.network              import SystemMessageId

qn = "1103_OracleTeleport"

TOWN_DAWN = [31078,31079,31080,31081,31083,31084,31082,31692,31694,31997,31168]
TOWN_DUSK = [31085,31086,31087,31088,31090,31091,31089,31693,31695,31998,31169]
TEMPLE_PRIEST = [31127,31128,31129,31130,31131,31137,31138,31139,31140,31141]
RIFT_POSTERS = range(31488,31494)

TELEPORTERS = {
# Dawn
31078:0,31079:1,31080:2,31081:3,31082:4,31083:5,31084:6,31692:7,31694:8,31997:9,31168:10,
# Dusk
31085:11,31086:12,31087:13,31088:14,31089:15,31090:16,31091:17,31693:18,31695:19,31998:20,31169:21,
# Catacombs and Necropolis
31494:22,31495:23,31496:24,31497:25,31498:26,31499:27,31500:28,31501:29,31502:30,31503:31,31504:32,31505:33,31506:34,31507:35,
# Ziggurats
31095:36,31096:37,31097:38,31098:39,31099:40,31100:41,31101:42,31102:43,31103:44,31104:45,31105:46,31106:47,31107:48,31108:49,31109:50,31110:51,31114:52,31115:53,31116:54,31117:55,31118:56,31119:57,31120:58,31121:59,31122:60,31123:61,31124:62,31125:63
}

RETURN_LOCS = [[-80555,150337,-3040],[-13953,121404,-2984],[16354,142820,-2696],[83369,149253,-3400], \
              [111386,220858,-3544],[83106,53965,-1488],[146983,26595,-2200],[148256,-55454,-2779], \
              [45664,-50318,-800],[86795,-143078,-1341],[115136,74717,-2608],[-82368,151568,-3120], \
              [-14748,123995,-3112],[18482,144576,-3056],[81623,148556,-3464],[112486,220123,-3592], \
              [82819,54607,-1520],[147570,28877,-2264],[149888,-56574,-2979],[44528,-48370,-800], \
              [85129,-142103,-1542],[116642,77510,-2688],[-41572,209731,-5087],[-52872,-250283,-7908], \
              [45256,123906,-5411],[46192,170290,-4981],[111273,174015,-5437],[-20604,-250789,-8165], \
              [-21726, 77385,-5171],[140405, 79679,-5427],[-52366, 79097,-4741],[118311,132797,-4829], \
              [172185,-17602,-4901],[ 83000,209213,-5439],[-19500, 13508,-4901],[12525, -248496,-9580], \
              [-415611,209225,-5087],[45242,124466,-5413],[110711,174010,-5439],[-22341,77375,-5173], \
              [-52889,79098,-4741],[117760,132794,-4831],[171792,-17609,-4901],[82564,209207,-5439], \
              [-41565,210048,-5085],[45278,123608,-5411],[111510,174013,-5437],[-21489,77372,-5171], \
              [-52016,79103,-4739],[118557,132804,-4829],[172570,-17605,-4899],[83347,209215,-5437], \
              [42495,143944,-5381],[45666,170300,-4981],[77138,78389,-5125],[139903,79674,-5429], \
              [-20021,13499,-4901],[113418,84535,-6541],[-52940,-250272,-7907],[46499,170301,-4979], \
              [-20280,-250785,-8163],[140673,79680,-5437],[-19182,13503,-4899],[12837,-248483,-9579]]

class Quest (JQuest) :

 def __init__(self, id, name, descr): JQuest.__init__(self, id, name, descr)

 def onAdvEvent (self,event,npc,player):
    st = player.getQuestState(qn)
    if not st: 
       st = self.newQuestState(player)
    npcId = npc.getNpcId()
    htmltext = event
    if event == "Return" :
       if npcId in TEMPLE_PRIEST :
          x,y,z = RETURN_LOCS[st.getInt("id")]
          player.teleToLocation(x,y,z)
          player.setIsIn7sDungeon(False)
          st.exitQuest(1)
          return
       elif npcId in RIFT_POSTERS :
          x,y,z = RETURN_LOCS[st.getInt("id")]
          player.teleToLocation(x,y,z)
          htmltext = "rift_back.htm"
          st.exitQuest(1)
       else: 	
          x,y,z = RETURN_LOCS[1]
          player.teleToLocation(x,y,z)
          player.setIsIn7sDungeon(False)
          st.exitQuest(1)
          return
    elif event == "Festival" :
       id = st.getInt("id")
       if id in TOWN_DAWN:
          player.teleToLocation(-80157,111344,-4901)
          player.setIsIn7sDungeon(True)
          return
       elif id in TOWN_DUSK:
          player.teleToLocation(-81261,86531,-5157)
          player.setIsIn7sDungeon(True)
          return
       else :
          htmltext = "oracle1.htm"
    elif event == "Dimensional" :
       htmltext = "oracle.htm"
       player.teleToLocation(-114755,-179466,-6752)
    elif event == "5.htm" :
       id = st.getInt("id")
       if id:
          htmltext="5a.htm"
       st.set("id",str(TELEPORTERS[npcId]))
       st.setState(State.STARTED)
       player.teleToLocation(-114755,-179466,-6752)
    elif event == "6.htm" :
       st.exitQuest(1)
    elif event == "zigurratDimensional" :
       playerLevel = player.getLevel()
       if playerLevel >= 20 and playerLevel < 30 :
          st.takeItems(57,2000)
       elif playerLevel >= 30 and playerLevel < 40 :
          st.takeItems(57,4500)
       elif playerLevel >= 40 and playerLevel < 50 :
          st.takeItems(57,8000)
       elif playerLevel >= 50 and playerLevel < 60 :
          st.takeItems(57,12500)
       elif playerLevel >= 60 and playerLevel < 70 :
          st.takeItems(57,18000)
       elif playerLevel >= 70 :
          st.takeItems(57,24500)
       st.set("id",str(TELEPORTERS[npcId]))
       st.setState(State.STARTED)
       st.playSound("ItemSound.quest_accept")
       htmltext = "ziggurat_rift.htm"
       player.teleToLocation(-114755,-179466,-6752)
    return htmltext

 def onTalk (Self, npc, player):
    st = player.getQuestState(qn)
    if not st: return
    npcId = npc.getNpcId()
    htmltext = None
    ##################
    # Dawn Locations #
    ##################
    if npcId in TOWN_DAWN: 
       st.setState(State.STARTED)
       st.set("id",str(TELEPORTERS[npcId]))
       st.playSound("ItemSound.quest_accept")
       player.teleToLocation(-80157,111344,-4901)
       player.setIsIn7sDungeon(True)
    ##################
    # Dusk Locations #
    ##################
    elif npcId in TOWN_DUSK: 
       st.setState(State.STARTED)
       st.set("id",str(TELEPORTERS[npcId]))
       st.playSound("ItemSound.quest_accept")
       player.teleToLocation(-81261,86531,-5157)
       player.setIsIn7sDungeon(True)
    elif npcId in range(31494,31508):
       if player.getLevel() < 20 :
          st.exitQuest(1)
          htmltext="1.htm"
       elif len(player.getAllActiveQuests()) > 23 :
          st.exitQuest(1)
          htmltext="1a.htm"
       elif not st.getQuestItemsCount(7079) :
          htmltext="3.htm"
       else :
          st.setState(State.CREATED)
          htmltext="4.htm"
    elif npcId in range(31095,31111)+range(31114,31126) :
       playerLevel = player.getLevel()
       if playerLevel < 20 :
          st.exitQuest(1)
          htmltext="ziggurat_lowlevel.htm"
       elif len(player.getAllActiveQuests()) > 23 :
          htmltext=""
          player.sendPacket(SystemMessageId.TOO_MANY_QUESTS)
          st.exitQuest(1)
       elif not st.getQuestItemsCount(7079) :
          htmltext="ziggurat_nofrag.htm"
          st.exitQuest(1)
       elif playerLevel >= 20 and playerLevel < 30 and st.getQuestItemsCount(57) < 2000 :
          htmltext="ziggurat_noadena.htm"
          st.exitQuest(1)
       elif playerLevel >= 30 and playerLevel < 40 and st.getQuestItemsCount(57) < 4500 :
          htmltext="ziggurat_noadena.htm"
          st.exitQuest(1)
       elif playerLevel >= 40 and playerLevel < 50 and st.getQuestItemsCount(57) < 8000 :
          htmltext="ziggurat_noadena.htm"
          st.exitQuest(1)
       elif playerLevel >= 50 and playerLevel < 60 and st.getQuestItemsCount(57) < 12500 :
          htmltext="ziggurat_noadena.htm"
          st.exitQuest(1)
       elif playerLevel >= 60 and playerLevel < 70 and st.getQuestItemsCount(57) < 18000 :
          htmltext="ziggurat_noadena.htm"
          st.exitQuest(1)
       elif playerLevel >= 70 and st.getQuestItemsCount(57) < 24500 :
          htmltext="ziggurat_noadena.htm"
          st.exitQuest(1)
       else :
          htmltext="ziggurat.htm"
    return htmltext

QUEST      = Quest(1103, qn, "Teleports")

for i in TELEPORTERS.keys() + TEMPLE_PRIEST + range(31494,31508)+range(31095,31111)+range(31114,31126):
    QUEST.addStartNpc(i)
    QUEST.addTalkId(i)

for l in RIFT_POSTERS:
    QUEST.addStartNpc(l)
    QUEST.addTalkId(l)