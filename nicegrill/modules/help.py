import logging
from nicegrill.modules import _init
from .. import utils

class Help:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def helpxxx(message):
        help = " ‎\n•{}•".format("<b>Help</b>".center(85))
        mods, classinfo = _init.modules, _init.classes
        name = utils.get_arg(message)
        if name and (name in mods or name in classinfo):
            for mod in mods:
               if name == mod:
                   templ = (
                       "{}\n\n<b>Here's the help for</b> <i>{}</i> <b>command:</b>\n\n"
                       .format(help, mod))
                   await message.edit(
                       templ + mods[mod].__doc__) if mods[mod].__doc__ else await message.edit(
                       "<b>No help found for that command</b>")
                   return
            for cls in classinfo:
                if name == cls:
                   templ = (
                       "{}\n\n<b>Here's the commands in</b> <i>{}</i> <b>module:</b>\n\n"
                       .format(help, cls))
                   await message.edit(
                       templ + ", ".join(classinfo[cls]))
                   return
        elif name and (name not in mods or name not in classinfo):
            await message.edit("<b>There's nothing found under that name</b>")
            return
        for cls in classinfo:
            help += "\n\n<b>⬤ {}:</b>\n<i>".format(cls)
            help += ", ".join(classinfo[cls]) + "</i>"
        await message.edit(help)

    async def supportxxx(message):
        await message.edit("<b>Join</b> <a href=https://t.me/c/1409290957>Here</a> <b>for support!</b>")