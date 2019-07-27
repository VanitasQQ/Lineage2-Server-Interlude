package custom.Services;

import java.sql.Connection;
import java.sql.PreparedStatement;

import org.apache.log4j.Logger;

import ru.catssoftware.L2DatabaseFactory;
import ru.catssoftware.gameserver.datatables.CharNameTable;
import ru.catssoftware.gameserver.datatables.ClanTable;
import ru.catssoftware.gameserver.datatables.SkillTable;
import ru.catssoftware.gameserver.model.actor.instance.L2NpcInstance;
import ru.catssoftware.gameserver.model.actor.instance.L2PcInstance;
import ru.catssoftware.gameserver.model.quest.Quest;
import ru.catssoftware.gameserver.model.quest.QuestState;
import ru.catssoftware.gameserver.util.PcAction;

/**
 * @author TrueMan
 */
public class Services extends Quest
{
	public static final Logger _log = Logger.getLogger(Services.class.getName());
	
	// ID НПЦ
	int ServicesNpcId = 70000;
	
	// Продажа нубла
	int nobleItemId = 4037;
	int nobleItemCount = 10;
	
	// Продажа фул клан скилов
	int skillItemId = 4037;
	int skillItemCount = 10;
	
	// Смена ника
	int changeNameItemId = 4037;
	int changeNameItemCount = 4;
	boolean logNameChanges = true;
	
	// Покраска ника и титула
	int changeColourItemId = 4037;
	int changeColourItemCount = 6;
	
	// Смена имени клана
	int changeClanNameItemId = 4037;
	long changeClanNameItemCount = 3;
	int clanMinLevel = 6;
	boolean logClanNameChanges = true;
	
	// Продажа уровня клана
	int clanLevelItemsId6 = 4037;
	int clanLevelItemsCount6 = 5;
	int clanLevelItemsId7 = 4037;
	int clanLevelItemsCount7 = 7;
	int clanLevelItemsId8 = 4037;
	int clanLevelItemsCount8 = 10;
	
	// Репутация клана
	int clanReputationPointsItemId = 4037;
	int clanReputationPointsItemCount = 2;
	int clanReputationPointsItemId1 = 4037;
	int clanReputationPointsItemCount1 = 3;
	int clanReputationPointsItemId2 = 4037;
	int clanReputationPointsItemCount2 = 4;
	
	// Премиум аккаунт
	int premiumItemIt1 = 4037;
	int premiumItemCount1 = 2;
	int premiumItemIt2 = 4037;
	int premiumItemCount2 = 3;
	int premiumItemIt3 = 4037;
	int premiumItemCount3 = 5;
	int premiumItemIt4 = 4037;
	int premiumItemCount4 = 7;
	int premiumItemIt5 = 4037;
	int premiumItemCount5 = 10;
	
	public Services(int questId, String name, String descr)
	{
		super(questId, name, descr);
		
		addStartNpc(ServicesNpcId);
		addFirstTalkId(ServicesNpcId);
		addTalkId(ServicesNpcId);
	}
	
	public static void main(String[] args)
	{
		new Services(-1, Services.class.getSimpleName(), "custom");
	}
	
	@Override
	public String onFirstTalk(L2NpcInstance npc, L2PcInstance player)
	{
		if (player.getQuestState(getName()) == null)
		{
			newQuestState(player);
		}
		else if (player.isInCombat())
		{
			return "Services-Blocked.htm";
		}
		else if (player.getPvpFlag() == 1)
		{
			return "Services-Blocked.htm";
		}
		else if (player.getKarma() != 0)
		{
			return "Services-Blocked.htm";
		}
		else if (player.isDead() || player.isFakeDeath())
		{
			return "Services-Blocked.htm";
		}
		
		return "Services.htm";
	}
	
	@Override
	public String onAdvEvent(String event, L2NpcInstance npc, L2PcInstance player)
	{
		String htmlText = event;
		QuestState st = player.getQuestState(getName());
		
		if (event.equals("getPremium1"))
		{
			if (player.getPremiumService() == 0)
			{
				if (st.getQuestItemsCount(premiumItemIt1) >= premiumItemCount1)
				{
					st.takeItems(premiumItemIt1, premiumItemCount1);
					PcAction.addPremiumServices(player, 1, player.getAccountName());
					player.broadcastUserInfo();
					return "PremiumAccount-Success.htm";
				}
				return "PremiumAccount-NoItems.htm";
			}
			return "PremiumAccount-Alredy.htm";
		}
		
		if (event.equals("getPremium2"))
		{
			if (player.getPremiumService() == 0)
			{
				if (st.getQuestItemsCount(premiumItemIt2) >= premiumItemCount2)
				{
					st.takeItems(premiumItemIt2, premiumItemCount2);
					PcAction.addPremiumServices(player, 3, player.getAccountName());
					player.broadcastUserInfo();
					return "PremiumAccount-Success.htm";
				}
				return "PremiumAccount-NoItems.htm";
			}
			return "PremiumAccount-Alredy.htm";
		}
		
		if (event.equals("getPremium3"))
		{
			if (player.getPremiumService() == 0)
			{
				if (st.getQuestItemsCount(premiumItemIt3) >= premiumItemCount3)
				{
					st.takeItems(premiumItemIt3, premiumItemCount3);
					PcAction.addPremiumServices(player, 7, player.getAccountName());
					player.broadcastUserInfo();
					return "PremiumAccount-Success.htm";
				}
				return "PremiumAccount-NoItems.htm";
			}
			return "PremiumAccount-Alredy.htm";
		}
		
		if (event.equals("getPremium4"))
		{
			if (player.getPremiumService() == 0)
			{
				if (st.getQuestItemsCount(premiumItemIt4) >= premiumItemCount4)
				{
					st.takeItems(premiumItemIt4, premiumItemCount4);
					PcAction.addPremiumServices(player, 14, player.getAccountName());
					player.broadcastUserInfo();
					return "PremiumAccount-Success.htm";
				}
				return "PremiumAccount-NoItems.htm";
			}
			return "PremiumAccount-Alredy.htm";
		}
		
		if (event.equals("getPremium5"))
		{
			if (player.getPremiumService() == 0)
			{
				if (st.getQuestItemsCount(premiumItemIt5) >= premiumItemCount5)
				{
					st.takeItems(premiumItemIt5, premiumItemCount5);
					PcAction.addPremiumServices(player, 30, player.getAccountName());
					player.broadcastUserInfo();
					return "PremiumAccount-Success.htm";
				}
				return "PremiumAccount-NoItems.htm";
			}
			return "PremiumAccount-Alredy.htm";
		}
		
		else if (event.equals("setNoble"))
		{
			if (!player.isNoble())
			{
				if (st.getQuestItemsCount(nobleItemId) >= nobleItemCount)
				{
					st.takeItems(nobleItemId, nobleItemCount);
					player.setNoble(true);
					player.setTarget(player);
					player.broadcastUserInfo();
					return "NoblesseServices-Success.htm";
				}
				return "NoblesseServices-NoItems.htm";
			}
			return "NoblesseServices-AlredyNoble.htm";
		}
		
		else if (event.startsWith("levelUp"))
		{
			if (player.isClanLeader())
			{
				if (event.equals("levelUp6Clan"))
				{
					if (st.getQuestItemsCount(clanLevelItemsId6) >= clanLevelItemsCount6)
					{
						st.takeItems(clanLevelItemsId6, clanLevelItemsCount6);
						player.getClan().changeLevel(6);
						player.getClan().broadcastClanStatus();
						player.sendMessage("Your clan is now level " + player.getClan().getLevel() + ".");
						player.setTarget(player);
						return "ClanLevelUp.htm";
					}
					return "ClanLevelUp-NoItems.htm";
				}
				else if (event.equals("levelUp7Clan"))
				{
					if (st.getQuestItemsCount(clanLevelItemsId7) >= clanLevelItemsCount7)
					{
						st.takeItems(clanLevelItemsId7, clanLevelItemsCount7);
						player.getClan().changeLevel(7);
						player.getClan().broadcastClanStatus();
						player.sendMessage("Your clan is now level " + player.getClan().getLevel() + ".");
						player.setTarget(player);
						return "ClanLevelUp.htm";
					}
					return "ClanLevelUp-NoItems.htm";
				}
				else if (event.equals("levelUp8Clan"))
				{
					if (st.getQuestItemsCount(clanLevelItemsId8) >= clanLevelItemsCount8)
					{
						st.takeItems(clanLevelItemsId8, clanLevelItemsCount8);
						player.getClan().changeLevel(8);
						player.getClan().broadcastClanStatus();
						player.sendMessage("Your clan is now level " + player.getClan().getLevel() + ".");
						player.setTarget(player);
						return "ClanLevelUp.htm";
					}
					return "ClanLevelUp-NoItems.htm";
				}
			}
			else
				return "ClanLevelUp-NoLeader.htm";
		}
		
		if (event.equals("setClanSkill"))
		{
			if (player.getClan() != null)
			{
				if (player.isClanLeader())
				{
					if (player.getClan().getLevel() == 8)
					{
						if (st.getQuestItemsCount(skillItemId) >= skillItemCount)
						{
							st.takeItems(skillItemId, skillItemCount);
							player.setTarget(player);
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(370, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(371, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(372, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(373, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(374, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(375, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(376, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(377, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(378, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(379, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(380, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(381, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(382, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(383, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(384, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(385, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(386, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(387, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(388, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(389, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(390, 3));
							st.getPlayer().getClan().addNewSkill(SkillTable.getInstance().getInfo(391, 1));
							player.broadcastUserInfo();
							return "ClanSkillServices-Success.htm";
						}
						return "ClanSkillServices-NoItems.htm";
					}
				}
			}
			return "ClanSkillServices-Error.htm";
		}
		
		else if (event.startsWith("changeName"))
		{
			try
			{
				String newName = event.substring(11);
				
				if (st.getQuestItemsCount(changeNameItemId) >= changeNameItemCount)
				{
					if (newName == null)
					{
						return "ChangeName.htm";
					}
					if (!newName.matches("^[a-zA-Z0-9]+$"))
					{
						player.sendMessage("Incorrect name. Please try again.");
						return "ChangeName.htm";
					}
					if (newName.equals(player.getName()))
					{
						player.sendMessage("Please, choose a different name.");
						return "ChangeName.htm";
					}
					else if (CharNameTable.getInstance().doesCharNameExist(newName))
					{
						player.sendMessage("The name " + newName + " already exists.");
						return "ChangeName.htm";
					}
					else
					{
						st.takeItems(changeNameItemId, changeNameItemCount);
						player.setName(newName);
						player.store();
						player.sendMessage("Your new character name is " + newName);
						player.broadcastUserInfo();
						player.getClan().broadcastClanStatus();
						
						return "ChangeName-Success.htm";
					}
				}
				return "ChangeName-NoItems.htm";
			}
			catch (Exception e)
			{
				player.sendMessage("Вы успешно сменили ник!");
				return "ChangeName.htm";
			}
		}
		
		if (event.equals("Colour1"))
		{
			if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
			{
				st.takeItems(changeColourItemId, changeColourItemCount);
				st.getPlayer().getAppearance().setNameColor(0x00d7ff);
				player.broadcastUserInfo();
				return "ColourServices-Success.htm";
			}
			return "ColourServices-NoItems.htm";
		}
		
		if (event.equals("Colour2"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setNameColor(0x339933);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour3"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setNameColor(0x669933);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour4"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setNameColor(0x996633);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour5"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setNameColor(0x000000);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour6"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setNameColor(0x3f3f3f);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour7"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setNameColor(0x008cff);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour8"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setNameColor(0x999933);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour9"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setNameColor(0xFF99CC);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour10"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setNameColor(0x663300);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour11"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setNameColor(0x663333);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour12"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setNameColor(0x993300);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}

		if (event.equals("Colour15"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setTitleColor(0x000000);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour16"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setTitleColor(0x000090);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour17"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setTitleColor(0x0000ff);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour18"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setTitleColor(0x009000);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour19"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setTitleColor(0x00FF00);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour20"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setTitleColor(0x900000);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour21"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setTitleColor(0xFF0000);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour22"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setTitleColor(0x009090);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour23"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setTitleColor(0x0090FF);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour24"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setTitleColor(0x00FFFF);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour25"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setTitleColor(0x900090);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour26"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setTitleColor(0x9000FF);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour27"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setTitleColor(0xff00ff);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour28"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setTitleColor(0x909000);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour29"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setTitleColor(0xFFFF00);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		
		if (event.equals("Colour30"))
		{
			{
				if (st.getQuestItemsCount(changeColourItemId) >= changeColourItemCount)
				{
					st.takeItems(changeColourItemId, changeColourItemCount);
					st.getPlayer().getAppearance().setTitleColor(0xffffff);
					player.broadcastUserInfo();
					return "ColourServices-Success.htm";
				}
				return "ColourServices-NoItems.htm";
			}
		}
		else if (event.startsWith("changeClanName"))
		{
			if (player.getClan() == null)
			{
				return "ChangeClanName-NoClan.htm";
			}
			try
			{
				String newClanName = event.substring(15);
				
				if (st.getQuestItemsCount(changeClanNameItemId) >= changeClanNameItemCount)
				{
					if (newClanName == null)
					{
						return "ChangeClanName.htm";
					}
					if (!player.isClanLeader())
					{
						player.sendMessage("Only the clan leader can change the clan name.");
						return "ChangeClanName.htm";
					}
					else if (player.getClan().getLevel() < clanMinLevel)
					{
						player.sendMessage("Your clan must be at least level " + clanMinLevel + " to change the name.");
						return "ChangeClanName.htm";
					}
					else if (!newClanName.matches("^[a-zA-Z0-9]+$"))
					{
						player.sendMessage("Incorrect name. Please try again.");
						return "ChangeClanName.htm";
					}
					else if (newClanName.equals(player.getClan().getName()))
					{
						player.sendMessage("Please, choose a different name.");
						return "ChangeClanName.htm";
					}
					else if (ClanTable.getInstance().getClanByName(newClanName) != null)
					{
						player.sendMessage("The name " + newClanName + " already exists.");
						return "ChangeClanName.htm";
					}
					else
					{
						st.takeItems(changeNameItemId, changeNameItemCount);
						player.getClan().setName(newClanName);
						
						try
						{
							Connection con = L2DatabaseFactory.getInstance().getConnection();
							PreparedStatement statement = con.prepareStatement("UPDATE clan_data SET clan_name=? WHERE clan_id=?");
							statement.setString(1, newClanName);
							statement.setInt(2, player.getClan().getClanId());
							statement.execute();
							statement.close();
						}
						catch (Exception e)
						{
							_log.info("Error updating clan name for player " + player.getName() + ". Error: " + e);
						}
						
						player.sendMessage("Your new clan name is " + newClanName);
						player.getClan().broadcastClanStatus();
						
						return "ChangeClanName-Success.htm";
					}
				}
				return "ChangeClanName-NoItems.htm";
			}
			catch (Exception e)
			{
				player.sendMessage("Please, insert a correct name.");
				return "ChangeClanName.htm";
			}
		}
		else if (event.startsWith("krp1"))
		{
			if (player.getClan() == null)
			{
				return "ClanReputationPoints-NoClan.htm";
			}
			else if (!player.isClanLeader())
			{
				return "ClanReputationPoints-NoLeader.htm";
			}
			else
			{
				if (st.getQuestItemsCount(clanReputationPointsItemId) >= clanReputationPointsItemCount)
				{
					st.takeItems(clanReputationPointsItemId, clanReputationPointsItemCount);
					player.getClan().setReputationScore(st.getPlayer().getClan().getReputationScore() + 5000, true);
					player.getClan().broadcastClanStatus();
					return "ClanReputationPoints-5000.htm";
				}
				return "ClanReputationPoints-NoItems.htm";
			}
		}
		
		else if (event.startsWith("krp2"))
		{
			if (player.getClan() == null)
			{
				return "ClanReputationPoints-NoClan.htm";
			}
			else if (!player.isClanLeader())
			{
				return "ClanReputationPoints-NoLeader.htm";
			}
			else
			{
				if (st.getQuestItemsCount(clanReputationPointsItemId1) >= clanReputationPointsItemCount1)
				{
					st.takeItems(clanReputationPointsItemId1, clanReputationPointsItemCount1);
					player.getClan().setReputationScore(st.getPlayer().getClan().getReputationScore() + 10000, true);
					player.getClan().broadcastClanStatus();
					return "ClanReputationPoints-10000.htm";
				}
				return "ClanReputationPoints-NoItems.htm";
			}
		}
		
		else if (event.startsWith("krp3"))
		{
			if (player.getClan() == null)
			{
				return "ClanReputationPoints-NoClan.htm";
			}
			else if (!player.isClanLeader())
			{
				return "ClanReputationPoints-NoLeader.htm";
			}
			else
			{
				if (st.getQuestItemsCount(clanReputationPointsItemId2) >= clanReputationPointsItemCount2)
				{
					st.takeItems(clanReputationPointsItemId2, clanReputationPointsItemCount2);
					player.getClan().setReputationScore(st.getPlayer().getClan().getReputationScore() + 20000, true);
					player.getClan().broadcastClanStatus();
					return "ClanReputationPoints-20000.htm";
				}
				return "ClanReputationPoints-NoItems.htm";
			}
		}
		return htmlText;
	}
}