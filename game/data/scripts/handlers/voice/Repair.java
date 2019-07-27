package handlers.voice;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import ru.catssoftware.L2DatabaseFactory;
import ru.catssoftware.gameserver.handler.IVoicedCommandHandler;
import ru.catssoftware.gameserver.handler.VoicedCommandHandler;
import ru.catssoftware.gameserver.model.actor.instance.L2PcInstance;
import ru.catssoftware.gameserver.network.serverpackets.NpcHtmlMessage;


 /**
  * @author m095
  * Класс восстановления персонажа после краха клиента
  */
public class Repair implements IVoicedCommandHandler
{
	private static final String[]	VOICED_COMMANDS	=
	{
		"repair",
		"startrepair"
	};

	public boolean useVoicedCommand(String command, L2PcInstance activeChar, String target)
	{
		if (activeChar==null)
			return false;
		
		String repairChar=null;
		String[] cmdParams = target.split(" ");
		repairChar=cmdParams[0];

		// Send activeChar HTML page
		if (command.startsWith("repair"))
		{
			NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
			html.setFile("data/html/mods/repair/repair.htm");
			activeChar.sendPacket(html);
			return true;
		}
		// Command for enter repairFunction from html
		else if (command.startsWith("startrepair"))
		{
			if (checkAcc(activeChar,repairChar))
			{
				if (activeChar.getName().compareTo(repairChar)==0)
				{
					NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
					html.setFile("data/html/mods/repair/repair-self.htm");
					activeChar.sendPacket(html);
				}
				else if (checkJail(repairChar))
				{
					NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
					html.setFile("data/html/mods/repair/repair-jail.htm");
					activeChar.sendPacket(html);
				}
				else
				{
					repairBadCharacter(repairChar);
					NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
					html.setFile("data/html/mods/repair/repair-done.htm");
					activeChar.sendPacket(html);
				}
			}
			else
			{
				NpcHtmlMessage html = new NpcHtmlMessage(activeChar.getObjectId());
				html.setFile("data/html/mods/repair/repair-error.htm");
				activeChar.sendPacket(html);
			}
			return true;
		}
		return false;
	}
	
	/**
	 * Проверяет аккаунт чара
	 * @param activeChar
	 * @param repairChar
	 * @return
	 */
	private boolean checkAcc(L2PcInstance activeChar,String repairChar)
	{
		Connection con = null;
		try
		{
			con = L2DatabaseFactory.getInstance().getConnection(con);
			PreparedStatement statement = con.prepareStatement("SELECT account_name FROM characters WHERE char_name=?");
			statement.setString(1, repairChar);
			ResultSet rset = statement.executeQuery();
			if (rset.next())
			{
				if (activeChar.getAccountName().compareTo(rset.getString(1)) == 0)
					return true;
			}
			rset.close();
			statement.close();
		}
		catch (SQLException e)
		{
			e.printStackTrace();
		}
		finally
		{
			try
			{
				if (con != null)
					con.close();
			}
			catch (SQLException e)
			{
				e.printStackTrace();
			}
		}
		return false;
	}

	/**
	 * Проверяет находится ли чар в тюрьме
	 * @param repairChar
	 * @return
	 */
	private boolean checkJail(String repairChar)
	{
		Connection con = null;
		try
		{
			con = L2DatabaseFactory.getInstance().getConnection(con);
			PreparedStatement statement = con.prepareStatement("SELECT in_jail FROM characters WHERE char_name=?");
			statement.setString(1, repairChar);
			ResultSet rset = statement.executeQuery();
			if (rset.next())
			{
				if (rset.getInt(1) == 1)
					return true;
			}
			rset.close();
			statement.close();
		}
		catch (SQLException e)
		{
			e.printStackTrace();

		}
		finally
		{
			try
			{
				if (con != null)
					con.close();
			}
			catch (SQLException e)
			{
				e.printStackTrace();
			}
		}
		return false;
	}

	/**
	 * Восстанавливает персонажа, обновляет координаты, удаляет ярлыки, сбрасывает вещи в сумку
	 * @param charName
	 */
	private void repairBadCharacter(String charName)
	{
		Connection con = null;
		try
		{
			con = L2DatabaseFactory.getInstance().getConnection(con);

			PreparedStatement statement;
			statement = con.prepareStatement("SELECT charId FROM characters WHERE char_name=?");
			statement.setString(1, charName);
			ResultSet rset = statement.executeQuery();

			int objId = 0;
			if (rset.next())
			{
				objId = rset.getInt(1);
			}
			rset.close();
			statement.close();
			if (objId == 0)
			{
				con.close();
				return;
			}
			statement = con.prepareStatement("UPDATE characters SET x=17867, y=170259, z=-3503 WHERE charId=?");
			statement.setInt(1, objId);
			statement.execute();
			statement.close();
			statement = con.prepareStatement("DELETE FROM character_shortcuts WHERE charId=?");
			statement.setInt(1, objId);
			statement.execute();
			statement.close();
			statement = con.prepareStatement("UPDATE items SET loc=\"INVENTORY\" WHERE owner_id=? AND loc=\"PAPERDOLL\"");
			statement.setInt(1, objId);
			statement.execute();
			statement.close();
		}
		catch (SQLException e)
		{
			e.printStackTrace();
		}
		finally
		{
			try
			{
				if (con != null)
					con.close();
			}
			catch (SQLException e)
			{
				e.printStackTrace();
			}
		}
	}

	public String getDescription(String command)
	{
		if(command.equals("repair"))
			return "Востанавливает поврежденную информацию о персонаже.";
		return null;
	}

	public String[] getVoicedCommandList()
	{
		return VOICED_COMMANDS;
	}
	public static void main(String [] args) {
		VoicedCommandHandler.getInstance().registerVoicedCommandHandler(new Repair());
	}

	
}