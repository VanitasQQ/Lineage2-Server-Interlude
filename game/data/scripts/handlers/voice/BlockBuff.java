package handlers.voice;

import ru.catssoftware.Message;
import ru.catssoftware.gameserver.handler.IVoicedCommandHandler;
import ru.catssoftware.gameserver.handler.VoicedCommandHandler;
import ru.catssoftware.gameserver.model.actor.instance.L2PcInstance;

public class BlockBuff implements IVoicedCommandHandler
{
	@Override
	public String getDescription(String command)
	{
		// TODO Auto-generated method stub
		return "Блокирует/снимает блокировку получения бафов";
	}

	@Override
	public String[] getVoicedCommandList()
	{
		return new String [] {"blockbuff"};
	}

	@Override
	public boolean useVoicedCommand(String command, L2PcInstance activeChar, String target)
	{		
		activeChar.setPreventedFromReceivingBuffs(!activeChar.isPreventedFromReceivingBuffs());
		activeChar.sendMessage(String.format(Message.getMessage(activeChar, Message.MessageId.MSG_BLOCK_BUFF), activeChar.isPreventedFromReceivingBuffs()?"on":"off"));
		return true;
	}
	
	public static void main(String [] args)
	{
		VoicedCommandHandler.getInstance().registerVoicedCommandHandler(new BlockBuff());
	}
}
