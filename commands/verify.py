import disnake as discord
from disnake.ext import commands
import mctools
from mctools import  RCONClient


class Verify(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="верификация", description="Добавляет игрока в вайтлист", test_guilds=[921483461016031263])
    async def givecurator(self, inter, member: discord.Member, nickname: str):
        guild = self.client.get_guild(921483461016031263)
        role = discord.utils.get(guild.roles, id=1028254807129083954)
        if role in member.roles:
            await inter.send(f"<:phoenix_dnd:953725336942686268> Пользователь уже верифицирован.")
            return
        else:
            await member.add_roles(role)
            pass
        HOST = '135.181.126.159'
        PORT = 25571
        rcon = RCONClient(HOST, port = PORT)
        if rcon.login('59d82888-5420-43b9-a58b-98c382061602'):
            rcon.command(f'verify {nickname}')
            rcon.command(f'Добавление игрока в вайтлист')
            rcon.stop()
                            
            await inter.send(f'<:phoenix_onl:953725336825258015> Игрок {nickname} был добавлен в вайтлист и получил роль <@&1028254807129083954>.', ephemeral=True)
            return



def setup(client):
    client.add_cog(Verify(client))