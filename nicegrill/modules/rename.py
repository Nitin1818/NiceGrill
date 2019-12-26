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