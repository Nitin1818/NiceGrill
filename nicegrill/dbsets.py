from database.allinone import *

if not get_auth() or not getPM():
    stickerchat = "INSERT INTO auth (id) VALUES (0)"
    auth(stickerchat)
    max = "INSERT INTO antipm (max) VALUES (3)"
    setPM(max)
    notif = "UPDATE antipm SET mute = 1"
    setPM(notif)
    supblock = "UPDATE antipm SET supblock = 0"
    setPM(supblock)
    
if not getStats():
    setStats("INSERT INTO stats (id, name, msg) VALUES (1, False, False)")