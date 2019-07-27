package handlers;

//import ru.catssoftware.gameserver.datatables.NpcTable;
//import ru.catssoftware.gameserver.idfactory.IdFactory;
import ru.catssoftware.gameserver.model.actor.instance.L2NpcBufferInstance;
import ru.catssoftware.gameserver.model.entity.events.GameEvent.IGameEventScript;
import ru.catssoftware.gameserver.model.entity.events.TvT.TvT;

public class TVTHandler implements IGameEventScript {

	private L2NpcBufferInstance _eventBuffer;
	@Override
	public void onFinish(int instanceId) {
		// Удаляем бафера по окончанию эвента
		if(_eventBuffer!=null)
			_eventBuffer.deleteMe();
		_eventBuffer = null;
	}

	@Override
	public void onStart(int instanceId) {
/*		// Создаем  NPC-баффера
		_eventBuffer = new L2NpcBufferInstance(IdFactory.getInstance().getNextId(),NpcTable.getInstance().getTemplate(50000));
		// Переносим его в инстанс где идет эвент
		_eventBuffer.setInstanceId(instanceId);
		// Спавним его
		_eventBuffer.spawnMe(150345,46534,-3415);
*/
	}
	public static void main(String [] args) {
		// Устанавливаем хандлер для ТВТ эвента
		TvT.getInstance().setEventScript(new TVTHandler());
	}
}
