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
        process = subprocess.Popen(
            cmd.split(),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE)
        template = (
            "\n<b>⬤ Input:</b>\n\n<code>{}</code>\n\n<b>⬤ Output:</b>\n<code>"
            .format(cmd))
        await message.edit(template)
        if process.poll() is not None:
            returncode = str(process.wait())
            out = process.stdout.read().decode() + process.stderr.read().decode()
            result = template + "{}</code>".format(
                "Process returned with exit code: " + returncode if not out
                else out)
            await message.edit(result)
            return
        TERMLIST.update({message.id: process})
        out = ""
        for line in process.stdout:
            if Terminal.FLOODCONTROL < 4:
                Terminal.FLOODCONTROL += 1
                out += "<code>{}\n</code>".format(line.decode() if line.decode else process.stderr.readline().decode())
                continue
            Terminal.FLOODCONTROL = 0
            out += "<code>{}\n</code>".format(line.decode() if line.decode else process.stderr.readline().decode())
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
