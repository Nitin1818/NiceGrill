import logging
from nicegrill import utils
from database.allinone import set_snip, get_snip, get_storage, others, get_others

logger = logging.getLogger(__name__)


class Snips:
    """Saves some texts to call on them literally anywhere and anytime"""

    async def snipxxx(message):
        """Adds a snip into the list. Separate it with comma(,)"""
        args = utils.arg_split_with(message, ",")
        reply = await message.get_reply_message()
        name = args[0]
        if len(args) == 0:
            await message.edit("<b>Enter the name of the snip first</b>")
            return
        if len(args) == 1 and not message.is_reply:
            await message.edit("<b>Enter or reply to a text to save as snip</b>")
            return
        if message.is_reply:
            if reply.media:
                value = (await message.send_message(get_storage()[0][0], reply)).id
                media = True
            else:
                value = reply.message
                media = False
        else:
            value = args[1]
            media = False
        if get_snip() and name in str(get_snip()):
            set_snip(
                f"UPDATE snips SET name='{name}', value='{value}', media={media}")
        else:
            set_snip(
                f"INSERT INTO snips (name, value, media) VALUES ('{name}', '{value}', {media})")
        await message.edit(
            "<b>Snip </b><i>{}</i><b> successfully saved into the list."
            "Type </b><i>${}</i><b> to call it.</b>".format(name, name))

    async def remsnipxxx(message):
        """Removes a snip from the list."""
        snipn = utils.get_arg(message)
        get = get_snip()
        if not snipn:
            await message.edit("<b>Please specify the name of the snip to remove.</b>")
            return
        if not get:
            await message.edit("<b>You don't have any snips saved.</b>")
            return
        if snipn in str(get):
            set_snip(f"DELETE FROM snips WHERE name='{snipn}'")
            await message.edit("<b>Snip </b><i>{}</i><b> successfully removed from the list.</b>".format(snipn))
        else:
            await message.edit("<b>Snip </b><i>{}</i><b> not found in snips list</b>".format(snipn))

    async def remsnipsxxx(message):
        """Clears out the snip list."""
        ls = get_snip()
        if not ls:
            await message.edit("<b>There are no snips in the list to clear out.</b>")
            return
        set_snip("DELETE FROM snips")
        await message.edit("<b>All snips successfully removed from the list.</b>")

    async def snipsxxx(message):
        """Shows saved snips."""
        snips = ""
        get = get_snip()
        if not get:
            await message.edit("<b>No snip found in snips list.</b>")
            return
        for key in get:
            snips += "<b> -  " + key[0] + "</b>\n"
        snipl = "<b>Snips that you saved: </b>\n\n" + snips
        await message.edit(snipl)

    async def othersxxx(message):
        """Turns on/off snips for others usage."""
        state = utils.get_arg(message)
        if state == "on":
            others("DELETE FROM others")
            others("INSERT INTO others (other) VALUES ('on')")
            await message.edit("<b>Snips are now open to use for anyone.</b>")
        elif state == "off":
            others("DELETE FROM others")
            await message.edit("<b>Snips are now turned off for others.</b>")
            return

    async def watchout(message):
        snips = get_snip()
        if not snips:
            return
        args = message.text
        if not get_others():
            if message.sender_id != (await message.client.get_me()).id:
                return
        if args.startswith("$"):
            argsraw = args[1::]
            for key in snips:
                if argsraw == key[0]:
                    value = (
                        key[1] if not key[2]
                        else await message.client.get_messages(get_storage()[0][0], ids=key[2]))
                    if isinstance(value, str):
                        if message.sender_id == (await message.client.get_me()).id:
                            await message.edit(value)
                        else:
                            await message.reply(value)
                    else:
                        await message.client.send_message(message.chat_id, value)
