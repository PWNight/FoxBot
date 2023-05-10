import disnake as discord
import requests
import json
from disnake.ext import commands
from api.check import utils, block
from api.server import base, main


class Dog(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="собака", description="🐩 Показывает изображение собаки", test_guilds=[921483461016031263])
    @block.block()
    async def dog(self, inter):
        response = requests.get('https://some-random-api.ml/img/dog')
        json_data = json.loads(response.text)

        embed = discord.Embed(color = 0xFFA500, title = main.get_lang(inter.guild, "DOG_TITLE"))
        embed.set_image(url = json_data['link'])

        await inter.send(embed = embed)


def setup(client):
    client.add_cog(Dog(client))