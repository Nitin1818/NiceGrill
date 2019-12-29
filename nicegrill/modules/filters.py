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

from database import notesdb as nicedb, settingsdb as settings
from nicegrill import utils
import logging

BLACKLIST = [".stop", ".stopall", ".filter"]


class Filters:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def filterxxx(message):
        args = utils.arg_split_with(message, ",")
        storage = await settings.check_asset()
        media = None
        reply = await message.get_reply_message()
        if not args:
            await message.edit("<b>You need to enter a filter name</b>")
            return
        if len(args) == 1 and not message.is_reply:
            await message.edit("<b>You need to either enter a a text or reply to a message to save as filter</b>")
            return
        if message.is_reply:
            value = reply.text
        else:
            value = " ".join(args[1:])
        name = args[0]
        chatid = message.chat_id
        if reply and reply.media and not reply.web_preview:
            media = (await message.client.send_message(storage, reply)).id
        if await nicedb.check_one("Filters", chatid, name):
            await nicedb.update("Filters", {"Chat": chatid, "Key": name},
                chatid, name, value, media)
            await message.edit("<b>Filter succesfully updated</b>")
        else:
            await nicedb.add("Filters", chatid, name, value, media)
            await message.edit("<b>Filter succesfully saved</b>")

    async def filtersxxx(message):
        chatid = message.chat_id
        filters = await nicedb.check("Filters", chatid)
        if not filters:
            await message.edit("<b>No filter found in this chat</b>")
            return
        caption = "<b>Word(s) you filtered in this chat:\n\n</b>"
        list = ""
        for filter in filters:
            list += "<b>  ◍ " + filter["Key"] + "</b>\n"
        caption += list
        await message.edit(caption)

    async def stopxxx(message):
        args = utils.get_arg(message)
        chatid = message.chat_id
        if not await nicedb.check_one("Filters", chatid, args):
            await message.edit("<b>No filter found in that name</b>")
            return
        await nicedb.delete_one("Filters", chatid, args)
        await message.edit("<b>Filter deleted successfully</b>")

    async def stopallxxx(message):
        chatid = message.chat_id
        if not await nicedb.check("Filters", chatid):
            await message.edit("<b>There are no filters in this chat</b>")
            return
        await nicedb.delete("Filters", chatid)
        await message.edit("<b>Filters cleared out successfully</b>")

    async def watchout(message):
        for i in BLACKLIST:
            if message.text.startswith(i):
                return
        arg = message.text
        chatid = message.chat_id
        storage = await settings.check_asset()
        filters = await nicedb.check("Filters", chatid)
        if not filters:
            return
        for item in filters:
            if item["Key"] in arg:
                value = item["Value"] if not item["Media"] else item["Media"]
                if item["Media"]:
                    fetch = await message.client.get_messages(entity=storage, ids=value)
                    await message.client.send_message(chatid, fetch, reply_to=message.id)
                    return
                await message.reply(value)
