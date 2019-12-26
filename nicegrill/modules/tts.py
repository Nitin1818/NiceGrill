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

import logging
import os
from gtts import gTTS
from nicegrill import utils


class TextToSpeech:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def ttsxxx(message):
        """.tts <lang> <text>/replied message"""
        args = utils.arg_split_with(message, " ")
        if not args and not message.is_reply or len(args) < 1:
            await message.edit("<i>You're using it wrong, duh!</i>")
            return
        text = " ".join(args[1:]) if not message.is_reply else (await message.get_reply_message()).text
        try:
            gTTS(text, args[0]).save("tts.mp3")
        except ValueError:
            await message.edit("<i>Language not supported</i>")
            return
        except AssertionError:
            await message.edit("<i>No text to speak</i>")
            return
        await message.client.send_file(message.chat_id, "tts.mp3")
        await message.delete()
        os.remove("tts.mp3")