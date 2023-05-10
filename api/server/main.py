import disnake as discord
import json
import sqlite3
import datetime
import random
from configs import config


def get_lang(guild, key):
    with open(f'data/languages/ru.json', encoding='utf-8') as f:
        data = json.load(f)

    return data[key]


def done(guild, args):
    em = discord.Embed(colour=0x2ecc70, title=f'{config.okay} | {get_lang(guild, "EMBED_DONE")}', description=args)
    return em

def warn(guild, args):
    em = discord.Embed(colour=0x2ecc70, title=f'{config.warning} | {get_lang(guild, "EMBED_WARN")}', description=args)
    return em

def deny(guild, args):
    em = discord.Embed(colour=0xe74444, title=f'{config.error} | {get_lang(guild, "EMBED_DENY")}', description=args)
    return em

def ban(guild, args):
    em = discord.Embed(colour=0xe74444, title=f'{config.error}  | {get_lang(guild, "EMBED_BAN")}', description=args)
    return em

def embed(args, c=0x922ad3):
    em = discord.Embed(colour=c, description=args)
    return em


def time():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")


def year():
    return str(datetime.datetime.now().year)


def random_color():
    color = ('#%06x' % random.randint(8, 0xFFFFFF))
    color = int(color[1:], 16)
    color = discord.Color(value=color)
    return color