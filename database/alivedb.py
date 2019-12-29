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


cli = cli["NiceGrill"]["Alive"]


async def set_name(name):
    return cli.insert_one({"ID": 1, "Name": name})

async def set_message(msg):
    return cli.insert_one({"ID": 2, "Message": msg})

async def check_name():
    return False if not cli.find_one({"ID": 1}) else cli.find_one({"ID": 1})["Name"]

async def check_msg():
    return False if not cli.find_one({"ID": 2}) else cli.find_one({"ID": 2})["Message"]

async def update(query, newvalue):
    return cli.update_one(query, {"$set": newvalue})
