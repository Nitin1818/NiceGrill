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


cli = cli["NiceGrill"]["Admin"]


async def add_user(user, mute, gmute, gban, chat):
    return cli.insert_one(
        {"User": user, "Mute": mute, "GMute": gmute, "GBan": gban, "Chat": chat})

async def update_user(query, newvalue):
    return cli.update_one(query, {"$set": newvalue})

async def check_user(user):
    return (False if not cli.find_one({"User": user})
        else cli.find_one({"User": user}))
