import logging
from database.mongo import cli


cli = cli["NiceGrill"]["AFK"]


def set_afk(msg, time):
    return cli.insert_one({"Message": msg, "AFKTime": time})

def set_godark(opt):
    return cli.insert_one({"GoDark": opt})

def check_afk():
    return cli.find_one({"Message": {"$exists": True}})

def check_godark():
    return cli.find_one({"GoDark": {"$exists": True}})

def stop_afk():
    return cli.delete_one({"Message": {"$exists": True}})
