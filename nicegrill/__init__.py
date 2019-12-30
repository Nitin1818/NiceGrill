#    This file is part of NiceGrill.

#    NiceGrill is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    NiceGrill is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with NiceGrill.  If not, see <https://www.gnu.org/licenses/>.

from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession
from nicegrill.main import Main
from nicegrill.modules import _init
from config import API_HASH, API_ID, SESSION, MONGO_URI
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
    asyncio.get_event_loop().create_task(_init.loads())
    asyncio.get_event_loop().create_task(_init.filestorage(client))
    asyncio.get_event_loop().create_task(Main.read(client))
    client.add_event_handler((Main.outgoing,
        events.NewMessage(outgoing=True, forwards=False))
    client.add_event_handler(Main.outgoing,
        events.MessageEdited(outgoing=True, forwards=False))
    print(f"Logged in as {(client.get_me()).first_name}")
    client.run_until_disconnected()
