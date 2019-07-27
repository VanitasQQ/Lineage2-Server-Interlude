# By Deniska Spectr
import sys
from ru.catssoftware.gameserver                    import SevenSigns
from ru.catssoftware.gameserver.model.quest        import State
from ru.catssoftware.gameserver.model.quest        import QuestState
from ru.catssoftware.gameserver.model.quest.jython import QuestJython as JQuest

qn = "2211_HuntingGroundsTeleport"

GLUDIN_DAWN,GLUDIO_DAWN,DION_DAWN,GIRAN_DAWN,HEINE_DAWN,OREN_DAWN,ADEN_DAWN,\
GLUDIN_DUSK,GLUDIO_DUSK,DION_DUSK,GIRAN_DUSK,HEINE_DUSK,OREN_DUSK,ADEN_DUSK = range(31078,31092)
HW_DAWN,HW_DUSK = range(31168,31170)
GODDARD_DAWN,GODDARD_DUSK,RUNE_DAWN,RUNE_DUSK = range(31692,31696)
SCHUTTGART_DAWN,SCHUTTGART_DUSK = range(31997,31999)

class Quest (JQuest) :

  def __init__(self, id, name, descr): JQuest.__init__(self, id, name, descr)

  def onTalk (Self, npc, player):
    st = player.getQuestState(qn) 
    npcId = npc.getNpcId()
    playerCabal = SevenSigns.getInstance().getPlayerCabal(player)
    playerSeal = SevenSigns.getInstance().getPlayerSeal(player)
    sealOwnerGnosis = SevenSigns.getInstance().getSealOwner(SevenSigns.SEAL_GNOSIS)
    periodValidate = SevenSigns.getInstance().isSealValidationPeriod()

    if playerCabal == SevenSigns.CABAL_NULL :
      if npcId in [GLUDIN_DAWN,GLUDIO_DAWN,DION_DAWN,GIRAN_DAWN,OREN_DAWN,ADEN_DAWN,HEINE_DAWN,HW_DAWN,GODDARD_DAWN,RUNE_DAWN,SCHUTTGART_DAWN] :
        htmltext = "dawn_tele-no.htm"
      else :
        htmltext = "dusk_tele-no.htm"
    elif npcId in [GLUDIN_DAWN,GLUDIN_DUSK] :
      if periodValidate and sealOwnerGnosis and playerSeal == SevenSigns.SEAL_GNOSIS :
        htmltext = "low_gludin.htm"
      else :
        htmltext = "hg_gludin.htm"
    elif npcId in [GLUDIO_DAWN,GLUDIO_DUSK] :
      if periodValidate and sealOwnerGnosis and playerSeal == SevenSigns.SEAL_GNOSIS :
        htmltext = "low_gludio.htm"
      else :
        htmltext = "hg_gludio.htm"
    elif npcId in [DION_DAWN,DION_DUSK] :
      if periodValidate and sealOwnerGnosis and playerSeal == SevenSigns.SEAL_GNOSIS :
        htmltext = "low_dion.htm"
      else :
        htmltext = "hg_dion.htm"
    elif npcId in [GIRAN_DAWN,GIRAN_DUSK] :
      if periodValidate and sealOwnerGnosis and playerSeal == SevenSigns.SEAL_GNOSIS :
        htmltext = "low_giran.htm"
      else :
        htmltext = "hg_giran.htm"
    elif npcId in [OREN_DAWN,OREN_DUSK] :
      if periodValidate and sealOwnerGnosis and playerSeal == SevenSigns.SEAL_GNOSIS :
        htmltext = "low_oren.htm"
      else :
        htmltext = "hg_oren.htm"
    elif npcId in [ADEN_DAWN,ADEN_DUSK] :
      if periodValidate and sealOwnerGnosis and playerSeal == SevenSigns.SEAL_GNOSIS :
        htmltext = "low_aden.htm"
      else :
        htmltext = "hg_aden.htm"
    elif npcId in [HEINE_DAWN,HEINE_DUSK] :
      if periodValidate and sealOwnerGnosis and playerSeal == SevenSigns.SEAL_GNOSIS :
        htmltext = "low_heine.htm"
      else :
        htmltext = "hg_heine.htm"
    elif npcId in [HW_DAWN,HW_DUSK] :
      if periodValidate and sealOwnerGnosis and playerSeal == SevenSigns.SEAL_GNOSIS :
        htmltext = "low_hw.htm"
      else :
        htmltext = "hg_hw.htm"
    elif npcId in [GODDARD_DAWN,GODDARD_DUSK] :
      if periodValidate and sealOwnerGnosis and playerSeal == SevenSigns.SEAL_GNOSIS :
        htmltext = "low_goddard.htm"
      else :
        htmltext = "hg_goddard.htm"
    elif npcId in [RUNE_DAWN,RUNE_DUSK] :
      if periodValidate and sealOwnerGnosis and playerSeal == SevenSigns.SEAL_GNOSIS :
        htmltext = "low_rune.htm"
      else :
        htmltext = "hg_rune.htm"
    elif npcId in [SCHUTTGART_DAWN,SCHUTTGART_DUSK] :
      if periodValidate and sealOwnerGnosis and playerSeal == SevenSigns.SEAL_GNOSIS :
        htmltext = "low_schuttgart.htm"
      else :
        htmltext = "hg_schuttgart.htm"
    else :
      htmltext = "hg_wrong.htm"
    st.exitQuest(1)
    return htmltext

QUEST    = Quest(2211, qn, "Teleports")

for i in range(31078,31092)+range(31168,31170)+range(31692,31696)+range(31997,31999) :
   QUEST.addStartNpc(i)
   QUEST.addTalkId(i)