from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import textwrap
import urllib
import logging
import os


class Quote:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    async def process(msg, reply, client):
        if not os.path.isdir(".tmp"):
            os.mkdir(".tmp", 0o755)
            urllib.request.urlretrieve(
                'https://github.com/erenmetesar/modules-repo/raw/master/pfp.jpg',
                '.tmp/pfp.jpg')
            urllib.request.urlretrieve(
                'https://github.com/erenmetesar/modules-repo/raw/master/top.jpg',
                '.tmp/top.jpg')
            urllib.request.urlretrieve(
                'https://github.com/erenmetesar/modules-repo/raw/master/mid.jpg',
                '.tmp/mid.jpg')
            urllib.request.urlretrieve(
                'https://github.com/erenmetesar/modules-repo/raw/master/bottom.jpg',
                '.tmp/bottom.jpg')
            urllib.request.urlretrieve(
                'https://github.com/erenmetesar/modules-repo/raw/master/DejaVuSansCondensed.ttf',
                '.tmp/DejaVuSansCondensed.ttf')
            urllib.request.urlretrieve(
                'https://github.com/erenmetesar/modules-repo/raw/master/DejaVuSansCondensed-Bold.ttf',
                '.tmp/DejaVuSansCondensed-Bold.ttf')
        top = Image.open(".tmp/top.jpg", "r").convert('RGBA')
        mid = Image.open(".tmp/mid.jpg", "r").convert('RGBA')
        bottom = Image.open(".tmp/bottom.jpg", "r").convert('RGBA')
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
                


        dlpfp = await client.download_profile_photo(reply.id)
        paste = Image.open(dlpfp)
        os.remove(dlpfp)
        pfp = Image.open(".tmp/pfp.jpg")
        paste.thumbnail((110, 115))

        # MASK
        mask_im = Image.new("L", paste.size, 0)
        draw = ImageDraw.Draw(mask_im)
        draw.ellipse((0, 0, 110, 115), fill=255)

        # APPLY MASK
        pfpbg = pfp.copy()
        pfp = mask_im.copy()
        pfpbg.paste(paste, (10, 20), mask_im)

        lname = "" if not reply.last_name else reply.last_name
        tot = reply.first_name + " " + lname

        font = ImageFont.truetype(".tmp/DejaVuSansCondensed-Bold.ttf", 43, encoding="utf-16")
        font2 = ImageFont.truetype(".tmp/DejaVuSansCondensed.ttf", 33, encoding="utf-16")
        width, height = font2.getsize("o"*maxlength)
        namewidth, nameheight = font.getsize(tot)
        if namewidth > width:
            width = namewidth + 30
        if width < 200:
            width = 200
        height = len(text) * 40

        top = top.resize((width + 70, top.height))
        mid = mid.resize((width + 70, height + 50))
        bottom = bottom.resize((width + 70, top.height))

        canvas = Image.new(
            'RGB',
            (width + 70
             + pfpbg.width,
             top.height
             + height
             + bottom.height))
        canvas.paste(pfpbg, (0, 0))
        canvas.paste(top, (pfpbg.width, 0))
        canvas.paste(mid, (pfpbg.width, top.height))
        canvas.paste(bottom, (pfpbg.width, top.height + mid.height))


        draw = ImageDraw.Draw(canvas)

        draw.text((pfp.width + 70, 40), tot, font=font, fill='#E9967A')

        lnh = 70
        for line in text:
            draw.text((pfp.width + 70, lnh + 40),
                      line, font=font2, fill='white')
            lnh += 40
        return True, canvas

    async def quotexxx(message):
        """Converts the replied message into an independent sticker"""
        await message.delete()
        reply = await message.get_reply_message()
        msg = (await message.get_reply_message()).message
        reply = (
            await message.client.get_entity(reply.fwd_from.from_id) if reply.fwd_from
            else reply.sender)
        res, canvas = await Quote.process(msg, reply, message.client)
        if not res:
            return
        canvas.save('.tmp/done.webp')
        await message.client.send_file(message.chat_id, ".tmp/done.webp")