from nicegrill.modules import _init

def get_arg(message):
    split = message.message.message[1:].replace("\n", " \n").split(" ")
    return " ".join(split[1:])

def arg_split_with(message, char):
    args = get_arg(message).split(char)
    for space in args:
        if space.strip() == "": args.remove(space)
    return args

async def run(message):
    command = await message.get_reply_message()
    await message.client.edit_message(
        message.chat_id, command.id, await _init.modules[command.text.split(" ")[0]](command.text.split(" ")[1:]))