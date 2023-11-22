import disnake as discord
from disnake.ext import commands
from os import listdir
from util.logger import Logger
from api.server import main
from configs import config


intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.guilds = True
intents.messages = True

client = commands.Bot(
    command_prefix = config.prefix,
    help_command = None,
    intents = discord.Intents.all()
)

for filename in listdir("./commands/"):
    if filename.endswith(".py"):
        client.load_extension(f"commands.{filename[:-3]}")
    else:
        if (filename != "__pycache__"):
            for file in listdir(f"./commands/{filename}/"):
                if file.endswith(".py"):
                    client.load_extension(f"commands.{filename}.{file[:-3]}")

for filename in listdir("./events/"):
    if filename.endswith(".py"):
        client.load_extension(f"events.{filename[:-3]}")

@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.reply(embed = main.done(ctx.guild, f"Модуль `{extension}` был загружен"))

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.reply(embed = main.done(ctx.guild, f"Модуль `{extension}` был отключен"))

@client.command()
async def reload(ctx, extension):
    client.reload_extension(f"cogs.{extension}")
    await ctx.reply(embed = main.done(ctx.guild, f"Модуль `{extension}` был перезагружен"))
    
# * ----------------

@client.command()
async def cload(ctx, extension):
    client.load_extension(f"commands.{extension}")
    await ctx.reply(embed = main.done(ctx.guild, f"Команда `{extension}` была включена"))


@client.command()
async def cmd_unload(ctx, extension):
    client.unload_extension(f"commands.{extension}")
    await ctx.reply(embed = main.done(ctx.guild, f"Команда `{extension}` была отключена"))


@client.command()
async def cmd_reload(ctx, extension):
    client.reload_extension(f"commands.{extension}")
    await ctx.reply(embed = main.done(ctx.guild, f"Команда `{extension}` была перезагружена"))

# * ----------------

@client.command()
async def event_load(ctx, extension):
    client.load_extension(f"events.{extension}")
    await ctx.reply(embed = main.done(ctx.guild, f"Событие `{extension}` было включено"))

@client.command()
async def event_unload(ctx, extension):
    client.unload_extension(f"events.{extension}")
    await ctx.reply(embed = main.done(ctx.guild, f"Событие `{extension}` было отключено"))

@client.command()
async def event_reload(ctx, extension):
    client.reload_extension(f"events.{extension}")
    await ctx.reply(embed = main.done(ctx.guild, f"Событие `{extension}` было перезагружено"))

# * ----------------

@client.command()
async def log_load(ctx, extension):
    client.load_extension(f"logs.{extension}")
    await ctx.reply(embed = main.done(ctx.guild, f"Лог `{extension}` был загружен"))

@client.command()
async def log_unload(ctx, extension):
    client.unload_extension(f"logs.{extension}")
    await ctx.reply(embed = main.done(ctx.guild, f"Лог `{extension}` был отключен"))

@client.command()
async def log_reload(ctx, extension):
    client.reload_extension(f"logs.{extension}")
    await ctx.reply(embed = main.done(ctx.guild, f"Лог `{extension}` был  перезагружен"))
    
client.version = config.version
client.logger = Logger
client.config = config


client.run(config.token)