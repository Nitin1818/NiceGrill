import logging
from database.mongo import cli


cli = cli["NiceGrill"]["Admin"]


def add_user(user, mute, gmute, gban, chat):
    return cli.insert_one(
        {"User": user, "Mute": mute, "GMute": gmute, "GBan": gban, "Chat": chat})

def update_user(query, newvalue):
    return cli.update_one(query, {"$set": newvalue})

def check_user(user):
    return (False if not cli.find_one({"User": user})
        else cli.find_one({"User": user}))
