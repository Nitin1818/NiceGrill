from datetime import datetime, timedelta
from .. import utils
from database.allinone import set_afk, get_afk, clr_afk, get_storage
import logging
import asyncio

class AFK:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)
    flood_ctrl = 0
    godark = False
    
    async def afkxxx(message):
        """AFK means Away from Keyboard ya dummy.. duh!"""
        msg = utils.get_arg(message)
        current = str(datetime.now())
        if not msg:
            msg = "No Reason"
        await clr_afk()
        await set_afk(True, msg, current)
        await message.edit("<b>I'm going AFK</b>")

    async def godarkxxx(message):
        """Ah this one...It actually turns on/off tag notification
sounds when you're AFK af. Don't worry, I will send
the message informations to you so that you can see
them later. Check your storage channel."""
        msg = utils.get_arg(message)
        if not msg:
            await message.edit("<b>Enter on/off as an option</b>")
            return
        if msg == "on":
            AFK.godark = True
            await message.edit("<b>AFK notifications muted</b>")
        else:
            AFK.godark = False
            await message.edit("<b>AFK notifications unmuted</b>")

    async def watchout(message):
        attr = await get_afk()
        if not attr:
            return
        msg = attr[0][1]
        then = datetime.strptime(attr[0][2], '%Y-%m-%d %H:%M:%S.%f')
        if getattr(message, "message") and message.mentioned and attr:
            storage = await message.client.get_entity((get_storage())[0][0])
            if AFK.godark:
                await message.client.send_read_acknowledge(
                    message.chat, message, clear_mentions=True)
                sentmsg = message.text
                user = message.sender.first_name
                chat = message.chat
                link = "<a href=https://t.me/c/{}/{}>Here</a>".format(chat.id, message.id)
                await message.client.send_message(entity=storage.id, link_preview=False, message=
                    "<b>YOU GOT THIS MESSAGE WHEN YOU WERE UNAVAILABLE</b>\n\n"
                    "<b># User: </b><a href=tg://user?id={}>{}</a>\n"
                    "<b># Chat: </b><a href=https://t.me/c/{}>{}</a>\n"
                    "<b># Message Link: </b>{}\n\n"
                    "<b>Message:</b>\n<i>{}</i>"
                    .format(message.sender.id, user, chat.id, chat.title, link, sentmsg))
            if not AFK.flood_ctrl > 0:
                AFK.flood_ctrl += 1
            else:
                AFK.flood_ctrl = 0
                return
            now = datetime.now()
            delta = now - then
            time = str(timedelta(seconds=delta.seconds)).split(":")
            days = "" if delta.days == 0 else str(delta.days) + " days"
            hours = "" if time[0] == "0" else time[0] + " hours"
            minutes = "" if time[1] == "00" else time[1] + " minutes and "
            then = then.strftime('%Y-%m-%d %H:%M:%S')
            afkmsg = ("<b>I'm AFK for the moment\nReason:</b> <i>{}</i>\n\n"
                   "<b>I've been AFK for {}{}{}{} seconds.\nAFK time:</b> <i>{}</i>"
                   .format(msg, days, hours, minutes, time[2], then))
            await message.respond(afkmsg)
        if message.sender_id == (await message.client.get_me()).id and attr:
            if message.text.startswith(".afk") or message.text.startswith(".godark"):
                return
            await clr_afk()
            await message.client.send_message(
                entity=message.chat_id, 
                message="<b>I'm not AFK anymore.</b>",
                reply_to=message.id)