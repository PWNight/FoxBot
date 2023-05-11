import disnake as discord
from disnake.ext import commands
from api.server import base, main


class Avatar(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="аватар", description="👥 Показывает аватар пользователя.", test_guilds=[921483461016031263])
    async def avatar(self, inter, member: discord.Member = None):
        send = inter.response.send_message
        if not member:
            member = inter.author

        try:
            embed = discord.Embed(color = 0x2f3136)
            embed.add_field(name = main.get_lang(inter.guild, 'AVATAR_FIELD_TITLE'),value = main.get_lang(inter.guild, 'AVATAR_FIELD_VALUE').format(member.mention),inline = False)
            embed.set_image(url = member.display_avatar.url)
            embed.set_footer(text = main.get_lang(inter.guild, 'COMMANDS_FOOTER').format(inter.author),icon_url = inter.author.display_avatar.url)
            await send(embed = embed)
        except:
            embed = discord.Embed(color = 0x2f3136)
            embed.add_field(name = main.get_lang(inter.guild, 'AVATAR_FIELD_TITLE'),value = main.get_lang(inter.guild, 'AVATAR_FIELD_VALUE1').format(member.mention),inline = False)
            embed.set_footer(text = main.get_lang(inter.guild, 'COMMANDS_FOOTER').format(inter.author))
            await send(embed = embed)            


def setup(client):
    client.add_cog(Avatar(client))