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

from nicegrill import utils
from weather import Weather as wtr
from database import settingsdb as settings
import logging


class Weather:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def weatherxxx(message):
        """Shows the weather of specified city"""
        if not await settings.check_city() and not utils.get_arg(message):
            await message.edit("<b>Enter a city name first</b>")
            return
        city = await settings.check_city() if not utils.get_arg(
            message) else utils.get_arg(message)
        weather = wtr.find(city)
        await message.edit(
            f"<b>City:</b> <i>{weather['weather']['city']}</i>\n"
            f"<b>Temperature:</b> <i>{round(weather['weather']['temp'])}°C</i>\n"
            f"<b>Pressure:</b> <i>{weather['weather']['pressure']} hPa</i>\n"
            f"<b>Humidity:</b> <i>{weather['weather']['humidity']}%</i>\n"
            f"<b>Latency:</b> <i>{weather['weather']['lat']}</i>\n"
            f"<b>Status:</b> <i>{weather['main']}</i>\n"
            f"<b>Description:</b> <i>{weather['description'].capitalize()}</i>\n"
            f"<b>Wind Speed:</b> <i>{weather['wind']['speed']} m/s</i>\n")

    async def setcityxxx(message):
        """Sets a default city so that you don't have to type it everytime"""
        if not utils.get_arg(message):
            await settings.delete("City")
            await message.edit("<b>Saved city name removed</b>")
            return
        await settings.delete("City")
        await settings.set_city(utils.get_arg(message))
        await message.edit("<b>Successfully saved</b>")
