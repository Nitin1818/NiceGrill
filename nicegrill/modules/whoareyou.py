import logging

class WhoAreYou:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    async def whoxxx(message):
        user  = (
            (await message.get_reply.message()).sender if message.is_reply
            else message.sender)
        identify = (
            f"<b>First Name:</b> <i>{user.first_name}</i>\n"
            f"<b>Last Name:</b> <i>{user.last_name}</i>\n"
            f"<b>Username:</b> <i>{user.username}</i>\n"
            f"<b>ID:</b> <i>{user.id}</i>\n"
            f"<b>Bot:</b> <i>{user.bot}</i>\n"
            f"<b>Permanent Link:</b> <a href=tg://user?id={user.id}>{user.first_name}</a>")
        await message.reply(identify)
