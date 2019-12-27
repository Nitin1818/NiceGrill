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

from PIL import Image, ImageDraw, ImageFont, ImageOps
import emoji
import textwrap
import urllib
import logging
import random
import json
import os

COLORS = [
    "#F07975", "#F49F69", "#F9C84A", "#8CC56E", "#6CC7DC", "#80C1FA", "#BCB3F9", "#E181AC"]

class Quote:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    async def process(msg, reply, client, replied=None):
        if not os.path.isdir(".tmp"):
            os.mkdir(".tmp", 0o755)
            urllib.request.urlretrieve(
                'https://github.com/erenmetesar/modules-repo/raw/master/DejaVuSansCondensed.ttf',
                '.tmp/DejaVuSansCondensed.ttf')
            urllib.request.urlretrieve(
                'https://github.com/erenmetesar/modules-repo/raw/master/Roboto-Medium.ttf',
                '.tmp/Roboto-Medium.ttf')

        # Splitting text
        maxlength = 0
        text = []
        for line in msg.split("\n"):
            length = len(line)
            if length > 43:
                text += textwrap.wrap(line, 43)
                next
            else:
                text.append(line + "\n")
            if length > maxlength:
                maxlength = length
                if length > 43:
                    maxlength = 43

        # Importıng fonts and gettings the size of text
        font = ImageFont.truetype(".tmp/Roboto-Medium.ttf", 43, encoding="utf-16")
        font2 = ImageFont.truetype(".tmp/DejaVuSansCondensed.ttf", 33, encoding="utf-16")
        width, height = font2.getsize("o"*maxlength)

        # Get user name
        lname = "" if not reply.last_name else reply.last_name
        tot = reply.first_name + " " + lname

        namewidth = font.getsize(tot)[0]

        if namewidth > width:
            width = namewidth + 30
        if width < 200:
            width = 200
        height = len(text) * 40

        # Top part
        top = Image.new('RGBA', (width + 80, 20), (0,0,0,0))
        draw = ImageDraw.Draw(top)
        draw.line((10, 0, top.width - 20, 0),  fill="#191919", width=50)
        draw.pieslice((0, 0, 30, 50), 180, 270, fill="#191919")
        draw.pieslice((top.width - 75, 0, top.width, 50), 270, 360, fill="#191919")

        # Middle part
        middle = Image.new("RGBA", (top.width, height + 75), (25, 25, 25, 255))
        
        # Bottom part
        bottom = ImageOps.flip(top)

        # Profile Photo BG
        pfpbg = Image.new("RGBA", (125, 600), (0, 0, 0, 0))

        # Profile Photo Check and Fetch
        yes = False
        color = random.choice(COLORS)
        async for photo in client.iter_profile_photos(reply, limit=1):
            yes = True
        if yes:
            pfp = await client.download_profile_photo(reply)
            paste = Image.open(pfp)
            os.remove(pfp)
            paste.thumbnail((105, 105))

            # Mask
            mask_im = Image.new("L", paste.size, 0)
            draw = ImageDraw.Draw(mask_im)
            draw.ellipse((0, 0, 105, 105), fill=255)

            # Apply Mask
            pfpbg.paste(paste, (0, 0), mask_im)
        else:
            paste, color = await Quote.no_photo(reply, tot)
            pfpbg.paste(paste, (0, 0))

        # Creating a big canvas to gather all the elements
        canvassize = (
            middle.width + pfpbg.width, top.height + middle.height + bottom.height)
        canvas = Image.new('RGBA', canvassize)
        draw = ImageDraw.Draw(canvas)

        y = 80
        if replied:
            # Creating a big canvas to gather all the elements
            replname = "" if not replied.sender.last_name else replied.sender.last_name
            reptot = replied.sender.first_name + " " + replname
            replywidth = font.getsize(reptot)[0] + 20
            canvas = canvas.resize((canvas.width + replywidth, canvas.height + 120))
            middle = middle.resize((middle.width + replywidth, middle.height + 120))
            canvas.paste(pfpbg, (0, 0))
            canvas.paste(top, (pfpbg.width, 0))
            canvas.paste(middle, (pfpbg.width, top.height))
            canvas.paste(bottom, (pfpbg.width, top.height + middle.height))
            draw = ImageDraw.Draw(canvas)
            if replied.sticker:
                replied.text = "Sticker"
            elif replied.photo:
                replied.text = "Photo"
            elif replied.audio:
                replied.text = "Audio"
            elif replied.voice:
                replied.text = "Voice Message"
            elif replied.document:
                replied.text = "Document"
            await Quote.replied_user(draw, font, font2, reptot, replied.message, top.width)
            y = 200
        else:
            canvas.paste(pfpbg, (0, 0))
            canvas.paste(top, (pfpbg.width, 0))
            canvas.paste(middle, (pfpbg.width, top.height))
            canvas.paste(bottom, (pfpbg.width, top.height + middle.height))
            y = 80

        # Writing User's Name
        space = pfpbg.width + 30
        for letter in tot:
            if letter in emoji.UNICODE_EMOJI:
                newemoji, mask = await Quote.emoji_fetch(letter)
                canvas.paste(newemoji, (space, 24), mask)
                space += 40
            else:
                draw.text((space, 20), letter, font=font, fill=color)
                space += font.getsize(letter)[0]

        # Writing all separating emojis and regular texts
        x = pfpbg.width + 30
        for line in text:
            splitemoji = emoji.get_emoji_regexp().split(line)
            for word in splitemoji:
                if word in emoji.UNICODE_EMOJI:
                    newemoji, mask = await Quote.emoji_fetch(word)
                    canvas.paste(newemoji, (x, y - 2), mask)
                    x += 45
                else:
                    draw.text((x, y), word, font=font2, fill='white')
                    x += font2.getsize(word)[0]
            y += 40
            x = pfpbg.width + 30
        return True, canvas

    async def no_photo(reply, tot):
        pfp = Image.new("RGBA", (105, 105), (0, 0, 0, 0))
        pen = ImageDraw.Draw(pfp)
        color = random.choice(COLORS)
        pen.ellipse((0, 0, 105, 105), fill=color)
        letter = "" if not tot else tot[0]
        font = ImageFont.truetype(".tmp/DejaVuSansCondensed.ttf", 60)
        pen.text((32, 17), letter, font=font, fill="white")
        return pfp, color

    async def emoji_fetch(emoji):
        emojis = json.loads(
            urllib.request.urlopen("https://github.com/erenmetesar/modules-repo/raw/master/emojis.txt").read().decode())
        img = emojis[emoji]
        return await Quote.transparent(urllib.request.urlretrieve(img, ".tmp/emoji.png")[0])
        
    async def transparent(emoji):
        emoji = Image.open(emoji).convert("RGBA")
        emoji.thumbnail((40, 40))
        
        # Mask
        mask = Image.new("L", (40, 40), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 40, 40), fill=255)
        return emoji, mask

    async def replied_user(draw, namefont, textfont, tot, text, len1):
        namefont = ImageFont.truetype(".tmp/Roboto-Medium.ttf", 38)
        textfont = ImageFont.truetype(".tmp/Roboto-Medium.ttf", 32)
        text = text[:len(tot) - 3] + ".." if len(text) > len(tot) else text
        draw.line((165, 90, 165, 170), width=5, fill="white")
        draw.text((180, 86), tot, font=namefont, fill="#888888")
        draw.text((180, 132), text, font=textfont, fill="white")

    async def quotexxx(message):
        """Converts the replied message into an independent sticker"""
        await message.delete()
        reply = await message.get_reply_message()
        msg = reply.message
        repliedreply = await reply.get_reply_message()
        reply = (
            await message.client.get_entity(reply.fwd_from.from_id) if reply.fwd_from
            else reply.sender)
        res, canvas = await Quote.process(msg, reply, message.client, repliedreply)
        if not res:
            return
        canvas.save('.tmp/sticker.webp')
        await message.client.send_file(message.chat_id, ".tmp/sticker.webp")
        os.remove('.tmp/sticker.webp')
