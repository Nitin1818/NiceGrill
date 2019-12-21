import logging
from database.mongo import cli


cli = cli["NiceGrill"]["Dloads"]


def dload(name, link):
    return cli.insert_one({"Name": name, "URL": link})

def unload(name):
    return cli.delete_one({"Name": name})

def check_dload():
    return (False if not cli.find({"Name": {"$exists": True}})
        else cli.find({"Name": {"$exists": True}}))

def delete(name):
    return cli.delete_one({name: {"$regex": "."}})
        

