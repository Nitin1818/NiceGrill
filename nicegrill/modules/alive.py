import time
import logging
import platform
from telethon import version
from database import alivedb as nicedb
from nicegrill import utils
from datetime import datetime


class Stats:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def pingxxx(message):
        """Shows you the response speed of the bot"""
        a = datetime.now()
        await message.edit("<i>Ping...</i>")
        b = datetime.now()
        await message.edit("<i>Pong... {}ms</i>".format(round((b - a).microseconds / 1000), 2))

    async def alivexxx(message):
        """Show off to people with my bot using this command"""
        if not nicedb.check_name():
            nicedb.set_name("NiceGrill Bot")
        if not nicedb.check_msg():
            nicedb.set_message("Hold on, Whaa.. I'm alive 🤥🤥")
        username = nicedb.check_name()
        msg = nicedb.check_msg()
        tot = (
            "<i>{}</i>".format(msg)
            + "<b>\n\nUser's name:</b> <i>{}</i>\n<b>Python version:</b> <i>{}</i>\n"
            "<b>Telethon version:</b> <i>{}</i>\n<b>Current time:</b> <i>{}</i>" .format(
                username,
                platform.python_version(),
                version.__version__,
                time.strftime('%X %x')))
        await message.edit(tot)

    async def setalivexxx(message):
        """Sets your alive message"""
        msg = utils.get_arg(message)
        if not msg:
            nicedb.set_message("Hold on, Whaa.. I'm alive 🤥🤥")
            await message.edit("<i>Alive message set to default</i>")
            return
        if not nicedb.check_msg():
            nicedb.set_message(msg)
            await message.edit("<i>Message succesfully set</i>")
        else:
            nicedb.update({"ID": 2}, {"Message": msg})
            await message.edit("<i>Message succesfully updated</i>")

    async def setnamexxx(message):
        """Sets your alive name"""
        name = utils.get_arg(message)
        if not name:
            nicedb.set_message("NiceGrill Bot")
            await message.edit("<i>Alive message set to default</i>")
            return
        if not nicedb.check_name():
            nicedb.set_message(name)
            await message.edit("<i>Name succesfully set</i>")
        else:
            nicedb.update({"ID": 1}, {"Name": name})
            await message.edit("<i>Name succesfully updated</i>")
