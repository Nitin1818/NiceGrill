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
import urbandict
from nicegrill import utils
from urllib.error import HTTPError


class Urban:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def udxxx(message):
        """Searches through urban dictionary"""
        word = (
            utils.get_arg(message) if not message.is_reply
            else (await message.get_reply_message()).text)
        try:
            a = urbandict.define(word)
        except HTTPError:
            await message.edit("<b>Nothing found</b>")
            return
        await message.edit(
            f"<b>◍ Word:</b>\n<i>{a[0]['word']}</i>\n\n<b>◍ Meaning:</b>\n"
            f"<i>{a[0]['def']}</i>\n\n<b>◍ Example:</b>\n<i>{a[0]['example']}</i>")
