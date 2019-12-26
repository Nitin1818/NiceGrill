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
