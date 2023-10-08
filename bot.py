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
    
client.version = config.version
client.logger = Logger
client.config = config


client.run(config.token)