import sqlite3
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)



#  Notes

async def add_note(chatid, key, value, file):
    try:
        connection = sqlite3.connect("database/database.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS notes (chat, key PRIMARY KEY, value, id)")
        cursor.execute("INSERT INTO notes (chat , key, value, id) VALUES (?, ?, ?, ?)", (chatid, key, value, file))
        connection.commit()
    except Exception:
        logger.exception("")


async def get_notes(chatid):
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT key FROM notes WHERE chat = {}".format(chatid))
        notes = cursor.fetchall()
        return notes
    except sqlite3.OperationalError as e:
        return None


async def del_note(chatid, key):
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE  FROM notes WHERE chat = {} AND key = '{}'".format(chatid, key))
        connection.commit()
        return True
    except sqlite3.OperationalError as e:
        return False
        logger.exception("")

async def del_notes(chatid):
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM notes WHERE chat = {}".format(chatid))
        connection.commit()
        return True
    except sqlite3.OperationalError as e:
        return False
        logger.exception("")
    
async def get_note(chatid, key):
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT value, id FROM notes WHERE chat = {} AND key = '{}'".format(chatid, key))
        note = cursor.fetchall()
        return note
    except sqlite3.OperationalError as e:
        return None
        logger.exception("")


#  Filters


async def add_filter(chatid, key, value, file):
    try:
        connection = sqlite3.connect("database/database.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS filters (chat, key PRIMARY KEY, value, id)")
        cursor.execute("INSERT INTO filters (chat , key, value, id) VALUES (?, ?, ?, ?)", (chatid, key, value, file))
        connection.commit()
    except Exception:
        logger.exception("")


async def get_filters(chatid):
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM filters WHERE chat = {}".format(chatid))
        filters = cursor.fetchall()
        return filters
    except sqlite3.OperationalError as e:
        return None


async def del_filter(chatid, key):
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE  FROM filters WHERE chat = {} AND key = '{}'".format(chatid, key))
        connection.commit()
        return True
    except sqlite3.OperationalError as e:
        return False
        logger.exception("")
    
async def del_filters(chatid):
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM filters WHERE chat = {}".format(chatid))
        connection.commit()
        return True
    except sqlite3.OperationalError as e:
        return False
        logger.exception("")



#  Restart

async def add_status(status, chat, msgid):
    try:
        connection = sqlite3.connect("database/database.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS restart (status, chat, id)")
        cursor.execute("INSERT INTO restart (status , chat, id) VALUES (?, ?, ?)", (status, chat, msgid))
        connection.commit()
    except Exception:
        logger.exception("")
        return None
        
def get_status():
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT chat, id FROM restart")
        state = cursor.fetchall()
        return state
    except sqlite3.OperationalError:
        return None


def del_status():
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM restart")
        connection.commit()
    except sqlite3.OperationalError:
        return None



#  Storage

def add_storage(channel):
    try:
        connection = sqlite3.connect("database/database.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS storage (id)")
        cursor.execute("INSERT INTO storage (id) VALUES (?)", (channel,))
        connection.commit()
    except Exception:
        logger.exception("")
        return None
        
def get_storage():
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM storage")
        id = cursor.fetchall()
        return id
    except sqlite3.OperationalError as e:
        return None

def del_storage():
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM storage")
        connection.commit()
    except sqlite3.OperationalError as e:
        logger.exception("")
        return None

def setpath(command):
    try:
        connection = sqlite3.connect("database/database.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS downloader (path)")
        cursor.execute(command)
        connection.commit()
        return True
    except Exception:
        logger.exception("")
        return False
        
def getpath():
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM downloader")
        path = cursor.fetchall()
        return path
    except sqlite3.OperationalError as e:
        return None



#  Prefix

def set_pref(command):
    try:
        connection = sqlite3.connect("database/database.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS core (prefix)")
        cursor.execute(command)
        connection.commit()
    except Exception:
        logger.exception("")
        return None


def get_pref():
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM core")
        prefix = cursor.fetchall()
        return prefix
    except sqlite3.OperationalError as e:
        pass


#  AFK

async def set_afk(status, msg, time):
    try:
        connection = sqlite3.connect("database/database.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS afk (status, msg, time)")
        cursor.execute("INSERT INTO afk (status, msg, time) VALUES (?, ?, ?)", (status, msg, time))
        connection.commit()
    except Exception:
        logger.exception("")
        return None
        
async def get_afk():
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM afk")
        afk = cursor.fetchall()
        return afk
    except sqlite3.OperationalError as e:
        return None

async def clr_afk():
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE  FROM afk")
        connection.commit()
    except sqlite3.OperationalError as e:
        logger.exception("")
        return




# APPROVALS

def auth(command):
    try:
        connection = sqlite3.connect("database/database.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS auth (id PRIMARY KEY)")
        cursor.execute(command)
        connection.commit()
    except Exception:
        logger.exception("")


def get_auth():
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM auth")
        notes = cursor.fetchall()
        return notes
    except sqlite3.OperationalError as e:
        return None


def setPM(command):
    try:
        connection = sqlite3.connect("database/database.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS antipm (mute, max, supblock)")
        cursor.execute(command)
        connection.commit()
    except Exception:
        logger.exception("")
        return None


def getPM():
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM antipm")
        getpm = cursor.fetchall()
        return getpm
    except sqlite3.OperationalError as e:
        return None

        

#  STATS

def setStats(command):
    try:
        connection = sqlite3.connect("database/database.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS stats (id, name, msg)")
        cursor.execute(command)
        connection.commit()
    except Exception:
        logger.exception("")
        return None

def getStats():
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM stats")
        msg = cursor.fetchall()
        return msg
    except sqlite3.OperationalError as e:
        return None


#  STICKERS

def set_Packid(id):
    try:
        connection = sqlite3.connect("database/database.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS stickers (id TEXT)")
        cursor.execute(f"INSERT INTO stickers (id) VALUES ('{id}')")
        connection.commit()
    except Exception:
        logger.exception("")
        return None


def get_Packid():
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM stickers")
        id = cursor.fetchall()
        return id
    except sqlite3.OperationalError as e:
        return None


def del_Packid():
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM stickers")
        connection.commit()
    except sqlite3.OperationalError as e:
        logger.exception("")
        return None


# ADMİN

def add(command):
    try:
        connection = sqlite3.connect("database/database.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS admin (id INT, mute INT, gmute INT, gban INT, chatid INT)")
        cursor.execute(command)
        connection.commit()
    except Exception:
        logger.exception("")
        return None

def get():
    try:
        connection = sqlite3.connect("database/database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM admin")
        users = cursor.fetchall()
        return users
    except Exception:
        return None


# WEATHER

def setcity(command):
    try:
        connection = sqlite3.connect("database/database.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS weather (city)")
        cursor.execute(command)
        connection.commit()
    except Exception:
        logger.exception("")
        return None

def getcity():
    try:
        connection = sqlite3.connect("database/database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM weather")
        city = cursor.fetchall()
        return city
    except Exception:
        return None



# GDRIVE

def setGFolder(command):
    try:
        connection = sqlite3.connect("database/database.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS gdrive (folderid)")
        cursor.execute(command)
        connection.commit()
    except Exception:
        logger.exception("")
        return None

def getGFolder():
    try:
        connection = sqlite3.connect("database/database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM gdrive")
        folderid = cursor.fetchall()
        return folderid
    except Exception:
        return None
