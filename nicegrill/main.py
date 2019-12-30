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

import logging
import asyncio
from telethon import events
from database import settingsdb as settings
from nicegrill.modules import _init

logging.basicConfig(
    filename='error.txt',
    level=logging.ERROR,
    format='%(asctime)s  %(name)s  %(levelname)s: %(message)s')

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('error.txt')
file_handler.setLevel(logging.ERROR)
formatter = logging.Formatter(
    '%(asctime)s  %(name)s  %(levelname)s: %(message)s')
logger.addHandler(file_handler)


class Main:

    loadclient = None

    async def outgoing(message):
        mods = {}
        ls = [_init.modules[obj] for obj in _init.modules]
        for item in ls:
            mods.update(item)
        prefix = await settings.check_prefix()
        if getattr(message, "message") and message.text.startswith(prefix):
            if message.text.startswith(prefix * 2):
                await message.edit(message.text[1:])
                return
            args = (message.text[2:]).split(" ") if message.text.startswith(
                prefix + " ") else message.text[1:].split(" ")
            if "\n" in message.text.split(" ")[0]:  # Prevention for new lines
                args = message.text[1:].split("\n")
            for cmd in mods:
                if args[0] == cmd:
                    try:
                        await mods[cmd](message)
                    except BaseException:
                        logger.exception("")
                        await message.edit("<b>Loading..</b>")
                        await message.client.send_file(entity=message.chat_id, message=message, file="error.txt",
                                                       caption="<b>NiceGrill has crashed. Command was .{}.\n"
                                                       "Check logs for more information.</b>".format(cmd))
                        await message.delete()
                        with open('error.txt', 'w'):
                            pass

    async def read(client):
        watchouts = _init.watchouts
        for watchout in watchouts:
            client.add_event_handler(watchout,
                events.NewMessage(outgoing=True, incoming=True))
        await Main.restart(client)

    async def restart(client):
        restart = await settings.check_restart()
        if not restart:
            return
        try:
            chat = await client.get_entity(restart["Chat"])
            await client.edit_message(entity=chat, text="<b>Restarted</b>", message=restart["Message"])
        except Exception:
            pass
        except ValueError:
            pass
        await settings.delete("Restart")
