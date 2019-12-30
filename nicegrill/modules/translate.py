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
        target = (utils.arg_split_with(message, " "))
        if not target:
            await message.edit("<i>Specify the target language.</i>")
            return
        if target and len(target) < 2 and not message.is_reply:
            await message.edit("<i>Specify the text to be translated.</i>")
            return
        reply = await message.get_reply_message()
        text = (
            target[1] if not message.is_reply else
            reply.text)
        target = target[0]
        if reply and not reply.text:
            await message.edit("<i>Babe..Are you okay? You can not translate files you know.</i>")
            return
        await message.edit("<i>Translating...</i>")
        result = translate(text, target, 'auto')
        await message.edit(
                           "<b>Text:</b> <i>{}</i>\n"
                           "<b>Detected Language:</b> <i>{}</i>\n\n"
                           "<b>Translated to:</b>\n<i>{}</i>"
                           .format(text, detect(text), result))
