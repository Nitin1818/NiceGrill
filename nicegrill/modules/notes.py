from database.allinone import *
from .. import utils
import sqlite3
import logging

class Notes:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def savexxx(message):
        args = utils.arg_split_with(message, ",")
        storage = await message.client.get_entity((get_storage())[0][0])
        media = None
        reply = await message.get_reply_message()
        if not args:
            await message.edit("<b>You need to enter a note name</b>")
            return
        if len(args) == 1 and not message.is_reply:
            await message.edit("<b>You need to either enter a a text or reply to a message to save as note</b>")
            return
        value = reply.text if message.is_reply else " ".join(args[1:])
        name = args[0]
        chatid = message.chat_id
        if reply and reply.media and not reply.web_preview:
            media = (await message.client.send_file(entity=storage, file=reply.media)).id
        try:
            await del_note(chatid, name)
            await add_note(chatid, name, value, media)
        except sqlite3.OperationalError:
            pass
            await add_note(chatid, name, value, media)
        await message.edit("<b>Note succesfully saved</b>")

    async def notesxxx(message):
        chatid = message.chat_id
        notes = await get_notes(chatid)
        if not notes:
            await message.edit("<b>No notes found in this chat</b>")
            return
        caption = "<b>Notes you saved in this chat:\n\n</b>"
        list = ""
        for note in notes:
            list += "<b>  - " + note[0][:] + "</b>\n"
        caption += list
        await message.edit(caption)

    async def clearxxx(message):
        args = utils.get_arg(message)
        chatid = message.chat_id
        note = await del_note(chatid, args)
        if not note:
            await message.edit("<b>No notes found in that name</b>")
            return
        await message.edit("<b>Note deleted successfully</b>")

    async def clearallxxx(message):
        chatid = message.chat_id
        notes = await del_notes(chatid)
        if not notes:
            await message.edit("<b>There are no notes in this chat</b>")
            return
        await message.edit("<b>Notes cleared out successfully</b>")

    async def watchout(message):
        arg = message.text[1::]
        chatid = message.chat_id
        if get_storage():
            storage = await message.client.get_entity((get_storage())[0][0])
        notes = await get_note(chatid, arg)
        if not notes:
            return
        fetch = None if not notes[0][1] else await message.client.get_messages(entity=storage.id, ids=notes[0][1])
        if hasattr(fetch, "media"):
            await message.client.send_message(entity=chatid, file=fetch.media, message=notes[0][0])
            return
        await message.reply(notes[0][0])
