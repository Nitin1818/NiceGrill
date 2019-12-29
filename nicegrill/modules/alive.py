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
        if not await nicedb.check_name():
            await nicedb.set_name("NiceGrill Bot")
        if not await nicedb.check_msg():
            await nicedb.set_message("Hold on, Whaa.. I'm alive 🤥🤥")
        username = await nicedb.check_name()
        msg = await nicedb.check_msg()
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
            await nicedb.set_message("Hold on, Whaa.. I'm alive 🤥🤥")
            await message.edit("<i>Alive message set to default</i>")
            return
        if not await nicedb.check_msg():
            await nicedb.set_message(msg)
            await message.edit("<i>Message succesfully set</i>")
        else:
            await nicedb.update({"ID": 2}, {"Message": msg})
            await message.edit("<i>Message succesfully updated</i>")

    async def setnamexxx(message):
        """Sets your alive name"""
        name = utils.get_arg(message)
        if not name:
            await nicedb.set_message("NiceGrill Bot")
            await message.edit("<i>Alive message set to default</i>")
            return
        if not await nicedb.check_name():
            await nicedb.set_message(name)
            await message.edit("<i>Name succesfully set</i>")
        else:
            await nicedb.update({"ID": 1}, {"Name": name})
            await message.edit("<i>Name succesfully updated</i>")
