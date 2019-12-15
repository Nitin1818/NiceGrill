import logging
from .. import utils
from database.allinone import auth, get_auth, setPM, getPM
from telethon import functions, tl


class AntiPM:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    FLOOD_CTRL = 0
    ALLOWED = []
    USERS_AND_WARNS = {}
    
    WARNING = ("<b>I have not allowed you to PM, please ask or say whatever</b>"
                 "<b> it is in a group chat or at least ask for my permission to PM</b>\n\n"
                 "<b>I'm letting you off the hook for this time but be warned that </b>"
                 "<b>you will be blocked & reported spam if you continue.</b>")

    BLOCKED = ("<b>I have warned you several times now. However, you did not stop</b>"
                 "<b>spamming my chat. Therefore, you have been blocked and reported</b>"
                 "<b>as spam. Good luck!</b>")

    async def approvexxx(message):
        """Allows that person to PM you, you can either reply to user,
type their username or use this in their chat"""
        id = None if not utils.get_arg(message) else (await message.client.get_entity(utils.get_arg(message))).id
        reply = None if not message.is_reply else (await message.get_reply_message()).sender_id
        chat = None if not hasattr(message.to_id, "user_id") else message.chat_id
        if not reply and not id and not chat:
            await message.edit("<b>No user found</b>")
            return
        pick = reply or id or chat
        if pick == (await message.client.get_me()).id:
            await message.edit("<b>Why would you wanna approve yourself?</b>")
            return
        if str(pick) not in str(get_auth()):
            command = f"INSERT INTO auth (id) VALUES ({pick})"
        else:
            command = f"UPDATE auth SET id={pick}"
        auth(command)
        await message.edit(
            "<a href=tg://user?id={}>{}</a> <b>is approved to PM you now</b>"
            .format(pick, (await message.client.get_entity(pick)).first_name))


    async def disapprovexxx(message):
        """Prevents that person to PM you, you can either reply to user,
type their username or use this in their chat"""
        id = None if not utils.get_arg(message) else (await message.client.get_entity(utils.get_arg(message))).id 
        reply = None if not message.is_reply else (await message.get_reply_message()).sender_id
        chat = None if not hasattr(message.to_id, "user_id") else message.chat_id
        if not reply and not id and not chat:
            await message.edit("<b>No user found</b>")
            return
        pick = reply if not id and not chat else id or chat
        if pick == (await message.client.get_me()).id:
            await message.edit("<b>Why would you wanna disapprove yourself?</b>")
            return
        if str(pick) not in str(get_auth()):
            await message.edit("<b>User is not approved at all</b>")
        else:
            command = f"DELETE FROM auth WHERE id={pick}"
        auth(command)
        await message.edit(
            "<a href=tg://user?id={}>{}</a> <b>is disapproved to PM you now</b>"
            .format(pick, (await message.client.get_entity(pick)).first_name))


    async def blockxxx(message):
        """Simply blocks the person..duh!!"""
        id = None if not utils.get_arg(message) else (await message.client.get_entity(utils.get_arg(message))).id 
        reply = None if not message.is_reply else (await message.get_reply_message()).sender_id
        chat = None if not hasattr(message.to_id, "user_id") else message.chat_id
        if not reply and not id and not chat:
            await message.edit("<b>No user found</b>")
            return
        pick = reply or id or chat
        if pick == (await message.client.get_me()).id:
            await message.edit("<b>Why would you wanna block yourself?</b>")
            return
        await message.client(functions.contacts.BlockRequest(id=pick))
        if str(pick) in str(get_auth()):
            command = f"DELETE FROM auth WHERE id={pick}"
            auth(command)
        await message.edit(
            "<a href=tg://user?id={}>{}</a> <b>has been blocked</b>"
            .format(pick, (await message.client.get_entity(pick)).first_name))


    async def unblockxxx(message):
        """Simply unblocks the person..duh!!"""
        id = None if not utils.get_arg(message) else (await message.client.get_entity(utils.get_arg(message))).id 
        reply = None if not message.is_reply else (await message.get_reply_message()).sender_id
        chat = None if not hasattr(message.to_id, "user_id") else message.chat_id
        if not reply and not id and not chat:
            await message.edit("<b>No user found</b>")
            return
        pick = reply or id or chat
        if pick == (await message.client.get_me()).id:
            await message.edit("<b>Why would you wanna unblock yourself?</b>")
            return
        await message.client(functions.contacts.UnblockRequest(id=pick))
        await message.edit(
            "<a href=tg://user?id={}>{}</a> <b>has been unblocked</b>"
            .format(pick, (await message.client.get_entity(pick)).first_name))


    async def notifsxxx(message):
        """Ah this one again...It turns on/off tag notification
sounds from unwanted PMs. It auto-sends a
a message in your name until that user gets blocked or approved"""
        val = utils.get_arg(message)
        if not val:
            await message.edit("<b>Please type on/off</b>")
            return
        if val == "off":
            command = (
                "INSERT INTO antipm (mute) VALUES (0)" if not getPM()
                else "UPDATE antipm SET mute = 0")
            await message.edit("<b>Notifications from unapproved PMs are muted</b>")
        if val == "on":
            command = (
                "INSERT INTO antipm (mute) VALUES (0)" if not getPM()
                else "UPDATE antipm SET mute = 0")
            await message.edit("<b>Notifications from unapproved PMs are unmuted</b>")
        setPM(command)

    async def setlimitxxx(message):
        """This one sets a max. message limit for unwanted
PMs and when they go beyond it, bamm!"""
        limit = int(utils.get_arg(message))
        if not limit or not str(limit).isdigit():
            await message.edit("<b>Please type a number</b>")
            return
        if limit > 0:
            command = (
                "INSERT INTO antipm (max) VALUES (0)" if not getPM()
                else "UPDATE antipm SET max = 0")
            await message.edit("<b>Max. PM message limit successfully updated</b>")


    async def superblockxxx(message):
        """If unwanted users spams your chat, the chat 
will be deleted when the idiot passes the message limit"""
        val = utils.get_arg(message)
        if not val:
            await message.edit("<b>Please type on/off</b>")
            return
        if val == "on":
            command = (
                "INSERT INTO antipm (supblock) VALUES (1)" if not getPM()
                else "UPDATE antipm SET mute = 1")
            await message.edit("<b>Chats from unapproved PMs will be removed</b>")
        if val == "off":
            command = (
                "INSERT INTO antipm (supblock) VALUES (0)" if not getPM()
                else "UPDATE antipm SET mute = 0")
            await message.edit("<b>Chats from unapproved PMs will not be removed anymore</b>")


    async def watchout(message):
        if message.sender_id != (await message.client.get_me()).id and type(message.to_id) is tl.types.PeerUser:
            if getattr(message.sender, "bot", True):
                return
            AntiPM.ALLOWED.clear()
            [AntiPM.ALLOWED.append(ls[0]) for ls in get_auth()]
            if AntiPM.ALLOWED and message.sender_id in AntiPM.ALLOWED:
                return
            if not getPM()[0][0]:
                await message.client.send_read_acknowledge(message.chat_id)
            user = message.sender_id
            user_warns = 0 if user not in AntiPM.USERS_AND_WARNS else AntiPM.USERS_AND_WARNS[user]
            if user_warns <= getPM()[0][1] - 2:
                user_warns += 1
                AntiPM.USERS_AND_WARNS.update({user: user_warns})
                if not AntiPM.FLOOD_CTRL > 0:
                    AntiPM.FLOOD_CTRL += 1
                else:
                    AntiPM.FLOOD_CTRL = 0
                    return
                async for msg in message.client.iter_messages(entity=message.chat_id,
                                                              from_user='me',
                                                              search="I have not allowed you to PM",
                                                              limit=1):
                    await msg.delete()
                await message.reply(AntiPM.WARNING)
                return
            await message.reply(AntiPM.BLOCKED)
            await message.client(functions.messages.ReportSpamRequest(peer=message.sender_id))
            await message.client(functions.contacts.BlockRequest(id=message.sender_id))
            if getPM()[0][2] == 1:
                await message.client.delete_dialog(entity=message.chat_id, revoke=True)
            AntiPM.USERS_AND_WARNS.update({user: 0})