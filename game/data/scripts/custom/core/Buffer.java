package custom.core;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ScheduledFuture;

import org.apache.log4j.Logger;

import ru.catssoftware.Config;
import ru.catssoftware.L2DatabaseFactory;
import ru.catssoftware.gameserver.Shutdown;
import ru.catssoftware.gameserver.cache.HtmCache;
import ru.catssoftware.gameserver.datatables.NpcBufferTable;
import ru.catssoftware.gameserver.datatables.SkillTable;
import ru.catssoftware.gameserver.model.L2Character;
import ru.catssoftware.gameserver.model.L2ItemInstance;
import ru.catssoftware.gameserver.model.L2Skill;
import ru.catssoftware.gameserver.model.L2World;
import ru.catssoftware.gameserver.model.actor.instance.L2MonsterInstance;
import ru.catssoftware.gameserver.model.actor.instance.L2NpcInstance;
import ru.catssoftware.gameserver.model.actor.instance.L2PcInstance;
import ru.catssoftware.gameserver.model.quest.Quest;
import ru.catssoftware.gameserver.model.quest.QuestState;
import ru.catssoftware.gameserver.model.zone.L2Zone;
import ru.catssoftware.gameserver.network.SystemMessageId;
import ru.catssoftware.gameserver.network.serverpackets.SystemMessage;

import javolution.util.FastList;
import javolution.util.FastMap;

public class Buffer extends Quest
{
	private int itemId = Config.ITEM_ID_FOR_PREMIUM_BUFFER;
	private static final Logger _logs = Logger.getLogger(Buffer.class.getName());
	public static String qn = "50000_Buffer";
	private static String htmlBase = "data/html/mods/buffer/Buffer";
	private Map<Integer, String> _lastPage;
	private Map<Integer, Boolean> _isPetTarget = new FastMap<Integer, Boolean>();
	private String _err = "";

	private class BuffProfile
    {
		private List<Integer> _buffs = new FastList<Integer>();
	}
	private Map<Integer,Map<String,BuffProfile>> _buffprofiles = new FastMap<Integer, Map<String,BuffProfile>>();
	private Map<Integer, Long> _restoreDelays = new FastMap<Integer, Long>();

	public Buffer()
    {
		super(-1, qn, "custom");
		NpcBufferTable.getInstance();
		_lastPage = new FastMap<Integer, String>();
		Shutdown.getInstance().registerShutdownHandler(saveProfiles);
		Shutdown.getInstance().registerShutdownHandler(stopBuffTask);
	}

	private Runnable saveProfiles  = new Runnable() {

		@Override
		public void run() {
			try {
				Connection con = L2DatabaseFactory.getInstance().getConnection();
				for(int playerId: _buffprofiles.keySet()) {
					PreparedStatement stm = con.prepareStatement("delete from character_buff_profiles where charId=?");
					stm.setInt(1, playerId);
					stm.execute();
					stm.close();
					stm = con.prepareStatement("insert into character_buff_profiles values (?,?,?)");
					stm.setInt(1, playerId);
					Map<String,BuffProfile> profiles = _buffprofiles.get(playerId);
					for( String s : profiles.keySet()) {
						stm.setString(2, s);
						for(int buffs : profiles.get(s)._buffs) {
							stm.setInt(3,buffs);
							stm.execute();
						}
					}
					stm.close();
				}
				con.close();
			} catch(SQLException e) {
				System.out.println("Buffer: Can't save profiles "+e);
			}
		}

	};

	private Runnable stopBuffTask = new Runnable()
    {
		@Override
		public void run()
        {
			try
            {
				if(autoBuffTask != null)
					autoBuffTask.Shutdown();
			}
            catch (Exception e)
            {
				System.out.println("Buffer: Can't stopBuffTask " + e);
			}
		}
	};

	@Override
	public String onFirstTalk(L2NpcInstance npc, L2PcInstance player)
    {
		return onTalk(npc, player);
	}

	@Override
	public String onTalk(L2NpcInstance npc, L2PcInstance talker)
    {
		if (talker.getQuestState(qn) == null)
        {
			newQuestState(talker);
		}
		getActiveProfile(talker);
		_lastPage.put(talker.getObjectId(), htmlBase + ".htm");
		_isPetTarget.put(talker.getObjectId(), false);
        createBuffProfiles(talker);
		String html = HtmCache.getInstance().getHtm(htmlBase + ".htm", talker);
		return fillHtml(talker, html);
	}

	private String ShowLastPage(int playerId)
    {
		if (_lastPage.containsKey(playerId))
        {
			String html = HtmCache.getInstance().getHtm(_lastPage.get(playerId), L2World.getInstance().getPlayer(playerId));
			return fillHtml(L2World.getInstance().getPlayer(playerId), html);
		}
		return null;
	}

	private boolean isValidTalker(L2PcInstance player)
    {
		if (checkMagicCondition(player))
        {
			return true;
		}
		return false;
	}

	private boolean checkMagicCondition(L2PcInstance player)
    {
		boolean ok = true;
		if (player.isInJail() && Config.BUFFER_RESTRICTION.contains("JAIL"))
        {
			ok = false;
		}
		if (player.getOlympiadGameId() >= 0 && Config.BUFFER_RESTRICTION.contains("OLY"))
        {
			ok = false;
		}
		if (player.isInCombat() && Config.BUFFER_RESTRICTION.contains("COMBAT"))
        {
			ok = false;
		}
		if (player.getKarma() > 0 && Config.BUFFER_RESTRICTION.contains("KARMA"))
        {
			ok = false;
		}
		if (player.getPvpFlag() > 0 && Config.BUFFER_RESTRICTION.contains("PVP"))
        {
			ok = false;
		}
		if (player.isInsideZone(L2Zone.FLAG_SIEGE) && Config.BUFFER_RESTRICTION.contains("SIEGE"))
        {
			ok = false;
		}
		if (player.isInsideZone(L2Zone.FLAG_NOSUMMON) && Config.BUFFER_RESTRICTION.contains("RB"))
        {
			ok = false;
		}
		if (player.isInsideZone(L2Zone.FLAG_PVP) && Config.BUFFER_RESTRICTION.contains("ARENA"))
        {
			ok = false;
		}
		return ok;
	}

	public boolean restoreCheck(L2PcInstance player)
    {
		Long lastRestore = _restoreDelays.get(player.getObjectId());
		if (Config.BUFFER_RESTORE_DELAY <= 0)
        {
			return true;
		}
		if (lastRestore == null)
        {
			_restoreDelays.put(player.getObjectId(), System.currentTimeMillis());
			return true;
		}
		if (System.currentTimeMillis() + (Config.BUFFER_RESTORE_DELAY * 1000) < lastRestore)
        {
			_restoreDelays.put(player.getObjectId(), System.currentTimeMillis());
			return true;
		}
		return true;
	}

	@Override
	public String onEvent(String event, QuestState qs) {
		try {
			L2PcInstance player = qs.getPlayer();
			if (player == null) {
				return null;
			}
			if ((player.isAlikeDead() || player.isAfraid() || player.isImmobilized()) && !event.startsWith("Chat")) {
				return null;
			}
			if (!checkMagicCondition(player)) {
				String htm = htmlBase + "-not.htm";
				String html = HtmCache.getInstance().getHtm(htm, player);
				return fillHtml(player, html);
			}

			L2Character target = player;
			if (_isPetTarget.get(player.getObjectId()) && player.getPet() != null) {
				target = player.getPet();
			}

			if (event.startsWith("Chat")) {
				if (!checkMagicCondition(player)) {
					_lastPage.put(player.getObjectId(), htmlBase + "-not.htm");
					return ShowLastPage(player.getObjectId());
				}
				String chatId = "";
				String htm = htmlBase + ".htm";
				if (event.indexOf(" ") != -1) {
					chatId = event.substring(event.indexOf(" ") + 1);
				}
				if (!chatId.equals("0")) {
					chatId = "-" + chatId;
					if (_isPetTarget.get(player.getObjectId())) {
						if (HtmCache.getInstance().pathExists(htmlBase + "-pet" + chatId + ".htm")) {
							htm = htmlBase + "-pet" + chatId + ".htm";
						} else {
							htm = htmlBase + chatId + ".htm";
						}
					} else {
						htm = htmlBase + chatId + ".htm";
					}
				}
				_lastPage.put(player.getObjectId(), htm);
				String html = HtmCache.getInstance().getHtm(htm, player);
				return fillHtml(player, html);
			} else if (event.startsWith("addpremium")) {
				String htm = htmlBase + "-notPremium.htm";
				if (player.getInventory().getItemByItemId(itemId) != null)
                {
                    htm = htmlBase + "-Premium.htm";
					String html = HtmCache.getInstance().getHtm(htm, player);
					return fillHtml(player, html);
				} else {
					player.sendMessage("У вас нет бафф итема.");
				}
			} else if (event.startsWith("SelectProfile")) {
				if (!checkMagicCondition(player)) {
					_lastPage.put(player.getObjectId(), htmlBase + "-not.htm");
					return ShowLastPage(player.getObjectId());
				}
				String[] args = event.split(" ");
			    player.getCharacterData().set("BuffProfile",args[1]);
				String html = HtmCache.getInstance().getHtm(htmlBase + "-p2.htm", player);
				_lastPage.put(player.getObjectId(), htmlBase + "-p2.htm");
				html = fillHtml(player, html);
				return html;
			} else if (event.startsWith("Profile")) {
				if (!checkMagicCondition(player)) {
					_lastPage.put(player.getObjectId(), htmlBase + "-not.htm");
					return ShowLastPage(player.getObjectId());
				}
				String html = HtmCache.getInstance().getHtm(htmlBase + "-p1.htm", player);
				_lastPage.put(player.getObjectId(), htmlBase + "-p1.htm");
				return fillHtml(player, html);
			} else if (event.startsWith("ClearProfile")) {
				BuffProfile profile = getActiveProfile(player);
				profile._buffs.clear();
				return onEvent("Profile", qs);
            }
            else if (event.startsWith("DeleteProfile")) {
			    Map<String,BuffProfile> _profiles = _buffprofiles.get(player.getObjectId());
			    if(getActiveProfile(player)!=null)
				    _profiles.remove(getActiveProfileName(player));
			    player.getCharacterData().set("BuffProfile",(String)null);
			    return onEvent("Profile",qs);
		    }
            else if (event.startsWith("CreateProfile")) {
			    Map<String,BuffProfile> _profiles = _buffprofiles.get(player.getObjectId());
			    if(_profiles==null) {
				    _buffprofiles.put(player.getObjectId(), new FastMap<String, BuffProfile>());
				    _profiles = _buffprofiles.get(player.getObjectId());
			    }
			    String []args = event.split(" ");
			    if(!_profiles.containsKey(args[1])) {
				    _profiles.put(args[1],new BuffProfile());
			    }
			    player.getCharacterData().set("BuffProfile",args[1]);
			    return onEvent("Profile",qs);
			}
            else if (event.startsWith("UseProfile") && checkMagicCondition(player)) {
				BuffProfile profile = getActiveProfile(player);
				target = player;
				if (profile != null) {
					for (int buff : profile._buffs) {
						int[] group = NpcBufferTable.getInstance().getSkillInfo(50000, buff);
						useBuff(buff, group, player, target);
					}
				}
			} else if (event.startsWith("RemBuff")) {
				if (isValidTalker(player) && player.destroyItemByItemId("GM Buffer", Config.BUFFER_REMOVE_ITEM_ID, Config.BUFFER_REMOVE_PRICE, player, true)) {
					target.stopAllEffects();
				}
			} else if (event.startsWith("recHp")) {
				if (!checkMagicCondition(player)) {
					_lastPage.put(player.getObjectId(), htmlBase + "-not.htm");
					return ShowLastPage(player.getObjectId());
				}
				if (restoreCheck(player) && isValidTalker(player)) {
					if (target.getStatus().getCurrentCp() < target.getMaxCp()) {
						if (player.destroyItemByItemId("GM Buffer", Config.BUFFER_CP_ITEM_ID, Config.BUFFER_CP_PRICE, player, true)) {
							target.getStatus().setCurrentCp(target.getMaxCp());
							player.sendMessage("CP восстановлено.");
						} else {
							player.sendMessage("Недостаточно средств для восстановления CP.");
						}
					}
					if (target.getStatus().getCurrentHp() < target.getMaxHp() && player.destroyItemByItemId("GM Buffer", Config.BUFFER_HP_ITEM_ID, Config.BUFFER_HP_PRICE, player, true)) {
						if (player.destroyItemByItemId("GM Buffer", Config.BUFFER_HP_ITEM_ID, Config.BUFFER_HP_PRICE, player, true)) {
							target.getStatus().setCurrentHp(target.getMaxHp());
							player.sendMessage("HP восстановлено.");
						} else {
							player.sendMessage("Недостаточно средств для восстановления HP.");
						}
					}
					if (target.getStatus().getCurrentMp() < target.getMaxMp()) {
						if (player.destroyItemByItemId("GM Buffer", Config.BUFFER_MP_ITEM_ID, Config.BUFFER_MP_PRICE, player, true)) {
							target.getStatus().setCurrentMp(target.getMaxMp());
							player.sendMessage("MP восстановлено.");
						} else {
							player.sendMessage("Недостаточно средств для восстановления MP.");
						}
					}
				}
			} else if (event.startsWith("recCp")) {
				if (!checkMagicCondition(player)) {
					_lastPage.put(player.getObjectId(), htmlBase + "-not.htm");
					return ShowLastPage(player.getObjectId());
				}
				if (restoreCheck(player) && isValidTalker(player) && player.destroyItemByItemId("GM Buffer", Config.BUFFER_CP_ITEM_ID, Config.BUFFER_CP_PRICE, player, true)) {
					target.getStatus().setCurrentCp(target.getMaxCp());
				}
			} else if (event.startsWith("recMp")) {
				if (!checkMagicCondition(player)) {
					_lastPage.put(player.getObjectId(), htmlBase + "-not.htm");
					return ShowLastPage(player.getObjectId());
				}
				if (restoreCheck(player) && isValidTalker(player) && player.destroyItemByItemId("GM Buffer", Config.BUFFER_MP_ITEM_ID, Config.BUFFER_MP_PRICE, player, true)) {
					target.getStatus().setCurrentMp(target.getMaxMp());
				}
			} else if (event.startsWith("Target")) {
				_isPetTarget.put(player.getObjectId(), !_isPetTarget.get(player.getObjectId()));
			} else if (event.startsWith("Buff")) {
				if (!checkMagicCondition(player)) {
					_lastPage.put(player.getObjectId(), htmlBase + "-not.htm");
					return ShowLastPage(player.getObjectId());
				}
				if (!isValidTalker(player)) {
					return ShowLastPage(player.getObjectId());
				}

				String[] buffGroupArray;
				if (event.startsWith("BuffPet")) {
					buffGroupArray = event.substring(8).split(" ");
				} else {
					buffGroupArray = event.substring(5).split(" ");
				}

				for (String buffGroupList : buffGroupArray) {
					if (buffGroupList == null) {
						_logs.warn("NPC Buffer Warning: buffer has no buffGroup set in the bypass for the buff selected.");
						return ShowLastPage(player.getObjectId());
					}

					int buffGroup = Integer.parseInt(buffGroupList);
					int[] npcBuffGroupInfo = NpcBufferTable.getInstance().getSkillInfo(50000, buffGroup);

					if (npcBuffGroupInfo == null) {
						_logs.warn("NPC Buffer Warning: Player: " + player.getName() + " has tried to use skill group (" + buffGroup + ") not assigned to the NPC Buffer!");
						return ShowLastPage(player.getObjectId());
					}
					if (Config.LIST_BUFFER_PREMIUM_BUFF_ALLOW.contains(buffGroup)) {
						_lastPage.put(player.getObjectId(), htmlBase + "-Premium.htm");
					}
					useBuff(buffGroup, npcBuffGroupInfo, player, target);

				}
			}
			return ShowLastPage(player.getObjectId());
		} catch (Exception e) {
			return htmlBase + ".htm";
		}
	}

	private String getActiveProfileName(L2PcInstance player) {
		try {
			return player.getCharacterData().getString("BuffProfile");
		} catch(IllegalArgumentException e) {
			return "Нет";
		}

	}

	private BuffProfile getActiveProfile(L2PcInstance player) {
		String profileName = null;
		try {
			profileName = player.getCharacterData().getString("BuffProfile");
		} catch(IllegalArgumentException e) {
			return null;
		}

		Map<String,BuffProfile> _profiles = _buffprofiles.get(player.getObjectId());

		if(profileName!=null && _profiles!=null)
			return _profiles.get(profileName);
		return null;
	}

	private synchronized String fillHtml(L2PcInstance player, String html)
    {
		try
        {
			html = html.replace("%target%", _isPetTarget.get(player.getObjectId())?"Слуга":"Персонаж");
			html = html.replace("%profile%",getActiveProfileName(player));
			html = html.replace("%err%",_err);
		_err = "";
		String profiles = "";
		try
        {
		Map<String,BuffProfile> _profiles = _buffprofiles.get(player.getObjectId());
		if(_profiles!=null)
			for(String profileName : _profiles.keySet())
				profiles+="<tr><td><center><a action=\"bypass -h Quest 50000_Buffer SelectProfile "+profileName+"\">"+profileName+"</a></center></td></tr>";
		if(profiles.length()==0)
			profiles = "<tr><td><center>Отсутствуют</center></td></tr>";
		html = html.replace("%profilelist%", profiles);
		BuffProfile profile = getActiveProfile(player);
		if(profile!=null && profile._buffs!=null && profile._buffs.size()>0)
        {
			html = html.replace("%useprofile%","<button action=\"bypass -h Quest 50000_Buffer UseProfile\" value=\"Исп. профиль\" width=100 height=21 back=\"sek.cbui94\" fore=\"sek.cbui92\">");
			String buffs = "";
			int npcid = 50000;
			for(Integer buff : profile._buffs)
            {
				if(player.getTarget()!=null && (player.getTarget() instanceof L2NpcInstance && !(player.getTarget() instanceof L2MonsterInstance)))
                {
					npcid = ((L2NpcInstance)player.getTarget()).getNpcId();
				}
				int [] group = NpcBufferTable.getInstance().getSkillInfo(npcid, buff);
				buffs+="<tr><td><center>"+SkillTable.getInstance().getSkillName(group[0])+"</center></td></tr>";
			}
			html = html.replace("%buflist%", buffs);
		}
		else
			html = html.replace("%useprofile%","");
		}
        catch(Exception e)
        {
			html = html.replace("%useprofile%","");
			_buffprofiles.remove(player.getObjectId());
			_log.error("Error getting profiles for "+player.getName()+", cleaning");
		}
		return html;
		}
        catch(Exception e)
        {
			return "<html><body><br><center>Произошла ошибка при обрашении к баферу, попробуйте позже</center></body></html>";
		}
	}

	private boolean useBuff(int grpid, int[] npcBuffGroupInfo, L2PcInstance player, L2Character target)
    {
		for (int i = 0; i < npcBuffGroupInfo.length; i += 4)
        {
			int skillId = npcBuffGroupInfo[i];
			int skillLevel = npcBuffGroupInfo[i + 1];
			int skillFeeId = npcBuffGroupInfo[i + 2];
			int skillFeeAmount = npcBuffGroupInfo[i + 3];
			if (!Config.LIST_BUFFER_BUFF_ALLOW.contains(skillId) && !Config.LIST_BUFFER_PREMIUM_BUFF_ALLOW.contains(skillId))
            {
				player.sendMessage("Недопустимый эффект!");
				return false;
			}
			if (Config.LIST_BUFFER_PREMIUM_BUFF_ALLOW.contains(skillId) && !(player.getInventory().getItemByItemId(itemId) != null))
            {
				player.sendMessage("Недопустимый эффект");
				return false;
			}
			if (skillFeeId != 0)
            {
				L2ItemInstance itemInstance = player.getInventory().getItemByItemId(skillFeeId);
			    if (itemInstance == null || (!itemInstance.isStackable() && player.getInventory().getInventoryItemCount(skillFeeId, -1) < skillFeeAmount))
			    {
				    SystemMessage sm = new SystemMessage(SystemMessageId.NOT_ENOUGH_ITEMS);
				    player.sendPacket(sm);
				    return false;
                }
			    if (itemInstance.isStackable())
                {
				    if (!player.destroyItemByItemId("Npc Buffer", skillFeeId, skillFeeAmount, player.getTarget(), true))
                    {
					    player.sendPacket(SystemMessageId.NOT_ENOUGH_ITEMS);
					    return false;
				    }
			    }
                else
                {
				    for (int k = 0; k < skillFeeAmount; ++k)
                    {
				        player.destroyItemByItemId("Npc Buffer", skillFeeId, 1, player.getTarget(), true);
				    }
			    }
		    }
            L2Skill skill;
		    skill = SkillTable.getInstance().getInfo(skillId,skillLevel);

		    if (skill != null)
		    {
			    skill.getEffects(target, target);
			    BuffProfile profile = getActiveProfile(player);
			    if(profile!=null)
                {
				    if(!profile._buffs.contains(grpid))
					    profile._buffs.add(grpid);
		        }
		    }
		}
        return true;
	}

	private Map<String,BuffProfile> createBuffProfiles(L2PcInstance player)
    {
		Map<String, BuffProfile> result;
		result = _buffprofiles.get(player.getObjectId());
		if (result == null)
        {
			result = new FastMap<String, BuffProfile>();
			_buffprofiles.put(player.getObjectId(), result);
            try
            {
				Connection con = L2DatabaseFactory.getInstance().getConnection();
				PreparedStatement stm = con.prepareStatement("select * from character_buff_profiles where charId=? order by profileName");
				stm.setInt(1, player.getObjectId());
				ResultSet rs = stm.executeQuery();
				String profileName = "";
				BuffProfile profile = null;
				while(rs.next())
                {
					if(!rs.getString("profileName").equals(profileName))
                    {
						profileName = rs.getString("profileName");
						profile = new BuffProfile();
						result.put(profileName, profile);
					}
					profile._buffs.add(rs.getInt("buffGroup"));
				}
				rs.close();
				stm.close();
				con.close();
			}
            catch(SQLException e)
            {
				_log.error("Buffer: Can't load buf profiles",e);
			}
		}

		return result;
	}

    public class buffTasks
    {
		private ScheduledFuture<?> buffTask = null;

		public void Shutdown()
        {
			stopBuffTask(false);
		}

		private void stopBuffTask(final boolean mayInterruptIfRunning)
        {
			if (buffTask != null)
            {
				buffTask.cancel(mayInterruptIfRunning);
				buffTask = null;
			}
		}
	}

	/**
	 * Запускаем задачу автобафа
	 */
	private buffTasks autoBuffTask = null;

	public static void main(String[] args)
    {
		if (Config.BUFFER_ENABLED)
        {
			getInstance();
		}
	}

	public static Buffer getInstance()
    {
		return SingletonHolder._instance;
	}

	private static class SingletonHolder
    {
		protected static final Buffer _instance = new Buffer();
	}
}
