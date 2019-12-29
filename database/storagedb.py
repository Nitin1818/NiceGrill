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


cli = cli["NiceGrill"]["Storage"]


async def save_file(name, path, file):
    return cli.insert_one({"Name": name, "Path": path, "File": file})

async def update_file(name, path, newfile):
    return cli.update_one(
        {"Name": name}, {"$set": {"File": newfile, "Path": path}})

async def check():
    return (False if not [x for x in cli.find({}, {"File": 0})]
        else [x for x in cli.find({}, {"File": 0})])

async def retrieve():
    return (False if not [x for x in cli.find({})]
        else [x for x in cli.find({})])

async def check_one(name):
    return (False if not cli.find_one({"Name": name})
        else True)

async def delete():
    return cli.delete_many({})

async def delete_one(name):
    return cli.delete_one({"Name": name})
