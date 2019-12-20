from mtranslate import translate
from langdetect import detect
from nicegrill import utils
import logging


class Translate:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def trtxxx(message):
        """Translates desired text to whatever language.\n\n
Example usage:\n.trt <lang> with a replied message"""
        target = (utils.arg_split_with(message, " "))[0]
        text = (
            (utils.arg_split_with(message, " "))[1] if not message.is_reply else
            (await message.get_reply_message()).text)
        if not (await message.get_reply_message()).text:
            await message.edit("<i>Babe..Are you okay? You can not translate files you know.</i>")
            return
        await message.edit("<i>Translating...</i>")
        result = translate(text, target, 'auto')
        await message.edit(
                           "<b>Text:</b> <i>{}</i>\n"
                           "<b>Detected Language:</b> <i>{}</i>\n\n"
                           "<b>Translated to:</b>\n<i>{}</i>"
                           .format(text, detect(text), result))
