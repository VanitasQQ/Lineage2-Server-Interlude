package handlers.voice;

import ru.catssoftware.Config;
import ru.catssoftware.Message;
import ru.catssoftware.gameserver.GameTimeController;
import ru.catssoftware.gameserver.SevenSigns;
import ru.catssoftware.gameserver.ThreadPoolManager;
import ru.catssoftware.gameserver.ai.CtrlIntention;
import ru.catssoftware.gameserver.datatables.SkillTable;
import ru.catssoftware.gameserver.handler.IVoicedCommandHandler;
import ru.catssoftware.gameserver.handler.VoicedCommandHandler;
import ru.catssoftware.gameserver.instancemanager.CoupleManager;
import ru.catssoftware.gameserver.instancemanager.DimensionalRiftManager;
import ru.catssoftware.gameserver.instancemanager.SiegeManager;
import ru.catssoftware.gameserver.model.L2FriendList;
import ru.catssoftware.gameserver.model.L2Skill;
import ru.catssoftware.gameserver.model.L2World;
import ru.catssoftware.gameserver.model.actor.instance.L2PcInstance;
import ru.catssoftware.gameserver.model.entity.Siege;
import ru.catssoftware.gameserver.model.restriction.AvailableRestriction;
import ru.catssoftware.gameserver.model.restriction.ObjectRestrictions;
import ru.catssoftware.gameserver.model.zone.L2Zone;
import ru.catssoftware.gameserver.network.SystemMessageId;
import ru.catssoftware.gameserver.network.serverpackets.ConfirmDlg;
import ru.catssoftware.gameserver.network.serverpackets.MagicSkillUse;
import ru.catssoftware.gameserver.network.serverpackets.SetupGauge;
import ru.catssoftware.gameserver.network.serverpackets.SystemMessage;
import ru.catssoftware.gameserver.skills.AbnormalEffect;
import ru.catssoftware.gameserver.util.Broadcast;

public class Wedding implements IVoicedCommandHandler
{
	private static final String[]	VOICED_COMMANDS	=
	{
		"engage",
		"gotolove",
		"divorce"
	};

	public boolean useVoicedCommand(String command, L2PcInstance activeChar, String target)
	{
		if (command.startsWith("engage"))
			return engage(activeChar);
		else if (command.startsWith("divorce"))
			return divorce(activeChar);
		else if (command.startsWith("gotolove"))
			return goToLove(activeChar);
		return false;
	}

	public synchronized boolean divorce(L2PcInstance activeChar)
	{
		if (activeChar.getPartnerId() == 0)
			return false;

		int _partnerId = activeChar.getPartnerId();
		int _coupleId = activeChar.getCoupleId();
		int AdenaAmount = 0;

		if (activeChar.isMaried())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_YOU_DIVORCED));
			AdenaAmount = (activeChar.getAdena() / 100) * Config.WEDDING_DIVORCE_COSTS;
			activeChar.getInventory().reduceAdena("Wedding", AdenaAmount, activeChar, null);
		}
		else
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_NO_PARTNER));

		L2PcInstance partner = L2World.getInstance().getPlayer(_partnerId);
		if (partner != null)
		{
			partner.setPartnerId(0);
			if (partner.isMaried())
				partner.sendMessage(Message.getMessage(partner, Message.MessageId.MSG_PARTNER_ASK_DIVORCE));
			else
				partner.sendMessage(Message.getMessage(partner, Message.MessageId.MSG_PARTNER_ASK_DIVORCE));

			// give adena
			if (AdenaAmount > 0)
				partner.addAdena("WEDDING", AdenaAmount, null, false);
		}

		CoupleManager.getInstance().deleteCouple(_coupleId);
		return true;
	}

	public boolean engage(L2PcInstance activeChar)
	{
		// check target
		if (activeChar.getTarget() == null)
		{
			activeChar.sendPacket(new SystemMessage(SystemMessageId.YOU_MUST_SELECT_A_TARGET));
			return false;
		}

		// check if target is a l2pcinstance
		if (!(activeChar.getTarget() instanceof L2PcInstance))
		{
			activeChar.sendPacket(new SystemMessage(SystemMessageId.INCORRECT_TARGET));
			return false;
		}

		// check if player is already engaged
		if (activeChar.getPartnerId() != 0)
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_HAVE_PARTNER));
			if (Config.WEDDING_PUNISH_INFIDELITY)
			{
				activeChar.startAbnormalEffect(AbnormalEffect.BIG_HEAD); // give player a Big Head
				// lets recycle the sevensigns debuffs
				int skillId;
				int skillLevel = 1;

				if (activeChar.getLevel() > 40)
					skillLevel = 2;

				if (activeChar.isMageClass())
					skillId = 4361;
				else
					skillId = 4362;

				L2Skill skill = SkillTable.getInstance().getInfo(skillId, skillLevel);
				if (activeChar.getFirstEffect(skill) == null)
				{
					skill.getEffects(activeChar, activeChar);
					SystemMessage sm = new SystemMessage(SystemMessageId.YOU_FEEL_S1_EFFECT);
					sm.addSkillName(skill);
					activeChar.sendPacket(sm);
				}
			}
			return false;
		}

		L2PcInstance ptarget = (L2PcInstance) activeChar.getTarget();

		// check if player target himself
		if (ptarget.getObjectId() == activeChar.getObjectId())
		{
			activeChar.sendPacket(new SystemMessage(SystemMessageId.INCORRECT_TARGET));
			return false;
		}

		if (ptarget.isMaried())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_TARGET_IS_MARIED));
			return false;
		}

		if (ptarget.getPartnerId() != 0)
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_TARGET_IS_MARIED));
			return false;
		}

		if (ptarget.isEngageRequest())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_TARGET_IS_MARIED));
			return false;
		}

		if (ptarget.getAppearance().getSex() == activeChar.getAppearance().getSex() && !Config.WEDDING_SAMESEX)
		{
			activeChar.sendPacket(new SystemMessage(SystemMessageId.INCORRECT_TARGET));
			return false;
		}

		if (!L2FriendList.isInFriendList(activeChar, ptarget))
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_PARTNER_MUST_BE_FRIEND));
			return false;
		}

		ptarget.setEngageRequest(true, activeChar.getObjectId());
		ConfirmDlg dlg = new ConfirmDlg(SystemMessageId.S1.getId());
		ptarget.sendPacket(dlg.addString(activeChar.getName() + Message.getMessage(activeChar, Message.MessageId.MSG_ASK_YOU_ENGAGE)));
		return true;
	}

	private static L2PcInstance checkGoToLoveState(L2PcInstance activeChar)
	{
		Siege siege = SiegeManager.getInstance().getSiege(activeChar);

		if (!activeChar.isMaried())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_NO_PARTNER));
			return null;
		}
		else if (activeChar.getPartnerId() == 0)
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_ERROR_CONTACT_GM));
			return null;
		}
		// Check to see if the player is in olympiad.
		else if (activeChar.isInOlympiadMode())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_NOT_ALLOWED_AT_THE_MOMENT));
			return null;
		}
		// Check to see if the player is in observer mode
		else if (activeChar.inObserverMode())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_NOT_ALLOWED_AT_THE_MOMENT));
			return null;
		}
		// Check to see if the player is in an event
		else if (activeChar.isInFunEvent())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_NOT_ALLOWED_AT_THE_MOMENT));
			return null;
		}
		// Check to see if the player is in a festival.
		else if (activeChar.isFestivalParticipant())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_NOT_ALLOWED_AT_THE_MOMENT));
			return null;
		}
		// Check to see if the player is in dimensional rift.
		else if (activeChar.isInParty() && activeChar.getParty().isInDimensionalRift())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_NOT_ALLOWED_AT_THE_MOMENT));
			return null;
		}
		// Check to see if player is in jail
		else if (activeChar.isInJail() || activeChar.isInsideZone(L2Zone.FLAG_JAIL))
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_NOT_ALLOWED_AT_THE_MOMENT));
			return null;
		}
		// Check if player is in Siege
		else if (siege != null && siege.getIsInProgress())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_NOT_ALLOWED_AT_THE_MOMENT));
			return null;
		}
		// Check if player is in Duel
		else if (activeChar.isInDuel())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_CURRENT_IN_COMBAT));
			return null;
		}
		// Check if player is a Cursed Weapon owner
		else if (activeChar.isCursedWeaponEquipped())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_NOT_ALLOWED_AT_THE_MOMENT));
			return null;
		}
		// Check if player is in a Monster Derby Track
		else if (activeChar.isInsideZone(L2Zone.FLAG_NOESCAPE))
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_NOT_ALLOWED_AT_THE_MOMENT));
			return null;
		}
		else if (ObjectRestrictions.getInstance().checkRestriction(activeChar, AvailableRestriction.PlayerGotoLove))
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_NOT_ALLOWED_AT_THE_MOMENT));
			return null;
		}
		L2PcInstance partner = L2World.getInstance().getPlayer(activeChar.getPartnerId());
		if (partner != null)
		{
			siege = SiegeManager.getInstance().getSiege(partner);
		}
		else
		{
			activeChar.sendPacket(new SystemMessage(SystemMessageId.TARGET_IS_NOT_FOUND_IN_THE_GAME));
			return null;
		}
		if (activeChar.getInstanceId() != partner.getInstanceId())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_PARTNER_NOT_AVAILABLE));
			return null;
		}
		else if (partner.isInJail() || partner.isInsideZone(L2Zone.FLAG_JAIL))
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_PARTNER_NOT_AVAILABLE));
			return null;
		}
		else if (partner.isInOlympiadMode())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_PARTNER_NOT_AVAILABLE));
			return null;
		}
		else if (partner.isDead())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_PARTNER_NOT_AVAILABLE));
			return null;
		}
		else if (partner.inObserverMode())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_PARTNER_NOT_AVAILABLE));
			return null;
		}
		else if (partner.isInDuel())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_PARTNER_NOT_AVAILABLE));
			return null;
		}
		else if (partner.isInFunEvent())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_PARTNER_NOT_AVAILABLE));
			return null;
		}
		else if (DimensionalRiftManager.getInstance().checkIfInRiftZone(partner.getX(), partner.getY(), partner.getZ(), false))
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_PARTNER_NOT_AVAILABLE));
			return null;
		}
		else if (partner.isFestivalParticipant())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_PARTNER_NOT_AVAILABLE));
			return null;
		}
		else if (siege != null && siege.getIsInProgress())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_PARTNER_NOT_AVAILABLE));
			return null;
		}
		else if (partner.isCursedWeaponEquipped())
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_PARTNER_NOT_AVAILABLE));
			return null;
		}
		else if (partner.isInsideZone(L2Zone.FLAG_NOESCAPE) || partner.isInsideZone(L2Zone.FLAG_NOSUMMON))
		{
			activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_PARTNER_NOT_AVAILABLE));
			return null;
		}
		else if (partner.isIn7sDungeon() && !activeChar.isIn7sDungeon())
		{
			int playerCabal = SevenSigns.getInstance().getPlayerCabal(activeChar);
			boolean isSealValidationPeriod = SevenSigns.getInstance().isSealValidationPeriod();
			int compWinner = SevenSigns.getInstance().getCabalHighestScore();

			if (isSealValidationPeriod)
			{
				if (playerCabal != compWinner)
				{
					activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_PARTNER_NOT_AVAILABLE));
					return null;
				}
			}
			else
			{
				if (playerCabal == SevenSigns.CABAL_NULL)
				{
					activeChar.sendMessage(Message.getMessage(activeChar, Message.MessageId.MSG_PARTNER_NOT_AVAILABLE));
					return null;
				}
			}
		}
		return partner;
	}

	public boolean goToLove(L2PcInstance activeChar)
	{
		if (activeChar.isCastingNow() || activeChar.isMovementDisabled() || activeChar.isMuted() || activeChar.isAlikeDead() || activeChar.isDead())
			return false;

		L2PcInstance partner = null;
		if ((partner = checkGoToLoveState(activeChar)) == null)
			return false;

		int teleportTimer = Config.WEDDING_TELEPORT_INTERVAL * 1000;

		activeChar.sendMessage("После " + teleportTimer / 60000 + " мин., Вы будете перемещы к партнеру.");
		activeChar.getInventory().reduceAdena("Wedding", Config.WEDDING_TELEPORT_PRICE, activeChar, null);

		activeChar.getAI().setIntention(CtrlIntention.AI_INTENTION_IDLE);
		//SoE Animation section
		activeChar.setTarget(activeChar);
		activeChar.disableAllSkills();

		MagicSkillUse msk = new MagicSkillUse(activeChar, 1050, 1, teleportTimer, 0, false);
		Broadcast.toSelfAndKnownPlayersInRadius(activeChar, msk, 810000);
		SetupGauge sg = new SetupGauge(0, teleportTimer);
		activeChar.sendPacket(sg);
		//End SoE Animation section

		EscapeFinalizer ef = new EscapeFinalizer(activeChar, partner.getX(), partner.getY(), partner.getZ(), partner.isIn7sDungeon());
		// continue execution later
		activeChar.setSkillCast(ThreadPoolManager.getInstance().scheduleGeneral(ef, teleportTimer));
		activeChar.forceIsCasting(GameTimeController.getGameTicks() + teleportTimer / GameTimeController.MILLIS_IN_TICK);
		return true;
	}

	private static class EscapeFinalizer implements Runnable
	{
		private L2PcInstance	_activeChar;
		private int				_partnerx;
		private int				_partnery;
		private int				_partnerz;
		private boolean			_to7sDungeon;

		EscapeFinalizer(L2PcInstance activeChar, int x, int y, int z, boolean to7sDungeon)
		{
			_activeChar = activeChar;
			_partnerx = x;
			_partnery = y;
			_partnerz = z;
			_to7sDungeon = to7sDungeon;
		}

		public void run()
		{
			if (_activeChar.isDead())
				return;

			_activeChar.enableAllSkills();
			_activeChar.setIsCastingNow(false);

			if (checkGoToLoveState(_activeChar) == null)
				return;

			try
			{
				_activeChar.setIsIn7sDungeon(_to7sDungeon);
				_activeChar.teleToLocation(_partnerx, _partnery, _partnerz);
			}
			catch (Exception e)
			{
				_log.error(e.getMessage(), e);
			}
		}
	}

	public String getDescription(String command)
	{
		if(command.equals("engage"))
			return "Помолвка с вашим возлюбленным.";
		if(command.equals("divorce"))
			return "Позволяет развестись если вы женаты.";
		if(command.equals("gotolove"))
			return "Перемещает вас к супругу.";
		return null;
	}

	public String[] getVoicedCommandList()
	{
		return VOICED_COMMANDS;
	}
	public static void main(String [] args) {
		if (Config.ALLOW_WEDDING)
			VoicedCommandHandler.getInstance().registerVoicedCommandHandler(new Wedding());
	}
	
}