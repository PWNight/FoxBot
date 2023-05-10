import disnake as discord
import random
from disnake.ext import commands
from api.check import utils, block
from api.server import base, main


class Kiss(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="поцеловать", description="💋 Целует указанного пользователя", test_guilds=[921483461016031263])
    @block.block()
    async def kiss(self, inter, member: discord.Member = None):
        kisss = [
            'https://data.whicdn.com/images/294084710/original.gif',
            'https://avatars.mds.yandex.net/i?id=b32da311529547ca0cd188ede0d5f3cd-4642846-images-thumbs&n=13'
            'https://avatars.mds.yandex.net/i?id=b32da311529547ca0cd188ede0d5f3cd-4642846-images-thumbs&n=13',
            'https://steamuserimages-a.akamaihd.net/ugc/171536200083383839/16E90753956B1CBEF72A8311D9429562E18F8B1D/',
            'https://aniyuki.com/wp-content/uploads/2021/07/aniyuki-anime-gif-kiss-12.gif'
        ]
        embed = discord.Embed(color = 0xFFA500)
        if member != None:
            embed.description = main.get_lang(inter.guild, "KISS_ARGS").format(inter.author.mention, member.mention)
        else:
            embed.description = main.get_lang(inter.guild, "KISS_NOARGS").format(inter.author.mention)
        embed.set_image(url = random.choice(kisss))

        await inter.send(embed = embed)


def setup(client):
    client.add_cog(Kiss(client))