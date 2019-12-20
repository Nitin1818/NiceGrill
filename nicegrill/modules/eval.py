from meval import meval
from nicegrill import utils
from telethon.errors.rpcerrorlist import MessageTooLongError
from nicegrill.modules._init import cmds
import logging
import traceback
import sys
import html
import textwrap
import asyncio


class Python:

    reply = None
    message = None
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def evalxxx(message):
        """A nice tool (like you 🥰) to test python codes"""
        args = utils.get_arg(message).strip()
        caption = "<b>⬤ Evaluated expression:</b>\n<code>{}</code>\n\n<b>⬤ Result:</b>\n".format(
            args)
        try:
            res = str(await meval(args, globals(), **await Python.funcs(message)))
        except Exception:
            caption = "<b>⬤ Evaluation failed:</b>\n<code>{}</code>\n\n<b>⬤ Result:</b>\n".format(
                args)
            etype, value, tb = sys.exc_info()
            res = ''.join(traceback.format_exception(etype, value, None, 0))
        try:
            await message.edit(caption + f"<code>{html.escape(res)}</code>")
        except MessageTooLongError:
            res = textwrap.wrap(res, 4096-len(caption))
            await message.edit(caption + f"<code>{res[0]}</code>")
            for part in res[1::]:
                await asyncio.sleep(1)
                await message.reply(f"<code>{part}</code>")

    async def execxxx(message):
        """A nice tool (like you 🥰) to test python codes
There's no output on this one tho"""
        args = utils.get_arg(message).strip()
        try:
            await meval(args, globals(), **await Python.funcs(message))
        except Exception as e:
            Python.logger.error(e)

    async def funcs(message):
        Python.reply = await message.get_reply_message()
        Python.message = message
        return {"message": message, "reply": await message.get_reply_message(),
                "client": message.client, "getme": (await message.client.get_me()).id,
                "dispatch": Python.dispatch}

    def dispatch(cmd, msg):
        return cmds[cmd](msg)
