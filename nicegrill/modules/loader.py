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
            if loader.Loadmod.load(file, message.client):
                await message.edit("<b>Module loaded</b>")
            else:
                await message.edit("<b>Loading failed</b>")
            os.remove(file)

    async def unloadxxx(message):
        mod = utils.get_arg(message)
        await message.edit("<b>Module unloading...</b>")
        if oader.Loadmod.unload(mod, message.client):
            if mod.lower() + ".py" in [n["Name"] for n in await nicedb.check_dload()]:
                await nicedb.delete(mod.lower())
            await message.edit("<b>Module unloaded</b>")
        else:
            Loader.logger.error("")
            await message.edit("<b>Module not unloaded</b>")

    async def dloadxxx(message):
        link = utils.get_arg(message)
        name = link.split("/")[-1].lower()
        urllib.request.urlretrieve(link, "./" + name)
        clssname = loader.Loadmod.load(name, message.client)
        if clssname:
            if link in [l["URL"] for l in await nicedb.check_dload()]:
                await nicedb.delete("Name")
                await nicedb.dload(clssname, link)
            else:
                await nicedb.dload(name, link)
            await message.edit("<b>Module loaded</b>")
        else:
            await message.edit("<b>Loading failed</b>")
