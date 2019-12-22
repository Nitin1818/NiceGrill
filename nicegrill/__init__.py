from database import mongo
from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession
from nicegrill.main import main
from nicegrill.modules import _init
from config import API_HASH, API_ID, SESSION, MONGO_URI
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

if not MONGO_URI:
    print("Haven't you set your MongoDB URI yet?")
    quit()

with TelegramClient(StringSession(SESSION), API_ID, API_HASH) as client:
    client.parse_mode = 'html'
    _init.loads()
    asyncio.get_event_loop().create_task(_init.filestorage(client))
    main.read(client)
    client.add_event_handler(
        functools.partial(main.outgoing),
        events.NewMessage(outgoing=True, forwards=False))
    client.add_event_handler(
        functools.partial(main.outgoing),
        events.MessageEdited(outgoing=True, forwards=False))
    print(f"Logged in as {(client.get_me()).first_name}")
    client.run_until_disconnected()
