from database import settingsdb as settings
from nicegrill import utils
import logging


class Settings:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def setprefixxxx(message):
        pref = utils.get_arg(message)
        settings.delete("Prefix")
        settings.set_prefix(pref)
        await message.edit("<b>Prefix has been successfully set to: {}</b>".format(pref))
