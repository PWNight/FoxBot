import disnake as discord
import urllib
from disnake.ext import commands
from urllib.parse import quote
from api.check import utils, block
from api.server import base, main


class Youtubec(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="комментарий", description="📺 Делает введённый текст в виде коментария на ютубе.", test_guilds=[921483461016031263])
    @block.block()
    async def comment(self, inter, *, comment, member = None):
        if not member:
            member = inter.author
        try:
            embed = discord.Embed(color = 0xFFA500)
            embed.set_image(url = f'https://some-random-api.ml/canvas/youtube-comment?avatar={member.avatar.url}&username={quote(member.name)}&comment={quote(comment)}')
            await inter.send(embed = embed)
        except:
            await inter.send(embed = main.deny(inter.guild, main.get_lang(inter.guild, "AVATAR_FIELD_VALUE1")))

def setup(client):
    client.add_cog(Youtubec(client))