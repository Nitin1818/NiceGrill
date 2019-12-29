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


cli = cli["NiceGrill"]["Dloads"]


async def dload(name, link):
    return cli.insert_one({"Name": name, "URL": link})

async def unload(name):
    return cli.delete_one({"Name": name})

async def check_dload():
    return (False if not cli.find({"Name": {"$exists": True}})
        else cli.find({"Name": {"$exists": True}}))

async def delete(name):
    return cli.delete_one({name: {"$exists": True}})
        

