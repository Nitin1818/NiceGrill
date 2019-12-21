import logging
from database.mongo import cli


cli = cli["NiceGrill"]["Snips"]


def add(key, value, media):
    return cli.insert_one(
        {"Key": key, "Value": value, "Media": media})

def others(opt):
    return cli.insert_one({"Others": opt})

def check():
    return (False if not [x for x in cli.find({}, {"Others": 0})]
        else [x for x in cli.find({}, {"Others": 0})])

def check_one(key):
    return (False if not cli.find_one({"Key": key})
        else cli.find_one({"Key": key}))

def check_others():
    return False if cli.find_one({"Others": False}) else True

def update(query, key, value, media):
    return cli.update_one(
        query, {"$set": {"Key": key, "Value": value, "Media": media}})

def delete():
    return cli.delete_many({})

def delete_one(key):
    return cli.delete_one({"Key": key})

def delete_others(opt):
    cli.delete_one({"Others": True})
    cli.delete_one({"Others": False})