import disnake as discord
import aiohttp
import io
from disnake.ext import commands
from api.check import utils, block
from api.server import base, main


class Triggered(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="триггер", description="📛 Запретная техника : Триггер указанного участника", test_guilds=[921483461016031263])
    @block.block()
    async def triggered(self, inter, member: discord.Member = None):
        if not member:
            member = inter.author

        try:
            async with aiohttp.ClientSession() as trigSession:
                async with trigSession.get(f'https://some-random-api.ml/canvas/triggered?avatar={member.avatar.url}') as trigImg:
                    imageData = io.BytesIO(await trigImg.read())

                    await trigSession.close()

                    await inter.send(file = discord.File(imageData, 'triggered.gif'))
        except:
            await inter.send(embed = main.deny(inter.guild, main.get_lang(inter.guild, "AVATAR_FIELD_VALUE1")))

def setup(client):
    client.add_cog(Triggered(client))