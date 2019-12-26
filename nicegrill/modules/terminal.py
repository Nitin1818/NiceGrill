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

import asyncio
import subprocess
import logging
from nicegrill import utils
from telethon.errors.rpcerrorlist import MessageTooLongError, MessageNotModifiedError

TERMLIST = {}

class Terminal:

    FLOODCONTROL = 5
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)


    async def termxxx(message):
        cmd = utils.get_arg(message)
        process = await asyncio.create_subprocess_shell(
            cmd,
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE)
        template = (
            "\n<b>⬤ Input:</b>\n\n<code>{}</code>\n\n<b>⬤ Output:</b>\n\n<code>"
            .format(cmd))
        await message.edit(template)
        if process.returncode is not None:
            stdout, stderr = await process.communicate()
            out = stdout.decode() + stderr.decode()
            result = template + "{}</code>".format(
                "Process returned with exit code: " + str(process.returncode) if not out
                else out)
            await message.edit(result)
            return
        TERMLIST.update({message.id: process})
        out = ""
        for line in (await process.stdout.read()).decode().split("\n"):
            if Terminal.FLOODCONTROL < 4:
                Terminal.FLOODCONTROL += 1
                out += "<code>{}\n</code>".format(line if line else (await process.stderr.readline()).decode())
                continue
            Terminal.FLOODCONTROL = 0
            out += "<code>{}\n</code>".format(line if line else (await process.stderr.readline()).decode())
            if len(out) < 1500 and message.id in TERMLIST:
                await message.edit(template + out)
            else:
                out = out[600: -1]
                await message.edit(template + out)
        try:
            await message.edit(template + out)
        except MessageNotModifiedError:
            pass
        del TERMLIST[message.id]

    async def killxxx(message):
        if not message.is_reply:
            await message.edit("<i>You have to reply to a message with a process</i>")
            return
        process = await message.get_reply_message()
        if process.id not in TERMLIST:
            await message.edit("<i>No process running in that message</i>")
        else:
            TERMLIST[process.id].kill()
            del TERMLIST[process.id]
            await message.edit("<i>Successfully killed</i>")
