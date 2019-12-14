from database.allinone import set_pref
from .. import utils
import logging
import sqlite3

class Settings:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def setprefixxxx(message):
        pref = utils.get_arg(message)
        try:
            delete = "DELETE FROM core"
            add = f"INSERT INTO core (prefix) VALUES ('{pref}')"
            set_pref(delete)
            set_pref(add)
            await message.edit("<b>Prefix has been successfully set to: {}</b>".format(pref))
        except sqlite3.OperationalError as e:
            await message.edit("<b>Prefix could not be set</b>")
            Settings.logger.error(e)
            return