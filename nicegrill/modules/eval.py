from meval import meval
from .. import utils
import logging
import traceback
import sys

class Python:

    reply = None
    message = None
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)


    async def evalxxx(message):
        """A nice tool (like you 🥰) to test python codes"""
        args = utils.get_arg(message).strip()
        caption = "<b>⬤ Evaluated expression:</b>\n<code>{}</code>\n\n<b>⬤ Result:</b>\n".format(args)
        try:
            res = await meval(args, globals(), **await Python.funcs(message))
        except Exception as e:
            caption = "<b>⬤ Evaluation failed:</b>\n<code>{}</code>\n\n<b>⬤ Result:</b>\n".format(args)
            etype, value, tb = sys.exc_info()
            res = ''.join(traceback.format_exception(etype, value, None, 0))

        await message.edit(caption + "<code>" + str(res) + "</code>")

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
        print(Python.reply)
        return {"message": message, "reply": await message.get_reply_message(),
               "client": message.client, "getme": (await message.client.get_me()).id, "run": utils.run}
