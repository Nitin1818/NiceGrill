from database.mongo import cli
import logging


cli = cli["NiceGrill"]["AntiPM"]


def set_antipm(opt):
    return cli.insert_one({"AntiPM": opt})

def approve(user):
    return cli.insert_one({"Approved": user})

def set_limit(digit):
    return cli.insert_one({"Limit": digit})

def set_notif(opt):
    return cli.insert_one({"Notifications": opt})

def set_sblock(opt):
    return cli.insert_one({"SuperBlock": opt})

def check_antipm():
    return (False if not cli.find_one({"AntiPM": {"$exists": True}})
        else cli.find_one({"AntiPM": {"$exists": True}})["AntiPM"])

def check_limit():
    return (3 if not cli.find_one({"Limit": {"$exists": True}})
        else cli.find_one({"Limit": {"$exists": True}})["Limit"])
    
def check_sblock():
    return (False if not cli.find_one({"SuperBlock": {"$exists": True}})
        else cli.find_one({"SuperBlock": {"$exists": True}})["SuperBlock"])

def check_notifs():
    return (True if not cli.find_one({"Notifications": {"$exists": True}})
        else cli.find_one({"Notifications": {"$exists": True}})["Notifications"])

def check_approved(user):
    return cli.find_one({"Approved": user})

def delete(obj):
    if obj == "Notifications" or obj == "AntiPM":
        cli.delete_one({obj: True})
        cli.delete_one({obj: False})
        return
    if obj == "Limit":
        return cli.delete_one({obj: {"$regex": "[0-9]"}})

def disapprove(user):
    return cli.delete_one({"Approved": user})
