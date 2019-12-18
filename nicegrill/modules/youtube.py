from .. import utils
import os
import json
import logging
import glob
import subprocess

class YouTube:

    async def ytxxx(message):
        args = utils.get_arg(message)
        if not args:
            await message.edit("<i>Enter a search argument first</i>")
            return
        await message.edit("<i>Searching..</i>")
        results = json.loads(YoutubeSearch(args, max_results=10).to_json())
        text = ""
        for i in results["videos"]:
            text += f"<i>◍ {i['title']}</i>\nhttps://www.youtube.com{i['link']}\n\n"
        await message.edit(text)
        
    async def ytmp3xxx(message):
        link = utils.get_arg(message)
        cmd = f"youtube2mp3 -d {os.getcwd()} -y {link}"
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        for line in process.stdout:
            await message.edit(f"<i>{line.decode()}</i>")
        file = glob.glob("*.mp3")[0]
        await message.edit("<i>Uploading..</i>")
        await message.client.send_file(message.chat_id, file)
        await message.delete()
        os.remove(file)
        