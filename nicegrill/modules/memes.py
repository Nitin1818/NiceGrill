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
from nicegrill import utils
import time
import random


class Memes:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def mockxxx(message):
        msg = list(utils.get_arg(message))
        if message.is_reply:
            msg = list(await message.get_reply_message()).text)
        if not msg:
            await message.edit("<i>Give me a text to mockify</i>")
            return
        for chr in range(len(msg)):
            if random.randint(0, 1) == 1:
                msg[chr] = msg[chr].capitalize()
            else:
                msg[chr] = msg[chr].lower()
        await message.edit("".join(msg))

    async def ratexxx(message):
        if not message.is_reply:
            await message.edit("<i>Reply to a message first</i>")
            return
        await message.edit(f"<i>This person is {random.randint(0,101)}% gay</i>")

    async def watchout(message):
        if message.text.lower() == "yey":
            for i in range(10):
                await message.edit("Y" + "e" * i + "y")

        if message.text.lower() == "oof":
            for i in range(10):
                await message.edit("O" + "o" * i + "f")

        if message.text.lower() == ":/":
            for i in range(10):
                await message.edit(r":\/".replace("/", ""))
                time.sleep(0.3)
                await message.edit(":/")
                time.sleep(0.3)
