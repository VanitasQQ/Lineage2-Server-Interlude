package handlers.voice;

import ru.catssoftware.gameserver.handler.IVoicedCommandHandler;
import ru.catssoftware.gameserver.handler.VoicedCommandHandler;
import ru.catssoftware.gameserver.instancemanager.RaidPointsManager;
import ru.catssoftware.gameserver.model.actor.instance.L2PcInstance;
import ru.catssoftware.gameserver.network.serverpackets.NpcHtmlMessage;
import ru.catssoftware.gameserver.skills.Formulas;
import ru.catssoftware.gameserver.skills.Stats;

public class WhoAmI implements IVoicedCommandHandler {

	@Override
	public String getDescription(String command) {
		return "Дополнительная информация об игровом персонаже";
	}

	@Override
	public String[] getVoicedCommandList() {
		return new String[] {"whoami"};
	}

	@Override
	public boolean useVoicedCommand(String command, L2PcInstance activeChar,
			String target) {
		if(activeChar!=null) {
			String html = "<html><title>Информация о персонаже</title><body>";
			html+="<br><center>Персонаж <font color=\"LEVEL\">"+activeChar.getName()+"</font><br>";
			html+="<table width=200>";
			html+="<tr><td>HP regen. "+String.format("%3.2f", Formulas.calcHpRegen(activeChar))+"</td>";
			html+="<td>MP regen. "+String.format("%3.2f", Formulas.calcMpRegen(activeChar))+"</td></tr>";
			html+="<tr><td>СP regen. "+String.format("%3.2f", Formulas.calcCpRegen(activeChar))+"</td><td>Уворот "+String.format("%3d", activeChar.getEvasionRate(activeChar))+"</td></tr>";
			html+="</table>Сопротивления<table width=200>";
			html+="<tr><td>Огонь "+String.format("%3.2f", 100 - 100 * activeChar.calcStat(Stats.FIRE_VULN, 1.0, activeChar, null))+"</td>";
			html+="<td>Вода "+String.format("%3.2f", 100 - 100 * activeChar.calcStat(Stats.WATER_VULN, 1.0, activeChar, null))+"</td></tr>";
			html+="<tr><td>Воздух "+String.format("%3.2f", 100 - 100 * activeChar.calcStat(Stats.WIND_VULN, 1.0, activeChar, null))+"</td>";
			html+="<td>Земля "+String.format("%3.2f", 100 - 100 * activeChar.calcStat(Stats.EARTH_VULN, 1.0, activeChar, null))+"</td></tr>";
			html+="<tr><td>Тьма "+String.format("%3.2f", 100 - 100 * activeChar.calcStat(Stats.DARK_VULN, 1.0, activeChar, null))+"</td>";
			html+="<td>Святая "+String.format("%3.2f", 100 - 100 * activeChar.calcStat(Stats.HOLY_VULN, 1.0, activeChar, null))+"</td></tr>";
			
			html+="</table>Дополнительно<table width=200>";
			html+="<tr><td>Очки славы: "+activeChar.getFame()+"</td>";
			html+="<tr><td>Рейд-очки: "+RaidPointsManager.getPointsByOwnerId(activeChar.getObjectId())+"</td>";
			html+="<td>PC Bangs: "+activeChar.getPcCaffePoints()+"</td></tr>";
			html+="</center></table></body></html>";
			NpcHtmlMessage msg = new NpcHtmlMessage(5);
			msg.setHtml(html);
			activeChar.sendPacket(msg);
		}
		return false;
	}
	public static void main(String [] args) {
		VoicedCommandHandler.getInstance().registerVoicedCommandHandler(new WhoAmI());
	}

}
