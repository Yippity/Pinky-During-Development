# Pinky's code for interacting with a SQLite Database
# The purpose of using SQL is to enable Pinky's reaction role feature while maintaining efficiency
# SQLite was chosen over its alternatives for its lightweight nature and built-in Python functionality
# SQL queries will never be used from sources external to this specific .py file, only data being entered and retrieved.
# The code is formatted to not allow SQL injection


import sqlite3
import pickle  # Used for converting data into raw byte-streams to store in database


# Connect to database, or create it and rr_messages table if not found
db = sqlite3.connect("reaction_roles.db")
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS rr_messages (id INTEGER PRIMARY KEY, roles BLOB, emojis BLOB)")


# Enter necessary ordered data into database when reaction roles are made
def setEntry(key: int, roles: list, emojis: list):
    rolesEntry = pickle.dumps(roles)
    emojiEntry = pickle.dumps(emojis)
    cursor.execute("INSERT OR REPLACE INTO rr_messages (id, roles, emojis) VALUES (?, ?, ?)", (key, rolesEntry, emojiEntry))
    db.commit()

# Retrieve data from database when message is reacted to
def getEntry(key: int):
    cursor.execute("SELECT roles, emojis FROM rr_messages WHERE id = ?", (key,))
    dbEntry = cursor.fetchone()
    if not dbEntry:  # If message not in database, don't bother looking further
        return
    roles = pickle.loads(dbEntry[0])
    emojis = pickle.loads(dbEntry[1])
    return [roles, emojis]


# Delete entry with given key, intended for removing messages from database when they are deleted in Discord
def deleteEntry(key: int):
    cursor.execute("DELETE FROM rr_messages WHERE id = ?", (key,))
    db.commit()
