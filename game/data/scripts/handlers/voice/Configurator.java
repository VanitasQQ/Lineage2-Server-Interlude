package handlers.voice;

import ru.catssoftware.Config;
import ru.catssoftware.Message;
import ru.catssoftware.gameserver.handler.IVoicedCommandHandler;
import ru.catssoftware.gameserver.handler.VoicedCommandHandler;
import ru.catssoftware.gameserver.model.actor.instance.L2PcInstance;
import ru.catssoftware.gameserver.model.entity.events.CTF.CTF;
import ru.catssoftware.gameserver.model.entity.events.DeathMatch.DeathMatch;
import ru.catssoftware.gameserver.model.entity.events.LastHero.LastHero;
import ru.catssoftware.gameserver.model.entity.events.TvT.TvT;
import ru.catssoftware.gameserver.model.zone.L2Zone;
import ru.catssoftware.gameserver.network.serverpackets.NpcHtmlMessage;


 /**
  * Author: m095
  * Хандлер команд для конфигурации персонажа
  * EmuRT DevTeam
  **/

public class Configurator implements IVoicedCommandHandler
{
	private static final String[] VOICED_COMMANDS =
	{
		"menu",
		"events",
		"autoloot",
		"enableTrade",
		"disableTrade",
		"enableOffKnow",
		"disableOffKnow",
		"enableAutoloot",
		"disableAutoloot",
		"enableMessage",
		"showSkillSuccess",
		"disableMessage",
		"enableBuffAnim",
		"disableBuffAnim",
		"enableGainExp",
		"disableGainExp",
		"ignorecolors"
	};
	
	public boolean useVoicedCommand(String command, L2PcInstance activeChar, String target)
	{
		if (activeChar.isInOlympiadMode() || activeChar.isInFunEvent() || activeChar.isInCombat())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_NOT_ALLOWED_AT_THE_MOMENT));
			return true;
		}

		if (command.startsWith("menu"))
		{
			showMainPage(activeChar);
			return true;
		}
		else if (command.startsWith("events"))
		{
			showEventPage(activeChar);
			return true;
		}
		else if (command.startsWith("showSkillSuccess")) {
			if(!Config.SHOW_SKILL_SUCCESS_CHANCE)
				activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_FORBIDEN_BY_ADMIN));
			else
				activeChar.setShowSkillChance(!activeChar.isShowSkillChance());
			showMainPage(activeChar);
			return true;
		}
		else if(command.equals("ignorecolors")) {
			boolean val = true;
			try {
				val = !activeChar.getCharacterData().getBool("ignorecolors");
				activeChar.getCharacterData().set("ignorecolors",val);
			} catch(Exception e) {
				activeChar.getCharacterData().set("ignorecolors",val);
			}
			activeChar.sendMessage("Ignoring system colors "+(val?"endbled":"disabled"));
			
		}
		else if (command.startsWith("autoloot"))
		{
			if (!Config.ALLOW_AUTO_LOOT)
			{
				activeChar.notWorking(false);
				return true;
			}

			if (activeChar.isAutoLootEnabled())
			{
				activeChar.enableAutoLoot(false);
				activeChar.sendMessage("AutoLoot is off.");
			}
			else
			{
				activeChar.enableAutoLoot(true);
				activeChar.sendMessage("AutoLoot is on");
			}
		}
		else if (command.startsWith("enableTrade"))
		{
			activeChar.setTradeRefusal(false);
			showMainPage(activeChar);
			return true;
		}
		else if (command.startsWith("disableTrade"))
		{
			activeChar.setTradeRefusal(true);
			showMainPage(activeChar);
			return true;
		}
		else if (command.startsWith("enableOffKnow"))
		{
			if (!activeChar.isInsideZone(L2Zone.FLAG_PEACE))
			{
				activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_ONLY_IN_PEACE_ZONE));
				showMainPage(activeChar);
				return true;
			}
			activeChar.setKnowlistMode(true);
			showMainPage(activeChar);
			return true;
		}
		else if (command.startsWith("disableOffKnow"))
		{
			if (!activeChar.isInsideZone(L2Zone.FLAG_PEACE))
			{
				activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_ONLY_IN_PEACE_ZONE));
				showMainPage(activeChar);
				return true;
			}
			activeChar.setKnowlistMode(false);
			showMainPage(activeChar);
			return true;
		}
		else if (command.startsWith("enableAutoloot"))
		{
			if (Config.ALLOW_AUTO_LOOT)
				activeChar.enableAutoLoot(true);
			else
				activeChar.notWorking(false);
			showMainPage(activeChar);
			return true;
		}
		else if (command.startsWith("disableAutoloot"))
		{
			if (Config.ALLOW_AUTO_LOOT)
				activeChar.enableAutoLoot(false);
			else
				activeChar.notWorking(false);
			showMainPage(activeChar);
			return true;
		}
		else if (command.startsWith("enableGainExp"))
		{
			if (Config.ALLOW_USE_EXP_SET)
				activeChar.canGainExp(true);
			else
				activeChar.notWorking(false);
			showMainPage(activeChar);
			return true;
		}
		else if (command.startsWith("disableGainExp"))
		{
			if (Config.ALLOW_USE_EXP_SET)
				activeChar.canGainExp(false);
			else
				activeChar.notWorking(false);
			showMainPage(activeChar);
			return true;
		}
		else if (command.startsWith("enableMessage"))
		{
			activeChar.setMessageRefusal(false);
			showMainPage(activeChar);
			return true;
		}
		else if (command.startsWith("disableMessage"))
		{
			activeChar.setMessageRefusal(true);
			showMainPage(activeChar);
			return true;
		}
		else if (command.startsWith("enableBuffAnim"))
		{
			activeChar.setShowBuffAnim(true);
			showMainPage(activeChar);
			return true;
		}
		else if (command.startsWith("disableBuffAnim"))
		{
			activeChar.setShowBuffAnim(false);
			showMainPage(activeChar);
			return true;
		}
		return false;
	}

	private String getGainExpMode(L2PcInstance activeChar)
	{
		String result = "ON";
		if (activeChar.canGainExp())
			result = "OFF";
		return result;
	}
	
	private String getBuffAnimMode(L2PcInstance activeChar)
	{
		String result = "OFF";
		if (activeChar.ShowBuffAnim())
			result = "ON";
		return result;
	}

	private String getKnowListMode(L2PcInstance activeChar)
	{
		String result = "ON";
		if (activeChar.showTraders())
			result = "OFF";
		return result;
	}

	private String getTradeMode(L2PcInstance activeChar)
	{
		String result = "OFF";
		if (activeChar.getTradeRefusal())
			result = "ON";
		return result;
	}

	private String getMessageMode(L2PcInstance activeChar)
	{
		String result = "OFF";
		if (activeChar.getMessageRefusal())
			result = "ON";
		return result;
	}

	private String getLootMode(L2PcInstance activeChar)
	{
		String result = "OFF";
		if (activeChar.isAutoLootEnabled())
			result = "ON";
		return result;
	}
	
	private void showMainPage(L2PcInstance activeChar)
	{
		if(!Config.ALLOW_MENU)
			return;
		NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
		html.setFile("data/html/menu.htm");
		html.replace("%notraders%", getKnowListMode(activeChar));
		html.replace("%notrade%", getTradeMode(activeChar));
		html.replace("%autoloot%", getLootMode(activeChar));
		html.replace("%nomsg%", getMessageMode(activeChar));
		html.replace("%buffanim%", getBuffAnimMode(activeChar));
		html.replace("%gainexp%", getGainExpMode(activeChar));
		html.replace("%skillchance%",activeChar.isShowSkillChance()?"ON":"OFF");
		activeChar.sendPacket(html);	
	}

	private void showEventPage(L2PcInstance activeChar)
	{
		NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
		html.setFile("data/html/mods/event_npc.htm");
		html.replace("%tvt_state%", getEventStatus(0));
		html.replace("%ctf_state%", getEventStatus(1));
		html.replace("%lh_state%", getEventStatus(2));
		html.replace("%dm_state%", getEventStatus(2));
		activeChar.sendPacket(html);
	}
	
	private String getEventStatus(int event)
	{
		String result = "unknown";
		int state = 0;
		try {
		switch (event)
		{
			case 0:
				state = TvT.getInstance().getState();
				break;
			case 1:
				state = CTF.getInstance().getState();
				break;
			case 2:
				state = LastHero.getInstance().getState();
				break;
			case 3:
				state = DeathMatch.getInstance().getState();
				break;
		}
		
		switch (state)
		{
			case 0:
				result = "Inactive";
				break;
			case 1:
				result = "Active";
				break;
			case 2:
				result = "Running";
				break;
		}
		} catch(Exception e) { }
		return result;
	}

	public String getDescription(String command)
	{
		if(command.equals("menu"))
			return "Выводит меню команд.";
		return "Подробно в .menu";
	}

	public String[] getVoicedCommandList()
	{
		return VOICED_COMMANDS;
	}
	public static void main(String [] args) {
		VoicedCommandHandler.getInstance().registerVoicedCommandHandler(new Configurator());
	}

}