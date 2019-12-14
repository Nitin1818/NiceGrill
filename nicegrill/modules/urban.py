import logging
import urbandict
from .. import utils
from urllib.error import HTTPError

class Urban:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def udxxx(message):
        """Searches through urban dictionary"""
        word = (
            utils.get_arg(message) if not message.is_reply
            else (await message.get_reply_message()).text)
        try:
            a = urbandict.define(word)
        except HTTPError:
            await message.edit("<b>Nothing found</b>")
            return
        await message.edit(
            f"<b>Word:</b>\n<i>{a[0]['word']}</i>\n\n<b>Meaning:</b>\n"
            f"<i>{a[0]['def']}</i>\n\n<b>Example:</b>\n<i>{a[0]['example']}</i>")