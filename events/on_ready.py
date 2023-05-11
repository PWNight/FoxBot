import disnake as discord
from disnake.ext import commands, tasks
from disnake.ui import Button, View
import time


class OnReady(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()
        self.client.logger('Успешно запустился', 'ready')
        self.client.logger(f'Имя: {self.client.user.name}', 'ready')
        self.client.logger(f'ID: {self.client.user.id}' , 'ready')

        guild = self.client.get_guild(921483461016031263)

        #await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"за {guild.member_count} участниками"))
        await self.client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"за тех. работами"))

        chnla = await self.client.fetch_channel(939438939259949067) # ID канала, где при нажатии на реакцию создаётся тикет.
        msga = await chnla.fetch_message(1105549141922291782)

        emb = discord.Embed(description= '🔻 Выберите сервер, по которому желаете создать обращение', colour = 0x2f3136)
        row = Button(
                style = discord.ButtonStyle.blurple,
                label = 'Discord',
                custom_id = 'discord_openticket',
                emoji= '<:discord:856561477033263124>'
            )
        row2 = Button(
                style = discord.ButtonStyle.green,
                label = 'Minecraft',
                custom_id = 'minecraft_openticket',
                emoji= '<:minecraft:856561476873355316>'
            )
        view=View()
        view.add_item(row)
        view.add_item(row2)
        await msga.edit(embed = emb, view=view)
        self.status_task.start() 

    @tasks.loop(minutes = 0.2)
    async def status_task(self):
        guild = self.client.get_guild(921483461016031263)
        #await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"за {guild.member_count} участниками"))
        await self.client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"за тех. работами"))



    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.client.get_guild(921483461016031263)
        if payload.message_id == 1053186080368775258 and payload.emoji.name == '📰':
            role = discord.utils.get(guild.roles, id=951475369041616926)
            await payload.member.add_roles(role)

        if payload.message_id == 1053186080368775258 and payload.emoji.name == '📢':
            role = discord.utils.get(guild.roles, id=951475381691621466)
            await payload.member.add_roles(role)

        if payload.message_id == 1053186080368775258 and payload.emoji.name == '📆':
            role = discord.utils.get(guild.roles, id=1010607636229656638)
            await payload.member.add_roles(role)

        if payload.message_id == 1053186080368775258 and payload.emoji.name == '🔓':
            role = discord.utils.get(guild.roles, id=1035615119213854803)
            await payload.member.add_roles(role)
        
        if payload.message_id == 1077932023676686356 and payload.emoji.name == '🗿':
            role = discord.utils.get(guild.roles, id=1077928906235064320)
            await payload.member.add_roles(role)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.client.get_guild(921483461016031263)
        member = discord.utils.get(guild.members, id=payload.user_id)
        if payload.message_id == 1053186080368775258 and payload.emoji.name == '📰':
            role = discord.utils.get(guild.roles, id=951475369041616926)
            await member.remove_roles(role)

        if payload.message_id == 1053186080368775258 and payload.emoji.name == '📢':
            role = discord.utils.get(guild.roles, id=951475381691621466)
            await member.remove_roles(role)

        if payload.message_id == 1053186080368775258 and payload.emoji.name == '📆':
            role = discord.utils.get(guild.roles, id=1010607636229656638)
            await member.remove_roles(role)

        if payload.message_id == 1053186080368775258 and payload.emoji.name == '🔓':
            role = discord.utils.get(guild.roles, id=1035615119213854803)
            await member.remove_roles(role)

def setup(client):
    client.add_cog(OnReady(client))