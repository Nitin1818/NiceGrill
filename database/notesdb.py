import logging
from database.mongo import cli


cli = cli["NiceGrill"]


def add(colname, chat, key, value, media):
    return cli[colname].insert_one(
        {"Chat": chat, "Key": key, "Value": value, "Media": media})

def check(colname, chat):
    return [x for x in cli[colname].find({"Chat": chat})]

def check_one(colname, chat, key):
    return cli[colname].find_one({"Chat": chat, "Key": key})

def update(colname, query, chat, key, value, media):
    return cli[colname].update_one(
        query, {"$set": {"Chat": chat, "Key": key, "Value": value, "Media": media}})

def delete(colname, chat):
    return cli[colname].delete_many({"Chat": chat})

def delete_one(colname, chat, key):
    return cli[colname].delete_one({"Chat": chat, "Key": key})