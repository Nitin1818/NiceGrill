from PIL import Image, ImageDraw, ImageFont, ImageOps
import emoji
import textwrap
import urllib
import logging
import random
import os

COLORS = [
    "#F07975", "#F49F69", "#F9C84A", "#8CC56E", "#6CC7DC", "#80C1FA", "#BCB3F9", "#E181AC"]

class Quote:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    async def process(msg, reply, client):
        if not os.path.isdir(".tmp"):
            os.mkdir(".tmp", 0o755)
            urllib.request.urlretrieve(
                'https://github.com/erenmetesar/modules-repo/raw/master/DejaVuSansCondensed.ttf',
                '.tmp/DejaVuSansCondensed.ttf')
            urllib.request.urlretrieve(
                'https://github.com/erenmetesar/modules-repo/raw/master/DejaVuSansCondensed-Bold.ttf',
                '.tmp/DejaVuSansCondensed-Bold.ttf')
            urllib.request.urlretrieve(
                'https://github.com/erenmetesar/modules-repo/raw/master/DejaVuSansCondensed-Bold.ttf',
                '.tmp/twemoji.ttf')

        # Splitting text
        maxlength = 0
        text = []
        for line in msg.split("\n"):
            if len(line) > 43:
                text += textwrap.wrap(line, 43)
                next
            else:
                text.append(line + "\n")
            if len(line) > maxlength:
                maxlength = len(line)
                if len(line) > 43:
                    maxlength = 43

        # Importıng fonts and gettings the size of text
        font = ImageFont.truetype(".tmp/DejaVuSansCondensed-Bold.ttf", 43, encoding="utf-16")
        font2 = ImageFont.truetype(".tmp/DejaVuSansCondensed.ttf", 33, encoding="utf-16")
        # This was an emoji test and failed, but ill keep it just in case
        emojifont = ImageFont.truetype(".tmp/twemoji.ttf", 32, encoding="utf-16")
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
        top = Image.new('RGBA', (width + 100, 20), (0,0,0,0))
        draw = ImageDraw.Draw(top)
        draw.line((10, 0, top.width - 20, 0),  fill="#191919", width=50)
        draw.pieslice((0, 0, 30, 50), 180, 270, fill="#191919")
        draw.pieslice((top.width - 75, 0, top.width, 50), 270, 360, fill="#191919")

        # Middle part
        middle = Image.new("RGBA", (top.width, height + 75), (25, 25, 25, 255))
        
        # Bottom part
        bottom = ImageOps.flip(top)

        # Profile Photo BG
        pfpbg = Image.new("RGBA", (135, 600), (0, 0, 0, 0))

        # Creating a big canvas to gather all the elements
        canvassize = (
            middle.width + pfpbg.width, top.height + middle.height + bottom.height)
        canvas = Image.new('RGBA', canvassize)

        # Profile Photo Check and Fetch
        yes = False
        color = random.choice(COLORS)
        async for photo in client.iter_profile_photos(reply, limit=1):
            yes = True
        if yes:
            pfp = await client.download_profile_photo(reply)
            paste = Image.open(pfp)
            os.remove(pfp)
            paste.thumbnail((110, 115))

            # Mask
            mask_im = Image.new("L", paste.size, 0)
            draw = ImageDraw.Draw(mask_im)
            draw.ellipse((0, 0, 105, 113), fill=255)

            # Apply Mask
            pfpbg.paste(paste, (0, 20), mask_im)
        else:
            paste, color = await Quote.no_photo(reply, tot)
            pfpbg.paste(paste, (0, 20))

        # Gathering everything in one big canvas
        canvas.paste(pfpbg, (0, 0))
        canvas.paste(top, (pfpbg.width, 0))
        canvas.paste(middle, (pfpbg.width, top.height))
        canvas.paste(bottom, (pfpbg.width, top.height + middle.height))

        # Writing User's Name
        draw = ImageDraw.Draw(canvas)
        draw.text((pfpbg.width + 30, 20), tot, font=font, fill=color)

        # Writing all separating emojis and regular texts
        lineheight = 50
        x, y = pfpbg.width + 30, lineheight + 40
        for line in text:
            splitemoji = emoji.get_emoji_regexp().split(line)
            for word in splitemoji:
                wordwidth = 0
                if word in emoji.UNICODE_EMOJI:
                    draw.text((x, y), word, font=emojifont, fill="white")
                    x += font2.getsize(word)[0]
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

    async def quotexxx(message):
        """Converts the replied message into an independent sticker"""
        await message.delete()
        reply = await message.get_reply_message()
        msg = reply.message
        reply = (
            await message.client.get_entity(reply.fwd_from.from_id) if reply.fwd_from
            else reply.sender)
        res, canvas = await Quote.process(msg, reply, message.client)
        if not res:
            return
        canvas.save('.tmp/sticker.webp')
        await message.client.send_file(message.chat_id, ".tmp/sticker.webp")
        os.remove('.tmp/sticker.webp')