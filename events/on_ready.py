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

        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"за {guild.member_count} участниками"))
        #await self.client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"за тех. работами"))

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
        await ticketmsg.edit(embed = emb, view=view)\
        
        verifychnl = await self.client.fetch_channel(1111325108217315368) # ID канала, где при нажатии на реакцию создаётся тикет.
        verifymsg = await verifychnl.fetch_message(1125044148890779720)

        emb = discord.Embed(description= '\🔻 Нажмите на кнопку ниже, чтобы подать заявку.', colour = 0x2f3136)
        row = Button(
                style = discord.ButtonStyle.blurple,
                label = 'Подать заявку',
                custom_id = 'verify',
                emoji= '<:message:1105891497255108679>'
            )
        view=View()
        view.add_item(row)
        await verifymsg.edit(embed = emb, view=view)

        notifychnl = await self.client.fetch_channel(939438241290022924) # ID канала, где при нажатии на реакцию создаётся тикет.
        notifymsg = await notifychnl.fetch_message(1107322507473723412)
        emb2 = discord.Embed(title='🔔 Уведомления и особые роли', description= '''> 📰 — оповещения о новостях проекта в канале <#939438314954588201>.
        > 📆 — оповещения о предстоящих событиях проекта в канале  <#1100414892609130527>.
        
        > 🔓 — доступ к категории с каналами #скриншоты и #игра предыдущих сезонов.''', colour = 0xecac4b)
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
                emoji= '📦'
            )
        view=View()
        view.add_item(row)
        view.add_item(row2)
        view.add_item(row3)
        await notifymsg.edit(embed = emb2, view=view)
        self.status_task.start() 

    @tasks.loop(minutes = 0.2)
    async def status_task(self):
        guild = self.client.get_guild(921483461016031263)
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"за {guild.member_count} участниками"))
        #await self.client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"за тех. работами"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def notifysetup(self,ctx):
        emb1 = discord.Embed(title="", colour = 0xecac4b)
        emb1.set_image(url='https://media.discordapp.net/attachments/1053188377651970098/1107317077364178944/d7b96329cadf7c8b.png')
        emb2 = discord.Embed(title='🔔 Уведомления и особые роли', description= '''> 📰 — оповещения о новостях проекта в канале <#939438314954588201>.
        > 📆 — оповещения о предстоящих событиях проекта в канале  <#1100414892609130527>.
        
        > 📦 — доступ к категории с каналами #скриншоты и #игра предыдущих сезонов.''', colour = 0xecac4b)
        await ctx.send(embed=emb1)
        await ctx.send(embed=emb2)


    @commands.Cog.listener()
    async def on_button_click(self, inter):
        #Техническая информация для выдачи ролей.
        guild = self.client.get_guild(inter.guild.id)
        memberop = inter.author

        if inter.component.custom_id == "news":
                chooseemb = discord.Embed(title='📰 Выберите сервер, по которому желаете получать новости.', color = 0x607aff)
                row = Button(
                        style = discord.ButtonStyle.blurple,
                        label = 'Discord',
                        custom_id = 'discord_news',
                        emoji= '<:discord:856561477033263124>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.green,
                        label = 'Minecraft',
                        custom_id = 'minecraft_news',
                        emoji= '<:minecraft:856561476873355316>'
                    )
                view=View()
                view.add_item(row)
                view.add_item(row2)
                await inter.send(embed=chooseemb, view = view, ephemeral = True)
                return
        if inter.component.custom_id == "discord_news":
            resyes = '<a:phoenix_toggleon:953725340042293369> Роль <@&1095191584590549052> успешно выдана.'
            resno = '<a:phoenix_toggleoff:953725338347782145> Роль <@&1095191584590549052> успешно снята.'
            discordnewsrole = discord.utils.get(guild.roles, id=1095191584590549052)
            if discordnewsrole in memberop.roles:
                await memberop.remove_roles(discordnewsrole)
                await inter.send(resno, ephemeral = True)
                return
            if not discordnewsrole in memberop.roles:
                await memberop.add_roles(discordnewsrole)
                await inter.send(resyes, ephemeral = True)
        if inter.component.custom_id == "minecraft_news":
            resyes = '<a:phoenix_toggleon:953725340042293369> Роль <@&1095191555972804739> успешно выдана.'
            resno = '<a:phoenix_toggleoff:953725338347782145> Роль <@&1095191555972804739> успешно снята.'
            minecraftnewsrole = discord.utils.get(guild.roles, id=1095191555972804739)
            if minecraftnewsrole in memberop.roles:
                await memberop.remove_roles(minecraftnewsrole)
                await inter.send(resno, ephemeral = True)
                return
            if not minecraftnewsrole in memberop.roles:
                await memberop.add_roles(minecraftnewsrole)
                await inter.send(resyes, ephemeral = True)

        if inter.component.custom_id == "events":
                chooseemb = discord.Embed(title='📆 Выберите сервер, по которому желаете получать анонсы.', color = 0x607aff)
                row = Button(
                        style = discord.ButtonStyle.blurple,
                        label = 'Discord',
                        custom_id = 'discord_annonces',
                        emoji= '<:discord:856561477033263124>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.green,
                        label = 'Minecraft',
                        custom_id = 'minecraft_annonces',
                        emoji= '<:minecraft:856561476873355316>'
                    )
                view=View()
                view.add_item(row)
                view.add_item(row2)
                await inter.send(embed=chooseemb, view = view, ephemeral = True)
                return
        if inter.component.custom_id == "discord_annonces":
            resyes = '<a:phoenix_toggleon:953725340042293369> Роль <@&1095191824898990151> успешно выдана.'
            resno = '<a:phoenix_toggleoff:953725338347782145> Роль <@&1095191824898990151> успешно снята.'
            discordannoncesrole = discord.utils.get(guild.roles, id=1095191824898990151)
            if discordannoncesrole in memberop.roles:
                await memberop.remove_roles(discordannoncesrole)
                await inter.send(resno, ephemeral = True)
                return
            if not discordannoncesrole in memberop.roles:
                await memberop.add_roles(discordannoncesrole)
                await inter.send(resyes, ephemeral = True)

        if inter.component.custom_id == "minecraft_annonces":
            resyes = '<a:phoenix_toggleon:953725340042293369> Роль <@&951475369041616926> успешно выдана.'
            resno = '<a:phoenix_toggleoff:953725338347782145> Роль <@&951475369041616926> успешно снята.'
            minecraftanoncesrole = discord.utils.get(guild.roles, id=951475369041616926)
            if minecraftanoncesrole in memberop.roles:
                await memberop.remove_roles(minecraftanoncesrole)
                await inter.send(resno, ephemeral = True)
                return
            if not minecraftanoncesrole in memberop.roles:
                await memberop.add_roles(minecraftanoncesrole)
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

def setup(client):
    client.add_cog(OnReady(client))