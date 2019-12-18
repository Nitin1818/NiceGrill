import logging
import functools
import asyncio
from telethon import events, functions
from database.allinone import *
from telethon.sync import TelegramClient
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


class main:

    async def outgoing(message):
        mods = {}
        ls = [_init.modules[obj] for obj in _init.modules]
        for item in ls:
            mods.update(item)
        prefix = "." if not get_pref() else get_pref()[0][0]
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
                    except TypeError:
                        logger.exception("")
                        await message.edit("<b>Loading..</b>")
                        await message.client.send_file(entity=message.chat_id, message=message, file="error.txt",
                                                       caption="<b>NiceGrill has crashed. Command was .{}.\nCheck logs for more information.</b>".format(cmd))
                        await message.delete()
                        with open('error.txt', 'w'):
                            pass

    def read(client):
        watchouts = _init.watchouts
        for watchout in watchouts:
            client.add_event_handler(
                functools.partial(watchout),
                events.NewMessage(
                    outgoing=True,
                    incoming=True,
                    forwards=False))
        loop = asyncio.get_event_loop()
        rest = loop.create_task(main.restart(client))
        loop.run_until_complete(rest)

    async def restart(client):
        status = get_status()
        if not status:
            return
        chat = await client.get_entity(status[0][0])
        del_status()
        if status:
            try:
                await client.edit_message(entity=chat, text="<b>Restarted</b>", message=status[0][1])
            except Exception:
                pass

    async def storage(client):
        storages = []
        for storage in get_storage() if get_storage() else []:
            try:
                storages.append((await client.get_entity(storage[0])).id)
            except BaseException:
                pass
        del_storage()
        for storage in storages:
            add_storage(storage)
        controller = None if not get_storage() else get_storage()
        if not controller:
            channel = await client(functions.channels.CreateChannelRequest(
                title='NiceGrill Storage(DO NOT DELETE)',
                about='Storage channel for your files'))
            add_storage(channel.updates[1].channel_id)
            controller = get_storage()
        async for chat in client.iter_dialogs():
            if chat.id == int(str(-100) + str(controller[0][0])):
                return
