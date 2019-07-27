package handlers.voice;

import ru.catssoftware.Config;
import ru.catssoftware.gameserver.datatables.ItemTable;
import ru.catssoftware.gameserver.handler.IVoicedCommandHandler;
import ru.catssoftware.gameserver.handler.VoicedCommandHandler;
import ru.catssoftware.gameserver.model.L2ItemInstance;
import ru.catssoftware.gameserver.model.actor.instance.L2PcInstance;
import ru.catssoftware.gameserver.templates.item.L2Item;

public class Bank implements IVoicedCommandHandler {

	@Override
	public String getDescription(String command) {
		L2Item item = ItemTable.getInstance().getTemplate(Config.BANKING_GOLDBAR_ID);
		return "Обмен адены на "+item.getName()+" и обратно";
	}

	@Override
	public String[] getVoicedCommandList() {
		return new String [] {"bank"};
	}

	@Override
	public boolean useVoicedCommand(String command, L2PcInstance activeChar,
			String target) {
		if(!Config.BANKING_ENABLED)
			return false;
		if(target == null || target.length()==0) {
			showHelp(activeChar);
		} else  {
			if(target.equals("deposit")) {
				if(activeChar.getAdena()>=Config.BANKING_GOLDBAR_PRICE) {
					activeChar.reduceAdena("banking", Config.BANKING_GOLDBAR_PRICE, null, true);
					activeChar.addItem("banking", Config.BANKING_GOLDBAR_ID, 1, null, true);
				} else 
					showHelp(activeChar);
			} 
			else if(target.equals("widraw")) {
				L2ItemInstance item = activeChar.getInventory().getItemByItemId(Config.BANKING_GOLDBAR_ID);
				if(item!=null && activeChar.getAdena()+Config.BANKING_GOLDBAR_PRICE < Integer.MAX_VALUE) {
					activeChar.destroyItemByItemId("banking", Config.BANKING_GOLDBAR_ID, 1, null, true);
					activeChar.addAdena("banking", Config.BANKING_GOLDBAR_PRICE, null, true);
				} else
					showHelp(activeChar);
			}
			else 
				showHelp(activeChar);
		}
		return false;
	}
	private void showHelp(L2PcInstance cha) {
		L2Item item = ItemTable.getInstance().getTemplate(Config.BANKING_GOLDBAR_ID);
		cha.sendMessage("Обмен адены на "+item.getName()+" и обратно");
		cha.sendMessage(".bank deposit - для обмена "+Config.BANKING_GOLDBAR_PRICE+" на "+item.getName());
		cha.sendMessage(".bank widraw - для обмена "+item.getName()+" на "+Config.BANKING_GOLDBAR_PRICE+" адена ");
		cha.sendMessage("Убедитесь, что у вас достаточно предметов для совершения операции");
	}
	public static void main(String [] args) {
		VoicedCommandHandler.getInstance().registerVoicedCommandHandler(new Bank());
	}

}
