from .. import utils, loader
from nicegrill.modules import _init
from database.allinone import store_func, get_func
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
        if reply.document and reply.document.attributes[-1].file_name.endswith(
                ".py"):
            file = await reply.download_media()
            if loader.loadmod.load(file, message.client):
                await message.edit("<b>Module loaded</b>")
            else:
                await message.edit("<b>Loading failed</b>")

    async def unloadxxx(message):
        mod = utils.get_arg(message)
        await message.edit("<b>Module unloading...</b>")
        if loader.loadmod.unload(mod, message.client):
            if mod.lower() + ".py" in str(get_func()):
                store_func(
                    f"DELETE FROM loadmods WHERE name='{mod.lower()}.py'")
            await message.edit("<b>Module unloaded</b>")
        else:
            Loader.logger.error("")
            await message.edit("<b>Module not unloaded</b>")

    async def dloadxxx(message):
        link = utils.get_arg(message)
        name = link.split("/")[-1].lower()
        mod = urllib.request.urlretrieve(link, "./" + name)
        if loader.loadmod.load(name, message.client):
            if get_func() and link in str(get_func):
                store_func(
                    f"UPDATE loadmods SET name='{name}', links='{link}'")
            else:
                store_func(
                    f"INSERT INTO loadmods (name, links) VALUES ('{name}','{link}')")
            await message.edit("<b>Module loaded</b>")
        else:
            await message.edit("<b>Loading failed</b>")
