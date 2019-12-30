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

from datetime import datetime, timedelta
from nicegrill import utils
from database import afkdb as nicedb, settingsdb as settings
import logging


class AFK:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)
    flood_ctrl = 0

    async def afkxxx(message):
        """AFK means Away from Keyboard ya dummy.. duh!"""
        msg = utils.get_arg(message)
        current = str(datetime.now())
        if not msg:
            msg = "No Reason"
        await nicedb.set_afk(msg, current)
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
            await nicedb.set_godark(True)
            await message.edit("<b>AFK notifications muted</b>")
        else:
            await nicedb.set_godark(False)
            await message.edit("<b>AFK notifications unmuted</b>")

    async def watchout(message):
        if not await nicedb.check_afk():
            return
        getafk = await nicedb.check_afk()
        msg = getafk["Message"]
        then = datetime.strptime(getafk["AFKTime"], '%Y-%m-%d %H:%M:%S.%f')
        if getattr(message, "message") and message.mentioned and await settings.check_asset():
            storage = await message.client.get_entity(await settings.check_asset())
            if await nicedb.check_godark():
                await message.client.send_read_acknowledge(
                    message.chat, message, clear_mentions=True)
                sentmsg = message.text
                user = message.sender.first_name
                chat = message.chat
                link = "<a href=https://t.me/c/{}/{}>Here</a>".format(
                    chat.id, message.id)
                await message.client.send_message(entity=storage.id, link_preview=False,
                                                  message="<b>YOU GOT THIS MESSAGE WHEN YOU WERE UNAVAILABLE</b>\n\n"
                                                  "<b>◍ User: </b><a href=tg://user?id={}>{}</a>\n"
                                                  "<b>◍ Chat: </b><a href=https://t.me/c/{}>{}</a>\n"
                                                  "<b>◍ Message Link: </b>{}\n\n"
                                                  "<b>Message:</b>\n<i>{}</i>"
                                                  .format((await message.get_sender()).id, user, chat.id, chat.title, link, sentmsg))
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
            afkmsg = (
                "<b>I'm AFK for the moment\nReason:</b> <i>{}</i>\n\n"
                "<b>I've been AFK for {}{}{}{} seconds.\nAFK time:</b> <i>{}</i>" .format(
                    msg, days, hours, minutes, time[2], then))
            await message.respond(afkmsg)
        if (await message.get_sender()).id == (await message.client.get_me()).id:
            if message.text.startswith(
                    ".afk") or message.text.startswith(".godark"):
                return
            await nicedb.stop_afk()
            await message.reply("<b>I'm not AFK anymore.</b>")

