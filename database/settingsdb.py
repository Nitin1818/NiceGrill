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

import logging
from database.mongo import cli

cli = cli["NiceGrill"]["Settings"]


async def set_city(city):
    return cli.insert_one({"City": city})

async def set_path(path):
    return cli.insert_one({"Path": path})

async def set_pack(pack):
    return cli.insert_one({"Pack": pack})

async def set_prefix(prefix):
    return cli.insert_one({"Prefix": prefix})

async def set_restart(chat, msg):
    return cli.insert_one({"Restart": True, "Chat": chat, "Message": msg})

async def set_asset(id):
    return cli.insert_one({"Asset": id})

async def set_gfolder(id):
    return cli.insert_one({"GFolder": id})

async def check_city():
    return ("" if not cli.find_one({"City": {"$exists": True}})
        else cli.find_one({"City": {"$exists": True}})["City"])

async def check_pack():
    return ("" if not cli.find_one({"Pack": {"$exists": True}})
        else cli.find_one({"Pack": {"$exists": True}})["Pack"])

async def check_path():
    return ("./" if not cli.find_one({"Path": {"$exists": True}})
        else cli.find_one({"Path": {"$exists": True}})["Path"])
    
async def check_prefix():
    return ("." if not cli.find_one({"Prefix": {"$exists": True}})
        else cli.find_one({"Prefix": {"$exists": True}})["Prefix"])

async def check_restart():
    return (False if not cli.find_one({"Message": {"$exists": True}})
        else cli.find_one({"Message": {"$exists": True}}))

async def check_asset():
    return (False if not cli.find_one({"Asset": {"$exists": True}})
        else cli.find_one({"Asset": {"$exists": True}})["Asset"])

async def check_gfolder():
    return (False if not cli.find_one({"GFolder": {"$exists": True}})
        else cli.find_one({"GFolder": {"$exists": True}})["GFolder"])

async def delete(obj):
    return cli.delete_one({obj: {"$exists": True}})
        

