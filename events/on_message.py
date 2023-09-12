import disnake as discord
from disnake.ext import commands
import asyncio
import os
from disnake import File
from disnake.ui import Button, View
import shortuuid
shortuuid.uuid()

class On_message(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        channel = message.channel
        if channel.id == 939438314954588201: #Новости
          await message.add_reaction("👍")  
          await message.add_reaction("👎")
        if channel.id == 1100414892609130527: #Анонсы
          await message.add_reaction("👍")  
          await message.add_reaction("👎")
        if channel.id == 1151168366661357698: #Идеи
          if message.content.startswith('#'):
              await message.add_reaction("<:minecraft_accept:1080779491875491882>")  
              await message.add_reaction("<:minecraft_deny:1080779495386140684>")
              
          else:
              if message.author.bot:
                return
              if message.author.id == 660070694377357322:
                return
              else:
                delete = await message.reply(f'{message.author.mention}, идея должна начинаться с номера')
                await message.delete()
                await asyncio.sleep(30)
                await delete.delete()
        if channel.id == 880866817269190716: #Новые участники
          await message.add_reaction("👋")  


def setup(client):
    client.add_cog(On_message(client))