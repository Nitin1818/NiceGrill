import logging
from .. import utils
import time
import random

class Memes:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def mockxxx(message):
        msg = ",".join((utils.get_arg(message))).split(",")
        if message.is_reply:
            msg = ",".join(((await message.get_reply_message()).text)).split(",")
        for chr in range(len(msg)):
             if random.randint(0,1) == 1:
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
                await message.edit(":\/".replace("/", ""))
                time.sleep(0.3)
                await message.edit(":/")
                time.sleep(0.3)