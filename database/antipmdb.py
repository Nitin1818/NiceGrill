#    This file is part of NiceGrill.

#    NiceGrill is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    NiceGrill is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with NiceGrill.  If not, see <https://www.gnu.org/licenses/>.

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
    return cli.delete_one({obj: {"$exists": True}})

def disapprove(user):
    return cli.delete_one({"Approved": user})
