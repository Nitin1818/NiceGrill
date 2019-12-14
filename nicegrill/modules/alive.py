import time
import logging
import platform
import logging
from telethon import version
from .. import utils
from database.allinone import setStats, getStats
from datetime import datetime


class Stats:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def pingxxx(message):
        """Shows you the response speed of the bot"""
        a = datetime.now()
        await message.edit("<i>Ping...</i>")
        b = datetime.now()
        await message.edit("<i>Pong... {}ms</i>".format((b - a).microseconds / 1000))

    async def alivexxx(message):
        """Show off to people with my bot using this command"""
        username = "<i>NiceGrill bot</i>" if not getStats()[0][1] else getStats()[0][1]
        msg = "<i>Hold on...Whaaa.. I'm alive</i> 🤥🤥" if not getStats()[0][2] else getStats()[0][2]
        tot = (
            "<i>{}</i>".format(msg) +
            "<b>\n\nUser's name:</b> <i>{}</i>\n<b>Python version:</b> <i>{}</i>\n"
            "<b>Telethon version:</b> <i>{}</i>\n<b>Current time:</b> <i>{}</i>"
            .format(username, platform.python_version(), version.__version__, time.strftime('%X %x')))
        await message.edit(tot)


    async def setnamexxx(message):
        """Sets your alive name"""
        if not utils.get_arg(message):
            command = "UPDATE stats SET name = '<i>NiceGrill bot</i>' WHERE id=1"
            setStats(command)
            return
        command = f"UPDATE stats SET name = \"{utils.get_arg(message)}\" WHERE id=1"
        setStats(command)
        await message.edit("<b>Name succesfully updated</b>")

    async def setalivexxx(message):
        """Sets your alive message, yes, yes i actually allow people to customize their bot"""
        if not utils.get_arg(message):
            command = "UPDATE stats SET msg = '<i>Hold on...Whaaa.. I'm alive</i> 🤥🤥' WHERE id=1"
            setStats(command)
            return
        command = f"UPDATE stats SET msg = \"{utils.get_arg(message)}\" WHERE id=1"
        setStats(command)
        await message.edit("<b>Alive message succesfully updated</b>")