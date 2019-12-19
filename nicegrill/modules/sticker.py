from PIL import Image
from database.allinone import set_Packid, get_Packid, del_Packid
from .. import utils
import random
import logging
import os


class Stickers:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    EMOJI = [
        "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "☺", "😊", "😇", "🙂",
        "🙃", "😉", "😌", "😍", "🥰", "😘", "😗", "😙", "😚", "😋", "😛", "😝",
        "😜", "🤪", "🤨", "🧐", "🤓", "😎", "🤩", "🥳", "😏", "😒", "😞", "😔",
        "😟", "😕", "🙁", "☹", "😣", "😖", "😫", "😩", "🥺", "😢", "😭", "😤",
        "😠", "😡", "🤬", "🤯", "😳", "🥵", "🥶", "😱", "😨", "😰", "😥", "😓",
        "🤗", "🤔", "🤭", "🤫", "🤥", "😶", "😐", "😑", "😬", "🙄", "😯", "😦",
        "😧", "😮", "😲", "😴", "🤤", "😪", "😵", "🤐", "🥴", "🤢", "🤮", "🤧",
        "😷", "🤒", "🤕", "🤑", "🤠", "😈", "👿", "🎃", "😺", "😸", "😹", "😼",
        "😽", "🙀", "😿", "😾"]

    STRINGS = [
        "<i>Whatcha doin'! Stop lookin' at me while i kang, that's rude..!</i>",
        "<i>Hello, hey, I'mma just steal this sticker for a sec and be gone with it. Would you mind..?</i>",
        "<i>Woah, nice sticker! Look! A fish is flying! Look at the sky! While I kang 😈...</i>",
        "<i>Yea, I'm kanging this, so what? Oh shit! Run, run, run..!</i>",
        "<i>Aww, baby..! Who is a nice little sticker, yes you are, yes you are! Come over here...</i>"]

    async def dumpitxxx(message):
        reply = await message.get_reply_message()
        if not reply or not reply.sticker:
            await message.edit("<b>Reply to a sticker first</b>")
            return
        sticker = await message.client.download_media(reply, "sticker.png")
        await message.client.send_file(message.chat_id, sticker)
        await message.delete()
        os.remove(sticker)

    async def setpackxxx(message):
        """Defines which pack your stickers will be added"""
        packid = utils.get_arg(message)
        if packid == "clear":
            del_Packid()
            await message.edit("<b>Saved pack deleted successfully</b>")
            return
        pack = False
        async with message.client.conversation(429000) as conv:
            await conv.send_message("/addsticker")
            buttons = (await conv.get_response()).buttons
            await conv.send_message("/cancel")
            for button in buttons:
                for item in button:
                    if packid and (item.text == packid):
                        pack = True
        if not pack:
            await message.edit("<b>You don't own this pack</b>")
            return
        elif packid and pack:
            del_Packid()
            set_Packid(packid)
            await message.edit("<b>Pack saved successfully</b>")

    async def kangxxx(message):
        """Kangs a sticker or photo into you pack"""
        reply = await message.get_reply_message()
        if not reply.photo and not reply.sticker:
            await message.edit("<b>Reply to an image or get out</b>")
            return
        img = await reply.download_media()
        await Stickers.resize(message, img)
        packid = None if not get_Packid() else get_Packid()[0][0]
        if not packid:
            msg = "<b>You have no sticker pack set, so I'm creating a new pack</b>"
            task = "/newpack"
            result = (
                "<b>Your new pack has been created.</b>\n"
                "<b>Click</b> <a href=https://t.me/addstickers/{}sKangPack_{}>Here</a> "
                "<b>to access it</b>".format(message.sender.username.capitalize(), (await message.get_sender()).id))
            name, emoji, done, packid = False, False, False, False
            await Stickers.kang(
                message, msg, task, name, emoji, done, packid, result)
        else:
            msg = random.choice(Stickers.STRINGS)
            task = "/addsticker"
            result = (
                "<b>Sticker kanged succesfully.</b>\n"
                "<b>Click</b> <a href=https://t.me/addstickers/{}>Here</a> "
                "<b>to access it</b>".format(packid))
            emoji = utils.get_arg(message) if utils.get_arg(message) else False
            name, done = True, True
            await Stickers.kang(
                message, msg, task, name, emoji, done, packid, result)

    async def resize(message, img):
        file = Image.open(img)
        file.thumbnail((512, 512), Image.ANTIALIAS)
        if os.path.isfile(img):
            os.remove(img)
        file.save("sticker.png")
        return True

    async def kang(message, msg, task, name, emoji, done, packid, result):
        check_sticker_chat = False
        async with message.client.conversation(429000, total_timeout=15) as conv:
            async for chat in message.client.iter_dialogs():
                if 429000 == chat.id:
                    check_sticker_chat = True
                    await message.client.send_read_acknowledge(conv.chat_id)
            if not check_sticker_chat:
                await conv.send_message("/start")
            await message.edit(msg)
            await conv.send_message(task)
            await message.client.send_read_acknowledge(conv.chat_id)
            id = None if not packid else await conv.send_message(packid)
            await message.client.send_read_acknowledge(conv.chat_id)
            packname = None if name is True else await conv.send_message(
                "{}'s Kang Pack Vol".format(message.sender.first_name))
            await message.client.send_read_acknowledge(conv.chat_id)
            await message.client.send_file(
                entity=429000, file="sticker.png", force_document=True)
            await message.client.send_read_acknowledge(conv.chat_id)
            os.remove("sticker.png")
            pickemoji = random.choice(Stickers.EMOJI) if not emoji else emoji
            await conv.send_message(pickemoji)
            await message.client.send_read_acknowledge(conv.chat_id)
            if done:
                await conv.send_message("/done")
                await message.client.send_read_acknowledge(conv.chat_id)
                await message.edit(result)
                return
            await conv.send_message("/publish")
            await message.client.send_read_acknowledge(conv.chat_id)
            await conv.send_message("/skip")
            await message.client.send_read_acknowledge(conv.chat_id)
            id = await conv.send_message(
                "{}sKangPack_{}_{}".format(
                    message.sender.username.capitalize(), (await message.get_sender()).id, random.randint(0, 99999999)))
            await message.client.send_read_acknowledge(conv.chat_id)
            set_Packid(id)
            await message.edit(result)
