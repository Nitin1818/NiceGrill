import logging
import os
import asyncio
from .. import utils
from pySmartDL import SmartDL
from database.allinone import setpath, getpath
from datetime import datetime

DOWNLOADS = {}
shell = "○"*19
bar = ""

class Downloader:

    counter = 0
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def setpathxxx(message):
        """Sets a download path, make sure to add / in the end"""
        pathname = utils.get_arg(message)
        if not os.path.exists(pathname):
            await message.edit("<b>Not a DOWNLOADS[dl]id path.</b>")
            return
        add =  f"INSERT INTO downloader (path) DOWNLOADS[dl]UES ('{pathname}')"
        delete = "DELETE FROM downloader"
        setpath(delete)
        if setpath(add):
            await message.edit("<b>Successfully set.</b>")
        else:
            await message.edit("<b>Something went wrong.</b>")


    async def status(message, dl, reply, btime=0):
        while not dl.isFinished():
            await asyncio.sleep(1)
            await reply.edit(
                f"<b>File Name: </b> <i>{dl.get_dest()}</i>\n"
                f"<b>Size: </b> <i>{dl.get_final_filesize(human=True)}</i>\n"
                f"<b>Speed: </b> <i>{dl.get_speed(human=True)}</i>\n"
                f"<b>Time Passed: </b> <i>{str(datetime.now()-btime)[0:-7]}</i>\n"
                f"<b>Downloaded: </b> <i>{dl.get_final_filesize(human=True)}</i>\n"
                f"<b>Estimated: </b> <i>{dl.get_eta(human=True)}</i>\n"
                f"<b>Status: </b> <i>{dl.get_status().capitalize()}</i>\n"
                f"<i>{dl.get_progress_bar().replace('-', '○').replace('#', '●').replace('[', '').replace(']', '')}</i>")

    async def tgstatus(message, rec, tot, media, btime, process):
        perc= round((rec/tot)*100)
        if str((tot/rec)/1024) not in message.text:
            bar = str("●"*int(perc//5) + shell[int(perc//5)::])
            rec = (
                f"{round(rec/1024, 2)}KB" if not (rec/1024) > 1024
                else f"{round(rec/1048576, 2)}MB")
            down = (
                f"<b>File Name:</b> <i>{media}</i>\n"
                f"<b>Size:</b> <i>{round(tot/1048576, 2)}Mb</i>\n"
                f"<b>{process}</b> <i>{rec}</i>\n"
                f"<b>Time Passed:</b> <i>{str(datetime.now()-btime)[0:-7]}</i>\n"
                f"<i>{bar}</i>")
            if Downloader.counter < 1:
                await message.edit(down)
                Downloader.counter += 1
            else:
                Downloader.counter = 0


    async def dlxxx(message):
        """Downloads the replied media or input url with a nice progressbar"""
        path = "" if not getpath() else getpath()[0][0]
        target = (
            utils.get_arg(message) if not message.is_reply
            else (await message.get_reply_message()).media)
        try:
            name = (
                target.split("/")[-1] if not message.is_reply else
                target.document.attributes[-1].file_name)
        except AttributeError:
            if (await message.get_reply_message()).photo:
                name = (await message.get_reply_message()).photo.id
            elif (await message.get_reply_message()).video:
                name = (await message.get_reply_message()).video.attributes[1].file_name
            elif (await message.get_reply_message()).sticker:
                pass
            elif (await message.get_reply_message()).voice:
                name = "voice.ogg"
            elif (await message.get_reply_message()).audio:
                pass
        await message.edit("<b>Downloading</b> <i>{}</i>...".format(name))
        time = datetime.now()
        if getattr(await message.get_reply_message(), "media", None):
            media = await message.client.download_media(  
                await message.get_reply_message(), path, 
                progress_callback=lambda rec, tot: 
                asyncio.get_event_loop().create_task(
                    Downloader.tgstatus(message, rec, tot, name, time, "Downloaded:")))
            await message.edit(f"<b>Downloaded in:</b> <i>{media}</i>\n")
        else:
            dl = SmartDL(target, path, progress_bar=False)
            dl.start(blocking=False)
            DOWNLOADS[dl.get_dest()] = dl
            await Downloader.status(message, dl, message, time)
        return name

    async def dlstopxxx(message):
        """Stops the ongoing download, only works with url downloads"""
        if not message.is_reply and DOWNLOADS:
            for dl in DOWNLOADS:
                DOWNLOADS[dl].stop()
            DOWNLOADS.clear()
            await message.edit("<i>All downloads stopped</i>")
            return
        reply = await message.get_reply_message()
        await message.edit("<i>Stopping...</i>")
        for dl in DOWNLOADS:
            if dl in reply.text:
                DOWNLOADS[dl].stop()
                await message.edit("<i>Stopped</i>")
                del DOWNLOADS[dl]


    async def downloadsxxx(message):
        """Lists the downloads, only works with url downloads"""
        ls = ""
        if not DOWNLOADS:
            await message.edit("<b>There is no ongoing download</b>")
            return
        reply = await message.get_reply_message()
        await message.edit("<i>Processing...</i>")
        for dl in DOWNLOADS:
            ls += f"● <b>{dl}:\nSize:</b> <i>{DOWNLOADS[dl].get_final_filesize(human=True)}</i>\n<b>Status:</b> <i>{DOWNLOADS[dl].get_status().capitalize()}</i>\n\n"
        await message.edit(ls)

    async def dlpausexxx(message):
        """Pauses the ongoing download, only works with url downloads"""
        if not message.is_reply and DOWNLOADS:
            for dl in DOWNLOADS:
                DOWNLOADS[dl].pause()
            await message.edit("<i>All downloads paused</i>")
            return
        reply = await message.get_reply_message()
        await message.edit("<i>Pausing...</i>")
        for dl in DOWNLOADS:
            if dl in reply.text:
                DOWNLOADS[dl].pause()
                await message.edit("<i>Paused</i>")


    async def dlresumexxx(message):
        """Resumes the paused download, only works with url downloads"""
        if not message.is_reply and DOWNLOADS:
            for dl in DOWNLOADS:
                DOWNLOADS[dl].resume()
            await message.edit("<i>All downloads resumed</i>")
            return
        reply = await message.get_reply_message()
        await message.edit("<i>Resuming...</i>")
        for dl in DOWNLOADS:
            if dl in reply.text:
                DOWNLOADS[dl].resume()
                await message.edit("<i>Resumed</i>")


    async def upxxx(message):
        """Uploads the input file with a nice progressbar"""
        pathtofile = utils.get_arg(message).split("/")
        time = datetime.now()
        await message.edit("<b>Uploading</b> <i>{}</i>...".format(pathtofile[-1]))
        try:
            file = await message.client.upload_file(
                "/".join(pathtofile), progress_callback=lambda rec, tot: 
                asyncio.get_event_loop().create_task(
                    Downloader.tgstatus(message, rec, tot, pathtofile[-1], time, "Uploaded:")))
            await message.client.send_file(message.chat_id, file)
            await message.delete()
        except FileNotFoundError:
            await message.edit(
                "<b>You don't have a file called </b><i>{}</i><b> in this path</b>".format(pathtofile[-1]))
            return
