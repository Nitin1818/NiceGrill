import logging
from database.mongo import cli


cli = cli["NiceGrill"]["Alive"]


def set_name(name):
    return cli.insert_one({"ID": 1, "Name": name})

def set_message(msg):
    return cli.insert_one({"ID": 2, "Message": msg})

def check_name():
    return False if not cli.find_one({"ID": 1}) else cli.find_one({"ID": 1})["Name"]

def check_msg():
    return False if not cli.find_one({"ID": 2}) else cli.find_one({"ID": 2})["Message"]

def update(query, newvalue):
    return cli.update_one(query, {"$set": newvalue})
