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
from nicegrill import utils

class WhoAreYou:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def whoxxx(message):
        if not utils.get_arg(message):
            user = (
                (await message.get_reply_message()).sender if message.is_reply
                else message.sender)
        else:
            try:
                user = await message.client.get_entity(utils.get_arg(message))
            except ValueError:
                await message.edit("<i>No user found</i>")
                return
        identify = (
            f"<b>First Name:</b> <i>{user.first_name}</i>\n"
            f"<b>Last Name:</b> <i>{user.last_name}</i>\n"
            f"<b>Username:</b> <i>{user.username}</i>\n"
            f"<b>ID:</b> <i>{user.id}</i>\n"
            f"<b>Bot:</b> <i>{user.bot}</i>\n"
            f"<b>Permanent Link:</b> <a href=tg://user?id={user.id}>{user.first_name}</a>")
        await message.edit(identify)
