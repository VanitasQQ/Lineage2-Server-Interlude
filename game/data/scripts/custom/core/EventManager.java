package custom.core;

import ru.catssoftware.Config;
import ru.catssoftware.Message;
import ru.catssoftware.gameserver.cache.HtmCache;
import ru.catssoftware.gameserver.datatables.NpcTable;
import ru.catssoftware.gameserver.datatables.SpawnTable;
import ru.catssoftware.gameserver.handler.IVoicedCommandHandler;
import ru.catssoftware.gameserver.handler.VoicedCommandHandler;
import ru.catssoftware.gameserver.model.L2Spawn;
import ru.catssoftware.gameserver.model.actor.instance.L2NpcInstance;
import ru.catssoftware.gameserver.model.actor.instance.L2PcInstance;
import ru.catssoftware.gameserver.model.entity.events.CTF.CTF;
import ru.catssoftware.gameserver.model.entity.events.DeathMatch.DeathMatch;
import ru.catssoftware.gameserver.model.entity.events.LastHero.LastHero;
import ru.catssoftware.gameserver.model.entity.events.TvT.TvT;
import ru.catssoftware.gameserver.model.quest.Quest;
import ru.catssoftware.gameserver.model.quest.QuestState;
import ru.catssoftware.gameserver.network.serverpackets.NpcHtmlMessage;
import ru.catssoftware.gameserver.templates.chars.L2NpcTemplate;


public class EventManager extends Quest
{
	private static String		qn						= "EventManager";
	private static int[]		_locX					= {147390, 147688, 83674,82672, 111392, -13432, 87705, 11744};
	private static int[]		_locY					= {-55816, 27350, 148867, 54132, 219620, 122061, -142910, 182803};
	private static int[]		_locZ					= {-2761, -2204, -3408, -1499, -3680, -2992, -1317, -3565};
	private static int[]		_heading				= {45183, 48573, 32136, 47827, 12160, 14433, 12493, 5546};

	public EventManager()
	{
		super(-1, qn, "custom");

		int _npcId = Config.EVENT_MANAGER_ID ;
		addStartNpc(_npcId);
		addFirstTalkId(_npcId);
		addTalkId(_npcId);

		if (Config.SPAWN_EVENT_MANAGER)
		{
			_log.info("Spawn Game event manager");
			spawnNpc(_npcId, _locX[0], _locY[0], _locZ[0], _heading[0]);
			spawnNpc(_npcId, _locX[1], _locY[1], _locZ[1], _heading[1]);
			spawnNpc(_npcId, _locX[2], _locY[2], _locZ[2], _heading[2]);
			spawnNpc(_npcId, _locX[3], _locY[3], _locZ[3], _heading[3]);
			spawnNpc(_npcId, _locX[4], _locY[4], _locZ[4], _heading[4]);
			spawnNpc(_npcId, _locX[5], _locY[5], _locZ[5], _heading[5]);
			spawnNpc(_npcId, _locX[6], _locY[6], _locZ[6], _heading[6]);
			spawnNpc(_npcId, _locX[7], _locY[7], _locZ[7], _heading[7]);
		}
	}

	@Override
	public String onFirstTalk(L2NpcInstance npc, L2PcInstance player)
	{
		return onTalk(npc,player);
	}
	
	@Override
	public String onTalk(L2NpcInstance npc, L2PcInstance talker)
	{
		if (talker.getQuestState(qn)==null)
			newQuestState(talker);

		return HtmCache.getInstance().getHtm("data/html/mods/events/main.htm",talker);
	}
	
	@Override
	public String onEvent(String event, QuestState qs)
	{
		L2PcInstance player = qs.getPlayer();
		if (player == null)
			return null;
		String []commands = event.split(" ");
		if(commands[0].startsWith("MAIN"))
		{
			TOP(player);
			return null;
		}
		else if(commands[0].startsWith("TVT"))
		{
			String command = event.substring(4);
			if (command.startsWith("Top"))
			{
				TvT(player);
				return null;
			}
			else if (command.startsWith("Reg"))
			{
				useVC(player, "tvtjoin");
				TvT(player);
				return null;
			}
			else if (command.startsWith("Exit"))
			{
				useVC(player, "tvtleave");
				TvT(player);
				return null;
			}
		}
		else if(commands[0].startsWith("CTF"))
		{
			String command = event.substring(4);
			if (command.startsWith("Top"))
			{
				CTF(player);
				return null;
			}
			else if (command.startsWith("Reg"))
			{
				useVC(player, "ctfjoin");
				CTF(player);
				return null;
			}
			else if (command.startsWith("Exit"))
			{
				useVC(player, "ctfleave");
				CTF(player);
				return null;
			}
		}
		else if(commands[0].startsWith("LASTHERO"))
		{
			
			if (commands[1].startsWith("Top"))
			{
				LastHero(player);
				return null;
			}
			else if (commands[1].startsWith("Reg"))
			{
				useVC(player, "lhjoin");
				LastHero(player);
				return null;
			}
			else if (commands[1].startsWith("Exit"))
			{
				useVC(player, "lhleave");
				LastHero(player);
				return null;
			}
		}
		else if(commands[0].startsWith("DM"))
		{
			String command = event.substring(3);
			if (command.startsWith("Top"))
			{
				DeathMatch(player);
				return null;
			}
			else if (command.startsWith("Reg"))
			{
				useVC(player, "dmjoin");
				DeathMatch(player);
				return null;
			}
			else if (command.startsWith("Exit"))
			{
				useVC(player, "dmleave");
				DeathMatch(player);
				return null;
			}
		}
		return null;
	}

	private void TOP(L2PcInstance activeChar)
	{
		NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
		html.setFile("data/html/mods/events/main.htm");
		activeChar.sendPacket(html);
	}

	private void TvT(L2PcInstance activeChar)
	{
		NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
		html.setFile("data/html/mods/events/tvt.htm");
		html.replace("%state%", getEventStatus(0));
		html.replace("%free%", TvT.getInstance().getStatus());
		activeChar.sendPacket(html);
	}
	
	private void CTF(L2PcInstance activeChar)
	{
		NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
		html.setFile("data/html/mods/events/ctf.htm");
		html.replace("%state%", getEventStatus(1));
		html.replace("%free%", CTF.getInstance().getStatus());
		activeChar.sendPacket(html);
	}
	
	private void LastHero(L2PcInstance activeChar)
	{
		NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
		html.setFile("data/html/mods/events/lasthero.htm");
		html.replace("%state%", getEventStatus(2));
		html.replace("%free%", LastHero.getInstance().getStatus());
		activeChar.sendPacket(html);
	}
	
	private void DeathMatch(L2PcInstance activeChar)
	{
		NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
		html.setFile("data/html/mods/events/deathmatch.htm");
		html.replace("%state%", getEventStatus(3));
		html.replace("%free%", DeathMatch.getInstance().getStatus());
		activeChar.sendPacket(html);
	}

	private void useVC(L2PcInstance activeChar, String name)
	{
		IVoicedCommandHandler vc = VoicedCommandHandler.getInstance().getVoicedCommandHandler(name);
		if (vc == null)
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_COMMAND_IS_NULL));
			return;
		}
		vc.useVoicedCommand(name, activeChar, "");
	}

	private void spawnNpc(int npcId, int x, int y, int z, int h)
	{
		L2NpcTemplate template = NpcTable.getInstance().getTemplate(npcId);
		try
		{
			L2Spawn spawn;
			spawn = new L2Spawn(template);
			spawn.setLocx(x);
			spawn.setLocy(y);
			spawn.setLocz(z);
			spawn.setAmount(1);
			spawn.setHeading(h);
			spawn.setRespawnDelay(60);
			SpawnTable.getInstance().addNewSpawn(spawn, false);
			spawn.init();
		}
		catch (Exception e)
		{
			_log.error("QuestEngine: Error on spawn NPC: " + e.getMessage());
		}
	}
	
	private String getEventStatus(int event)
	{
		String result = "unknown";
		int state = 0;

		switch (event)
		{
			case 0:
				if(TvT.getInstance()!=null)
					state = TvT.getInstance().getState();
				break;
			case 1:
				if(CTF.getInstance()!=null)
					state = CTF.getInstance().getState();
				break;
			case 2:
				if(LastHero.getInstance()!=null)
					state = LastHero.getInstance().getState();
				break;
			case 3:
				if(DeathMatch.getInstance()!=null)
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
		return result;
	}
	
	public static void main(String [] args) {
		if (Config.ENABLE_EVENT_MANAGER)
			new EventManager();
	}
}
