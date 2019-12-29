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

from database import storagedb as nicedb, settingsdb as settings
from nicegrill import utils
import random
import logging

class Store:

    async def storexxx(message):
        if not await settings.check_asset():
            await message.edit(
                "<b>You haven't set a storage chat yet, it's:</b>\n\n"
                "<i>'.asset make'</i><b> for auto setup</b>\n"
                "<i>'.asset <chatid>'</i><b> to set a specific chat</b>\n")
            return
        reply = await message.get_reply_message()
        if not reply or not reply.media:
            await message.edit("<i>Make sure to reply to a message first</i>")
            return
        args = utils.get_arg(message).split()
        if len(args) <= 1:
            await message.edit("<i>Specify a file name and a path</i>")
            return
        name, path = args[0], args[1]
        file = await message.client.send_message(await settings.check_asset(), reply)
        if not await nicedb.check_one(name):
            await nicedb.save_file(name, path, file.id)
        else:
            await nicedb.update_file(name, path, file.id)
        await message.edit("<i>File saved to be restored</i>")

    async def delfilexxx(message):
        name = utils.get_arg(message)
        if not name:
            await message.edit("<i>Specify a file name</i>")
            return
        if not await nicedb.check_one(name):
            await message.edit("<i>File doesn't exist in database</i>")
            return
        await nicedb.delete_one(name)
        await message.edit("<i>Successfully removed</i>")

    async def storedxxx(message):
        await message.edit("<i>Retrieving..</i>")
        files = await nicedb.check()
        if not files:
            await message.edit("<i>There's no saved file</i>")
            return
        ls = ""
        for item in files:
            ls += f"<b>File:</b> <i>{item['Name']}</i>\n<b>Will be restored to:</b> <i>{item['Path']}</i>\n\n"
        await message.edit(ls)
