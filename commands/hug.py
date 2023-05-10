import disnake as discord
import requests
import json
from disnake.ext import commands
from api.check import utils, block
from api.server import base, main


class Hug(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="обнять", description="👐 Обнимает указанного пользователя.", test_guilds=[921483461016031263])
    @block.block()
    async def hug(self, inter, member: discord.Member = None):
        response = requests.get('https://some-random-api.ml/animu/hug')
        json_data = json.loads(response.text)

        embed = discord.Embed(color = 0xFFA500)
        if member != None:
            embed.description = main.get_lang(inter.guild, "HUG_ARGS").format(inter.author.mention, member.mention)
        else:
            embed.description = main.get_lang(inter.guild, "HUG_NOARGS").format(inter.author.mention)
        embed.set_image(url = json_data['link'])

        await inter.send(embed = embed)


def setup(client):
    client.add_cog(Hug(client))