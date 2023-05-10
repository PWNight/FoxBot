import disnake as discord
import traceback
from datetime import datetime
from disnake.ext import commands


class OnError(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):

        self.client.logger(event, 'error')
        channel = self.client.get_channel(self.client.config.errorlogs)
        embed = discord.Embed(title='Ошибка События', color=9579219)
        embed.add_field(name='Событие', value=event)
        embed.description = f"{traceback.format_exc()}"
        embed.timestamp = datetime.utcnow()
        await channel.send(embed=embed)

def setup(client):
    client.add_cog(OnError(client))