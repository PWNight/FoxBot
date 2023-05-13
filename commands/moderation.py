import disnake as discord
from disnake.ext import commands


class Moder(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name='очистить', description='💬 Очищает указанное количество сообщений в чате.', test_guilds=[921483461016031263])
    @commands.has_permissions(manage_messages=True)
    async def clear(inter, amount: int):
        await inter.channel.purge(limit=amount)
        await inter.send(content=f'💬 Сообщения очищены.', ephemeral=True)


    @commands.slash_command(name='лс', description='💬 Отправляет сообщение в ЛС участника.', test_guilds=[921483461016031263])
    @commands.has_permissions(manage_messages=True) 
    async def dm(inter, user: discord.User, *, message: str):
        try:
            await user.send(message)
            await inter.send(f"\✉️ Сообщение отправлено **{user}**", ephemeral=True)
        except discord.Forbidden:
            await inter.send("\✉️ Не удалось отправить сообщение, возможно указанный пользователь отключил возможность отправлять личные сообщения с данного сервера.", ephemeral=True)
    

def setup(client):
    client.add_cog(Moder(client))