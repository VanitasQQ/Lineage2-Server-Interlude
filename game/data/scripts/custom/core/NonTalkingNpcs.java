package custom.core;

import ru.catssoftware.gameserver.model.actor.instance.L2NpcInstance;
import ru.catssoftware.gameserver.model.actor.instance.L2PcInstance;
import ru.catssoftware.gameserver.model.quest.Quest;
import ru.catssoftware.gameserver.network.serverpackets.ActionFailed;

public class NonTalkingNpcs extends Quest
{
	private int NPCs[] = {31557,31606,31671,31672,31673,31674,32026,32030,32031,32032,32038};

	public NonTalkingNpcs()
	{
		super(-1,"1000_NonTalkingNpcs","custom");
		for (int id : NPCs)
			addFirstTalkId(id);
	}

	public String onFirstTalk (L2NpcInstance npc, L2PcInstance player)
	{
		player.sendPacket(ActionFailed.STATIC_PACKET);
		return null;
	}
	public static void main(String []args) {
		new NonTalkingNpcs();
	}
}