import disnake as discord
from disnake.ext import commands
import asyncio
import os
from disnake import File
from disnake.ui import Button, View

class RolesButtonClick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def notifysetup(self,ctx):
        emb1 = discord.Embed(title="", colour = 0xecac4b)
        emb1.set_image(url='https://media.discordapp.net/attachments/1053188377651970098/1107317077364178944/d7b96329cadf7c8b.png')
        emb2 = discord.Embed(title='🔔 Уведомления и особые роли', description= '''> 📰 — оповещения о новостях проекта в канале <#939438314954588201>.
        > 📆 — оповещения о предстоящих событиях проекта в канале  <#1100414892609130527>.
        
        > 📹 — оповещения о новых видеороликах и стримах по проекту.
                             
        > 📦 — доступ к категории с каналами #скриншоты и #игра предыдущих сезонов.''', colour = 0xecac4b)
        await ctx.send(embed=emb1)
        await ctx.send(embed=emb2)


    @commands.Cog.listener()
    async def on_button_click(self, inter):
        #Техническая информация для выдачи ролей.
        guild = self.client.get_guild(inter.guild.id)
        memberop = inter.author
        newsrole = discord.utils.get(guild.roles, id=1095192294950436864)
        anoncerole = discord.utils.get(guild.roles, id=1095191584590549052)

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
        if inter.component.custom_id == "media":
            resyes = '<a:phoenix_toggleon:953725340042293369> Роль <@&1147216415720480890> выдана.'
            resno = '<a:phoenix_toggleoff:953725338347782145> Роль <@&1147216415720480890> снята.'
            mediarole = discord.utils.get(guild.roles, id=1147216415720480890)
            if mediarole in memberop.roles:
                await memberop.remove_roles(mediarole)
                await inter.send(resno, ephemeral = True)
                return
            if not mediarole in memberop.roles:
                await memberop.add_roles(mediarole)
                await memberop.add_roles(newsrole)
                await inter.send(resyes, ephemeral = True)
        if inter.component.custom_id == "discord_news":
            resyes = '<a:phoenix_toggleon:953725340042293369> Роль <@&1095191584590549052> выдана.'
            resno = '<a:phoenix_toggleoff:953725338347782145> Роль <@&1095191584590549052> снята.'
            discordnewsrole = discord.utils.get(guild.roles, id=1095191584590549052)
            if discordnewsrole in memberop.roles:
                await memberop.remove_roles(discordnewsrole)
                await inter.send(resno, ephemeral = True)
                return
            if not discordnewsrole in memberop.roles:
                await memberop.add_roles(discordnewsrole)
                await memberop.add_roles(newsrole)
                await inter.send(resyes, ephemeral = True)
        if inter.component.custom_id == "minecraft_news":
            resyes = '<a:phoenix_toggleon:953725340042293369> Роль <@&1095191555972804739> выдана.'
            resno = '<a:phoenix_toggleoff:953725338347782145> Роль <@&1095191555972804739> снята.'
            minecraftnewsrole = discord.utils.get(guild.roles, id=1095191555972804739)
            if minecraftnewsrole in memberop.roles:
                await memberop.remove_roles(minecraftnewsrole)
                await inter.send(resno, ephemeral = True)
                return
            if not minecraftnewsrole in memberop.roles:
                await memberop.add_roles(minecraftnewsrole)
                await memberop.add_roles(newsrole)
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
            resyes = '<a:phoenix_toggleon:953725340042293369> Роль <@&1095191824898990151> выдана.'
            resno = '<a:phoenix_toggleoff:953725338347782145> Роль <@&1095191824898990151> снята.'
            discordannoncesrole = discord.utils.get(guild.roles, id=1095191824898990151)
            if discordannoncesrole in memberop.roles:
                await memberop.remove_roles(discordannoncesrole)
                await inter.send(resno, ephemeral = True)
                return
            if not discordannoncesrole in memberop.roles:
                await memberop.add_roles(discordannoncesrole)
                await memberop.add_roles(anoncerole)
                await inter.send(resyes, ephemeral = True)

        if inter.component.custom_id == "minecraft_annonces":
            resyes = '<a:phoenix_toggleon:953725340042293369> Роль <@&951475369041616926> выдана.'
            resno = '<a:phoenix_toggleoff:953725338347782145> Роль <@&951475369041616926> снята.'
            minecraftanoncesrole = discord.utils.get(guild.roles, id=951475369041616926)
            if minecraftanoncesrole in memberop.roles:
                await memberop.remove_roles(minecraftanoncesrole)
                await inter.send(resno, ephemeral = True)
                return
            if not minecraftanoncesrole in memberop.roles:
                await memberop.add_roles(minecraftanoncesrole)
                await memberop.add_roles(anoncerole)
                await inter.send(resyes, ephemeral = True)

        if inter.component.custom_id == "access":
            resyes = '<a:phoenix_toggleon:953725340042293369> Роль <@&1035615119213854803> выдана.'
            resno = '<a:phoenix_toggleoff:953725338347782145> Роль <@&1035615119213854803> снята.'
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
    client.add_cog(RolesButtonClick(client))