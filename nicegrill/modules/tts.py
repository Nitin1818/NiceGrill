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