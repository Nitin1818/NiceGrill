from telethon.sync import TelegramClient, events
import functools
import asyncio
from nicegrill.main import main
from nicegrill.modules import _init
from nicegrill import loader
from nicegrill import dbsets
from database.allinone import get_storage


API_ID = 1234
API_HASH = "1234"


with TelegramClient('NiceGrill', API_ID, API_HASH) as client:
    client.parse_mode = 'html'
    _init.loads()
    loop = asyncio.get_event_loop()
    task = loop.create_task(main.storage(client))
    loop.run_until_complete(task)
    main.read(client)
    client.add_event_handler(
       functools.partial(main.outgoing),
       events.NewMessage(outgoing=True, forwards=False))
    client.add_event_handler(
       functools.partial(main.outgoing),
       events.MessageEdited(outgoing=True, forwards=False))
    print(f"Logged in as {(client.get_me()).first_name}")
    client.run_until_disconnected()
