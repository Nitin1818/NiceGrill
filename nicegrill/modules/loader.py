from nicegrill import utils, loader
from database import dloadsdb as nicedb
import logging
import urllib
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
            os.remove(mod)

    async def unloadxxx(message):
        mod = utils.get_arg(message)
        await message.edit("<b>Module unloading...</b>")
        if loader.loadmod.unload(mod, message.client):
            if mod.lower() + ".py" in [n["Name"] for n in nicedb.check_dload()]:
                nicedb.delete(mod.lower())
            await message.edit("<b>Module unloaded</b>")
        else:
            Loader.logger.error("")
            await message.edit("<b>Module not unloaded</b>")

    async def dloadxxx(message):
        link = utils.get_arg(message)
        name = link.split("/")[-1].lower()
        urllib.request.urlretrieve(link, "./" + name)
        clssname = loader.loadmod.load(name, message.client)
        if clssname:
            if link in [l["URL"] for l in nicedb.check_dload()]:
                nicedb.delete("Name")
                nicedb.dload(clssname, link)
            else:
                nicedb.dload(name, link)
            await message.edit("<b>Module loaded</b>")
        else:
            await message.edit("<b>Loading failed</b>")
