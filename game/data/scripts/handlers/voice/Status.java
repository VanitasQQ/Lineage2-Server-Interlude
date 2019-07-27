package handlers.voice;

import ru.catssoftware.Config;
import ru.catssoftware.Message;
import ru.catssoftware.gameserver.L2GameServer;
import ru.catssoftware.gameserver.datatables.RecordTable;
import ru.catssoftware.gameserver.handler.IVoicedCommandHandler;
import ru.catssoftware.gameserver.handler.VoicedCommandHandler;
import ru.catssoftware.gameserver.model.L2World;
import ru.catssoftware.gameserver.model.actor.instance.L2PcInstance;
import ru.catssoftware.gameserver.network.serverpackets.NpcHtmlMessage;
import ru.catssoftware.gameserver.util.FloodProtector;
import ru.catssoftware.gameserver.util.FloodProtector.Protected;
import ru.catssoftware.info.Version;

/*
 * @Author: L2CatsSoftware Dev Team
 */

public class Status implements IVoicedCommandHandler
{
	private static final String[] VOICED_COMMANDS =
	{
		"status",
		"premium",
		"readmsg",
		"online",
		//"help",
		"info"
	};
	
	public boolean useVoicedCommand(String command, L2PcInstance activeChar, String target)
	{
		// Check activeChar
		if (activeChar == null)
			return false;

		if (command.equals("online")) {
			int curOnline = L2World.getInstance().getAllPlayers().size();
			int offline = 0;
			for(L2PcInstance pc : L2World.getInstance().getAllPlayers()) {
				if(pc.isOfflineTrade())
					offline++;
			}
			curOnline*=1.5;
			activeChar.sendMessage("Now "+curOnline+" player(s) online");
			activeChar.sendMessage(offline+" player(s) at offline trade");
			return true;
		}
		else if (command.equals("readmsg"))
		{
			activeChar.showUserMessages();
			return true;
		}
		else if (command.equals("status"))
		{
			NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());

			if (!activeChar.isGM() && !FloodProtector.tryPerformAction(activeChar, Protected.HTML_UPDATE))
			{
				html.setFile("data/html/mods/status/status-flood.htm");
				activeChar.sendPacket(html);
				return true;
			}

			// params
			long sUptime, sHour, sMinutes, sSeconds = 0;
			long pUptime, pHour, pMinutes, pSeconds = 0;
			int curOnline = L2World.getInstance().getAllPlayers().size();
			int maxOnline = RecordTable.getInstance().getMaxPlayer();
			String sTime = null;
			String pTime = null;

			// Server uptime start
			sUptime = ((System.currentTimeMillis() - L2GameServer._upTime) / 1000);
			sHour = sUptime / 3600;
			sMinutes = (sUptime - (sHour * 3600)) / 60;
			sSeconds = ((sUptime - (sHour * 3600)) - (sMinutes * 60));
			sTime = (sHour + " ч, " + sMinutes + " мин, " + sSeconds + " сек.");

			// Player uptime start
			pUptime = (activeChar.getUptime() / 1000);
			pHour = pUptime / 3600;
			pMinutes = (pUptime - (pHour * 3600)) / 60;
			pSeconds = ((pUptime - (pHour * 3600)) - (pMinutes * 60));
			pTime = (pHour + " ч, " + pMinutes + " мин, " + pSeconds + " сек.");

			// Build content  for player or GM
			if (activeChar.isGM())
			{
				int offOnline = 0;
				for (L2PcInstance player : L2World.getInstance().getAllPlayers())
				{
					if (player != null && player.isOfflineTrade())
						offOnline++;
				}
				html.setFile("data/html/mods/status/status-gm.htm");
				html.replace("%off-online%", offOnline);
			}
			else
				html.setFile("data/html/mods/status/status.htm");
			// Build static content
			html.replace("%online%", curOnline);
			html.replace("%online-max%", maxOnline);
			html.replace("%sUpTime%", sTime);
			html.replace("%pUpTime%", pTime);
			html.replace("%gsRev%", Version.Version);
			html.replace("%gsDate%", "");

			// Send HTML packet
			activeChar.sendPacket(html);
			return true;
		}
		else if (command.equals("premium"))
		{
			if (activeChar.getPremiumService() > 0)
				activeChar.showPremiumState(true);
			else
				activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_NO_PREMIUM));
			return true;
		}
		/*else if (command.startsWith("help"))
		{
			NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
			html.setFile("data/html/help.htm");
			activeChar.sendPacket(html);
		}*/
		else if (command.startsWith("info"))
		{
			if (Config.ALLOW_READ_RULES)
			{
				NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
				html.setFile("data/html/info.htm");
				html.replace("%name%", activeChar.getName());
				activeChar.sendPacket(html);
			}
			else
				activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_FORBIDEN_BY_ADMIN));
		}
		return false;
	}

	public String getDescription(String command)
	{
		if(command.equals("readmsg"))
			return "Показывает сообщение сервера.";
		if(command.equals("status"))
			return "показывает подробный статус сервера.";
		if(command.equals("premium"))
			return "Выводит состояние премиум акаунта.";
		return null;
	}

	public String[] getVoicedCommandList()
	{
		return VOICED_COMMANDS;
	}
	public static void main(String [] args) {
		VoicedCommandHandler.getInstance().registerVoicedCommandHandler(new Status());
	}
	
}