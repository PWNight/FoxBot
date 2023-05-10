import disnake as discord
import sqlite3
from disnake.ext import commands
from api.server import base, main


def block():
    async def wrapper(ctx):
        if base.blacklist(ctx.author) is not None:
            if ctx.author.id != base.blacklist(ctx.author)[1]:
                return True
            await ctx.reply(embed = main.deny(ctx.guild, main.get_lang(ctx.guild, 'CHECK_BLOCK').format(base.blacklist(ctx.author)[2], base.blacklist(ctx.author)[3], base.blacklist(ctx.author)[4], base.blacklist(ctx.author)[5])))
        else:
            return True
    return commands.check(wrapper)