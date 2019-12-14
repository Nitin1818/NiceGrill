import os
import sys
import asyncio
import logging
from database.allinone import add_status, del_status, get_status
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
        exit()
         
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