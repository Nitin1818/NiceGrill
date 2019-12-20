from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession
from nicegrill import dbsets
from nicegrill.main import main
from nicegrill.modules import _init
from config import API_HASH, API_ID, SESSION
import functools
import asyncio
import os


if not API_ID or not API_HASH:
    API_ID = int(input("Enter your API ID:"))
    API_HASH = input("Enter your API HASH:")
    file = open("config.py", "a+")
    file.write(f"API_ID={API_ID}\nAPI_HASH=\"{API_HASH}\"")
    file.close()

if not SESSION:
    print("Run generate_session.py to create a string session first")
    quit()

async def restore(client):
    async for msg in client.iter_messages((await client.get_me()).id, limit=2):
        if msg.document and msg.document.attributes[0].file_name == "database.db":
            await client.download_media(msg)
            await msg.delete()
    if not os.path.isfile("database.db"):
        return
    os.rename("database.db", "database/database.db")


with TelegramClient(StringSession(SESSION), API_ID, API_HASH) as client:
    asyncio.get_event_loop().create_task(restore(client))
    client.parse_mode = 'html'
    _init.loads()
    main.read(client)
    client.add_event_handler(
        functools.partial(main.outgoing),
        events.NewMessage(outgoing=True, forwards=False))
    client.add_event_handler(
        functools.partial(main.outgoing),
        events.MessageEdited(outgoing=True, forwards=False))
    print(f"Logged in as {(client.get_me()).first_name}")
    client.run_until_disconnected()
