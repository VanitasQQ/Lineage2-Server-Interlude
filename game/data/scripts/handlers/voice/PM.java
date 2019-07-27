package handlers.voice;

import ru.catssoftware.gameserver.handler.ChatHandler;
import ru.catssoftware.gameserver.handler.IChatHandler;
import ru.catssoftware.gameserver.handler.IVoicedCommandHandler;
import ru.catssoftware.gameserver.handler.VoicedCommandHandler;
import ru.catssoftware.gameserver.model.actor.instance.L2PcInstance;
import ru.catssoftware.gameserver.network.SystemChatChannelId;

public class PM implements IVoicedCommandHandler {

	@Override
	public String getDescription(String arg0) {
		// TODO Auto-generated method stub
		return "Отправляет сообщение в ПМ персонажу который на таргете";
	}

	@Override
	public String[] getVoicedCommandList() {
		// TODO Auto-generated method stub
		return new String [] { "pm" }; 
	}

	@Override
	public boolean useVoicedCommand(String cmd, L2PcInstance cha, String params) {
		if(cha.getTarget()!=null && cha.getTarget().getActingPlayer()!=null) {
			L2PcInstance pc = cha.getTarget().getActingPlayer();
			IChatHandler tell = ChatHandler.getInstance().getChatHandler(SystemChatChannelId.Chat_Tell);
			tell.useChatHandler(cha, pc.getName(), SystemChatChannelId.Chat_Tell, params);
		} else {
			cha.sendMessage("У вас на таргете должен быть персонаж или его саммон которому вы хотите сказать");
		}
		return false;
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		VoicedCommandHandler.getInstance().registerVoicedCommandHandler(new PM());

	}

}
