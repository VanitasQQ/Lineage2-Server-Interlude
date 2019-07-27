package handlers.voice;

import ru.catssoftware.Config;
import ru.catssoftware.gameserver.handler.IVoicedCommandHandler;
import ru.catssoftware.gameserver.handler.VoicedCommandHandler;
import ru.catssoftware.gameserver.instancemanager.AwayManager;
import ru.catssoftware.gameserver.instancemanager.SiegeManager;
import ru.catssoftware.gameserver.model.actor.instance.L2PcInstance;
import ru.catssoftware.gameserver.model.entity.Siege;
import ru.catssoftware.gameserver.model.zone.L2Zone;
import ru.catssoftware.gameserver.network.serverpackets.NpcHtmlMessage;

/*
 * @Author: L2CatsSoftware Dev Team 
 */

public class Away implements IVoicedCommandHandler
{
	private static final String[]	VOICED_COMMANDS	=
	{
		"away"
	};

	public boolean useVoicedCommand(String command, L2PcInstance activeChar, String text)
	{
		if (command.startsWith("away"))
		{
			if (!activeChar.isAway())
				away(activeChar, text);
			else
				back(activeChar);
		}
		return false;
	}

	private void away(L2PcInstance activeChar, String text)
	{
		if (activeChar.isAway())
		{
			NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
			html.setFile("data/html/mods/away/away-enabled.htm");
			activeChar.sendPacket(html);
			return;
		}
		if (!activeChar.isInsideZone(L2Zone.FLAG_PEACE) && Config.ALT_AWAY_PEACE_ZONE)
		{
			NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
			html.setFile("data/html/mods/away/away-peace.htm");
			activeChar.sendPacket(html);
			return;
		}
		if (activeChar.isDead() || activeChar.isAlikeDead() || activeChar.isMovementDisabled())
		{
			NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
			html.setFile("data/html/mods/away/away-dead.htm");
			activeChar.sendPacket(html);
			return;
		}
 		if (activeChar.isInOlympiadMode() || activeChar.isOlympiadStart())
		{
			NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
			html.setFile("data/html/mods/away/away-olympiad.htm");
			activeChar.sendPacket(html);
			return;
		}
		if (activeChar.isInFunEvent())
		{
			NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
			html.setFile("data/html/mods/away/away-events.htm");
			activeChar.sendPacket(html);
			return;
		}
		Siege siege = SiegeManager.getInstance().getSiege(activeChar);
		if (siege != null && siege.getIsInProgress())
		{
			NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
			html.setFile("data/html/mods/away/away-siege.htm");
			activeChar.sendPacket(html);
			return;
		}
		if (activeChar.isInJailMission())
		{
			NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
			html.setFile("data/html/mods/away/away-jail.htm");
			activeChar.sendPacket(html);
			return;
		}
		if (activeChar.isInCombat())
		{
			NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
			html.setFile("data/html/mods/away/away-combat.htm");
			activeChar.sendPacket(html);
			return;
		}
		if (activeChar.getKarma() > 0)
		{
			NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
			html.setFile("data/html/mods/away/away-pk.htm");
			activeChar.sendPacket(html);
			return;
		}
		if (activeChar.isInDuel())
		{
			NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
			html.setFile("data/html/mods/away/away-duel.htm");
			activeChar.sendPacket(html);
			return;
		}
		if (activeChar.isInStoreMode() || activeChar.isInCraftMode())
		{
			NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
			html.setFile("data/html/mods/away/away-store-craft.htm");
			activeChar.sendPacket(html);
			return;
		}
		if (activeChar.isInParty() && activeChar.getParty().isInDimensionalRift())
		{
			NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
			html.setFile("data/html/mods/away/away-dimension.htm");
			activeChar.sendPacket(html);
			return;
		}
		if (activeChar.inObserverMode())
		{
			NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
			html.setFile("data/html/mods/away/away-error.htm");
			activeChar.sendPacket(html);
			return;
		}
		if (activeChar.isImmobilized())
		{
			NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
			html.setFile("data/html/mods/away/away-error.htm");
			activeChar.sendPacket(html);
			return;
		}
 		if (text.length() > 10)
		{
			NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
			html.setFile("data/html/mods/away/away-error.htm");
			activeChar.sendPacket(html);
			return;
		}
		if (activeChar.getTarget() == null && text.length() <= 1 || text.length() <= 10)
			AwayManager.getInstance().setAway(activeChar, text);
	}

	private void back(L2PcInstance activeChar)
	{
		if (!activeChar.isAway())
		{
			NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
			html.setFile("data/html/mods/away/away-noaway.htm");
			activeChar.sendPacket(html);
			return;
		}
		AwayManager.getInstance().setBack(activeChar);
	}

	public String getDescription(String command)
	{
		if(command.equals("away"))
			return "Позволяет отлучится не на долго из игры.";
		return null;
	}

	public String[] getVoicedCommandList()
	{
		return VOICED_COMMANDS;
	}
	public static void main(String [] args) {
		if (Config.ALT_ALLOW_AWAY_STATUS)
			VoicedCommandHandler.getInstance().registerVoicedCommandHandler(new Away());
	}
}