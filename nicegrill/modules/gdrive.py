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
from pygdrive3fixed import service
from database import settingsdb as settings
from nicegrill import utils
from nicegrill.modules.downloader import Downloader as dl


class GoogleDrive:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def get_service():
         return service.DriveService('./client_secret.json')

    async def gdrivexxx(message):
        """Uploads the replied media or input url to your gdrive with a progressbar"""
        gservice = GoogleDrive.get_service()
        gservice.auth()
        # await message.edit("<b>Check your terminal screen for authorization
        # link</b>")
        arg = utils.get_arg(message)
        if message.is_reply or arg.startswith("http") or arg.startswith("www"):
            file = (await dl.dlxxx(message)).split("/")
        else:
            if "/" not in arg:
                file = arg.split("/")
        if await settings.check_gfolder():
            folder = await settings.check_gfolder()
        elif gservice.list_folders_by_name('Telegram'):
            folder = gservice.list_folders_by_name('Telegram')[
                0]["id"]
        else:
            folder = gservice.create_folder('Telegram')
        await message.edit("<i>Uploading to GDrive</i>")
        try:
            up = gservice.upload_file(
                file[-1], "/".join(file), folder)
        except MemoryError:
            await message.edit("<b>Your drive is full</b>")
            return
        except NameError:
            await message.edit("<b>This file type is not supported</b>")
            return
        except FileNotFoundError:
            await message.edit("<b>This file doesn't exist</b>")
            return
        await message.edit(
            f"<i>{file[-1]}</i> <b>uploaded to your GDrive folder. </b>"
            f"<a href={gservice.anyone_permission(up)}>Click Here</a> <b>to access it</b>")
        os.remove("/".join(file))

    async def setgfolderxxx(message):
        """Specifies what folder your downloads go in in your drive"""
        gservice = GoogleDrive.get_service()
        gservice.auth()
        folder = gservice.list_folders_by_name(
            utils.get_arg(message))[0]["id"]
        if not folder:
            folder = gservice.create_folder(
                utils.get_arg(message))
            await message.edit("<b>You dont have this folder in your drive so i created it for you</b>")
        await settings.delete("GFolder")
        await settings.set_gfolder(folder)
        await message.edit("<b>Succesfully saved</b>")
