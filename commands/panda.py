import disnake as discord
import requests
import json
from disnake.ext import commands
from api.check import utils, block
from api.server import base, main


class Panda(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="панда", description="🐼 Показывает изображение панды", test_guilds=[921483461016031263])
    @block.block()
    async def panda(self, inter):
        response = requests.get('https://some-random-api.ml/img/panda')
        json_data = json.loads(response.text)

        embed = discord.Embed(color=0xFFA500, title = main.get_lang(inter.guild, "PANDA_TITLE"))
        embed.set_image(url = json_data['link'])

        await inter.send(embed = embed)


def setup(client):
    client.add_cog(Panda(client))