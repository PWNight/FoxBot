import disnake as discord
import random
from disnake.ext import commands
from api.check import utils, block
from api.server import base, main


class Tickle(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="щекотать", description="😆 Щекочет указанного участника", test_guilds=[921483461016031263])
    @block.block()
    async def tickle(self, inter, member: discord.Member = None):
        tickkle = [
            'https://i.gifer.com/KVjQ.gif',
            'https://i.gifer.com/O4QR.gif'
        ]
        embed = discord.Embed(color = 0xFFA500)
        if member != None:
            embed.description = main.get_lang(inter.guild, "TICKLE_ARGS").format(inter.author.mention, member.mention)
        else:
            embed.description = main.get_lang(inter.guild, "TICKLE_NOARGS").format(inter.author.mention)
        embed.set_image(url = random.choice(tickkle))

        await inter.send(embed = embed)


def setup(client):
    client.add_cog(Tickle(client))