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


cli = cli["NiceGrill"]["AFK"]


async def set_afk(msg, time):
    return cli.insert_one({"Message": msg, "AFKTime": time})

async def set_godark(opt):
    return cli.insert_one({"GoDark": opt})

async def check_afk():
    return cli.find_one({"Message": {"$exists": True}})

async def check_godark():
    return cli.find_one({"GoDark": {"$exists": True}})

async def stop_afk():
    return cli.delete_one({"Message": {"$exists": True}})
