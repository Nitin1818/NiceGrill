from nicegrill.modules import _init

cli = None

def get_arg(message):
    split = message.message.message[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


def arg_split_with(message, char):
    args = get_arg(message).split(char)
    for space in args:
        if space.strip() == "":
            args.remove(space)
    return args
