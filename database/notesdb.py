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


cli = cli["NiceGrill"]


async def add(colname, chat, key, value, media):
    return cli[colname].insert_one(
        {"Chat": chat, "Key": key, "Value": value, "Media": media})

async def check(colname, chat):
    return [x for x in cli[colname].find({"Chat": chat})]

async def check_one(colname, chat, key):
    return cli[colname].find_one({"Chat": chat, "Key": key})

async def update(colname, query, chat, key, value, media):
    return cli[colname].update_one(
        query, {"$set": {"Chat": chat, "Key": key, "Value": value, "Media": media}})

async def delete(colname, chat):
    return cli[colname].delete_many({"Chat": chat})

async def delete_one(colname, chat, key):
    return cli[colname].delete_one({"Chat": chat, "Key": key})