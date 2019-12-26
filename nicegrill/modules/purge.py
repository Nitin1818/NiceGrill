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
import asyncio
from nicegrill import utils


class Purge:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    async def purgexxx(message):
        """Perfect tool(like you 🥰) for a spring cleaning\n
Purges the chat with a given message count or until the replied message"""
        client = message.client
        count = int(utils.get_arg(message)) + \
            1 if utils.get_arg(message).isdigit() else None
        msgs = []
        if not count and not message.is_reply:
            await message.edit("<b>Enter a number or reply to a message</b>")
            return
        elif not count and message.is_reply:
            count = (await message.get_reply_message()).id - 1
        async for msg in client.iter_messages(message.chat_id, limit=count, min_id=count):
            msgs.append(msg.id)
        await client.delete_messages(message.chat_id, msgs)
        success = (
            await client.send_message(message.chat_id,
                                      "<b>Purge has been successful. This message will disappear in 3 seconds.</b>"))
        await asyncio.sleep(3)
        await client.delete_messages(message.chat_id, success.id)

    async def purgemexxx(message):
        """Perfect tool(like you 🥰) for a spring cleaning\n
Purges the chat with a given message count or till the replied message but only your messages
        """
        client = message.client
        count = int(utils.get_arg(message)) + \
            1 if utils.get_arg(message).isdigit() else None
        msgs = []
        if not count and not message.is_reply:
            await message.edit("<b>Enter a number or reply to a message</b>")
            return
        elif not count and message.is_reply:
            count = (await message.get_reply_message()).id - 1
        async for msg in client.iter_messages(message.chat_id, from_user='me', limit=count, min_id=count):
            msgs.append(msg.id)
        await client.delete_messages(message.chat_id, msgs)
        success = (
            await client.send_message(message.chat_id,
                                      "<b>Purge has been successful. This message will disappear in 3 seconds.</b>"))
        await asyncio.sleep(3)
        await client.delete_messages(message.chat_id, success.id)

    async def delxxx(message):
        """This poor boi just deletes the replied message"""
        reply = await message.get_reply_message()
        await message.delete()
        await reply.delete()
