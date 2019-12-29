from PIL import Image
from database import settingsdb as settings
from nicegrill import utils
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
            await message.edit("<i>Reply to a sticker first</i>")
            return
        sticker = await message.client.download_media(reply, "sticker.png")
        await message.client.send_file(message.chat_id, sticker)
        await message.delete()
        os.remove(sticker)

    async def setpackxxx(message):
        """Defines which pack your stickers will be added"""
        packid = utils.get_arg(message)
        if packid == "clear":
            await settings.delete("Pack")
            await message.edit("<i>Saved pack deleted successfully</i>")
            return
        pack = False
        async with message.client.conversation("@stickers") as conv:
            await conv.send_message("/addsticker")
            buttons = (await conv.get_response()).buttons
            await conv.send_message("/cancel")
            for button in buttons:
                for item in button:
                    if packid and (item.text == packid):
                        pack = True
        if not pack:
            await message.edit("<i>You don't own this pack</i>")
            return
        elif packid and pack:
            await settings.delete("Pack")
            await settings.set_pack(packid)
            await message.edit("<i>Pack saved successfully</i>")

    async def kangxxx(message):
        """Kangs a sticker or photo into you pack"""
        reply = await message.get_reply_message()
        if not reply.photo and not reply.sticker:
            await message.edit("<i>Reply to an image or get out</i>")
            return
        img = await reply.download_media()
        await Stickers.resize(message, img)
        packid = await settings.check_pack()
        if not packid:
            msg = "<i>You have no sticker pack set, so I'm creating a new pack</i>"
            task = "/newpack"
            pn = pn = "NiceGrill" if not message.sender.username else message.sender.username.capitalize()
            result = (
                "<i>Your new pack has been created.</i>\n"
                "<i>Click</i> <a href=https://t.me/addstickers/{}>Here</a> "
                "<i>to access it</i>")
            name, emoji, done, packid = False, False, False, False
            await Stickers.kang(
                message, msg, task, name, emoji, done, packid, result)
        else:
            msg = random.choice(Stickers.STRINGS)
            task = "/addsticker"
            result = (
                "<i>Sticker kanged succesfully.</i>\n"
                "<i>Click</i> <a href=https://t.me/addstickers/{}>Here</a> "
                "<i>to access it</i>".format(packid))
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
        async with message.client.conversation("@stickers", total_timeout=15) as conv:
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
            pn = "NiceGrill" if not message.sender.username else message.sender.username.capitalize()
            id = await conv.send_message(
                "{}sKangPack_{}_{}".format(
                    pn, (await message.get_sender()).id, random.randint(0, 99999999)))
            await message.client.send_read_acknowledge(conv.chat_id)
            await settings.set_pack(id.message)
            await message.edit(result.format(id.message))
