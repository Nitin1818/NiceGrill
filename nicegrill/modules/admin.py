from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest
from telethon.tl.types import ChatAdminRights, ChatBannedRights
from telethon.errors.rpcerrorlist import *
from telethon.tl import functions
from database.allinone import add, get
from .. import utils
from datetime import timedelta
import logging

PROMOTE = ChatAdminRights(
    post_messages=None,
    add_admins=None,
    invite_users=None,
    change_info=True,
    ban_users=None,
    delete_messages=True,
    pin_messages=True,
    edit_messages=None)

DEMOTE = ChatAdminRights(
    post_messages=None,
    add_admins=None,
    invite_users=None,
    change_info=None,
    ban_users=None,
    delete_messages=None,
    pin_messages=None,
    edit_messages=None)

BAN = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True)

UNBAN = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None)

MUTE = ChatBannedRights(
    until_date=timedelta(days=366),
    send_messages=True)

UNMUTE = ChatBannedRights(
    until_date=timedelta(days=366),
    send_messages=False)

class Admin:

    async def promotexxx(message):
        await message.edit("<b>Promoting...</b>")
        chat = message.input_chat
        try:
            user = (
                (await message.client.get_entity(utils.get_arg(message))).id if not message.is_reply else
                (await message.get_reply_message()).sender.id)
        except ValueError:
            await message.edit("<b>No user found in that name</b>")
            return
        try:
            await message.client(EditAdminRequest(chat, user, PROMOTE, "Admin"))
            await message.edit("<b>Successfully promoted</b>")
        except TypeError:
            await message.edit("<b>Are you sure this is a genuine chat?</b>")
        except AdminsTooMuchError:
            await message.edit("<b>There are too many admins in this chat</b>")
        except UserPrivacyRestrictedError:
            await message.edit("<b>The user's privacy settings do not allow you to do this</b>")
        except UserNotMutualContactError:
            await message.edit("<b>The provided user is not a mutual contact</b>")
        except UserIdInvalidError:
            await message.edit("<b>Specified user is a no go</b>")
        except UserCreatorError:
            await message.edit("<b>Wtf, that is the chat owner..</b>")
        except RightForbiddenError:
            await message.edit("<b>You either don't have enough permissions or there's something wrong with the admin rights</b>")
        except ChatAdminRequiredError:
            await message.edit("<b>Oh honey, you're not admin enough to promote this user 🙄</b>")

    async def demotexxx(message):
        await message.edit("<b>Demoting...</b>")
        chat = message.input_chat
        try:
            user = (
                (await message.client.get_entity(utils.get_arg(message))).id if not message.is_reply else
                (await message.get_reply_message()).sender.id)
        except ValueError:
            await message.edit("<b>No user found in that name</b>")
            return
        try:
            await message.client(EditAdminRequest(chat, user, DEMOTE, "User"))
            await message.edit("<b>Successfully demoted</b>")
        except TypeError:
            await message.edit("<b>Are you sure this is a genuine chat?</b>")
        except AdminsTooMuchError:
            await message.edit("<b>There are too many admins in this chat</b>")
        except UserPrivacyRestrictedError:
            await message.edit("<b>The user's privacy settings do not allow you to do this</b>")
        except UserNotMutualContactError:
            await message.edit("<b>The provided user is not a mutual contact</b>")
        except UserIdInvalidError:
            await message.edit("<b>Specified user is a no go</b>")
        except UserCreatorError:
            await message.edit("<b>Wtf, that is the chat owner..</b>")
        except RightForbiddenError:
            await message.edit("<b>You either don't have enough permissions or there's something wrong with the admin rights</b>")
        except ChatAdminRequiredError:
            await message.edit("<b>Oh honey, you're not admin enough to promote this user 🙄</b>")


    async def mutexxx(message):
        await message.edit("<b>Muting...</b>")
        chat = message.input_chat
        try:
            user = (
                (await message.client.get_entity(utils.get_arg(message))).id if not message.is_reply else
                (await message.get_reply_message()).sender.id)
        except ValueError:
            await message.edit("<b>No user found in that name</b>")
            return
        if not get() or str(user) not in str(get()):
            command = f'INSERT INTO admin (id, mute, gmute, gban, chatid) VALUES ({user}, 1, 0, 0, {message.chat_id})'
        elif str(user) in str(get()):
            command = f'UPDATE admin SET mute=1 WHERE id={user}'
        add(command)
        try:
            await message.client(EditBannedRequest(chat, user, MUTE))
            await message.edit("<b>Successfully muted</b>")
        except TypeError:
            await message.edit("<b>You need to be in a chat to do this</b>")
            return
        except UserAdminInvalidError:
            await message.edit("<b>You're either not an admin or that's more admin than you</b>")
        except UserIdInvalidError:
            await message.edit("<b>Specified user is a no go</b>")
        except ChatAdminRequiredError:
            await message.edit("<b>Oh honey, you're not admin enough to mute this user 🙄</b>")

    async def unmutexxx(message):
        await message.edit("<b>Unmuting...</b>")
        chat = message.input_chat
        try:
            user = (
                (await message.client.get_entity(utils.get_arg(message))).id if not message.is_reply else
                (await message.get_reply_message()).sender.id)
        except ValueError:
            await message.edit("<b>No user found in that name</b>")
            return
        if not get() or str(user) not in str(get()):
            pass
        elif str(user) in str(get()):
            command = f'UPDATE admin SET mute=0 WHERE id={user}'
            add(command)
        try:
            await message.client(EditBannedRequest(chat, user, UNMUTE))
            # add_unmuted(user)
            await message.edit("<b>Successfully unmuted</b>")
        except TypeError:
            await message.edit("<b>You need to be in a chat to do this</b>")
            return
        except TypeError:
            await message.edit("<b>You need to be in a chat to do this</b>")
            return
        except UserAdminInvalidError:
            await message.edit("<b>You're either not an admin or that's more admin than you</b>")
        except UserIdInvalidError:
            await message.edit("<b>Specified user is a no go</b>")
        except ChatAdminRequiredError:
            await message.edit("<b>Oh honey, you're not admin enough to unmute this user 🙄</b>")

    async def kickxxx(message):
        chat = message.input_chat
        try:
            user = (
                (await message.client.get_entity(utils.get_arg(message))).id if not message.is_reply else
                (await message.get_reply_message()).sender.id)
        except ValueError:
            await message.edit("<b>No user found in that name</b>")
            return
        try:
            await message.client(EditBannedRequest(chat, user, ChatBannedRights(
                until_date=None, view_messages=True)))
            await message.edit("<b>Kicked...</b>")
        except TypeError:
            await message.edit("<b>You need to be in a chat to do this</b>")
            return
        except UserAdminInvalidError:
            await message.edit("<b>You're either not an admin or that's more admin than you</b>")
        except UserIdInvalidError:
            await message.edit("<b>Specified user is a no go</b>")
        except ChatAdminRequiredError:
            await message.edit("<b>Oh honey, you're not admin enough to kick this user 🙄</b>")

    async def banxxx(message):
        chat = message.input_chat
        try:
            user = (
                (await message.client.get_entity(utils.get_arg(message))).id if not message.is_reply else
                (await message.get_reply_message()).sender.id)
        except ValueError:
            await message.edit("<b>No user found in that name</b>")
            return
        try:
            await message.client(EditBannedRequest(chat, user, BAN))
            await message.edit("<b>Banned...</b>")
        except TypeError:
            await message.edit("<b>You need to be in a chat to do this</b>")
            return
        except UserAdminInvalidError:
            await message.edit("<b>You're either not an admin or that's more admin than you</b>")
        except UserIdInvalidError:
            await message.edit("<b>Specified user is a no go</b>")
        except ChatAdminRequiredError:
            await message.edit("<b>Oh honey, you're not admin enough to ban this user 🙄</b>")

    async def unbanxxx(message):
        chat = message.input_chat
        try:
            user = (
                (await message.client.get_entity(utils.get_arg(message))).id if not message.is_reply else
                (await message.get_reply_message()).sender.id)
        except ValueError:
            await message.edit("<b>No user found in that name</b>")
            return
        try:
            await message.client(EditBannedRequest(chat, user, UNBAN))

            await message.edit("<b>Alright, fine..All is forgiven, unbanned..</b>")
        except TypeError:
            await message.edit("<b>You need to be in a chat to do this</b>")
            return
        except UserAdminInvalidError:
            await message.edit("<b>You're either not an admin or that's more admin than you</b>")
        except UserIdInvalidError:
            await message.edit("<b>Specified user is a no go</b>")
        except ChatAdminRequiredError:
            await message.edit("<b>Oh honey, you're not admin enough to unban this user 🙄</b>")

    async def pinxxx(message):
        reply = await message.get_reply_message()
        loud = True if utils.get_arg(message) == "loud" else False
        if not reply:
            await message.edit("<b>Reply to a message first.</b>")
            return
        await message.client.pin_message(
            message.input_chat, reply.id, notify=loud)
        await message.edit("<b>Pinned succesfully.</b>")


    async def unpinxxx(message):
        reply = await message.get_reply_message()
        if not reply:
            await message.edit("<b>Reply to a message first.</b>")
            return
        await message.client.pin_message(
            message.input_chat, reply.id, notify=loud)
        await message.edit("<b>Pinned succesfully.</b>")


    async def gbanxxx(message):
        chat = message.input_chat
        try:
            user = (
                (await message.client.get_entity(utils.get_arg(message))).id if not message.is_reply else
                (await message.get_reply_message()).sender.id)
        except ValueError:
            await message.edit("<b>No user found in that name</b>")
            return
        if not get() or str(user) not in str(get()):
            command = f'INSERT INTO admin (id, mute, gmute, gban) VALUES ({user}, 0, 0, 1)'
        elif str(user) in str(get()):
            command = f'UPDATE admin SET gban=1 WHERE id={user}'
        add(command)
        await message.edit("<b>Globally banned...</b>")


    async def ungbanxxx(message):
        chat = message.input_chat
        try:
            user = (
                (await message.client.get_entity(utils.get_arg(message))).id if not message.is_reply else
                (await message.get_reply_message()).sender.id)
        except ValueError:
            await message.edit("<b>No user found in that name</b>")
            return
        if not get() or str(user) not in str(get()):
            await message.edit('<b>This user is not gbanned</b>')
            return
        elif str(user) in str(get()):
            command = f'UPDATE admin SET gban=0 WHERE id={user}'
            add(command)
        await message.edit("<b>Global ban lifted...</b>")

    async def gmutexxx(message):
        await message.edit("<b>Muting...</b>")
        chat = message.input_chat
        try:
            user = (
                (await message.client.get_entity(utils.get_arg(message))).id if not message.is_reply else
                (await message.get_reply_message()).sender.id)
        except ValueError:
            await message.edit("<b>No user found in that name</b>")
            return
        if not get() or str(user) not in str(get()):
            command = f'INSERT INTO admin (id, mute, gmute, gban) VALUES ({user}, 1, 1, 0)'
        elif str(user) in str(get()):
            command = f'UPDATE admin SET gmute=1 WHERE id={user}'
        add(command)
        await message.edit("<b>Globally muted</b>")

    async def ungmutexxx(message):
        await message.edit("<b>Unmuting...</b>")
        chat = message.input_chat
        try:
            user = (
                (await message.client.get_entity(utils.get_arg(message))).id if not message.is_reply else
                (await message.get_reply_message()).sender.id)
        except TypeError:
            await message.edit("<b>No user found in that name</b>")
            return
        if not get() or str(user) not in str(get()):
            await message.edit('<b>This user is not gmuted</b>')
            return
        elif str(user) in str(get()):
            command = f'UPDATE admin SET gmute=0 WHERE id={user}'
            add(command)
        await message.edit("<b>Global mute lifted</b>")

    async def kickmexxx(message):
        await message.edit("<b>Okay, im leaving the chat</b>")
        await message.client(functions.channels.LeaveChannelRequest(channel=message.chat_id))

    async def watchout(message):
        user = message.sender_id
        chat = message.chat_id
        if get():
            for i in range(len(get())):
                if (await message.client.get_me()).id == get()[i][0]:
                    return
                if user in get()[i] and get()[i][2] == 1:
                    await message.delete()
                if user in get()[i] and get()[i][4] == message.chat_id and get()[i][1] == 1:
                    await message.delete()
                if user in get()[i] and get()[i][3] == 1:
                    try:
                        await message.client(EditBannedRequest(chat, user, BAN))
                    except Exception:
                        pass