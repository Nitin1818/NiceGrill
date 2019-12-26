from PIL import Image, ImageFont, ImageDraw
import io
import os
from glob import glob
import asyncio

class TestFont:
	async def testfontxxx(event):
		if event.message.message.split()[1:] == []:
			text = "𝖘𝖓𝖆𝖕𝖉𝖗𝖆𝖌𝖔𝖓"
		else:
			text = ' '.join(event.message.message.split()[1:])
		for font1 in glob("testfonts/*"):
			canvas = Image.new("RGBA", (200, 200), (0, 0, 0, 255))
			draw = ImageDraw.Draw(canvas)
			try:
				font = ImageFont.truetype(font1, 15)

				draw.text((20, 80), text, font=font, fill="white")
				canvas.save("testfont.webp", format="PNG")
				await event.client.send_file(event.chat_id, "testfont.webp")
				await event.respond(font1)
				await asyncio.sleep(1)
			except Exception:
				pass
		os.remove("testfont.webp")