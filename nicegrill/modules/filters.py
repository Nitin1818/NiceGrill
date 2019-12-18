from database.allinone import *
from .. import utils
import sqlite3

BLACKLIST = [".stop", ".stopall", ".filter"]


class Filters:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def filterxxx(message):
        args = utils.arg_split_with(message, ",")
        storage = await message.client.get_entity((get_storage())[0][0])
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
            media = (await message.client.send_file(entity=storage, file=reply.media)).id
        try:
            await del_filter(chatid, name)
            await add_filter(chatid, name, value, media)
        except sqlite3.OperationalError:
            pass
            await add_filter(chatid, name, value, media)
        await message.edit("<b>Filter succesfully saved</b>")
        message.message = ""

    async def filtersxxx(message):
        chatid = message.chat_id
        filters = await get_filters(chatid)
        if not filters:
            await message.edit("<b>No filters found in this chat</b>")
            return
        caption = "<b>Filters you saved in this chat:\n\n</b>"
        list = ""
        for filter in filters:
            list += "<b>  - " + filter[1] + "</b>\n"
        caption += list
        await message.edit(caption)
        message.message = ""

    async def stopxxx(message):
        args = utils.get_arg(message)
        chatid = message.chat_id
        filter = await del_filter(chatid, args)
        if not filter:
            await message.edit("<b>No filters found in that name</b>")
            return
        await message.edit("<b>Filters deleted successfully</b>")
        message.message = ""

    async def stopallxxx(message):
        chatid = message.chat_id
        filters = await del_filters(chatid)
        if not filters:
            await message.edit("<b>There are no filters in this chat</b>")
            return
        await message.edit("<b>Filters cleared out successfully</b>")
        message.message = ""

    async def watchout(message):
        for i in BLACKLIST:
            if message.text.startswith(i):
                return
        arg = message.text
        chatid = message.chat_id
        if get_storage():
            storage = await message.client.get_entity((get_storage())[0][0])
        filters = await get_filters(chatid)
        if not filters:
            return
        for list in filters:
            if list[1] in arg:
                value = list[2]
                id = list[3]
                if id:
                    fetch = await message.client.get_messages(entity=storage.id, ids=id)
                    await message.client.send_message(entity=chatid, file=fetch.media, message=value)
                    return
                await message.reply(value)
