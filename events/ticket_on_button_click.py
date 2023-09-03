import disnake as discord
from disnake.ext import commands
import asyncio
import os
from disnake import File
from disnake.ui import Button, View
from api.server.dataIO import fileIO
import shortuuid
shortuuid.uuid()
verifymembers = []
counterverify = 0
voprosmembers = []
countervopros = 0

class ButtonClick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        #Техническая информация для тикетов.
        guild = self.client.get_guild(inter.guild.id)
        ticket_num = shortuuid.ShortUUID().random(length=6)
        logchannel = self.client.get_channel(939513221046472744) # ID канала с логами.
        mainCategory = discord.utils.get(guild.categories, id=939513361425657947) #ID категории, где будут создаваться тикеты.
        staffrole = discord.utils.get(guild.roles,id=939476433196171324)
        internrole = discord.utils.get(guild.roles,id=995056541734539354)
        memberop = inter.author
        
        #Текстовая информация для тикетов.
        res = '<:minecraft_accept:1080779491875491882> Обращение создано. \nОжидайте пинга в нужном канале.'
        resno = '<:minecraft_deny:1080779495386140684> **У вас уже есть отправленная заявка.** \nОжидайте решения по предыдущей заявке, чтобы открыть новую.'
        dcreport = discord.Embed(
        title='Добро пожаловать в службу поддержки Discord.', 
        description='Чтобы получить ответ как можно быстрее, опишите суть вашей жалобы по следующей форме заполнения: \n1) Ваш никнейм. \n2) Никнейм нарушителя. \n3) Нарушенное правило.\n4) Подробность нарушения. \n5) Доказательства нарушения. \nКоманда проекта в ближайшее время рассмотрит ваше обращение и накажет нарушителя.', 
        color = 0x2f3136)
        dcbugreport = discord.Embed(
        title='Добро пожаловать в службу поддержки Discord.', 
        description='Чтобы получить ответ как можно быстрее, опишите найденный вами баг и способ его получения как можно подробнее.\nКоманда проекта в ближайшее время рассмотрит ваше обращение и исправит баг.', 
        color = 0x2f3136)
        dcquestion = discord.Embed(
        title='Добро пожаловать в службу поддержки Discord.', 
        description='Чтобы получить ответ как можно быстрее, опишите суть вашего вопроса как можно подробнее.\nКоманда проекта в ближайшее время ответит на ваш вопрос.', 
        color = 0x2f3136)
        dcother = discord.Embed(
        title='Добро пожаловать в службу поддержки Discord.', 
        description='Чтобы получить ответ как можно быстрее, опишите суть вашего обращения как можно подробнее.\nКоманда проекта в ближайшее время рассмотрит ваше обращение.', 
        color = 0x2f3136)
        dcadmins = discord.Embed(
        title='Добро пожаловать в службу поддержки Discord.', 
        description='Чтобы получить ответ как можно быстрее, опишите суть вашего обращения к руководству как можно подробнее.\nРуководство проекта в ближайшее время рассмотрит ваше обращение.', 
        color = 0x2f3136)
        mcreport = discord.Embed(
        title='Добро пожаловать в службу поддержки Minecraft.', 
        description='Чтобы получить ответ как можно быстрее, опишите суть вашей жалобы по следующей форме заполнения: \n1) Ваш никнейм. \n2) Никнейм нарушителя. \n3) Нарушенное правило.\n4) Подробность нарушения. \n5) Доказательства нарушения. \nКоманда проекта в ближайшее время рассмотрит ваше обращение и накажет нарушителя.', 
        color = 0x2f3136)
        mcbugreport = discord.Embed(
        title='Добро пожаловать в службу поддержки Minecraft.', 
        description='Чтобы получить ответ как можно быстрее, опишите найденный вами баг и способ его получения как можно подробнее.\nКоманда проекта в ближайшее время рассмотрит ваше обращение и исправит баг.', 
        color = 0x2f3136)
        mcquestion = discord.Embed(
        title='Добро пожаловать в службу поддержки Minecraft.', 
        description='Чтобы получить ответ как можно быстрее, опишите суть вашего вопроса как можно подробнее.\nКоманда проекта в ближайшее время ответит на ваш вопрос.', 
        color = 0x2f3136)
        mcother = discord.Embed(
        title='Добро пожаловать в службу поддержки Minecraft.', 
        description='Чтобы получить ответ как можно быстрее, опишите суть вашего обращения как можно подробнее.\nКоманда проекта в ближайшее время рассмотрит ваше обращение.', 
        color = 0x2f3136)
        mcadmins = discord.Embed(
        title='Добро пожаловать в службу поддержки Minecraft.', 
        description='Чтобы получить ответ как можно быстрее, опишите суть вашего обращения к руководству как можно подробнее.\nРуководство проекта в ближайшее время рассмотрит ваше обращение.', 
        color = 0x2f3136)
        responceemb = discord.Embed(title='Когда мне ответят?', description=" Обращения разбираются в порядке очереди. В среднем обращения разбираются от 1 до 3-х часов в рабочие дни с 08:00 по 22:00. В выходные время ответа может быть дольше, но не более 9-ти часов. \n\nЕсли с момента отправки последнего сообщения прошло более 3-х часов, а вам не ответили - можете упомянуть <@&939476433196171324>. \nЕсли прошло более 6-ти часов - упоминайте <@&922561682780332102>.", color = 0x2f3136)
        buttonembed = discord.Embed(title='', description='<:info:871310064135327775> Обращения закрываются сотрудниками кнопкой ниже.', color = 0x2f3136)
        maintenance = '<:minecraft_deny:1080779495386140684> Служба поддержки временно недоступна.** \nПричина: проведение технических работ. \nВ ближайшее время данная служба будет восстановлена.'

        if inter.component.custom_id == "maintenance_dc":
            await inter.send(maintenance, ephemeral = True)
            return   
        if inter.component.custom_id == "maintenance_mc":
            await inter.send(maintenance, ephemeral = True)
            return   
        if inter.component.custom_id == "discord_openticket":
            if memberop.id in voprosmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in voprosmembers:
                chooseemb = discord.Embed(title='Выберите тип обращения Discord', color = 0x607aff)
                row = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Жалоба',
                        custom_id = 'discord_report',
                        emoji= '<:report:1105878279736528977>'
                    )
                row3 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Отчёт о баге',
                        custom_id = 'discord_bugreport',
                        emoji= '<:bughunter:1105878297176457337>'
                    )
                row4 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Вопрос',
                        custom_id = 'discord_question',
                        emoji= '<:quest:1105887328771260446>'
                    )
                row5 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Прочее',
                        custom_id = 'discord_other',
                        emoji= '<:message:1105891497255108679>'
                    )
                row6 = Button(
                        style = discord.ButtonStyle.danger,
                        label = 'Обращение к руководству',
                        custom_id = 'discord_admins',
                        emoji= '<:message:1105891497255108679>'
                    )
                view=View()
                view.add_item(row)
                view.add_item(row3)
                view.add_item(row4)
                view.add_item(row5)
                view.add_item(row6)
                await inter.send(embed=chooseemb, view = view, ephemeral = True)
                return

        if inter.component.custom_id == "discord_admins":
            if memberop.id in voprosmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in voprosmembers:
                global countervopros
                countervopros += 1
                voprosmembers.append(memberop.id)
                ticket_server = '<:discord:856561477033263124> `Discord`'
                ticket_type = '<:admins:1105927773219987486> `Обращение к руководству`'
                ticket_systemname= 'admin_discord'
                mainCategory = mainCategory
                channel2 = await guild.create_text_channel(f"ticket {ticket_num}", category = mainCategory)
                await channel2.set_permissions(staffrole,send_messages=False,read_messages=False,read_message_history=False)
                await channel2.set_permissions(internrole,send_messages=False,read_messages=False,read_message_history=False)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)

                embinfo = discord.Embed(title='<:info:871310064135327775> Информация об обращении', description=f'**Автор:** <:member:1105878287978340415> `{memberop}` \n **ID обращения:**  `{ticket_num}` \n\n**Сервер:** <:discord:856561477033263124> `Discord`. \n**Тип обращения:** <:admins:1105927773219987486> `Обращение к руководству`.', color = 0x2f3136)
                emb1 = dcadmins
                responceemb = responceemb
                buttonembed = buttonembed
                await channel2.send(embed=embinfo)
                await channel2.send(embed=emb1)
                await channel2.send(embed=responceemb)

                row = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Закрыть обращение',
                        custom_id = 'accept_admin_discord',
                        emoji= '<:blurplelock:856563321321816104>'
                    )
                view2=View()
                view2.add_item(row)
                msgtic = await channel2.send(embed=buttonembed, view=view2)
                delete = await channel2.send(content = f'{memberop.mention}')
                await delete.delete()

                def check(m):
                    return m.message.id == msgtic.id and m.author.guild_permissions.manage_messages == True
                try:
                   m = await self.client.wait_for("button_click", check=check)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде тикетов") 
                else:
                    if m.component.custom_id == "accept_admin_discord":
                        pwnight = await self.client.fetch_user(int(660070694377357322))
                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Обращение закрыто.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Сервер:', value=f'{ticket_server}')
                        embedth.add_field(name='Тип обращения:', value=f'{ticket_type}')
                        embedth.add_field(name='Руководитель:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор:', value=f'<:member:1105878287978340415> `{memberop}`')  

                        with open(f"{ticket_systemname}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")   
               
                        await pwnight.send(embed=embedth,file=File(f'{ticket_systemname}.txt'))
                        await channel2.delete()
                        clsembed=discord.Embed(title="Поддержка проекта FoxWorld", description=f'Приветствую. \nВаше обращение закрыто Руководителем {m.author.mention} ({m.author.display_name}). \n\nID:  `{ticket_num}` \nСервер: <:discord:856561477033263124> `Discord`.\nТип обращения: <:report:1105878279736528977> `Жалоба`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1105878293187678208.webp?size=96&quality=lossless")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        
                        voprosmembers.remove(memberop.id)
                        os.remove(f'{ticket_systemname}.txt')
                        return
                                
        if inter.component.custom_id == "discord_report":
            if memberop.id in voprosmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in voprosmembers:
                await inter.send(res, ephemeral = True)
                countervopros += 1
                voprosmembers.append(memberop.id)
                ticket_server = '<:discord:856561477033263124> `Discord`'
                ticket_type = '<:report:1105878279736528977> `Жалоба`'
                ticket_systemname= 'report_discord'
                mainCategory = mainCategory
                channel2 = await guild.create_text_channel(f"ticket {ticket_num}", category = mainCategory)
                await channel2.set_permissions(staffrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(internrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)

                embinfo = discord.Embed(title='<:info:871310064135327775> Информация об обращении', description=f'**Автор:** <:member:1105878287978340415> `{memberop}` \n **ID обращения:**  `{ticket_num}` \n\n**Сервер:** <:discord:856561477033263124> `Discord`. \n**Тип обращения:** <:report:1105878279736528977> `Жалоба`.', color = 0x2f3136)
                emb1 = dcreport
                responceemb = responceemb
                buttonembed = buttonembed
                await channel2.send(embed=embinfo)
                await channel2.send(embed=emb1)
                await channel2.send(embed=responceemb)

                row = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Закрыть обращение',
                        custom_id = 'accept_report_discord',
                        emoji= '<:blurplelock:856563321321816104>'
                    )
                view2=View()
                view2.add_item(row)
                msgtic = await channel2.send(embed=buttonembed, view=view2)
                delete = await channel2.send(content = f'{memberop.mention}')
                await delete.delete()

                def check(m):
                    return m.message.id == msgtic.id and m.author.guild_permissions.manage_messages == True
                try:
                   m = await self.client.wait_for("button_click", check=check)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде тикетов") 
                else:
                    if m.component.custom_id == "accept_report_discord":

                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Обращение закрыто.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Сервер:', value=f'{ticket_server}')
                        embedth.add_field(name='Тип обращения:', value=f'{ticket_type}')
                        embedth.add_field(name='Сотрудник:', value=f'<:moderatorbadge:953725334518378616> `{m.author.display_name}`')
                        embedth.add_field(name='Автор:', value=f'<:member:1105878287978340415> `{memberop}`')  

                        with open(f"{ticket_systemname}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")   
               
                        await logchannel.send(embed=embedth,file=File(f'{ticket_systemname}.txt'))
                        await channel2.delete()
                        clsembed=discord.Embed(title="Поддержка проекта FoxWorld", description=f'Приветствую. \nВаше обращение закрыто Сотрудником {m.author.mention} ({m.author.display_name}). \n\nID:  `{ticket_num}` \nСервер: <:discord:856561477033263124> `Discord`.\nТип обращения: <:report:1105878279736528977> `Жалоба`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1105878293187678208.webp?size=96&quality=lossless")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        
                        voprosmembers.remove(memberop.id)
                        os.remove(f'{ticket_systemname}.txt')
                        return
        if inter.component.custom_id == "discord_bugreport":
            if memberop.id in voprosmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in voprosmembers:
                await inter.send(res, ephemeral = True)
                countervopros += 1
                voprosmembers.append(memberop.id)
                ticket_server = '<:discord:856561477033263124> `Discord`'
                ticket_type = '<:bughunter:1105878297176457337> `Отчёт о баге`'
                ticket_systemname= 'bugreport_discord'
                mainCategory = mainCategory
                channel2 = await guild.create_text_channel(f"ticket {ticket_num}", category = mainCategory)
                staffrole = staffrole
                await channel2.set_permissions(staffrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(internrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)

                embinfo = discord.Embed(title='<:info:871310064135327775> Информация об обращении', description=f'**Автор:** <:member:1105878287978340415> `{memberop}` \n **ID обращения:**  `{ticket_num}` \n\n**Сервер:** <:discord:856561477033263124> `Discord`. \n**Тип обращения:** <:bughunter:1105878297176457337> `Отчёт о баге`.', color = 0x2f3136)
                emb1 = dcbugreport
                responceemb = responceemb
                buttonembed = buttonembed
                await channel2.send(embed=embinfo)
                await channel2.send(embed=emb1)
                await channel2.send(embed=responceemb)

                row = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Закрыть обращение',
                        custom_id = 'accept_bugreport_discord',
                        emoji= '<:blurplelock:856563321321816104>'
                    )
                view2=View()
                view2.add_item(row)
                msgtic = await channel2.send(embed=buttonembed, view=view2)
                delete = await channel2.send(content = f'{memberop.mention}')
                await delete.delete()

                def check(m):
                    return m.message.id == msgtic.id and m.author.guild_permissions.manage_messages == True
                try:
                   m = await self.client.wait_for("button_click", check=check)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде тикетов") 
                else:
                    if m.component.custom_id == "accept_bugreport_discord":

                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Обращение закрыто.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Сервер:', value=f'{ticket_server}')
                        embedth.add_field(name='Тип обращения:', value=f'{ticket_type}')
                        embedth.add_field(name='Сотрудник:', value=f'<:blurplecertifiedmoderator:856563321541230602> `{m.author.display_name}`')
                        embedth.add_field(name='Автор:', value=f'<:member:1105878287978340415> `{memberop}`')  

                        with open(f"{ticket_systemname}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")   
               
                        await logchannel.send(embed=embedth,file=File(f'{ticket_systemname}.txt'))
                        await channel2.delete()
                        clsembed=discord.Embed(title="Поддержка проекта FoxWorld", description=f'Приветствую. \nВаше обращение закрыто Сотрудником {m.author.mention} ({m.author.display_name}). \n\nID:  `{ticket_num}` \nСервер: <:discord:856561477033263124> `Discord`.\nТип обращения: <:report:1105878279736528977> `Жалоба`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1105878293187678208.webp?size=96&quality=lossless")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        
                        voprosmembers.remove(memberop.id)
                        os.remove(f'{ticket_systemname}.txt')
                        return 

        if inter.component.custom_id == "discord_question":
            if memberop.id in voprosmembers:
                resno = '<:error:1105878281246482484> У вас уже есть открытое обращение. Вы не можете открыть новое обращение, пока предыдущее не будет закрыто.'
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in voprosmembers:
                await inter.send(res, ephemeral = True)
                countervopros += 1
                voprosmembers.append(memberop.id)
                ticket_server = '<:discord:856561477033263124> `Discord`'
                ticket_type = '<:quest:1105887328771260446> `Вопрос`'
                ticket_systemname= 'question_discord'
                mainCategory = mainCategory
                channel2 = await guild.create_text_channel(f"ticket {ticket_num}", category = mainCategory)
                staffrole = staffrole
                await channel2.set_permissions(staffrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(internrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)

                embinfo = discord.Embed(title='<:info:871310064135327775> Информация об обращении', description=f'**Автор:** <:member:1105878287978340415> `{memberop}` \n **ID обращения:**  `{ticket_num}` \n\n**Сервер:** <:discord:856561477033263124> `Discord`. \n**Тип обращения:** <:quest:1105887328771260446> `Вопрос`.', color = 0x2f3136)
                emb1 = dcquestion
                responceemb = responceemb
                buttonembed = buttonembed
                await channel2.send(embed=embinfo)
                await channel2.send(embed=emb1)
                await channel2.send(embed=responceemb)

                row = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Закрыть обращение',
                        custom_id = 'accept_question_discord',
                        emoji= '<:blurplelock:856563321321816104>'
                    )
                view2=View()
                view2.add_item(row)
                msgtic = await channel2.send(embed=buttonembed, view=view2)
                delete = await channel2.send(content = f'{memberop.mention}')
                await delete.delete()

                def check(m):
                    return m.message.id == msgtic.id and m.author.guild_permissions.manage_messages == True
                try:
                   m = await self.client.wait_for("button_click", check=check)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде тикетов") 
                else:
                    if m.component.custom_id == "accept_question_discord":

                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Обращение закрыто.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Сервер:', value=f'{ticket_server}')
                        embedth.add_field(name='Тип обращения:', value=f'{ticket_type}')
                        embedth.add_field(name='Сотрудник:', value=f'<:blurplecertifiedmoderator:856563321541230602> `{m.author.display_name}`')
                        embedth.add_field(name='Автор:', value=f'<:member:1105878287978340415> `{memberop}`')  

                        with open(f"{ticket_systemname}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")   
               
                        await logchannel.send(embed=embedth,file=File(f'{ticket_systemname}.txt'))
                        await channel2.delete()
                        clsembed=discord.Embed(title="Поддержка проекта FoxWorld", description=f'Приветствую. \nВаше обращение закрыто Сотрудником {m.author.mention} ({m.author.display_name}). \n\nID:  `{ticket_num}` \nСервер: <:discord:856561477033263124> `Discord`.\nТип обращения: <:report:1105878279736528977> `Жалоба`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1105878293187678208.webp?size=96&quality=lossless")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        
                        voprosmembers.remove(memberop.id)
                        os.remove(f'{ticket_systemname}.txt')
                        return
        if inter.component.custom_id == "discord_other":
            if memberop.id in voprosmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in voprosmembers:
                await inter.send(res, ephemeral = True)
                countervopros += 1
                voprosmembers.append(memberop.id)
                ticket_server = '<:discord:856561477033263124> `Discord`'
                ticket_type = '<:message:1105891497255108679> `Прочее`'
                ticket_systemname= 'other_discord'
                mainCategory = mainCategory
                channel2 = await guild.create_text_channel(f"ticket {ticket_num}", category = mainCategory)
                staffrole = staffrole
                await channel2.set_permissions(staffrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(internrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)

                embinfo = discord.Embed(title='<:info:871310064135327775> Информация об обращении', description=f'**Автор:** <:member:1105878287978340415> `{memberop}` \n **ID обращения:**  `{ticket_num}` \n\n**Сервер:** <:discord:856561477033263124> `Discord`. \n**Тип обращения:** <:message:1105891497255108679> `Прочее`.', color = 0x2f3136)
                emb1 = dcother
                responceemb = responceemb
                buttonembed = buttonembed
                await channel2.send(embed=embinfo)
                await channel2.send(embed=emb1)
                await channel2.send(embed=responceemb)

                row = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Закрыть обращение',
                        custom_id = 'accept_other_discord',
                        emoji= '<:blurplelock:856563321321816104>'
                    )
                view2=View()
                view2.add_item(row)
                msgtic = await channel2.send(embed=buttonembed, view=view2)
                delete = await channel2.send(content = f'{memberop.mention}')
                await delete.delete()

                def check(m):
                    return m.message.id == msgtic.id and m.author.guild_permissions.manage_messages == True
                try:
                   m = await self.client.wait_for("button_click", check=check)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде тикетов") 
                else:
                    if m.component.custom_id == "accept_other_discord":

                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Обращение закрыто.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Сервер:', value=f'{ticket_server}')
                        embedth.add_field(name='Тип обращения:', value=f'{ticket_type}')
                        embedth.add_field(name='Сотрудник:', value=f'<:blurplecertifiedmoderator:856563321541230602> `{m.author.display_name}`')
                        embedth.add_field(name='Автор:', value=f'<:member:1105878287978340415> `{memberop}`')  

                        with open(f"{ticket_systemname}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")   
               
                        await logchannel.send(embed=embedth,file=File(f'{ticket_systemname}.txt'))
                        await channel2.delete()
                        clsembed=discord.Embed(title="Поддержка проекта FoxWorld", description=f'Приветствую. \nВаше обращение закрыто сотрудником {m.author.mention} ({m.author.display_name}). \n\nID:  `{ticket_num}` \nСервер: <:discord:856561477033263124> `Discord`.\nТип обращения: <:report:1105878279736528977> `Жалоба`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1105878293187678208.webp?size=96&quality=lossless")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        
                        voprosmembers.remove(memberop.id)
                        os.remove(f'{ticket_systemname}.txt')
                        return
        if inter.component.custom_id == "minecraft_openticket":
            if memberop.id in voprosmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in voprosmembers:
                chooseemb = discord.Embed(title='Выберите тип обращения Minecraft', color = 0x9cdf39)
                row = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Жалоба',
                        custom_id = 'mc_report',
                        emoji= '<:report:1105878279736528977>'
                    )
                row3 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Отчёт о баге',
                        custom_id = 'mc_bugreport',
                        emoji= '<:bughunter:1105878297176457337>'
                    )
                row4 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Вопрос',
                        custom_id = 'mc_question',
                        emoji= '<:quest:1105887328771260446>'
                    )
                row5 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Прочее',
                        custom_id = 'mc_other',
                        emoji= '<:message:1105891497255108679>'
                    )
                row6 = Button(
                        style = discord.ButtonStyle.danger,
                        label = 'Обращение к руководству',
                        custom_id = 'discord_admins',
                        emoji= '<:message:1105891497255108679>'
                    )
                view=View()
                view.add_item(row)
                view.add_item(row3)
                view.add_item(row4)
                view.add_item(row5)
                view.add_item(row6)
                await inter.send(embed=chooseemb, view = view, ephemeral = True)
                return
            
        if inter.component.custom_id == "mc_admins":
            if memberop.id in voprosmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in voprosmembers:
                await inter.send(res, ephemeral = True)
                countervopros += 1
                voprosmembers.append(memberop.id)
                ticket_server = '<:minecraft:856561476873355316>  `Minecraft`'
                ticket_type = '<:admins:1105927773219987486> `Обращение к руководству`'
                ticket_systemname= 'admin_mc'
                mainCategory = mainCategory
                channel2 = await guild.create_text_channel(f"ticket {ticket_num}", category = mainCategory)
                await channel2.set_permissions(staffrole,send_messages=False,read_messages=False,read_message_history=False)
                await channel2.set_permissions(internrole,send_messages=False,read_messages=False,read_message_history=False)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)

                embinfo = discord.Embed(title='<:info:871310064135327775> Информация об обращении', description=f'**Автор:** <:member:1105878287978340415> `{memberop}` \n **ID обращения:**  `{ticket_num}` \n\n**Сервер:** <:minecraft:856561476873355316>  `Minecraft`. \n**Тип обращения:** <:admins:1105927773219987486> `Обращение к руководству`.', color = 0x2f3136)
                emb1 = mcadmins
                responceemb = responceemb
                buttonembed = buttonembed
                await channel2.send(embed=embinfo)
                await channel2.send(embed=emb1)
                await channel2.send(embed=responceemb)

                row = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Закрыть обращение',
                        custom_id = 'accept_admin_mc',
                        emoji= '<:blurplelock:856563321321816104>'
                    )
                view2=View()
                view2.add_item(row)
                msgtic = await channel2.send(embed=buttonembed, view=view2)
                delete = await channel2.send(content = f'{memberop.mention}')
                await delete.delete()

                def check(m):
                    return m.message.id == msgtic.id and m.author.guild_permissions.manage_messages == True
                try:
                   m = await self.client.wait_for("button_click", check=check)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде тикетов") 
                else:
                    if m.component.custom_id == "accept_admin_mc":
                        pwnight = await self.client.fetch_user(int(660070694377357322))
                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Обращение закрыто.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Сервер:', value=f'{ticket_server}')
                        embedth.add_field(name='Тип обращения:', value=f'{ticket_type}')
                        embedth.add_field(name='Руководитель:', value=f'<:moderatorbadge:953725334518378616> `{m.author.display_name}`')
                        embedth.add_field(name='Автор:', value=f'<:member:1105878287978340415> `{memberop}`')  

                        with open(f"{ticket_systemname}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")   
               
                        await pwnight.send(embed=embedth,file=File(f'{ticket_systemname}.txt'))
                        await channel2.delete()
                        clsembed=discord.Embed(title="Поддержка проекта FoxWorld", description=f'Приветствую. \nВаше обращение закрыто администратором {m.author.mention} ({m.author.display_name}). \n\nID:  `{ticket_num}` \nСервер: <:discord:856561477033263124> `Discord`.\nТип обращения: <:report:1105878279736528977> `Жалоба`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1105878293187678208.webp?size=96&quality=lossless")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        
                        voprosmembers.remove(memberop.id)
                        os.remove(f'{ticket_systemname}.txt')
                        return

        if inter.component.custom_id == "mc_report":
            if memberop.id in voprosmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in voprosmembers:
                await inter.send(res, ephemeral = True)
                countervopros += 1
                voprosmembers.append(memberop.id)
                ticket_server = '<:minecraft:856561476873355316> `Minecraft`'
                ticket_type = '<:report:1105878279736528977> `Жалоба`'
                ticket_systemname= 'report_minecraft'
                mainCategory = mainCategory
                channel2 = await guild.create_text_channel(f"ticket {ticket_num}", category = mainCategory)
                staffrole = staffrole
                await channel2.set_permissions(staffrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(internrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)

                embinfo = discord.Embed(title='<:info:871310064135327775> Информация об обращении', description=f'**Автор:** <:member:1105878287978340415> `{memberop}` \n **ID обращения:**  `{ticket_num}` \n\n**Сервер:** <:minecraft:856561476873355316> `Minecraft`. \n**Тип обращения:** <:report:1105878279736528977> `Жалоба`.', color = 0x2f3136)
                emb1 = mcreport
                responceemb = responceemb
                buttonembed = buttonembed
                await channel2.send(embed=embinfo)
                await channel2.send(embed=emb1)
                await channel2.send(embed=responceemb)

                row = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Закрыть обращение',
                        custom_id = 'accept_report_mc',
                        emoji= '<:blurplelock:856563321321816104>'
                    )
                view2=View()
                view2.add_item(row)
                msgtic = await channel2.send(embed=buttonembed, view=view2)
                delete = await channel2.send(content = f'{memberop.mention}')
                await delete.delete()

                def check(m):
                    return m.message.id == msgtic.id and m.author.guild_permissions.manage_messages == True
                try:
                   m = await self.client.wait_for("button_click", check=check)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде тикетов") 
                else:
                    if m.component.custom_id == "accept_report_mc":

                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Обращение закрыто.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Сервер:', value=f'{ticket_server}')
                        embedth.add_field(name='Тип обращения:', value=f'{ticket_type}')
                        embedth.add_field(name='Сотрудник:', value=f'<:blurplecertifiedmoderator:856563321541230602> `{m.author.display_name}`')
                        embedth.add_field(name='Автор:', value=f'<:member:1105878287978340415> `{memberop}`')  

                        with open(f"{ticket_systemname}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")   
               
                        await logchannel.send(embed=embedth,file=File(f'{ticket_systemname}.txt'))
                        await channel2.delete()
                        clsembed=discord.Embed(title="Поддержка проекта FoxWorld", description=f'Приветствую. \nВаше обращение закрыто Сотрудником {m.author.mention} ({m.author.display_name}). \n\nID:  `{ticket_num}` \nСервер: <:discord:856561477033263124> `Discord`.\nТип обращения: <:report:1105878279736528977> `Жалоба`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1105878293187678208.webp?size=96&quality=lossless")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        
                        voprosmembers.remove(memberop.id)
                        os.remove(f'{ticket_systemname}.txt')
                        return
                    
        if inter.component.custom_id == "mc_bugreport":
            if memberop.id in voprosmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in voprosmembers:
                await inter.send(res, ephemeral = True)
                countervopros += 1
                voprosmembers.append(memberop.id)
                ticket_server = '<:minecraft:856561476873355316> `Minecraft`'
                ticket_type = '<:bughunter:1105878297176457337> `Отчёт о баге`'
                ticket_systemname= 'bugreport_minecraft'
                mainCategory = mainCategory
                channel2 = await guild.create_text_channel(f"ticket {ticket_num}", category = mainCategory)
                staffrole = staffrole
                await channel2.set_permissions(staffrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(internrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)

                embinfo = discord.Embed(title='<:info:871310064135327775> Информация об обращении', description=f'**Автор:** <:member:1105878287978340415> `{memberop}` \n **ID обращения:**  `{ticket_num}` \n\n**Сервер:** <:minecraft:856561476873355316> `Minecraft`. \n**Тип обращения:** <:bughunter:1105878297176457337> `Отчёт о багое`.', color = 0x2f3136)
                emb1 = mcbugreport
                responceemb = responceemb
                buttonembed = buttonembed
                await channel2.send(embed=embinfo)
                await channel2.send(embed=emb1)
                await channel2.send(embed=responceemb)

                row = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Закрыть обращение',
                        custom_id = 'accept_bugreport_mc',
                        emoji= '<:blurplelock:856563321321816104>'
                    )
                view2=View()
                view2.add_item(row)
                msgtic = await channel2.send(embed=buttonembed, view=view2)
                delete = await channel2.send(content = f'{memberop.mention}')
                await delete.delete()

                def check(m):
                    return m.message.id == msgtic.id and m.author.guild_permissions.manage_messages == True
                try:
                   m = await self.client.wait_for("button_click", check=check)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде тикетов") 
                else:
                    if m.component.custom_id == "accept_bugreport_mc":

                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Обращение закрыто.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Сервер:', value=f'{ticket_server}')
                        embedth.add_field(name='Тип обращения:', value=f'{ticket_type}')
                        embedth.add_field(name='Сотрудник:', value=f'<:blurplecertifiedmoderator:856563321541230602> `{m.author.display_name}`')
                        embedth.add_field(name='Автор:', value=f'<:member:1105878287978340415> `{memberop}`')  

                        with open(f"{ticket_systemname}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")   
               
                        await logchannel.send(embed=embedth,file=File(f'{ticket_systemname}.txt'))
                        await channel2.delete()
                        clsembed=discord.Embed(title="Поддержка проекта FoxWorld", description=f'Приветствую. \nВаше обращение закрыто Сотрудником {m.author.mention} ({m.author.display_name}). \n\nID:  `{ticket_num}` \nСервер: <:discord:856561477033263124> `Discord`.\nТип обращения: <:report:1105878279736528977> `Жалоба`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1105878293187678208.webp?size=96&quality=lossless")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        
                        voprosmembers.remove(memberop.id)
                        os.remove(f'{ticket_systemname}.txt')
                        return

        if inter.component.custom_id == "mc_question":
            if memberop.id in voprosmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in voprosmembers:
                await inter.send(res, ephemeral = True)
                countervopros += 1
                voprosmembers.append(memberop.id)
                ticket_server = '<:minecraft:856561476873355316> `Minecraft`'
                ticket_type = '<:quest:1105887328771260446> `Вопрос`'
                ticket_systemname= 'question_minecraft'
                mainCategory = mainCategory
                channel2 = await guild.create_text_channel(f"ticket {ticket_num}", category = mainCategory)
                staffrole = staffrole
                await channel2.set_permissions(staffrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(internrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)

                embinfo = discord.Embed(title='<:info:871310064135327775> Информация об обращении', description=f'**Автор:** <:member:1105878287978340415> `{memberop}` \n **ID обращения:**  `{ticket_num}` \n\n**Сервер:** <:minecraft:856561476873355316> `Minecraft`. \n**Тип обращения:** <:quest:1105887328771260446> `Вопрос`.', color = 0x2f3136)
                emb1 = mcquestion
                responceemb = responceemb
                buttonembed = buttonembed
                await channel2.send(embed=embinfo)
                await channel2.send(embed=emb1)
                await channel2.send(embed=responceemb)

                row = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Закрыть обращение',
                        custom_id = 'accept_question_mc',
                        emoji= '<:blurplelock:856563321321816104>'
                    )
                view2=View()
                view2.add_item(row)
                msgtic = await channel2.send(embed=buttonembed, view=view2)
                delete = await channel2.send(content = f'{memberop.mention}')
                await delete.delete()

                def check(m):
                    return m.message.id == msgtic.id and m.author.guild_permissions.manage_messages == True
                try:
                   m = await self.client.wait_for("button_click", check=check)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде тикетов") 
                else:
                    if m.component.custom_id == "accept_question_mc":

                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Обращение закрыто.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Сервер:', value=f'{ticket_server}')
                        embedth.add_field(name='Тип обращения:', value=f'{ticket_type}')
                        embedth.add_field(name='Сотрудник:', value=f'<:blurplecertifiedmoderator:856563321541230602> `{m.author.display_name}`')
                        embedth.add_field(name='Автор:', value=f'<:member:1105878287978340415> `{memberop}`')  

                        with open(f"{ticket_systemname}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")   
               
                        await logchannel.send(embed=embedth,file=File(f'{ticket_systemname}.txt'))
                        await channel2.delete()
                        clsembed=discord.Embed(title="Поддержка проекта FoxWorld", description=f'Приветствую. \nВаше обращение закрыто сотрудником {m.author.mention} ({m.author.display_name}). \n\nID:  `{ticket_num}` \nСервер: <:discord:856561477033263124> `Discord`.\nТип обращения: <:report:1105878279736528977> `Жалоба`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1105878293187678208.webp?size=96&quality=lossless")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        
                        voprosmembers.remove(memberop.id)
                        os.remove(f'{ticket_systemname}.txt')
                        return

        if inter.component.custom_id == "mc_other":
            if memberop.id in voprosmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in voprosmembers:
                await inter.send(res, ephemeral = True)
                countervopros += 1
                voprosmembers.append(memberop.id)
                ticket_server = '<:minecraft:856561476873355316> `Minecraft`'
                ticket_type = '<:message:1105891497255108679> `Прочее`'
                ticket_systemname= 'other_minecraft'
                mainCategory = mainCategory
                channel2 = await guild.create_text_channel(f"ticket {ticket_num}", category = mainCategory)
                staffrole = staffrole
                await channel2.set_permissions(staffrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(internrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)

                embinfo = discord.Embed(title='<:info:871310064135327775> Информация об обращении', description=f'**Автор:** <:member:1105878287978340415> `{memberop}` \n **ID обращения:**  `{ticket_num}` \n\n**Сервер:** <:minecraft:856561476873355316> `Minecraft`. \n**Тип обращения:** <:message:1105891497255108679> `Прочее`.', color = 0x2f3136)
                emb1 = mcother
                responceemb = responceemb
                buttonembed = buttonembed
                await channel2.send(embed=embinfo)
                await channel2.send(embed=emb1)
                await channel2.send(embed=responceemb)

                row = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Закрыть обращение',
                        custom_id = 'accept_other_mc',
                        emoji= '<:blurplelock:856563321321816104>'
                    )
                view2=View()
                view2.add_item(row)
                msgtic = await channel2.send(embed=buttonembed, view=view2)
                delete = await channel2.send(content = f'{memberop.mention}')
                await delete.delete()

                def check(m):
                    return m.message.id == msgtic.id and m.author.guild_permissions.manage_messages == True
                try:
                   m = await self.client.wait_for("button_click", check=check)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде тикетов") 
                else:
                    if m.component.custom_id == "accept_other_mc":

                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Обращение закрыто.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Сервер:', value=f'{ticket_server}')
                        embedth.add_field(name='Тип обращения:', value=f'{ticket_type}')
                        embedth.add_field(name='Сотрудник:', value=f'<:moderatorbadge:953725334518378616> `{m.author.display_name}`')
                        embedth.add_field(name='Автор:', value=f'<:member:1105878287978340415> `{memberop}`')  

                        with open(f"{ticket_systemname}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")   
               
                        await logchannel.send(embed=embedth,file=File(f'{ticket_systemname}.txt'))
                        await channel2.delete()
                        clsembed=discord.Embed(title="Поддержка проекта FoxWorld", description=f'Приветствую. \nВаше обращение закрыто Сотрудником {m.author.mention} ({m.author.display_name}). \n\nID:  `{ticket_num}` \nСервер: <:discord:856561477033263124> `Discord`.\nТип обращения: <:report:1105878279736528977> `Жалоба`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1105878293187678208.webp?size=96&quality=lossless")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        
                        voprosmembers.remove(memberop.id)
                        os.remove(f'{ticket_systemname}.txt')
                        return  

def setup(client):
    client.add_cog(ButtonClick(client))