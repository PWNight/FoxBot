import disnake as discord
from disnake.ext import commands
from mctools import  RCONClient
import datetime
from datetime import timezone, timedelta

class give_foxplus(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="выдать-подписку", description="💸 Выдаёт подписку на указанное время.", test_guilds=[921483461016031263])
    async def avatar(self, inter, member: discord.Member, time: int, type: str):
        HOST = '135.181.126.159';
        PORT = 25571;
        rcon = RCONClient(HOST, port = PORT);
        notifychnl = await self.client.fetch_channel(1111753012441006201)
        buylogchnl = await self.client.fetch_channel(1130119557126832259)
        timezone_offset = +3.0  # Pacific Standard Time (UTC+03:00)
        tzinfo = timezone(timedelta(hours=timezone_offset))
        date = datetime.datetime.now(tzinfo)
        if time == 1:
            month = 'месяц'
        if time == 2 or time == 3 or time == 4:
            month = 'месяца'
        if time > 4:
            month = 'месяцев'

        if rcon.login('59d82888-5420-43b9-a58b-98c382061602'):
            rcon.command(f'lp user {member.nick} parent addtemp foxplus {time}mo');
            rcon.stop();
        if type == 'buy':
            responce = discord.Embed(description=f'{member.mention} приобрёл FoxPlus на {time} {month}.', colour = 0xfc9d53)
            responce.set_author(name=f"{member.nick}",icon_url=f"{member.avatar}")
            await notifychnl.send(embed = responce)

            detailedresponce = discord.Embed(description=f'{member.mention} приобрёл FoxPlus на {time} {month}.\nДата покупки: {date.strftime("%d.%m.%Y в %H:%M")}', colour = 0xfc9d53)
            detailedresponce.set_author(name=f"{member.nick}",icon_url=f"{member.avatar}")
            await buylogchnl.send(embed = detailedresponce)
        if type == 'gift':
            responce = discord.Embed(description=f'{inter.author.mention} подарил подписку FoxPlus игроку {member.mention} на {time} {month}.', colour = 0xfc9d53)
            responce.set_author(name=f"{member.nick}",icon_url=f"{member.avatar}")
            await notifychnl.send(embed = responce)

            detailedresponce = discord.Embed(description=f'{inter.author.mention} подарил подписку FoxPlus игроку {member.mention} на {time} {month}.\nДата покупки: {date.strftime("%d.%m.%Y в %H:%M")}', colour = 0xfc9d53)
            detailedresponce.set_author(name=f"{member.nick}",icon_url=f"{member.avatar}")
            await buylogchnl.send(embed = detailedresponce)
        await inter.send(f"\💸 Подписка FoxPlus на {time} {month} успешно выдана игроку {member.mention}", ephemeral=True)


def setup(client):
    client.add_cog(give_foxplus(client))