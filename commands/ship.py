import disnake as discord
import random
from disnake.ext import commands
from api.server import main


class Ship(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="шип", description="💞 Расчитывает процент шипперства между указанными пользователями", test_guilds=[921483461016031263])
    async def ship(self, inter, user_1 : discord.Member, user_2 : discord.Member):
        try:
            embed = discord.Embed(color = 0xFFA500)
            embed.add_field(name = main.get_lang(inter.guild, "SHIP_FIELD_TITLE"),value = main.get_lang(inter.guild, "SHIP_FIELD_VALUE").format(user_1.mention, user_2.mention, random.randint(1,100)))
            embed.set_footer(text = main.get_lang(inter.guild, "COMMANDS_FOOTER").format(inter.author),icon_url = inter.author.display_avatar.url)
            await inter.send(embed = embed)
        except:
            embed = discord.Embed(color = 0xFFA500)
            embed.add_field(name = main.get_lang(inter.guild, "SHIP_FIELD_TITLE"),value = main.get_lang(inter.guild, "SHIP_FIELD_VALUE").format(user_1.mention, user_2.mention, random.randint(1,100)))
            embed.set_footer(text = main.get_lang(inter.guild, "COMMANDS_FOOTER").format(inter.author))
            await inter.send(embed = embed)

def setup(client):
    client.add_cog(Ship(client))