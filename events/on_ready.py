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

        ticketchnl = await self.client.fetch_channel(939438939259949067) # ID канала, где при нажатии на реакцию создаётся тикет.
        ticketmsg = await ticketchnl.fetch_message(1105549141922291782)

        emb = discord.Embed(description= '\🔻 Выберите сервер, по которому желаете создать обращение', colour = 0x2f3136)
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
        await ticketmsg.edit(embed = emb, view=view)

        notifychnl = await self.client.fetch_channel(939438241290022924) # ID канала, где при нажатии на реакцию создаётся тикет.
        notifymsg = await notifychnl.fetch_message(1107025615141482538)
        emb2 = discord.Embed(title='🔔 Уведомления и особые роли', description= '''> \📰 — оповещения о новостях проекта в канале <#939438314954588201>.
        > \📆 — оповещения о предстоящих событиях проекта в канале  <#1100414892609130527>.
        
        > \🔓 — доступ к категории с каналами #скриншоты и #игра предыдущих сезонов.
        > \🗿 — доступ к каналу <#1064971796203446423>, место содержания чудиков проекта''', colour = 0xecac4b)
        row = Button(
                style = discord.ButtonStyle.gray,
                custom_id = 'news',
                emoji= '📰'
            )
        row2 = Button(
                style = discord.ButtonStyle.gray,
                custom_id = 'events',
                emoji= '📆'
            )
        row3 = Button(
                style = discord.ButtonStyle.gray,
                custom_id = 'access',
                emoji= '🔓'
            )
        row4 = Button(
                style = discord.ButtonStyle.gray,
                custom_id = 'durka',
                emoji= '🗿'
            )
        view=View()
        view.add_item(row)
        view.add_item(row2)
        view.add_item(row3)
        view.add_item(row4)
        await notifymsg.edit(embed = emb2, view=view)
        self.status_task.start() 

    @tasks.loop(minutes = 0.2)
    async def status_task(self):
        guild = self.client.get_guild(921483461016031263)
        #await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"за {guild.member_count} участниками"))
        await self.client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"за тех. работами"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def notifysetup(self,ctx):
        emb1 = discord.Embed(title="", colour = 0xecac4b)
        emb1.set_image(url='https://cdn.discordapp.com/attachments/939510519629479946/1024399934423847032/photo1664023949_1.jpeg')
        emb2 = discord.Embed(title='🔔 Уведомления и особые роли', description= '''> \📰 — оповещения о новостях проекта в канале <#939438314954588201>.
        > \📆 — оповещения о предстоящих событиях проекта в канале  <#1100414892609130527>.
        
        > \🔓 — доступ к категории с каналами #скриншоты и #игра предыдущих сезонов.
        > \🗿 — доступ к каналу <#1064971796203446423>, место содержания чудиков проекта''', colour = 0xecac4b)
        await ctx.send(embed=emb1)
        await ctx.send(embed=emb2)


    @commands.Cog.listener()
    async def on_button_click(self, inter):
        #Техническая информация для выдачи ролей.
        guild = self.client.get_guild(inter.guild.id)
        memberop = inter.author

        if inter.component.custom_id == "news":
            resyes = '<a:phoenix_toggleon:953725340042293369> Роль <@&951475369041616926> успешно выдана.'
            resno = '<a:phoenix_toggleoff:953725338347782145> Роль <@&951475369041616926> успешно снята.'
            role = discord.utils.get(guild.roles, id=951475369041616926)
            if role in memberop.roles:
                role = discord.utils.get(guild.roles, id=951475369041616926)
                await memberop.remove_roles(role)
                await inter.send(resno, ephemeral = True)
                return
            if not role in memberop.roles:
                await memberop.add_roles(role)
                await inter.send(resyes, ephemeral = True)

        if inter.component.custom_id == "events":
            resyes = '<a:phoenix_toggleon:953725340042293369> Роль <@&1010607636229656638> успешно выдана.'
            resno = '<a:phoenix_toggleoff:953725338347782145> Роль <@&1010607636229656638> успешно снята.'
            role = discord.utils.get(guild.roles, id=1010607636229656638)
            if role in memberop.roles:
                role = discord.utils.get(guild.roles, id=1010607636229656638)
                await memberop.remove_roles(role)
                await inter.send(resno, ephemeral = True)
                return
            if not role in memberop.roles:
                await memberop.add_roles(role)
                await inter.send(resyes, ephemeral = True)

        if inter.component.custom_id == "access":
            resyes = '<a:phoenix_toggleon:953725340042293369> Роль <@&1035615119213854803> успешно выдана.'
            resno = '<a:phoenix_toggleoff:953725338347782145> Роль <@&1035615119213854803> успешно снята.'
            role = discord.utils.get(guild.roles, id=1035615119213854803)
            if role in memberop.roles:
                role = discord.utils.get(guild.roles, id=1035615119213854803)
                await memberop.remove_roles(role)
                await inter.send(resno, ephemeral = True)
                return
            if not role in memberop.roles:
                await memberop.add_roles(role)
                await inter.send(resyes, ephemeral = True)

        if inter.component.custom_id == "durka":
            resyes = '<a:phoenix_toggleon:953725340042293369> Роль <@&1077928906235064320> успешно выдана.'
            resno = '<a:phoenix_toggleoff:953725338347782145> Роль <@&1077928906235064320> успешно снята.'
            role = discord.utils.get(guild.roles, id=1077928906235064320)
            if role in memberop.roles:
                role = discord.utils.get(guild.roles, id=1077928906235064320)
                await memberop.remove_roles(role)
                await inter.send(resno, ephemeral = True)
                return
            if not role in memberop.roles:
                await memberop.add_roles(role)
                await inter.send(resyes, ephemeral = True)

def setup(client):
    client.add_cog(OnReady(client))