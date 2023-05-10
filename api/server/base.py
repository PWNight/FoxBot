import disnake as discord
import sqlite3


def guild(guild):
    connection = sqlite3.connect('data/db/main/Database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS guilds(guild INT, name TEXT, prefix TEXT, language TEXT, autorole INT, modlogs INT, welcome INT, goodbye INT, lvlmessage INT, warn INT, _warn TEXT)'.format(guild))
    cursor.execute(f"SELECT * FROM guilds WHERE guild = {guild.id}")
    result = cursor.fetchone()
    return result
def user(user):
    connection = sqlite3.connect('data/db/main/Database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS users(guild INT, name TEXT, id INT, xp INT, level INT, warn INT)'.format(user))
    cursor.execute(f"SELECT * FROM users WHERE guild = {user.guild.id} AND id = {user.id}")
    result = cursor.fetchone()
    return result

def bages(user):
    connection = sqlite3.connect('data/db/main/Database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS bages(user_name TEXT, userid BIGINT, dev INT, moder INT, bughunt INT, idea INT, supported INT, partner INT, winter INT DEFAULT 0)'.format(user))
    cursor.execute(f"SELECT * FROM bages WHERE userid = {user.id}")
    result = cursor.fetchone()
    return result

def blacklist(user):
    connection = sqlite3.connect('data/db/main/Database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS blacklist(name TEXT, id INT, reason TEXT, mod_id INT, date TEXT)'.format(user))
    cursor.execute(f"SELECT * FROM blacklist WHERE id = {user.id}")
    result = cursor.fetchone()
    return result

def send(result):
    connection = sqlite3.connect('data/db/main/Database.db')
    cursor = connection.cursor()
    #print(result)
    cursor.execute(result)
    connection.commit()

def warns(warnid):
    connection = sqlite3.connect('data/db/main/Database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS warns(user_name TEXT, user_id BIGINT, moder_name TEXT, moder_id BIGINT, warnid INT)'.format(warnid))
    cursor.execute(f"SELECT * FROM guilds WHERE guild = {guild.id}")
    result = cursor.fetchone()
    return result