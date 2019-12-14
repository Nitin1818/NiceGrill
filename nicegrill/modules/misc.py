import os
import sys
import asyncio
import logging
from database.allinone import add_status, del_status, get_status, get_storage
from telethon.errors import rpcerrorlist

class Misc:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def restartxxx(message):
        msg = await message.edit("<b>Restarting...</b>")
        if get_status():
            del_status()
        await add_status(True, msg.chat_id, msg.id)
        os.execl(sys.executable, sys.executable, *sys.argv)


    async def shutdownxxx(message):
        await message.edit("<b>Shutting down...</b>")
        await message.client.disconnect()

    async def logsxxx(message):
        try:
            await message.client.send_file(entity=message.chat_id, file="error.log",
            caption="<b>Here's logs in ERROR level.</b>")
            await message.delete()
            with open('error.log', 'w'):
                pass
        except rpcerrorlist.FilePartsInvalidError as e:
            await message.edit("<b>There is no log in ERROR level</b>")
            return

    async def updatexxx(message):
        await message.edit("<b>Updating</b>")
        update = await asyncio.create_subprocess_shell(
            "git init && git remote add origin https://github.com/erenmetesar/NiceGrill &&"
            "git pull origin master",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await update.communicate()
        if stdout:
            await message.edit("<b>Updated</b>")
        elif stderr:
            await message.edit(f"<b>{stderr.decode()}</b>")
            await asyncio.sleep(1)
            await message.edit("<b>Updated</b>")
        else:
            await message.edit("<b>Update Failed</b>")