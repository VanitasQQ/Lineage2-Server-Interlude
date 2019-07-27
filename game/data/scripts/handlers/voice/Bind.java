package handlers.voice;

import java.io.IOException;

import ru.catssoftware.Message;
import ru.catssoftware.gameserver.LoginServerThread;
import ru.catssoftware.gameserver.handler.IVoicedCommandHandler;
import ru.catssoftware.gameserver.handler.VoicedCommandHandler;
import ru.catssoftware.gameserver.model.actor.instance.L2PcInstance;
import ru.catssoftware.gameserver.network.gameserverpackets.ChangeIpAddres;

public class Bind implements IVoicedCommandHandler {

	private static String [] commands = {"bindip","bindhwid","hwidstatus","ipstatus"};
	
	@Override
	public String getDescription(String command) {
		if(command.equals("ipstatus"))
			return "Показать статус привязки аккаунта к IP-адресу";
		else if(command.equals("bindip"))
			return "Включить/выключить привязку аккаунта к IP-адресу";
		return null;
	}

	@Override
	public String[] getVoicedCommandList() {
		return commands;
	}

	@Override
	public boolean useVoicedCommand(String command, L2PcInstance activeChar,
			String target) {
		if(command.equals("hwidstatus")) {
			if(activeChar.getHWid()==null || activeChar.getHWid().length()==0) {
				activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_NOT_ACCESSABLE));
				return false;
			}
			try {
				activeChar.getAccountData().getString("hwbind");
			} catch(IllegalArgumentException e) {
				activeChar.getAccountData().set("hwbind","");
			}
			activeChar.sendMessage(String.format(Message.getMessage(activeChar, Message.MessageId.MSG_HWID_REC), activeChar.getAccountData().getString("hwbind").length()>0?"on":"off"));
		}
		else if(command.equals("bindhwid")) {
			if(activeChar.getHWid()==null || activeChar.getHWid().length()==0) {
				activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_NOT_ACCESSABLE));
				return false;
			}
			try {
				if(activeChar.getAccountData().getString("hwbind").length()==0)
					activeChar.getAccountData().set("hwbind",activeChar.getHWid());
				else 
					activeChar.getAccountData().set("hwbind","");
			} catch(IllegalArgumentException e) {
				activeChar.getAccountData().set("hwbind",activeChar.getHWid());
			}
			activeChar.sendMessage(String.format(Message.getMessage(activeChar, Message.MessageId.MSG_HWID_REC), activeChar.getAccountData().getString("hwbind").length()>0?"on":"off"));
		}
		if(command.equals("ipstatus")) try {
			activeChar.sendMessage(String.format(Message.getMessage(activeChar, Message.MessageId.MSG_IP_REC), activeChar.getAccountData().getBool("ipbind")?"on":"off"));
		} catch(IllegalArgumentException e) {
			activeChar.sendMessage(String.format(Message.getMessage(activeChar, Message.MessageId.MSG_IP_REC), "off"));
		}
		else if(command.equals("bindip")) try {
			try {
				if(activeChar.getAccountData().getBool("ipbind"))
					LoginServerThread.getInstance().sendPacket(new ChangeIpAddres(activeChar.getClient().getAccountName(),"*"));
				else	
					LoginServerThread.getInstance().sendPacket(new ChangeIpAddres(activeChar.getClient().getAccountName(),activeChar.getClient().getHostAddress()));
				activeChar.getAccountData().set("ipbind",!activeChar.getAccountData().getBool("ipbind"));
				activeChar.sendMessage(String.format(Message.getMessage(activeChar, Message.MessageId.MSG_IP_REC), activeChar.getAccountData().getBool("ipbind")?"on":"off"));
			} catch(IllegalArgumentException e) {
				LoginServerThread.getInstance().sendPacket(new ChangeIpAddres(activeChar.getClient().getAccountName(),activeChar.getClient().getHostAddress()));
				activeChar.sendMessage(String.format(Message.getMessage(activeChar, Message.MessageId.MSG_IP_REC), "on"));
				activeChar.getAccountData().set("ipbind",true);
			}
		} catch(IOException e) {
			
		}
		return false;
	}
	public static void main(String [] args) {
		VoicedCommandHandler.getInstance().registerVoicedCommandHandler(new Bind());
	}

}
