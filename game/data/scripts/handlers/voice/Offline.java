package handlers.voice;

import ru.catssoftware.Config;
import ru.catssoftware.Message;
import ru.catssoftware.gameserver.handler.IVoicedCommandHandler;
import ru.catssoftware.gameserver.handler.VoicedCommandHandler;
import ru.catssoftware.gameserver.model.actor.instance.L2PcInstance;
import ru.catssoftware.gameserver.network.SystemMessageId;

/**
 * Автор: L2CatsSoftware
 * Хандлер для включения offline режима
 **/

public class Offline implements IVoicedCommandHandler
{
	private static final String[]	VOICED_COMMANDS	=
	{
		"offline"
	};

	public boolean useVoicedCommand(String command, L2PcInstance activeChar, String target)
	{
		if (activeChar == null)
			return false;

		if (command.startsWith("offline"))
		{
			int StoreType = activeChar.getPrivateStoreType();

			if ((StoreType == L2PcInstance.STORE_PRIVATE_BUY || StoreType == L2PcInstance.STORE_PRIVATE_SELL || StoreType == L2PcInstance.STORE_PRIVATE_PACKAGE_SELL || StoreType == L2PcInstance.STORE_PRIVATE_MANUFACTURE))
			{
				{
					int _itemId = Config.OFFLINE_TRADE_PRICE_ITEM_ID;
					int _count = Config.OFFLINE_TRADE_PRICE_COUNT;

					if (_count > 0)
					{
						if (cantEnable(activeChar))
						{
							activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_NOT_ACCESSABLE));
							return false;
						}
						else if (activeChar.getInventory().getInventoryItemCount(_itemId, -1) < _count)
						{
							activeChar.sendPacket(SystemMessageId.NOT_ENOUGH_ITEMS);
							return false;
						}
						else
						{
							activeChar.destroyItemByItemId("OfflinePrice", _itemId, _count, activeChar, true);
							return activeChar.doOffline();
						}
					}
					else
					{
						if (cantEnable(activeChar))
						{
							activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_NOT_ACCESSABLE));
							return false;
						}
						else
							return activeChar.doOffline();
					}
				}
			}
			else if (StoreType == 5 && Config.ALLOW_OFFLINE_TRADE_CRAFT)
			{
				int _itemId = Config.OFFLINE_CRAFT_PRICE_ITEM_ID;
				int _count = Config.OFFLINE_CRAFT_PRICE_COUNT;
				if (_count > 0)
				{
					if (cantEnable(activeChar))
					{
						activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_NOT_ACCESSABLE));
						return false;
					}
					else if (activeChar.getInventory().getInventoryItemCount(_itemId, -1) < _count)
					{
						activeChar.sendPacket(SystemMessageId.NOT_ENOUGH_ITEMS);
						return false;
					}
					else
					{
						activeChar.destroyItemByItemId("OfflinePrice", _itemId, _count, activeChar, true);
						return activeChar.doOffline();
					}
				}
				else
				{
					if (cantEnable(activeChar))
					{
						activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_NOT_ACCESSABLE));
						return false;
					}
					else
						return activeChar.doOffline();
				}				
			}
			else
			{
				activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_SERVICE_NEED_TO_ACTIVE));
				activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_OFFLINE_TRADE_NEED));
				if (Config.ALLOW_OFFLINE_TRADE_CRAFT)
					activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_OFFLINE_CRAFT_NEED));		
				return false;
			}
		}
		return false;
	}

	public boolean cantEnable(L2PcInstance activeChar)
	{
		if (activeChar.getActiveEnchantItem() != null)
			return true;
		if (activeChar.getPrivateStoreType() != 5 && !activeChar.inTradeZone())
			return true;
		return false;
	}

	public String getDescription(String command)
	{
		if(command.equals("offline"))
			return "Включает режим офлайн торговли.";
		return null;
	}

	public String[] getVoicedCommandList()
	{
		return VOICED_COMMANDS;
	}
	public static void main(String [] args) {
		if (Config.ALLOW_OFFLINE_TRADE)
			VoicedCommandHandler.getInstance().registerVoicedCommandHandler(new Offline());
	}
}
