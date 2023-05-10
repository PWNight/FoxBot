import disnake as discord
import json
from disnake.ext import commands


def developer():
    def wrapper(ctx):
        with open('data/access/dev.json') as f:
            devs = json.load(f)
        if ctx.author.id in devs:
            return True
        raise commands.MissingPermissions('В доступе отказано. Вы не являетесь разработчиком.')
    return commands.check(wrapper)