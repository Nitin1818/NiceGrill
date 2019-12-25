import logging
import os
from urllib import request
from nicegrill import utils

class Renamer:

    async def rnxxx(message):
        reply = await message.get_reply_message()
        name = utils.get_arg(message)
        if not message.is_reply or not reply.media:
            await message.edit("<i>Reply to a message with media</i>")
            return
        if not name:
            await message.edit("<i>Specify a new name for the file</i>")
            return
        await message.edit("<i>Downloading..</i>")
        if os.path.isfile(name):
            os.remove(name)
        dl = await reply.download_media()
        await message.edit("<i>Renaming..</i>")
        file = await message.client.upload_file(dl)
        file.name = name
        await message.client.send_message(message.chat_id, file=file, reply_to=reply.id)
        await message.delete()
        os.remove(dl)

    async def rndlxxx(message):
        args = utils.get_arg(message).split()
        if not args or len(args) < 2:
            await message.edit("<i>First comes the URL, then the name</i>")
            return
        await message.edit("<i>Downloading..</i>")
        name = " ".join(args[1:])
        if os.path.isfile(name):
            os.remove(name)
        try:
            request.urlretrieve(args[0], "./" + name)
        except ValueError:
            await message.edit("<i>You did it wrong.. It's .rndl <url> <name> </i>")
            return
        await message.edit("<i>Renaming..</i>")
        file = await message.client.upload_file(name)
        file.name = name
        await message.client.send_message(message.chat_id, file=file)
        await message.delete()
        os.remove(name)