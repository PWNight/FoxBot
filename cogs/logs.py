import disnake as discord
from disnake.ext import commands
from datetime import datetime


logs_guildschat = False #Логирование чата с гильдии (on_message) [Фалн находится в директории (.\data\logs\guilds) ]


class Logs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.logger(self.__class__.__name__, 'cogs')

    #MESSAGE
    @commands.Cog.listener()
    async def on_message(self, message):
        if logs_guildschat:
            timeshtamp = datetime.now().replace(microsecond = 0)
            
            with open(f"data/logs/guilds/{message.guild.id}_on_message.log", "a", encoding = "utf-8") as file:
                    file.write(f"Пользвоатель {message.author} написал: [ {message.content} ]\n")
        else:
            pass

        
def setup(client):
    client.add_cog(Logs(client))