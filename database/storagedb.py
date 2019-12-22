import logging
from database.mongo import cli


cli = cli["NiceGrill"]["Storage"]


def save_file(name, path, file):
    return cli.insert_one({"Name": name, "Path": path, "File": file})

def update_file(name, path, newfile):
    return cli.update_one(
        {"Name": name}, {"$set": {"File": newfile, "Path": path}})

def check():
    return (False if not [x for x in cli.find({}, {"File": 0})]
        else [x for x in cli.find({}, {"File": 0})])

def retrieve():
    return (False if not [x for x in cli.find({})]
        else [x for x in cli.find({})])

def check_one(name):
    return (False if not cli.find_one({"Name": name})
        else True)

def delete():
    return cli.delete_many({})

def delete_one(name):
    return cli.delete_one({"Name": name})
