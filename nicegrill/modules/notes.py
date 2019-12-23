from nicegrill import utils
from database import notesdb as nicedb, settingsdb as settings
import logging


class Notes:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def savexxx(message):
        args = utils.arg_split_with(message, ",")
        storage = settings.check_asset()
        media = None
        reply = await message.get_reply_message()
        if not args:
            await message.edit("<b>You need to enter a note name</b>")
            return
        if len(args) == 1 and not message.is_reply:
            await message.edit(
                "<b>You need to either enter a a text or reply to a message to save as note</b>")
            return
        value = reply.text if message.is_reply else " ".join(args[1:])
        name = args[0]
        chatid = message.chat_id
        if reply and reply.media and not reply.web_preview:
            media = (await message.client.send_message(storage, reply)).id
        if nicedb.check_one("Notes", chatid, name):
            nicedb.update("Notes", {"Chat": chatid, "Key": name},
                chatid, name, value, media)
            await message.edit("<b>Note succesfully updated</b>")
        else:
            nicedb.add("Notes", chatid, name, value, media)
            await message.edit("<b>Note succesfully saved</b>")

    async def notesxxx(message):
        chatid = message.chat_id
        notes = nicedb.check("Notes", chatid)
        if not notes:
            await message.edit("<b>No notes found in this chat</b>")
            return
        caption = "<b>Notes you saved in this chat:\n\n</b>"
        list = ""
        for note in notes:
            list += "<b>  ◍ " + note["Key"] + "</b>\n"
        caption += list
        await message.edit(caption)

    async def clearxxx(message):
        args = utils.get_arg(message)
        chatid = message.chat_id
        if not nicedb.check_one("Notes", chatid, args):
            await message.edit("<b>No notes found in that name</b>")
            return
        nicedb.delete_one("Notes", chatid, args)
        await message.edit("<b>Note deleted successfully</b>")

    async def clearallxxx(message):
        chatid = message.chat_id
        if not nicedb.check("Notes", chatid):
            await message.edit("<b>There are no notes in this chat</b>")
            return
        nicedb.delete("Notes", chatid)
        await message.edit("<b>Notes cleared out successfully</b>")

    async def watchout(message):
        arg = message.text[1::]
        chatid = message.chat_id
        storage = settings.check_asset()
        note = nicedb.check_one("Notes", chatid, arg)
        if not note:
            return
        fetch = None if not note["Media"] else await message.client.get_messages(entity=storage, ids=note["Media"])
        if hasattr(fetch, "media"):
            await utils.reply(message, fetch)
            return
        await message.reply(note["Value"])
