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


cli = cli["NiceGrill"]["Snips"]


async def add(key, value, media):
    return cli.insert_one(
        {"Key": key, "Value": value, "Media": media})

async def others(opt):
    return cli.insert_one({"Others": opt})

async def check():
    return (False if not [x for x in cli.find({}, {"Others": 0})]
        else [x for x in cli.find({}, {"Others": 0})])

async def check_one(key):
    return (False if not cli.find_one({"Key": key})
        else cli.find_one({"Key": key}))

async def check_others():
    return False if cli.find_one({"Others": False}) else True

async def update(query, key, value, media):
    return cli.update_one(
        query, {"$set": {"Key": key, "Value": value, "Media": media}})

async def delete():
    return cli.delete_many({})

async def delete_one(key):
    return cli.delete_one({"Key": key})

async def delete_others():
    cli.delete_one({"Others": {"$exists": True}})