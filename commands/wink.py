import disnake as discord
import requests
import json
from disnake.ext import commands
from api.check import utils, block
from api.server import base, main


class Wink(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="подмигнуть", description="Подмигивает указанному участнику или кому-то неопределённому.", test_guilds=[921483461016031263])
    @block.block()
    async def wink(self, inter, member: discord.Member = None):
        response = requests.get('https://some-random-api.ml/animu/wink')
        json_data = json.loads(response.text)

        embed = discord.Embed(color = 0xFFA500)
        if member != None:
            embed.description = main.get_lang(inter.guild, "WINK_ARGS").format(inter.author.mention, member.mention)
        else:
            embed.description = main.get_lang(inter.guild, "WINK_NOARGS").format(inter.author.mention)
        embed.set_image(url = json_data['link'])

        await inter.send(embed = embed)


def setup(client):
    client.add_cog(Wink(client))