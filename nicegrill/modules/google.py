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
from PIL import Image
from nicegrill import utils
from search_engine_parser import GoogleSearch
from google_images_download import google_images_download

class Google:


    async def googlexxx(message):
        await message.edit("<i>Searching..</i>")
        search_args = (utils.get_arg(message), 1)
        gsearch = GoogleSearch()
        gresults = await gsearch.async_search(*search_args)
        text = ""
        try:
            for i in range(6):
                text +=  f"<b>◍ {gresults['titles'][i].upper()} :</b>\n\n<i>{gresults['descriptions'][i]}</i>\n\n{gresults['links'][i]}\n\n"
        except IndexError:
            pass
        await message.edit(text, link_preview=False)

    async def gimgxxx(message):
        keyword = utils.get_arg(message)
        response = google_images_download.googleimagesdownload()
        args = {"keywords": keyword, "limit":5, "print_urls":False}
        await message.edit("<i>Searching..</i>")
        paths = response.download(args)
        if not paths:
            await message.edit("<i>Nothing found</i>")
            return
        await message.edit("<i>Uploading..</i>")
        newlist = []
        for filename in os.listdir(f"downloads/{keyword}/"):
            try:
                with Image.open(f"downloads/{keyword}/{filename}") as im:
                    newlist.append(f"downloads/{keyword}/{filename}")
            except Exception:
                os.remove(f"downloads/{keyword}/{filename}")
        if not newlist:
            await message.edit("<i>Images were broken so nothing happened</i>")
            return
        await message.client.send_message(message.chat_id, file=newlist)
        await message.delete()
        for path in paths[0][keyword]:
            os.remove(path)
 
    async def lmgtfyxxx(message):
        keyword = (
            (await message.get_reply_message()).message 
            if not utils.get_arg(message) 
            else utils.get_arg(message))
        if not keyword:
            await message.edit(
                "<i>You didn't specify a keyword. Reply to a message"
                " or enter a keyword</i>")
            return
        link = f"https://lmgtfy.com/?q={keyword.replace(' ', '+')}"
        reply_id = (
            (await message.get_reply_message()).id if message.is_reply
            else None)
        await message.edit(link)

 