import disnake as discord
from disnake.ext import commands
import asyncio
import os
from disnake import File
from disnake.ui import Button, View
import shortuuid
shortuuid.uuid()
guildmembers = []
counterguild = 0

class GuildButtonClick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        guild = self.client.get_guild(inter.guild.id)
        ticket_num = shortuuid.ShortUUID().random(length=6)
        logchannel = self.client.get_channel(939513221046472744) # ID канала с логами.
        res = '<:phoenix_verify:953725334770040953> Обращение создано. Ожидайте пинга в нужном канале.' 
        res2 = '<:phoenix_verify:953725334770040953> Заявка отправлена. Ожидайте уведомления от главы организации.'

        resno = '<:phoenix_warn:953725334736502784> У вас уже есть открытое обращение. Вы не можете открыть обращение, пока предыдущее не будет закрыто.'
        error = '<:phoenix_warn:953725334736502784> Подача заявки в данную организацию временно недоступна или приостановлена.'
        noguild = '<:phoenix_warn:953725334736502784> Вы не являетесь участником данной организации.'
        memberop = inter.author
        if inter.component.custom_id == "error":
            await inter.send(error, ephemeral = True)


        if inter.component.custom_id == "guild2":
            if memberop.id in guildmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:
                chooseemb = discord.Embed(title='Выберите тип заявки', color = 0x2f3136)
                row = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Вступление в организацию',
                        custom_id = 'enter_guild_2',
                        emoji= '<:enter:991308332906328125>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Выход из организации',
                        custom_id = 'exit_guild_2',
                        emoji= '<:exit:991308335506784276>'
                    )
                view=View()
                view.add_item(row)
                view.add_item(row2)
                await inter.send(embed=chooseemb, view = view, ephemeral = True)

        if inter.component.custom_id == "enter_guild_2":
            if memberop.id in guildmembers:
                resno = '<:phoenix_warn:953725334736502784> У вас уже есть открытое обращение. Вы не можете открыть новое обращение, пока предыдущее не будет закрыто.'
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:
                global counterguild

                name = ':flag_jp:  `НСВС`'
                ticket_name = 'japan'
                guildownerid = '755815621958172792'
                guildroleid = '1045186866430881802'

                await inter.send(res, ephemeral = True)
                counterguild += 1
                guildmembers.append(memberop.id)
                mainCategory = discord.utils.get(guild.categories, id=939513361425657947) #ID категории, где будут создаваться тикеты.
                channel2 = await guild.create_text_channel(f"ticket {ticket_num}", category = mainCategory)
                modrole = await self.client.fetch_user(int(guildownerid))
                await channel2.set_permissions(modrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)
                embinfo = discord.Embed(title='Информация об обращении', description=f'**Автор:** <:member:979406123587223562> `{memberop}` \n **ID обращения:** `{ticket_num}` \n\n**Тип обращения:** <:guild:991309617420304465> `Вступление в организацию` \n**Организация:** {name}', color = 0x2f3136)
                emb1 = discord.Embed(title='Добро пожаловать в службу организаций.', description='Заполните заявку по следующей форме: \n1) Ваш никнейм на сервере. \n2) Количество наигранных часов\n 3)Почему вы решили вступить в данную организацию.', color = 0x2f3136)
                nhtrhtrjtremb1 = discord.Embed(title='Когда мне ответят?', description="Время рассмотрения заявки зависит от главы организации, но обычно заявки рассматриваются в течение дня.", color = 0x2f3136)
                embed3 = discord.Embed(title='', description='<:info:871310064135327775> Заявки на вступление рассматриваются главой организации с помощью кнопок ниже.', color = 0x2f3136)
                await channel2.send(embed=embinfo)
                await channel2.send(embed=emb1)
                await channel2.send(embed=nhtrhtrjtremb1)
                row = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Одобрить заявку',
                        custom_id = 'accept_guild2',
                        emoji= '<:discordcheck:954092021084196904>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Отклонить заявку',
                        custom_id = 'deny_guild2',
                        emoji= '<:discordcross:954092020882870312>'
                    )
                view2=View()
                view2.add_item(row)
                view2.add_item(row2)
                msgtic = await channel2.send(embed=embed3, view=view2)
                delete = await channel2.send(content = f'{memberop.mention}')
                await delete.delete()
                def check(m):
                    return m.message.id == msgtic.id and m.author.id == int(guildownerid)
                try:
                   m = await self.client.wait_for("button_click", check=check)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде тикетов") 
                else:
                    if m.component.custom_id == f"accept_guild2":
                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Вступление в организацию одобрено.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Организация:', value=f'{name}')
                        embedth.add_field(name='Одорбил заявку:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор заявки:', value=f'<:member:979406123587223562> `{memberop}`')  
                        with open(f"guild_{ticket_name}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")      
                        await logchannel.send(embed=embedth,file=File(f'guild_{ticket_name}.txt'))
                        guildmembers.remove(memberop.id)
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба организаций.", description=f'Ваша заявка на вступление в организацию {name} одобрена главой организации `{m.author}`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        role = discord.utils.get(guild.roles,id=int(guildroleid)) 
                        await memberop.add_roles(role)
                        os.remove(f'guild_{ticket_name}.txt')
                        return
                    if m.component.custom_id == f"deny_guild2":
                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Вступление в организацию отклонено.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Организация:', value=f'{name}')
                        embedth.add_field(name='Отклонил заявку:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор заявки:', value=f'<:member:979406123587223562> `{memberop}`')  
                        with open(f"guild_{ticket_name}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")      
                        await logchannel.send(embed=embedth,file=File(f'guild_{ticket_name}.txt'))
                        guildmembers.remove(memberop.id)
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба организаций.", description=f'Ваша заявка на вступление в организацию {name} отклонена главой организации `{m.author}`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        os.remove(f'guild_{ticket_name}.txt')
                        return
        if inter.component.custom_id == f"exit_guild_2":
            role = discord.utils.get(guild.roles,id=int(guildroleid)) 
            name = ':flag_jp:  `НСВС`'
            ticket_name = 'japan'
            guildownerid = '755815621958172792'
            guildroleid = '1045186866430881802'

            if role in memberop.roles:
                await inter.send(res2, ephemeral = True)
                embed = discord.Embed(title='Игрок покинул вашу организацию.', description=f'Игрок: {memberop} \nОрганизация: {name}.', color = 0x2f3136)
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/991308335506784276.webp?size=96&quality=lossless")
                embed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                phoenix = await self.client.fetch_user(int(guildownerid))
                memberop.remove_roles(role)
                await phoenix.send(embed=embed)
                await logchannel.send(embed=embed)
            else:
                await inter.send(noguild, ephemeral = True)

        if inter.component.custom_id == "guild3":
            if memberop.id in guildmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:
                chooseemb = discord.Embed(title='Выберите тип заявки', color = 0x2f3136)
                row = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Вступление в организацию',
                        custom_id = 'enter_guild_3',
                        emoji= '<:enter:991308332906328125>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Выход из организации',
                        custom_id = 'exit_guild_3',
                        emoji= '<:exit:991308335506784276>'
                    )
                view=View()
                view.add_item(row)
                view.add_item(row2)
                await inter.send(embed=chooseemb, view = view, ephemeral = True)

        if inter.component.custom_id == "enter_guild_3":
            if memberop.id in guildmembers:
                resno = '<:phoenix_warn:953725334736502784> У вас уже есть открытое обращение. Вы не можете открыть новое обращение, пока предыдущее не будет закрыто.'
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:
                name = '🗺️ `Авиньон`'
                ticket_name = 'avignon'
                guildownerid = '585492782827831326'
                guildroleid = '1080414446666645548'

                await inter.send(res, ephemeral = True)
                counterguild += 1
                guildmembers.append(memberop.id)
                mainCategory = discord.utils.get(guild.categories, id=939513361425657947) #ID категории, где будут создаваться тикеты.
                channel2 = await guild.create_text_channel(f"ticket {ticket_num}", category = mainCategory)
                modrole = await self.client.fetch_user(int(guildownerid))
                await channel2.set_permissions(modrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)
                embinfo = discord.Embed(title='Информация об обращении', description=f'**Автор:** <:member:979406123587223562> `{memberop}` \n **ID обращения:** `{ticket_num}` \n\n**Тип обращения:** <:guild:991309617420304465> `Вступление в организацию` \n**Организация:** {name}', color = 0x2f3136)
                emb1 = discord.Embed(title='Добро пожаловать в службу организаций.', description='Заполните заявку по следующей форме: \n1) Ваш никнейм на сервере. \n2) Количество наигранных часов\n 3)Почему вы решили вступить в данную организацию.', color = 0x2f3136)
                nhtrhtrjtremb1 = discord.Embed(title='Когда мне ответят?', description="Время рассмотрения заявки зависит от главы организации, но обычно заявки рассматриваются в течение дня.", color = 0x2f3136)
                embed3 = discord.Embed(title='', description='<:info:871310064135327775> Заявки на вступление рассматриваются главой организации с помощью кнопок ниже.', color = 0x2f3136)
                await channel2.send(embed=embinfo)
                await channel2.send(embed=emb1)
                await channel2.send(embed=nhtrhtrjtremb1)
                row = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Одобрить заявку',
                        custom_id = 'accept_guild3',
                        emoji= '<:discordcheck:954092021084196904>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Отклонить заявку',
                        custom_id = 'deny_guild3',
                        emoji= '<:discordcross:954092020882870312>'
                    )
                view2=View()
                view2.add_item(row)
                view2.add_item(row2)
                msgtic = await channel2.send(embed=embed3, view=view2)
                delete = await channel2.send(content = f'{memberop.mention}')
                await delete.delete()
                def check(m):
                    return m.message.id == msgtic.id and m.author.id == int(guildownerid)
                try:
                   m = await self.client.wait_for("button_click", check=check)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде тикетов") 
                else:
                    if m.component.custom_id == f"accept_guild3":
                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Вступление в организацию одобрено.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Организация:', value=f'{name}')
                        embedth.add_field(name='Одорбил заявку:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор заявки:', value=f'<:member:979406123587223562> `{memberop}`')  
                        with open(f"guild_{ticket_name}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")      
                        await logchannel.send(embed=embedth,file=File(f'guild_{ticket_name}.txt'))
                        guildmembers.remove(memberop.id)
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба организаций.", description=f'Ваша заявка на вступление в организацию {name} одобрена главой организации `{m.author}`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        role = discord.utils.get(guild.roles,id=int(guildroleid)) 
                        await memberop.add_roles(role)
                        os.remove(f'guild_{ticket_name}.txt')
                        return
                    if m.component.custom_id == f"deny_guild3":
                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Вступление в организацию отклонено.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Организация:', value=f'{name}')
                        embedth.add_field(name='Отклонил заявку:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор заявки:', value=f'<:member:979406123587223562> `{memberop}`')  
                        with open(f"guild_{ticket_name}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")      
                        await logchannel.send(embed=embedth,file=File(f'guild_{ticket_name}.txt'))
                        guildmembers.remove(memberop.id)
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба организаций.", description=f'Ваша заявка на вступление в организацию {name} отклонена главой организации `{m.author}`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        os.remove(f'guild_{ticket_name}.txt')
                        return
        if inter.component.custom_id == f"exit_guild_3":
            name = '🗺️ `Авиньон`'
            ticket_name = 'avignon'
            guildownerid = '585492782827831326'
            guildroleid = '1080414446666645548'

            if role in memberop.roles:
                await inter.send(res2, ephemeral = True)
                embed = discord.Embed(title='Игрок покинул вашу организацию.', description=f'Игрок: {memberop} \nОрганизация: {name}.', color = 0x2f3136)
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/991308335506784276.webp?size=96&quality=lossless")
                embed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                phoenix = await self.client.fetch_user(int(guildownerid))
                memberop.remove_roles(role)
                await phoenix.send(embed=embed)
                await logchannel.send(embed=embed)
            else:
                await inter.send(noguild, ephemeral = True)

        if inter.component.custom_id == "guild4":
            if memberop.id in guildmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:
                chooseemb = discord.Embed(title='Выберите тип заявки', color = 0x2f3136)
                row = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Вступление в организацию',
                        custom_id = 'enter_guild_4',
                        emoji= '<:enter:991308332906328125>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Выход из организации',
                        custom_id = 'exit_guild_4',
                        emoji= '<:exit:991308335506784276>'
                    )
                view=View()
                view.add_item(row)
                view.add_item(row2)
                await inter.send(embed=chooseemb, view = view, ephemeral = True)

        if inter.component.custom_id == "enter_guild_4":
            if memberop.id in guildmembers:
                resno = '<:phoenix_warn:953725334736502784> У вас уже есть открытое обращение. Вы не можете открыть новое обращение, пока предыдущее не будет закрыто.'
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:
                name = '🏝 `Oasis`'
                ticket_name = 'oasis'
                guildownerid = '781169776277585951'
                guildroleid = '1052591259698593863'

                await inter.send(res, ephemeral = True)
                counterguild += 1
                guildmembers.append(memberop.id)
                mainCategory = discord.utils.get(guild.categories, id=939513361425657947) #ID категории, где будут создаваться тикеты.
                channel2 = await guild.create_text_channel(f"ticket {ticket_num}", category = mainCategory)
                modrole = await self.client.fetch_user(int(guildownerid))
                await channel2.set_permissions(modrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)
                embinfo = discord.Embed(title='Информация об обращении', description=f'**Автор:** <:member:979406123587223562> `{memberop}` \n **ID обращения:** `{ticket_num}` \n\n**Тип обращения:** <:guild:991309617420304465> `Вступление в организацию` \n**Организация:** {name}', color = 0x2f3136)
                emb1 = discord.Embed(title='Добро пожаловать в службу организаций.', description='Заполните заявку по следующей форме: \n1) Ваш никнейм на сервере. \n2) Количество наигранных часов\n 3)Почему вы решили вступить в данную организацию.', color = 0x2f3136)
                nhtrhtrjtremb1 = discord.Embed(title='Когда мне ответят?', description="Время рассмотрения заявки зависит от главы организации, но обычно заявки рассматриваются в течение дня.", color = 0x2f3136)
                embed3 = discord.Embed(title='', description='<:info:871310064135327775> Заявки на вступление рассматриваются главой организации с помощью кнопок ниже.', color = 0x2f3136)
                await channel2.send(embed=embinfo)
                await channel2.send(embed=emb1)
                await channel2.send(embed=nhtrhtrjtremb1)
                row = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Одобрить заявку',
                        custom_id = 'accept_guild4',
                        emoji= '<:discordcheck:954092021084196904>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Отклонить заявку',
                        custom_id = 'deny_guild4',
                        emoji= '<:discordcross:954092020882870312>'
                    )
                view2=View()
                view2.add_item(row)
                view2.add_item(row2)
                msgtic = await channel2.send(embed=embed3, view=view2)
                delete = await channel2.send(content = f'{memberop.mention}')
                await delete.delete()
                def check(m):
                    return m.message.id == msgtic.id and m.author.id == int(guildownerid)
                try:
                   m = await self.client.wait_for("button_click", check=check)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде тикетов") 
                else:
                    if m.component.custom_id == f"accept_guild4":
                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Вступление в организацию одобрено.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Организация:', value=f'{name}')
                        embedth.add_field(name='Одорбил заявку:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор заявки:', value=f'<:member:979406123587223562> `{memberop}`')  
                        with open(f"guild_{ticket_name}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")      
                        await logchannel.send(embed=embedth,file=File(f'guild_{ticket_name}.txt'))
                        guildmembers.remove(memberop.id)
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба организаций.", description=f'Ваша заявка на вступление в организацию {name} одобрена главой организации `{m.author}`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        role = discord.utils.get(guild.roles,id=int(guildroleid)) 
                        await memberop.add_roles(role)
                        os.remove(f'guild_{ticket_name}.txt')
                        return
                    if m.component.custom_id == f"deny_guild4":
                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Вступление в организацию отклонено.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Организация:', value=f'{name}')
                        embedth.add_field(name='Отклонил заявку:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор заявки:', value=f'<:member:979406123587223562> `{memberop}`')  
                        with open(f"guild_{ticket_name}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")      
                        await logchannel.send(embed=embedth,file=File(f'guild_{ticket_name}.txt'))
                        guildmembers.remove(memberop.id)
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба организаций.", description=f'Ваша заявка на вступление в организацию {name} отклонена главой организации `{m.author}`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        os.remove(f'guild_{ticket_name}.txt')
                        return
        if inter.component.custom_id == f"exit_guild_4":
            name = '🏝 `Oasis`'
            ticket_name = 'oasis'
            guildownerid = '781169776277585951'
            guildroleid = '1052591259698593863'

            if role in memberop.roles:
                await inter.send(res2, ephemeral = True)
                embed = discord.Embed(title='Игрок покинул вашу организацию.', description=f'Игрок: {memberop} \nОрганизация: {name}.', color = 0x2f3136)
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/991308335506784276.webp?size=96&quality=lossless")
                embed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                phoenix = await self.client.fetch_user(int(guildownerid))
                memberop.remove_roles(role)
                await phoenix.send(embed=embed)
                await logchannel.send(embed=embed)
            else:
                await inter.send(noguild, ephemeral = True)

        if inter.component.custom_id == "guild5":
            if memberop.id in guildmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:
                chooseemb = discord.Embed(title='Выберите тип заявки', color = 0x2f3136)
                row = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Вступление в организацию',
                        custom_id = 'enter_guild_5',
                        emoji= '<:enter:991308332906328125>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Выход из организации',
                        custom_id = 'exit_guild_5',
                        emoji= '<:exit:991308335506784276>'
                    )
                view=View()
                view.add_item(row)
                view.add_item(row2)
                await inter.send(embed=chooseemb, view = view, ephemeral = True)

        if inter.component.custom_id == "enter_guild_5":
            if memberop.id in guildmembers:
                resno = '<:phoenix_warn:953725334736502784> У вас уже есть открытое обращение. Вы не можете открыть новое обращение, пока предыдущее не будет закрыто.'
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:
                name = '<:woke:1007310533952798790> `Головорезы`'
                ticket_name = 'hunters'
                guildownerid = '1020378345298468914'
                guildroleid = '1062670679675240470'

                await inter.send(res, ephemeral = True)
                counterguild += 1
                guildmembers.append(memberop.id)
                mainCategory = discord.utils.get(guild.categories, id=939513361425657947) #ID категории, где будут создаваться тикеты.
                channel2 = await guild.create_text_channel(f"ticket {ticket_num}", category = mainCategory)
                modrole = await self.client.fetch_user(int(guildownerid))
                await channel2.set_permissions(modrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)
                embinfo = discord.Embed(title='Информация об обращении', description=f'**Автор:** <:member:979406123587223562> `{memberop}` \n **ID обращения:** `{ticket_num}` \n\n**Тип обращения:** <:guild:991309617420304465> `Вступление в организацию` \n**Организация:** {name}', color = 0x2f3136)
                emb1 = discord.Embed(title='Добро пожаловать в службу организаций.', description='Заполните заявку по следующей форме: \n1) Ваш никнейм на сервере. \n2) Количество наигранных часов\n 3)Почему вы решили вступить в данную организацию.', color = 0x2f3136)
                nhtrhtrjtremb1 = discord.Embed(title='Когда мне ответят?', description="Время рассмотрения заявки зависит от главы организации, но обычно заявки рассматриваются в течение дня.", color = 0x2f3136)
                embed3 = discord.Embed(title='', description='<:info:871310064135327775> Заявки на вступление рассматриваются главой организации с помощью кнопок ниже.', color = 0x2f3136)
                await channel2.send(embed=embinfo)
                await channel2.send(embed=emb1)
                await channel2.send(embed=nhtrhtrjtremb1)
                row = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Одобрить заявку',
                        custom_id = 'accept_guild5',
                        emoji= '<:discordcheck:954092021084196904>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Отклонить заявку',
                        custom_id = 'deny_guild5',
                        emoji= '<:discordcross:954092020882870312>'
                    )
                view2=View()
                view2.add_item(row)
                view2.add_item(row2)
                msgtic = await channel2.send(embed=embed3, view=view2)
                delete = await channel2.send(content = f'{memberop.mention}')
                await delete.delete()
                def check(m):
                    return m.message.id == msgtic.id and m.author.id == int(guildownerid)
                try:
                   m = await self.client.wait_for("button_click", check=check)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде тикетов") 
                else:
                    if m.component.custom_id == f"accept_guild5":
                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Вступление в организацию одобрено.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Организация:', value=f'{name}')
                        embedth.add_field(name='Одорбил заявку:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор заявки:', value=f'<:member:979406123587223562> `{memberop}`')  
                        with open(f"guild_{ticket_name}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")      
                        await logchannel.send(embed=embedth,file=File(f'guild_{ticket_name}.txt'))
                        guildmembers.remove(memberop.id)
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба организаций.", description=f'Ваша заявка на вступление в организацию {name} одобрена главой организации `{m.author}`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        role = discord.utils.get(guild.roles,id=int(guildroleid)) 
                        await memberop.add_roles(role)
                        os.remove(f'guild_{ticket_name}.txt')
                        return
                    if m.component.custom_id == f"deny_guild5":
                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Вступление в организацию отклонено.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Организация:', value=f'{name}')
                        embedth.add_field(name='Отклонил заявку:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор заявки:', value=f'<:member:979406123587223562> `{memberop}`')  
                        with open(f"guild_{ticket_name}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")      
                        await logchannel.send(embed=embedth,file=File(f'guild_{ticket_name}.txt'))
                        guildmembers.remove(memberop.id)
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба организаций.", description=f'Ваша заявка на вступление в организацию {name} отклонена главой организации `{m.author}`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        os.remove(f'guild_{ticket_name}.txt')
                        return
        if inter.component.custom_id == f"exit_guild_5":
            name = '<:woke:1007310533952798790> `Головорезы`'
            ticket_name = 'hunters'
            guildownerid = '1020378345298468914'
            guildroleid = '1062670679675240470'

            if role in memberop.roles:
                await inter.send(res2, ephemeral = True)
                embed = discord.Embed(title='Игрок покинул вашу организацию.', description=f'Игрок: {memberop} \nОрганизация: {name}.', color = 0x2f3136)
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/991308335506784276.webp?size=96&quality=lossless")
                embed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                phoenix = await self.client.fetch_user(int(guildownerid))
                memberop.remove_roles(role)
                await phoenix.send(embed=embed)
                await logchannel.send(embed=embed)
            else:
                await inter.send(noguild, ephemeral = True)

        if inter.component.custom_id == "guild6":
            if memberop.id in guildmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:
                chooseemb = discord.Embed(title='Выберите тип заявки', color = 0x2f3136)
                row = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Вступление в организацию',
                        custom_id = 'enter_guild_6',
                        emoji= '<:enter:991308332906328125>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Выход из организации',
                        custom_id = 'exit_guild_6',
                        emoji= '<:exit:991308335506784276>'
                    )
                view=View()
                view.add_item(row)
                view.add_item(row2)
                await inter.send(embed=chooseemb, view = view, ephemeral = True)

        if inter.component.custom_id == "enter_guild_6":
            if memberop.id in guildmembers:
                resno = '<:phoenix_warn:953725334736502784> У вас уже есть открытое обращение. Вы не можете открыть новое обращение, пока предыдущее не будет закрыто.'
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:
                name = '<:bruh:1056963324169949214> `Black Diamond`'
                ticket_name = 'blackdiamond'
                guildownerid = '699193462276358204'
                guildroleid = '1072879748541321266'

                await inter.send(res, ephemeral = True)
                counterguild += 1
                guildmembers.append(memberop.id)
                mainCategory = discord.utils.get(guild.categories, id=939513361425657947) #ID категории, где будут создаваться тикеты.
                channel2 = await guild.create_text_channel(f"ticket {ticket_num}", category = mainCategory)
                modrole = await self.client.fetch_user(int(guildownerid))
                await channel2.set_permissions(modrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)
                embinfo = discord.Embed(title='Информация об обращении', description=f'**Автор:** <:member:979406123587223562> `{memberop}` \n **ID обращения:** `{ticket_num}` \n\n**Тип обращения:** <:guild:991309617420304465> `Вступление в организацию` \n**Организация:** {name}', color = 0x2f3136)
                emb1 = discord.Embed(title='Добро пожаловать в службу организаций.', description='Заполните заявку по следующей форме: \n1) Ваш никнейм на сервере. \n2) Количество наигранных часов\n 3)Почему вы решили вступить в данную организацию.', color = 0x2f3136)
                nhtrhtrjtremb1 = discord.Embed(title='Когда мне ответят?', description="Время рассмотрения заявки зависит от главы организации, но обычно заявки рассматриваются в течение дня.", color = 0x2f3136)
                embed3 = discord.Embed(title='', description='<:info:871310064135327775> Заявки на вступление рассматриваются главой организации с помощью кнопок ниже.', color = 0x2f3136)
                await channel2.send(embed=embinfo)
                await channel2.send(embed=emb1)
                await channel2.send(embed=nhtrhtrjtremb1)
                row = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Одобрить заявку',
                        custom_id = 'accept_guild6',
                        emoji= '<:discordcheck:954092021084196904>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Отклонить заявку',
                        custom_id = 'deny_guild6',
                        emoji= '<:discordcross:954092020882870312>'
                    )
                view2=View()
                view2.add_item(row)
                view2.add_item(row2)
                msgtic = await channel2.send(embed=embed3, view=view2)
                delete = await channel2.send(content = f'{memberop.mention}')
                await delete.delete()
                def check(m):
                    return m.message.id == msgtic.id and m.author.id == int(guildownerid)
                try:
                   m = await self.client.wait_for("button_click", check=check)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде тикетов") 
                else:
                    if m.component.custom_id == f"accept_guild6":
                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Вступление в организацию одобрено.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Организация:', value=f'{name}')
                        embedth.add_field(name='Одорбил заявку:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор заявки:', value=f'<:member:979406123587223562> `{memberop}`')  
                        with open(f"guild_{ticket_name}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")      
                        await logchannel.send(embed=embedth,file=File(f'guild_{ticket_name}.txt'))
                        guildmembers.remove(memberop.id)
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба организаций.", description=f'Ваша заявка на вступление в организацию {name} одобрена главой организации `{m.author}`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        role = discord.utils.get(guild.roles,id=int(guildroleid)) 
                        await memberop.add_roles(role)
                        os.remove(f'guild_{ticket_name}.txt')
                        return
                    if m.component.custom_id == f"deny_guild6":
                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Вступление в организацию отклонено.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Организация:', value=f'{name}')
                        embedth.add_field(name='Отклонил заявку:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор заявки:', value=f'<:member:979406123587223562> `{memberop}`')  
                        with open(f"guild_{ticket_name}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")      
                        await logchannel.send(embed=embedth,file=File(f'guild_{ticket_name}.txt'))
                        guildmembers.remove(memberop.id)
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба организаций.", description=f'Ваша заявка на вступление в организацию {name} отклонена главой организации `{m.author}`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        os.remove(f'guild_{ticket_name}.txt')
                        return
        if inter.component.custom_id == f"exit_guild_6":
            name = '<:bruh:1056963324169949214> `Black Diamond`'
            ticket_name = 'blackdiamond'
            guildownerid = '699193462276358204'
            guildroleid = '1072879748541321266'

            if role in memberop.roles:
                await inter.send(res2, ephemeral = True)
                embed = discord.Embed(title='Игрок покинул вашу организацию.', description=f'Игрок: {memberop} \nОрганизация: {name}.', color = 0x2f3136)
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/991308335506784276.webp?size=96&quality=lossless")
                embed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                phoenix = await self.client.fetch_user(int(guildownerid))
                memberop.remove_roles(role)
                await phoenix.send(embed=embed)
                await logchannel.send(embed=embed)
            else:
                await inter.send(noguild, ephemeral = True)     

        if inter.component.custom_id == "guild7":
            if memberop.id in guildmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:
                chooseemb = discord.Embed(title='Выберите тип заявки', color = 0x2f3136)
                row = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Вступление в организацию',
                        custom_id = 'enter_guild_7',
                        emoji= '<:enter:991308332906328125>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Выход из организации',
                        custom_id = 'exit_guild_7',
                        emoji= '<:exit:991308335506784276>'
                    )
                view=View()
                view.add_item(row)
                view.add_item(row2)
                await inter.send(embed=chooseemb, view = view, ephemeral = True)

        if inter.component.custom_id == "enter_guild_7":
            if memberop.id in guildmembers:
                resno = '<:phoenix_warn:953725334736502784> У вас уже есть открытое обращение. Вы не можете открыть новое обращение, пока предыдущее не будет закрыто.'
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:
                name = '<:crosspeepo:939579485114744853> `Древняя Русь`'
                ticket_name = 'oldrussia'
                guildownerid = '685528401930485781'
                guildroleid = '1088062069015842816'
                await inter.send(res, ephemeral = True) 
                counterguild += 1
                guildmembers.append(memberop.id)
                mainCategory = discord.utils.get(guild.categories, id=939513361425657947) #ID категории, где будут создаваться тикеты.
                channel2 = await guild.create_text_channel(f"ticket {ticket_num}", category = mainCategory)
                modrole = await self.client.fetch_user(int(guildownerid))
                await channel2.set_permissions(modrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)
                embinfo = discord.Embed(title='Информация об обращении', description=f'**Автор:** <:member:979406123587223562> `{memberop}` \n **ID обращения:** `{ticket_num}` \n\n**Тип обращения:** <:guild:991309617420304465> `Вступление в организацию` \n**Организация:** {name}', color = 0x2f3136)
                emb1 = discord.Embed(title='Добро пожаловать в службу организаций.', description='Заполните заявку по следующей форме: \n1) Ваш никнейм на сервере. \n2) Количество наигранных часов\n 3)Почему вы решили вступить в данную организацию.', color = 0x2f3136)
                nhtrhtrjtremb1 = discord.Embed(title='Когда мне ответят?', description="Время рассмотрения заявки зависит от главы организации, но обычно заявки рассматриваются в течение дня.", color = 0x2f3136)
                embed3 = discord.Embed(title='', description='<:info:871310064135327775> Заявки на вступление рассматриваются главой организации с помощью кнопок ниже.', color = 0x2f3136)
                await channel2.send(embed=embinfo)
                await channel2.send(embed=emb1)
                await channel2.send(embed=nhtrhtrjtremb1)
                row = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Одобрить заявку',
                        custom_id = 'accept_guild7',
                        emoji= '<:discordcheck:954092021084196904>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Отклонить заявку',
                        custom_id = 'deny_guild7',
                        emoji= '<:discordcross:954092020882870312>'
                    )
                view2=View()
                view2.add_item(row)
                view2.add_item(row2)
                msgtic = await channel2.send(embed=embed3, view=view2)
                delete = await channel2.send(content = f'{memberop.mention}')
                await delete.delete()
                def check(m):
                    return m.message.id == msgtic.id and m.author.id == int(guildownerid)
                try:
                   m = await self.client.wait_for("button_click", check=check)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде тикетов") 
                else:
                    if m.component.custom_id == f"accept_guild7":
                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Вступление в организацию одобрено.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Организация:', value=f'{name}')
                        embedth.add_field(name='Одорбил заявку:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор заявки:', value=f'<:member:979406123587223562> `{memberop}`')  
                        with open(f"guild_{ticket_name}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")      
                        await logchannel.send(embed=embedth,file=File(f'guild_{ticket_name}.txt'))
                        guildmembers.remove(memberop.id)
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба организаций.", description=f'Ваша заявка на вступление в организацию {name} одобрена главой организации `{m.author}`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        role = discord.utils.get(guild.roles,id=int(guildroleid)) 
                        await memberop.add_roles(role)
                        os.remove(f'guild_{ticket_name}.txt')
                        return
                    if m.component.custom_id == f"deny_guild7":
                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Вступление в организацию отклонено.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Организация:', value=f'{name}')
                        embedth.add_field(name='Отклонил заявку:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор заявки:', value=f'<:member:979406123587223562> `{memberop}`')  
                        with open(f"guild_{ticket_name}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")      
                        await logchannel.send(embed=embedth,file=File(f'guild_{ticket_name}.txt'))
                        guildmembers.remove(memberop.id)
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба организаций.", description=f'Ваша заявка на вступление в организацию {name} отклонена главой организации `{m.author}`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        os.remove(f'guild_{ticket_name}.txt')
                        return
        if inter.component.custom_id == f"exit_guild_7":
            name = '<:crosspeepo:939579485114744853> `Древняя Русь`'
            ticket_name = 'oldrussia'
            guildownerid = '685528401930485781'
            guildroleid = '1088062069015842816'

            if role in memberop.roles:
                await inter.send(res2, ephemeral = True)
                embed = discord.Embed(title='Игрок покинул вашу организацию.', description=f'Игрок: {memberop} \nОрганизация: {name}.', color = 0x2f3136)
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/991308335506784276.webp?size=96&quality=lossless")
                embed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                phoenix = await self.client.fetch_user(int(guildownerid))
                memberop.remove_roles(role)
                await phoenix.send(embed=embed)
                await logchannel.send(embed=embed)
            else:
                await inter.send(noguild, ephemeral = True)    

def setup(client):
    client.add_cog(GuildButtonClick(client))