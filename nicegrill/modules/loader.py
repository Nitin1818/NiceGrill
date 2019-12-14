from .. import utils, loader
from nicegrill.modules import _init
import logging
import urllib
import shutil
import os

class Loader:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def loadxxx(message):
        reply = await message.get_reply_message()
        await message.edit("<b>Module loading...</b>")
        if reply.document and reply.document.attributes[-1].file_name.endswith(".py"):
            file = await reply.download_media()
            if loader.loadmod.load(file):
                await message.edit("<b>Module loaded</b>")
            else:
                await message.edit("<b>Loading failed</b>")

    async def unloadxxx(message):
        mod = utils.get_arg(message)
        await message.edit("<b>Module unloading...</b>")
        if loader.loadmod.unload(mod):
            await message.edit("<b>Module unloaded</b>")
        else:
            Loader.logger.error("")
            await message.edit("<b>Unloading failed</b>")


    async def dloadxxx(message):
        pass
