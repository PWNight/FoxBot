import disnake as discord
from disnake.ext import commands, tasks
from disnake.ui import Button, View
import time
from mcstatus import JavaServer 
import datetime
from datetime import timezone, timedelta


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

        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"за {guild.member_count} участниками"))
        #await self.client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"за тех. работами"))

        guildchnl = await self.client.fetch_channel(991247514495885393)
#Новая организация
        newmsg = await guildchnl.fetch_message(1045046216989343834)
        verify = Button(style = discord.ButtonStyle.grey, label = 'Подать заявку', custom_id = 'newguild', emoji= '<:invite:1105878276242673725>')
        #verify = Button(style = discord.ButtonStyle.grey, label = 'Подать заявку', custom_id = 'maintenance_guild', emoji= '<:invite:1105878276242673725>') #НЕ ЗАБЫТЬ МЕНЯТЬ ОБРАТНО ПОСЛЕ ТЕХНИЧЕСКИХ РАБОТ!!! ,
        viewverify=View()
        viewverify.add_item(verify)
        await newmsg.edit(view=viewverify) 
#Япония
        japanmsg = await guildchnl.fetch_message(1045184416714076292)
        verify = Button(style = discord.ButtonStyle.grey, label = 'Подать заявку', custom_id = 'japan', emoji= '🇯🇵')
        viewverify=View()
        viewverify.add_item(verify)
        await japanmsg.edit(view=viewverify) 
#Авиньон
        avimsg = await guildchnl.fetch_message(1080413919291641876)
        verify = Button(style = discord.ButtonStyle.grey, label = 'Подать заявку', custom_id = 'avignon', emoji= '🌁')
        viewverify=View()
        viewverify.add_item(verify)
        await avimsg.edit(view=viewverify)
#Хвардия
        guardmsg = await guildchnl.fetch_message(1129135604920238100)
        verify = Button(style = discord.ButtonStyle.grey, label = 'Подать заявку', custom_id = 'guard', emoji= '🏹')
        viewverify=View()
        viewverify.add_item(verify)
        await guardmsg.edit(view=viewverify)   
#Черный круг
        blackmsg = await guildchnl.fetch_message(1138522957539446964)
        verify = Button(style = discord.ButtonStyle.grey, label = 'Подать заявку', custom_id = 'black', emoji= '⚫')
        viewverify=View()
        viewverify.add_item(verify)
        await blackmsg.edit(view=viewverify)
#БВДК
        impermsg = await guildchnl.fetch_message(1154459536644653126)
        verify = Button(style = discord.ButtonStyle.grey, label = 'Подать заявку', custom_id = 'imperia', emoji= '✍️')
        viewverify=View()
        viewverify.add_item(verify)
        await impermsg.edit(view=viewverify)      
#Гробовщики
        grobmsg = await guildchnl.fetch_message(1158088404622397510)
        verify = Button(style = discord.ButtonStyle.grey, label = 'Подать заявку', custom_id = 'grob', emoji= '🫡')
        viewverify=View()
        viewverify.add_item(verify)
        await grobmsg.edit(view=viewverify)   

#Обновление канала поддержки
        ticketchnl = await self.client.fetch_channel(939438939259949067) 
        ticketmsg = await ticketchnl.fetch_message(1105549141922291782)
        emb = discord.Embed(description= '🔻 Выберите сервер, по которому желаете создать обращение', colour = 0x2f3136)
        row = Button(
                style = discord.ButtonStyle.blurple,
                label = 'Discord',
                #custom_id = 'maintenance_dc', #НЕ ЗАБЫТЬ МЕНЯТЬ ОБРАТНО ПОСЛЕ ТЕХНИЧЕСКИХ РАБОТ!!! 
                custom_id = 'discord_openticket',
                emoji= '<:discord:856561477033263124>'
            )
        row2 = Button(
                style = discord.ButtonStyle.green,
                label = 'Minecraft',
                #custom_id = 'maintenance_mc', #НЕ ЗАБЫТЬ МЕНЯТЬ ОБРАТНО ПОСЛЕ ТЕХНИЧЕСКИХ РАБОТ!!! ,
                custom_id = 'minecraft_openticket',
                emoji= '<:minecraft:856561476873355316>'
            )
        view=View()
        view.add_item(row)
        view.add_item(row2)
        await ticketmsg.edit(embed = emb, view=view)

#Обновление канала Верификации        
        verifychnl = await self.client.fetch_channel(1111325108217315368) 
        verifymsg = await verifychnl.fetch_message(1125044148890779720)
        emb = discord.Embed(description= '🔻 Нажмите на кнопку ниже, чтобы подать заявку.', colour = 0x2f3136)
        row = Button(
                style = discord.ButtonStyle.blurple,
                label = 'Подать заявку',
                custom_id = 'verify', #verify #НЕ ЗАБЫТЬ МЕНЯТЬ ОБРАТНО ПОСЛЕ ТЕХНИЧЕСКИХ РАБОТ!!!
                #custom_id = 'maintenance'
                emoji= '<:message:1105891497255108679>'
            )
        view=View()
        view.add_item(row)
        await verifymsg.edit(embed = emb, view=view)

#Обновление канала набора кадров
        naborchnl = await self.client.fetch_channel(1126877107658707074) # ID канала, где при нажатии на реакцию создаётся тикет.
        nabormsg = await naborchnl.fetch_message(1127575031682183290)
        emb = discord.Embed(description= '🔻 Нажмите на кнопку ниже, чтобы подать заявку в команду проекта.', colour = 0x2f3136)
        row = Button(
                style = discord.ButtonStyle.blurple,
                label = 'Подать заявку в команду',
                custom_id = 'nabor_kadrov',
                emoji= '<:message:1105891497255108679>'
            )
        view=View()
        view.add_item(row)
        await nabormsg.edit(embed = emb, view=view)

#Обновление канала с уведомлениями
        notifychnl = await self.client.fetch_channel(939438241290022924)
        notifymsg = await notifychnl.fetch_message(1107322507473723412)
        emb2 = discord.Embed(title='🔔 Уведомления и особые роли', description= '''> 📰 — оповещения о новостях проекта в канале <#939438314954588201>.
        > 📆 — оповещения о предстоящих событиях проекта в канале  <#1100414892609130527>.
        
        > 📹 — оповещения о новых видеороликах и стримах по проекту.
                             
        > 📦 — доступ к категории с каналами #скриншоты и #игра предыдущих сезонов.''', colour = 0xecac4b)
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
                custom_id = 'media',
                emoji= '📹'
            )
        row4 = Button(
                style = discord.ButtonStyle.gray,
                custom_id = 'access',
                emoji= '📦'
            )
        view=View()
        view.add_item(row)
        view.add_item(row2)
        view.add_item(row3)
        view.add_item(row4)
        await notifymsg.edit(embed = emb2, view=view)

#Обновление канала со статусом Minecraft сервера
        statuschnl = await self.client.fetch_channel(939438241290022924) 
        statusmsg = await statuschnl.fetch_message(1126854219295641611)
        server = JavaServer(host="135.181.126.159", port=25566) #MinecraftServer.lookup("135.181.126.159:25566")
        querystatus = server.query()

        timezone_offset = +3.0  # Pacific Standard Time (UTC+03:00)
        tzinfo = timezone(timedelta(hours=timezone_offset))
        date = datetime.datetime.now(tzinfo)
        embed = discord.Embed(title='Minecraft', colour = 0xadf36c)
        embed.set_thumbnail(url=f'https://cdn.discordapp.com/attachments/1053188377651970098/1158460340867190864/minecraft.png?ex=651c53c4&is=651b0244&hm=50b3e5288089a34ca01a869c5cade9b08d4e04f6547015b533d934f73527baf4&')
        embed.add_field(name = 'IP:',value = f'mc.foxworld.ru',inline = False)
        embed.add_field(name = 'Версия:',value = f'{querystatus.software.version}',inline = False)
        embed.add_field(name = 'Текущий онлайн:',value = f'{querystatus.players.online}/{querystatus.players.max}',inline = False)
        embed.set_footer(text=f"Статистика обновлена {date.strftime('%d.%m в %H:%M')}", icon_url="https://cdn.discordapp.com/attachments/1053188377651970098/1126862804150931487/Fox5.png")
        view=View()
        row = Button(
                style = discord.ButtonStyle.gray,
                label = 'Cписок игроков',
                custom_id = 'playerlist',
                emoji= '<:member:979406123587223562>'
            )
        view.add_item(row)
        await statusmsg.edit(embed = embed, view = view)
        self.status_task.start()   

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        if inter.component.custom_id == "playerlist":
            server = JavaServer.lookup("135.181.126.159:25566")
            status = server.query()
            if status.players.online == 0:
                await inter.send('<:member:979406123587223562> **Список игроков:** \nНа сервере нету игроков.', ephemeral = True)
            else:
                status.players = '\n'.join(status.players.names)
                await inter.send(f'<:member:979406123587223562> **Список игроков:** \n{status.players}', ephemeral = True)
                return

    @tasks.loop()
    async def status_task(self) -> None:
        timezone_offset = +3.0  # Pacific Standard Time (UTC+03:00)
        tzinfo = timezone(timedelta(hours=timezone_offset))
        date = datetime.datetime.now(tzinfo)
        
        guild = self.client.get_guild(921483461016031263)
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"за {guild.member_count} участниками"))
        #await self.client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"за тех. работами"))
        
        statuschnl = await self.client.fetch_channel(939438241290022924) 
        statusmsg = await statuschnl.fetch_message(1126854219295641611)
        server = JavaServer(host="135.181.126.159", port=25566) #MinecraftServer.lookup("135.181.126.159:25566")
        querystatus = server.query()

        embed = discord.Embed(title='Minecraft', colour = 0xadf36c)
        embed.set_thumbnail(url=f'https://cdn.discordapp.com/attachments/1053188377651970098/1158460340867190864/minecraft.png?ex=651c53c4&is=651b0244&hm=50b3e5288089a34ca01a869c5cade9b08d4e04f6547015b533d934f73527baf4&')
        embed.add_field(name = 'IP:',value = f'mc.foxworld.ru',inline = False)
        embed.add_field(name = 'Версия:',value = f'{querystatus.software.version}',inline = False)
        embed.add_field(name = 'Текущий онлайн:',value = f'{querystatus.players.online}/{querystatus.players.max}',inline = False)
        embed.set_footer(text=f"Статистика обновлена {date.strftime('%d.%m в %H:%M')}", icon_url="https://cdn.discordapp.com/attachments/1053188377651970098/1126862804150931487/Fox5.png")
        view=View()
        row = Button(
                style = discord.ButtonStyle.gray,
                label = 'Cписок игроков',
                custom_id = 'playerlist',
                emoji= '<:member:979406123587223562>'
            )
        view.add_item(row)
        await statusmsg.edit(embed = embed, view = view)
        await asyncio.sleep(20)

def setup(client):
    client.add_cog(OnReady(client))