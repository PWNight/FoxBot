import disnake as discord
from disnake.ext import commands
import asyncio
import os
from disnake import File
from disnake.ui import Button, View
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
        channel2 = await guild.create_text_channel(f"ticket {ticket_num}", category = mainCategory)
        staffrole = discord.utils.get(guild.roles,id=939476433196171324)
        internrole = discord.utils.get(guild.roles,id=995056541734539354)
        
        #Текстовая информация для тикетов.
        res = '<:phoenix_verify:953725334770040953> Обращение создано. Ожидайте пинга в нужном канале.' # ваш вывод сообщение что человек получил роль
        resno = '<:phoenix_warn:953725334736502784> У вас уже есть открытое обращение. Вы не можете открыть обращение, пока предыдущее не будет закрыто.'
        memberop = inter.author
        embinfo = discord.Embed(title='<:info:871310064135327775> Информация об обращении', description=f'**Автор:** <:member:979406123587223562> `{memberop}` \n **ID обращения:**  `{ticket_num}` \n\n**Сервер:** <:discord:856561477033263124> `Discord`. \n**Тип обращения:** <:serfmoderator:953725334627430411> `Жалоба`.', color = 0x2f3136)
        emb1 = discord.Embed(title='Добро пожаловать в службу поддержки Discord.', description='Чтобы получить ответ как можно быстрее, опишите суть вашей жалобы по следующей форме заполнения: \n1) Ваш никнейм. \n2) Никнейм нарушителя. \n3) Нарушенное правило.\n4) Подробность нарушения. \n5) Доказательства нарушения.', color = 0x2f3136)
        responceemb = discord.Embed(title='Когда мне ответят?', description=" Обращения разбираются в порядке очереди. В среднем обращения разбираются от 1 до 3-х часов в рабочие дни с 10:00 по 00:00. В выходные время ответа может быть дольше, но не более 9-ти часов. \n\nЕсли с момента отправки последнего сообщения прошло более 3-х часов, а вам не ответили - можете упомянуть <@&939476433196171324>. \nЕсли прошло более 6-ти часов - упоминайте <@&922561682780332102>.", color = 0x2f3136)
        buttonembed = discord.Embed(title='', description='<:info:871310064135327775> Обращения закрываются сотрудниками кнопкой ниже.', color = 0x2f3136)
        if inter.component.custom_id == "discord_open":
            if memberop.id in voprosmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in voprosmembers:
                chooseemb = discord.Embed(title='Выберите тип обращения Discord', color = 0x607aff)
                row = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Жалоба',
                        custom_id = 'discord_report',
                        emoji= '<:serfmoderator:953725334627430411>'
                    )
                row3 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Отчёт о баге',
                        custom_id = 'discord_bugreport',
                        emoji= '<:bughunter:979394820122476594>'
                    )
                row4 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Вопрос',
                        custom_id = 'discord_question',
                        emoji= '<:5342discordquestion:979396237558177792>'
                    )
                row5 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Прочее',
                        custom_id = 'discord_other',
                        emoji= '<:phoenix_text:856563321276071976>'
                    )
                view=View()
                view.add_item(row)
                view.add_item(row3)
                view.add_item(row4)
                view.add_item(row5)
                await inter.send(embed=chooseemb, view = view, ephemeral = True)
        if inter.component.custom_id == "discord_report":
            if memberop.id in voprosmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in voprosmembers:
                await inter.send(res, ephemeral = True)
                global countervopros
                countervopros += 1
                voprosmembers.append(memberop.id)
                ticket_server = '<:discord:856561477033263124> `Discord`'
                ticket_type = '<:serfmoderator:953725334627430411> `Жалоба`'
                ticket_systemname= 'report_discord'
                mainCategory = mainCategory
                channel2 = channel2
                staffrole = staffrole
                await channel2.set_permissions(staffrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(internrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)

                embinfo = embinfo
                emb1 = emb1
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
                        embedth.add_field(name='Модератор:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор:', value=f'<:member:979406123587223562> `{memberop}`')  

                        with open(f"{ticket_systemname}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")   
               
                        await logchannel.send(embed=embedth,file=File(f'{ticket_systemname}.txt'))
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба поддержки Discord.", description=f'Приветствую. \nВаше обращение закрыто сотрудником `{m.author}`. \nВы можете запросить файл с содержанием вашего обращения в течение 3-х дней с момента закрытия обращения. Для этого обратитесь к руководителю проекта `Найт#0550`, предъявив ID вашего обращения. \n\nID:  `{ticket_num}` \nСервер: <:discord:856561477033263124> `Discord`.\nТип обращения: <:serfmoderator:953725334627430411> `Жалоба`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
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
                ticket_type = '<:bughunter:979394820122476594> `Отчёт о баге`'
                ticket_systemname= 'bugreport_discord'
                mainCategory = mainCategory
                channel2 = channel2
                staffrole = staffrole
                await channel2.set_permissions(staffrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(internrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)

                embinfo = embinfo
                emb1 = emb1
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
                        embedth.add_field(name='Модератор:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор:', value=f'<:member:979406123587223562> `{memberop}`')  

                        with open(f"{ticket_systemname}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")   
               
                        await logchannel.send(embed=embedth,file=File(f'{ticket_systemname}.txt'))
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба поддержки Discord.", description=f'Приветствую. \nВаше обращение закрыто сотрудником `{m.author}`. \nВы можете запросить файл с содержанием вашего обращения в течение 3-х дней с момента закрытия обращения. Для этого обратитесь к руководителю проекта `Найт#0550`, предъявив ID вашего обращения. \n\nID:  `{ticket_num}` \nСервер: <:discord:856561477033263124> `Discord`.\nТип обращения: <:serfmoderator:953725334627430411> `Жалоба`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        
                        voprosmembers.remove(memberop.id)
                        os.remove(f'{ticket_systemname}.txt')
                        return 

        if inter.component.custom_id == "discord_question":
            if memberop.id in voprosmembers:
                resno = '<:phoenix_warn:953725334736502784> У вас уже есть открытое обращение. Вы не можете открыть новое обращение, пока предыдущее не будет закрыто.'
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in voprosmembers:
                await inter.send(res, ephemeral = True)
                countervopros += 1
                voprosmembers.append(memberop.id)
                ticket_server = '<:discord:856561477033263124> `Discord`'
                ticket_type = '<:5342discordquestion:979396237558177792> `Вопрос`'
                ticket_systemname= 'question_discord'
                mainCategory = mainCategory
                channel2 = channel2
                staffrole = staffrole
                await channel2.set_permissions(staffrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(internrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)

                embinfo = embinfo
                emb1 = emb1
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
                        embedth.add_field(name='Модератор:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор:', value=f'<:member:979406123587223562> `{memberop}`')  

                        with open(f"{ticket_systemname}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")   
               
                        await logchannel.send(embed=embedth,file=File(f'{ticket_systemname}.txt'))
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба поддержки Discord.", description=f'Приветствую. \nВаше обращение закрыто сотрудником `{m.author}`. \nВы можете запросить файл с содержанием вашего обращения в течение 3-х дней с момента закрытия обращения. Для этого обратитесь к руководителю проекта `Найт#0550`, предъявив ID вашего обращения. \n\nID:  `{ticket_num}` \nСервер: <:discord:856561477033263124> `Discord`.\nТип обращения: <:serfmoderator:953725334627430411> `Жалоба`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
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
                ticket_type = '<:phoenix_text:856563321276071976> `Прочее`'
                ticket_systemname= 'other_discord'
                mainCategory = mainCategory
                channel2 = channel2
                staffrole = staffrole
                await channel2.set_permissions(staffrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(internrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)

                embinfo = embinfo
                emb1 = emb1
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
                        embedth.add_field(name='Модератор:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор:', value=f'<:member:979406123587223562> `{memberop}`')  

                        with open(f"{ticket_systemname}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")   
               
                        await logchannel.send(embed=embedth,file=File(f'{ticket_systemname}.txt'))
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба поддержки Discord.", description=f'Приветствую. \nВаше обращение закрыто сотрудником `{m.author}`. \nВы можете запросить файл с содержанием вашего обращения в течение 3-х дней с момента закрытия обращения. Для этого обратитесь к руководителю проекта `Найт#0550`, предъявив ID вашего обращения. \n\nID:  `{ticket_num}` \nСервер: <:discord:856561477033263124> `Discord`.\nТип обращения: <:serfmoderator:953725334627430411> `Жалоба`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        
                        voprosmembers.remove(memberop.id)
                        os.remove(f'{ticket_systemname}.txt')
                        return
        if inter.component.custom_id == "minecraft_open":
            if memberop.id in voprosmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in voprosmembers:
                chooseemb = discord.Embed(title='Выберите тип обращения Minecraft', color = 0x9cdf39)
                row = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Жалоба',
                        custom_id = 'mc_report',
                        emoji= '<:serfmoderator:953725334627430411>'
                    )
                row3 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Отчёт о баге',
                        custom_id = 'mc_bugreport',
                        emoji= '<:bughunter:979394820122476594>'
                    )
                row4 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Вопрос',
                        custom_id = 'mc_question',
                        emoji= '<:5342discordquestion:979396237558177792>'
                    )
                row5 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Прочее',
                        custom_id = 'mc_other',
                        emoji= '<:phoenix_text:856563321276071976>'
                    )
                view=View()
                view.add_item(row)
                view.add_item(row3)
                view.add_item(row4)
                view.add_item(row5)
                await inter.send(embed=chooseemb, view = view, ephemeral = True)

        if inter.component.custom_id == "mc_report":
            if memberop.id in voprosmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in voprosmembers:
                await inter.send(res, ephemeral = True)
                countervopros += 1
                voprosmembers.append(memberop.id)
                ticket_server = '<:minecraft:856561476873355316> `Minecraft`'
                ticket_type = '<:serfmoderator:953725334627430411> `Жалоба`'
                ticket_systemname= 'report_minecraft'
                mainCategory = mainCategory
                channel2 = channel2
                staffrole = staffrole
                await channel2.set_permissions(staffrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(internrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)

                embinfo = embinfo
                emb1 = emb1
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
                        embedth.add_field(name='Модератор:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор:', value=f'<:member:979406123587223562> `{memberop}`')  

                        with open(f"{ticket_systemname}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")   
               
                        await logchannel.send(embed=embedth,file=File(f'{ticket_systemname}.txt'))
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба поддержки Discord.", description=f'Приветствую. \nВаше обращение закрыто сотрудником `{m.author}`. \nВы можете запросить файл с содержанием вашего обращения в течение 3-х дней с момента закрытия обращения. Для этого обратитесь к руководителю проекта `Найт#0550`, предъявив ID вашего обращения. \n\nID:  `{ticket_num}` \nСервер: <:discord:856561477033263124> `Discord`.\nТип обращения: <:serfmoderator:953725334627430411> `Жалоба`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
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
                ticket_type = '<:bughunter:979394820122476594> `Отчёт о баге`'
                ticket_systemname= 'bugreport_minecraft'
                mainCategory = mainCategory
                channel2 = channel2
                staffrole = staffrole
                await channel2.set_permissions(staffrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(internrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)

                embinfo = embinfo
                emb1 = emb1
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
                        embedth.add_field(name='Модератор:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор:', value=f'<:member:979406123587223562> `{memberop}`')  

                        with open(f"{ticket_systemname}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")   
               
                        await logchannel.send(embed=embedth,file=File(f'{ticket_systemname}.txt'))
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба поддержки Discord.", description=f'Приветствую. \nВаше обращение закрыто сотрудником `{m.author}`. \nВы можете запросить файл с содержанием вашего обращения в течение 3-х дней с момента закрытия обращения. Для этого обратитесь к руководителю проекта `Найт#0550`, предъявив ID вашего обращения. \n\nID:  `{ticket_num}` \nСервер: <:discord:856561477033263124> `Discord`.\nТип обращения: <:serfmoderator:953725334627430411> `Жалоба`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
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
                ticket_type = '<:5342discordquestion:979396237558177792> `Вопрос`'
                ticket_systemname= 'question_minecraft'
                mainCategory = mainCategory
                channel2 = channel2
                staffrole = staffrole
                await channel2.set_permissions(staffrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(internrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)

                embinfo = embinfo
                emb1 = emb1
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
                        embedth.add_field(name='Модератор:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор:', value=f'<:member:979406123587223562> `{memberop}`')  

                        with open(f"{ticket_systemname}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")   
               
                        await logchannel.send(embed=embedth,file=File(f'{ticket_systemname}.txt'))
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба поддержки Discord.", description=f'Приветствую. \nВаше обращение закрыто сотрудником `{m.author}`. \nВы можете запросить файл с содержанием вашего обращения в течение 3-х дней с момента закрытия обращения. Для этого обратитесь к руководителю проекта `Найт#0550`, предъявив ID вашего обращения. \n\nID:  `{ticket_num}` \nСервер: <:discord:856561477033263124> `Discord`.\nТип обращения: <:serfmoderator:953725334627430411> `Жалоба`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
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
                ticket_type = '<:phoenix_text:856563321276071976> `Прочее`'
                ticket_systemname= 'other_minecraft'
                mainCategory = mainCategory
                channel2 = channel2
                staffrole = staffrole
                await channel2.set_permissions(staffrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(internrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)

                embinfo = embinfo
                emb1 = emb1
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
                        embedth.add_field(name='Модератор:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор:', value=f'<:member:979406123587223562> `{memberop}`')  

                        with open(f"{ticket_systemname}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")   
               
                        await logchannel.send(embed=embedth,file=File(f'{ticket_systemname}.txt'))
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба поддержки Discord.", description=f'Приветствую. \nВаше обращение закрыто сотрудником `{m.author}`. \nВы можете запросить файл с содержанием вашего обращения в течение 3-х дней с момента закрытия обращения. Для этого обратитесь к руководителю проекта `Найт#0550`, предъявив ID вашего обращения. \n\nID:  `{ticket_num}` \nСервер: <:discord:856561477033263124> `Discord`.\nТип обращения: <:serfmoderator:953725334627430411> `Жалоба`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        
                        voprosmembers.remove(memberop.id)
                        os.remove(f'{ticket_systemname}.txt')
                        return


        #if inter.component.custom_id == "newguild":
        #    if memberop.id in voprosmembers:
        #        await inter.send(resno, ephemeral = True)
        #        return
        #    if not memberop.id in voprosmembers:
        #        await inter.send(res, ephemeral = True)
        #        countervopros += 1
        #        voprosmembers.append(memberop.id)
        #        mainCategory = discord.utils.get(guild.categories, id=939513361425657947) #ID категории, где будут создаваться тикеты.
        #        channel2 = await guild.create_text_channel(f"ticket {ticket_num}", category = mainCategory)
        #        modrole = discord.utils.get(guild.roles,id=939476433196171324) #ID роли модератора
        #        await channel2.set_permissions(modrole,send_messages=True,read_messages=True,read_message_history=True)
        #        await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
        #        await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)
        #        embinfo = discord.Embed(title='<:info:871310064135327775> Информация об обращении', description=f'**Автор:** <:member:979406123587223562> `{memberop}` \n **ID обращения:** `{ticket_num}` \n\n**Тип обращения:** <:phoenix_plus:953725336061886505> `Создание организации`.', color = 0x2f3136)
        #        emb1 = discord.Embed(title='Добро пожаловать в службу поддержки.', description='Для создания вашей организации, отправьте соообщение по следующей форме заполнения.: \n1) Название организации. \n2) Описание организации. \n3) Эмодзи для кнопки вступления в организацию. \n 4) Цвет роли организации (Форматом HEX). 5) Герб организации (https://minecraft.tools/en/banner.php)', color = 0x2f3136)
        #        nhtrhtrjtremb1 = discord.Embed(title='Когда мне ответят?', description=" Обращения разбираются в порядке очереди. В среднем обращения разбираются от 1 до 3-х часов в рабочие дни с 10:00 по 00:00. В выходные время ответа может быть дольше, но не более 9-ти часов. \n\nЕсли с момента отправки последнего сообщения прошло более 3-х часов, а вам не ответили - можете упомянуть <@&939476433196171324>. \nЕсли прошло более 6-ти часов - упоминайте <@&922561682780332102>.", color = 0x2f3136)
        #        embed3 = discord.Embed(title='', description='<:info:871310064135327775> Обращения закрываются сотрудниками кнопкой ниже.', color = 0x2f3136)
        #        await channel2.send(embed=embinfo)
        #        await channel2.send(embed=emb1)
        #        await channel2.send(embed=nhtrhtrjtremb1)
        #        row = Button(
        #                style = discord.ButtonStyle.grey,
        #                label = 'Закрыть обращение',
        #                custom_id = 'accept_guild',
        #                emoji= '<:blurplelock:856563321321816104>'
        #            )
        #        view2=View()
        #        view2.add_item(row)
        #        msgtic = await channel2.send(embed=embed3, view=view2)
        #        delete = await channel2.send(content = f'{memberop.mention}')
        #        await delete.delete()
        #        def check(m):
        #            return m.message.id == msgtic.id and m.author.guild_permissions.manage_messages == True
        #        try:
        #           m = await self.client.wait_for("button_click", check=check)
        #        except asyncio.TimeoutError:
        #            print("Неизвестная ошибка в коде тикетов") 
        #        else:
        #            if m.component.custom_id == "accept_guild":
        #                embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Обращение закрыто.', colour=0x2f3136)
        #                embedth.add_field(name='ID:', value=f'`{ticket_num}`')
        #                embedth.add_field(name='Тип обращения:', value=f'<:phoenix_plus:953725336061886505> `Создание организации`')
        #                embedth.add_field(name='Модератор:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
        #                embedth.add_field(name='Автор:', value=f'<:member:979406123587223562> `{memberop}`')  
        #                with open(f"newguild.txt", "a", encoding='utf8') as f:
        #                    async for msg12 in channel2.history(limit = 100):
        #                        f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")      
        #                await logchannel.send(embed=embedth,file=File(f'newguild.txt'))
        #                voprosmembers.remove(memberop.id)
        #                await channel2.delete()
        #                clsembed=discord.Embed(title="\📞 Оповещение службы поддержки.", description=f'Приветствую. \nВаше обращение закрыто сотрудником `{m.author}`. \nВы можете запросить файл с содержанием вашего обращения в течение 3-х дней с момента закрытия обращения. Для этого обратитесь к руководителю проекта `Найт#0550`, предъявив ID вашего обращения. \n\nID: `{ticket_num}` \nТип обращения: <:phoenix_plus:953725336061886505> `Создание организации`.', colour = 0x2f3136)
        #                clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
        #                clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
        #                await memberop.send(embed = clsembed)
        #                os.remove(f'newguild.txt')
        #                return     

def setup(client):
    client.add_cog(ButtonClick(client))