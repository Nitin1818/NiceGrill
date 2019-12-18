import time
import asyncio
import subprocess
import logging
from .. import utils
from telethon.errors.rpcerrorlist import MessageTooLongError


class Terminal:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    FWCONTROL = 0

    async def termxxx(message):
        output = "\n\n"
        cmd = utils.get_arg(message)
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,)
        template = await message.edit(
            "\n<b>⬤ Input:</b>\n\n<i>{}</i>\n\n<b>⬤ Output:</b>\n\n<code>"
            .format(cmd))
        if process._transport._closed is not False:
            output += (
                "<i>{}</i>".format(subprocess.getstatusoutput(cmd)[1]))
            await template.edit(template.text + output)
            return
        while process._transport._closed is False:
            output += (await process.stdout.readline()).decode().rstrip() + "\n\n"
            if Terminal.FWCONTROL < 1:
                try:
                    await template.edit(template.text + "<i>{}</i>".format(output))
                except MessageTooLongError:
                    crop = template.text.split("\n\n")
                    print(crop)
                    crop.pop(4)
                    await template.edit("\n\n".join(crop))
                Terminal.FWCONTROL += 1
            else:
                Terminal.FWCONTROL = 0
                pass
