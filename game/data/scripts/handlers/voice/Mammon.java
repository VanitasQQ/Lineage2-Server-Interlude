package handlers.voice;

import ru.catssoftware.Config;
import ru.catssoftware.Message;
import ru.catssoftware.gameserver.SevenSigns;
import ru.catssoftware.gameserver.datatables.SpawnTable;
import ru.catssoftware.gameserver.handler.IVoicedCommandHandler;
import ru.catssoftware.gameserver.handler.VoicedCommandHandler;
import ru.catssoftware.gameserver.instancemanager.TownManager;
import ru.catssoftware.gameserver.model.L2Spawn;
import ru.catssoftware.gameserver.model.actor.instance.L2PcInstance;
import ru.catssoftware.gameserver.model.entity.Town;

 /**
  * @author m095, L2CatsSoftware
  * @version: 2.0
  **/

public class Mammon implements IVoicedCommandHandler
{
	private SpawnTable				spawnTable			= SpawnTable.getInstance();
	private static final String[]	VOICED_COMMANDS		=
	{
		"mammon"
	};

	public boolean useVoicedCommand(String command, L2PcInstance activeChar, String target)
	{
		if (!SevenSigns.getInstance().isSealValidationPeriod())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_MAMMON_SEARCH_OFF));
			return false;
		}

		if(command.startsWith("mammon"))
		{
			findMMammon(activeChar);
			findBMammon(activeChar);
			return true;
		}
		return false;
	}

	/**
	 * Ищем Мамона Торгоша, если есть пишем список локаций
	 **/
	public void findMMammon(L2PcInstance activeChar)
	{
		// Стандартная переменная. Служит для распознования цикла
		int count = 0;

		// Поиск NPC по ID вреди спавнлиста сервера
		for (L2Spawn spawn : spawnTable.getSpawnTable().values())
		{
			if (31113 == spawn.getNpcid())
			{
				Town town = TownManager.getInstance().getClosestTown(spawn.getLocx(), spawn.getLocy(), spawn.getLocz());
				if (town != null)
				{
					activeChar.sendMessage(String.format(Message.getMessage(activeChar, Message.MessageId.MSG_MAMMON_TRADER),TownManager.getInstance().getTownName(town.getTownId())));
					count++;
				}
			}
		}

		if (count <= 0)
			activeChar.sendMessage(String.format(Message.getMessage(activeChar, Message.MessageId.MSG_MAMMON_TRADER),"not found."));
	}

	/**
	 * Ищем Мамона Кузнеца, если есть пишем список локаций
	 **/
	public void findBMammon(L2PcInstance activeChar)
	{
		// Стандартная переменная. Служит для распознования цикла
		int count = 0;

		// Поиск NPC по ID вреди спавнлиста сервера
		for (L2Spawn spawn : spawnTable.getSpawnTable().values())
		{
			if (31126 == spawn.getNpcid())
			{
				Town town = TownManager.getInstance().getClosestTown(spawn.getLocx(), spawn.getLocy(), spawn.getLocz());
				if (town != null)
				{
					activeChar.sendMessage(String.format(Message.getMessage(activeChar, Message.MessageId.MSG_MAMMON_BLACKSMITH),TownManager.getInstance().getTownName(town.getTownId())));
					count++;
				}
			}
		}

		if (count <= 0)
			activeChar.sendMessage(String.format(Message.getMessage(activeChar, Message.MessageId.MSG_MAMMON_BLACKSMITH),"not found."));
	}

	public String getDescription(String command)
	{
		if(command.equals("mammon"))
			return "Сообщает текущее местонахождение торговца и кузнеца мамона.";
		return null;
	}

	/**
	 * Возвращаем список команд
	 * Служит для получения списка зарегестрированых комманд
	 **/
	public String[] getVoicedCommandList()
	{
		return VOICED_COMMANDS;
	}
	public static void main(String [] args) {
		if (Config.ALLOW_MAMMON_SEARCH)
			VoicedCommandHandler.getInstance().registerVoicedCommandHandler(new Mammon());
	}

}