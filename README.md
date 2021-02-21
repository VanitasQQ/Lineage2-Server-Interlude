# Lineage2 Server Interlude (Multicraft x100)
Готовый cервер Lineage 2 Interlude. За основу взято ядро на Java. (Если память мне не изменяет, то ядро l2jLovely)

## Требования:
- Система: Linux (Ubuntu/Debian/ArchLinux), Windows Xp и выше.
- Процессор: 2-ух ядерный 2.7 ГГц.
- Оперативная память: For Linux [400 MB] For Windows [1GB]
- Java: 7-я версия и выше.

## Установка:
- Залить backup БД через Navicat. (Создать 2 базы [la2_login] и [la2_game]
- Прописать пароль к root пользователю в конфигах GameServer'a и LoginServer'a
- Регистрируем GamerServer (создаем hexid файл), и закидуем его в: ~\game\config\network
- Запускаем LoginServer, и после запуска LoginServer'a запускаем GamerServer.
- P.S. В комплекте L2_EDIT для изменения l2.ini файла. 
