import os
import sys
import asyncio
import logging
from database.allinone import add_status, del_status, get_status, add_storage, del_storage
from telethon.errors import rpcerrorlist
from telethon import functions
from nicegrill import utils


class Misc:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def restartxxx(message):
        msg = await message.edit("<b>Restarting...</b>")
        if get_status():
            del_status()
        await add_status(True, msg.chat_id, msg.id)
        if os.path.isfile(
                "database/database.db") and not os.path.getsize("database/database.db") == 0:
            db = await message.client.upload_file("database/database.db")
            await message.client.send_file((await message.client.get_me()).id, db)
        os.execl(sys.executable, sys.executable, *sys.argv)

    async def shutdownxxx(message):
        await message.edit("<b>Shutting down...</b>")
        await message.client.disconnect()

    async def logsxxx(message):
        try:
            await message.client.send_file(entity=message.chat_id, file="error.txt",
                                           caption="<b>Here's logs in ERROR level.</b>")
            await message.delete()
            with open('error.txt', 'w'):
                pass
        except rpcerrorlist.FilePartsInvalidError:
            await message.edit("<b>There is no log in ERROR level</b>")
            return

    async def updatexxx(message):
        if not utils.get_arg(message):
            os.popen("git fetch")
            await message.edit("<i>Checking...</i>")
            await asyncio.sleep(1)
            updates = os.popen(
                "git log --pretty=format:'%s - %an (%cr)' --abbrev-commit"
                " --date=relative master..origin/master").readlines()
            if updates:
                ls = "<b>Updates:</b>\n\n"
                for i in updates:
                    ls += f"◍  <i>{i.capitalize()}</i>"
                await message.edit(
                    f"{ls}\n\n<b>Type</b> <i>.update now</i> <b>to update</b>")
            else:
                await message.edit("<i>Well, no updates yet</i>")
            return
        print(utils.get_arg(message))
        await message.edit("<i>Updating</i>")
        update = os.popen("git pull").read()
        if "up to date" not in update:
            await message.edit(f"<i>Succesfully Updated</i>")
            await asyncio.sleep(1.5)
            await Misc.restartxxx(message)
        else:
            await message.edit(f"<i>{update}</i>")

    async def assetxxx(message):
        arg = utils.get_arg(message)
        if arg == "make":
            channel = await message.client(functions.channels.CreateChannelRequest(
                title='NiceGrill Storage(DO NOT DELETE)',
                about='Storage channel for your files'))
            arg = channel.updates[1].channel_id
        if not str(arg).isdigit() and arg != "make":
            await message.edit(f"<i>Either put an ID or type .asset make</i>")
            return
        del_storage()
        add_storage(int(arg))
        await message.edit("<b>Added successfully</b>")