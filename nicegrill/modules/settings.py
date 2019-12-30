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

from database import settingsdb as settings
from nicegrill import utils
import logging


class Settings:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def setprefixxxx(message):
        pref = utils.get_arg(message)
        await settings.delete("Prefix")
        await settings.set_prefix(pref)
        await message.edit("<b>Prefix has been successfully set to: {}</b>".format(pref))
