import logging
import os
from pygdrive3fixed import service
from database.allinone import getGFolder, setGFolder
from .. import utils
from nicegrill.modules.downloader import Downloader as dl

class GoogleDrive:


    drive_service = service.DriveService('./client_secret.json')
    

    async def gdrivexxx(message):
        """Uploads the replied media or input url to your gdrive with a progressbar"""
        GoogleDrive.drive_service.auth()
        # await message.edit("<b>Check your terminal screen for authorization link</b>")
        name = await dl.dlxxx(message)
        if getGFolder():
            folder = getGFolder()[0][0]
        elif GoogleDrive.drive_service.list_folders_by_name('Telegram'):
            folder = GoogleDrive.drive_service.list_folders_by_name('Telegram')[0]["id"]
        else:
            folder = GoogleDrive.drive_service.create_folder('Telegram')
        await message.edit("<i>Uploading to GDrive</i>")
        file = GoogleDrive.drive_service.upload_file(name, name, folder)
        await message.edit(
            f"<i>{name}</i> <b>uploaded to your GDrive folder. </b>"
            f"<a href={GoogleDrive.drive_service.anyone_permission(file)}>Click Here</a> <b>to access it</b>")
        os.remove(name)


    async def setgfolderxxx(message):
        """Specifies what folder your downloads go in in your drive"""
        GoogleDrive.drive_service.auth()
        folder = GoogleDrive.drive_service.list_folders_by_name(utils.get_arg(message))[0]["id"]
        if not folder:
            folder = GoogleDrive.drive_service.create_folder(utils.get_arg(message))
            await message.edit("<b>You dont have this folder in your drive so i created it for you</b>")
        delete = "DELETE FROM gdrive"
        add = f"INSERT INTO gdrive (folderid) VALUES ('{folder}')"
        setGFolder(delete)
        setGFolder(add)
        await message.edit("<b>Succesfully saved</b>")

