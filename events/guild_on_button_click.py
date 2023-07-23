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
        #Техническая информация
        memberop = inter.author
        guild = self.client.get_guild(inter.guild.id)
        ticket_num = shortuuid.ShortUUID().random(length=6)
        logchannel = self.client.get_channel(939513221046472744) # ID канала с логами.
        mainCategory = discord.utils.get(guild.categories, id=939513361425657947)

        japanroleid = '1045186866430881802'
        rolejapan = discord.utils.get(guild.roles,id=int(japanroleid))

        #Текстовая информация
        res = '<:minecraft_accept:1080779491875491882> Заявка отправлена. Ожидайте уведомления в открытом канале.'
        resno = '<:minecraft_deny:1080779495386140684> У вас уже есть открытая заявка в одну из организаций. Вы не можете открыть новую заявку, пока предыдущая не будет закрыта.'
        error = '<:minecraft_deny:1080779495386140684> Подача заявки в данную организацию временно недоступна.'
        noguild = '<:minecraft_deny:1080779495386140684> Вы не являетесь участником данной организации.'
        alreadyguild = '<:minecraft_deny:1080779495386140684> Вы уже состоите в другой организации.'
        alreadythisguild = '<:minecraft_deny:1080779495386140684> Вы уже состоите в данной организации.'
        emb1 = discord.Embed(title='Добро пожаловать в службу организаций', description='Заполните заявку по следующей форме: \n1) Ваш никнейм на сервере. \n2) Количество наигранных часов\n 3)Почему вы решили вступить в данную организацию.', color = 0x2f3136)
        nhtrhtrjtremb1 = discord.Embed(title='Когда мне ответят?', description="Время рассмотрения заявки зависит от главы организации, но обычно заявки рассматриваются в течение дня.", color = 0x2f3136)
        embed3 = discord.Embed(title='', description='<:info:871310064135327775> Заявки на вступление рассматриваются главой организации с помощью кнопок ниже.', color = 0x2f3136)

        if inter.component.custom_id == "error":
            await inter.send(error, ephemeral = True)
            
        if inter.component.custom_id == "japan":
            if memberop.id in guildmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:
                chooseemb = discord.Embed(title='Выберите тип заявки', color = 0x2f3136)
                row = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Вступление в организацию',
                        custom_id = 'enter_japan',
                        emoji= '<:enter:991308332906328125>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Выход из организации',
                        custom_id = 'exit_japan',
                        emoji= '<:exit:991308335506784276>'
                    )
                view=View()
                view.add_item(row)
                view.add_item(row2)
                await inter.send(embed=chooseemb, view = view, ephemeral = True)

        if inter.component.custom_id == "enter_japan":
            name = ':flag_jp:  `Япония`'
            ticket_name = 'japan'
            guildownerid = '755815621958172792'
            guildroleid = '1045186866430881802'

            if memberop.id in guildmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:

                if rolejapan in memberop.roles:
                    await inter.send(alreadythisguild, ephemeral = True) 
                else:
                    await inter.send(res, ephemeral = True)
                    global counterguild

                    counterguild += 1
                    guildmembers.append(memberop.id)
                    owner = await self.client.fetch_user(int(guildownerid))
                    channel2 = await guild.create_text_channel(f"guildjoin {ticket_num}", category = mainCategory)
                    embinfo = discord.Embed(title='Информация об обращении', description=f'**Автор:** <:member:979406123587223562> `{memberop}` \n **ID обращения:** `{ticket_num}` \n\n**Тип обращения:** <:blurplecertifiedmoderator:856563321541230602> `Вступление в организацию` \n**Организация:** {name}', color = 0x2f3136)
                    await channel2.set_permissions(owner,send_messages=True,read_messages=True,read_message_history=True)
                    await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                    await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)
                    await channel2.send(embed=embinfo)
                    await channel2.send(embed=emb1)
                    await channel2.send(embed=nhtrhtrjtremb1)
                    row = Button(
                            style = discord.ButtonStyle.grey,
                            label = 'Одобрить заявку',
                            custom_id = 'accept_japan',
                            emoji= '<:minecraft_accept:1080779491875491882>'
                        )
                    row2 = Button(
                            style = discord.ButtonStyle.grey,
                            label = 'Отклонить заявку',
                            custom_id = 'deny_japan',
                            emoji= '<:minecraft_deny:1080779495386140684>'
                        )
                    view2=View()
                    view2.add_item(row)
                    view2.add_item(row2)
                    msgtic = await channel2.send(embed=embed3, view=view2)
                    delete = await channel2.send(content = f'{memberop.mention} {owner.mention}')
                    await delete.delete()
                    def check(m):
                        return m.message.id == msgtic.id and m.author.id == int(guildownerid)
                    try:
                       m = await self.client.wait_for("button_click", check=check)
                    except asyncio.TimeoutError:
                        print("Неизвестная ошибка в коде тикетов") 
                    else:
                        if m.component.custom_id == f"accept_japan":
                            embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Вступление в организацию одобрено', colour=0x2f3136)
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
                            clsembed=discord.Embed(title="📞 Ответ от организации \"Япония\"", description=f'Ваша заявка на вступление в организацию {name} одобрена главой организации `{m.author}`.', colour = 0x2f3136)
                            clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                            clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                            await memberop.send(embed = clsembed)
                            await memberop.add_roles(rolejapan)
                            os.remove(f'guild_{ticket_name}.txt')
                            return
                        if m.component.custom_id == f"deny_japan":
                            embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Вступление в организацию отклонено', colour=0x2f3136)
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
                            clsembed=discord.Embed(title="📞 Ответ от организации \"Япония\"", description=f'Ваша заявка на вступление в организацию {name} отклонена главой организации `{m.author}`.', colour = 0x2f3136)
                            clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                            clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                            await memberop.send(embed = clsembed)
                            os.remove(f'guild_{ticket_name}.txt')
                            return
        if inter.component.custom_id == f"exit_japan":
            name = ':flag_jp:  `Япония`'
            ticket_name = 'japan'
            guildownerid = '755815621958172792'

            if rolejapan in memberop.roles:
                await inter.send(res, ephemeral = True)
                embed = discord.Embed(title='Игрок покинул вашу организацию', description=f'Игрок: {memberop} \nОрганизация: {name}.', color = 0x2f3136)
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/991308335506784276.webp?size=96&quality=lossless")
                embed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                phoenix = await self.client.fetch_user(int(guildownerid))
                memberop.remove_roles(rolejapan)
                await phoenix.send(embed=embed)
                await logchannel.send(embed=embed)
            else:
                await inter.send(noguild, ephemeral = True)

        if inter.component.custom_id == "avignon":
            if memberop.id in guildmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:
                chooseemb = discord.Embed(title='Выберите тип заявки', color = 0x2f3136)
                row = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Вступление в организацию',
                        custom_id = 'enter_avignon',
                        emoji= '<:enter:991308332906328125>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Выход из организации',
                        custom_id = 'exit_avignon',
                        emoji= '<:exit:991308335506784276>'
                    )
                view=View()
                view.add_item(row)
                view.add_item(row2)
                await inter.send(embed=chooseemb, view = view, ephemeral = True)

        if inter.component.custom_id == "enter_avignon":
            name = '🗺️ `Авиньон`'
            ticket_name = 'avignon'
            guildownerid = '585492782827831326'
            guildroleid = '1080414446666645548'
            roleavignon = discord.utils.get(guild.roles,id=int(guildroleid))
            if memberop.id in guildmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:
                if roleavignon in memberop.roles:
                    await inter.send(alreadythisguild, ephemeral = True)
                else:
                    await inter.send(res, ephemeral = True)

                    counterguild += 1
                    guildmembers.append(memberop.id)
                    owner = await self.client.fetch_user(int(guildownerid))
                    channel2 = await guild.create_text_channel(f"guildjoin {ticket_num}", category = mainCategory)
                    embinfo = discord.Embed(title='Информация об обращении', description=f'**Автор:** <:member:979406123587223562> `{memberop}` \n **ID обращения:** `{ticket_num}` \n\n**Тип обращения:** <:blurplecertifiedmoderator:856563321541230602> `Вступление в организацию` \n**Организация:** {name}', color = 0x2f3136)
                    await channel2.set_permissions(owner,send_messages=True,read_messages=True,read_message_history=True)
                    await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                    await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)
                    await channel2.send(embed=embinfo)
                    await channel2.send(embed=emb1)
                    await channel2.send(embed=nhtrhtrjtremb1)
                    row = Button(
                            style = discord.ButtonStyle.grey,
                            label = 'Одобрить заявку',
                            custom_id = 'accept_avignon',
                            emoji= '<:minecraft_accept:1080779491875491882>'
                        )
                    row2 = Button(
                            style = discord.ButtonStyle.grey,
                            label = 'Отклонить заявку',
                            custom_id = 'deny_avignon',
                            emoji= '<:minecraft_deny:1080779495386140684>'
                        )
                    view2=View()
                    view2.add_item(row)
                    view2.add_item(row2)
                    msgtic = await channel2.send(embed=embed3, view=view2)
                    delete = await channel2.send(content = f'{memberop.mention} {owner.mention}')
                    await delete.delete()
                    def check(m):
                        return m.message.id == msgtic.id and m.author.id == int(guildownerid)
                    try:
                       m = await self.client.wait_for("button_click", check=check)
                    except asyncio.TimeoutError:
                        print("Неизвестная ошибка в коде тикетов") 
                    else:
                        if m.component.custom_id == f"accept_avignon":
                            embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Вступление в организацию одобрено', colour=0x2f3136)
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
                            clsembed=discord.Embed(title="📞 Ответ от организации \"Авиньон\"", description=f'Ваша заявка на вступление в организацию {name} одобрена главой организации `{m.author}`.', colour = 0x2f3136)
                            clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                            clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                            await memberop.send(embed = clsembed)
                            await memberop.add_roles(roleavignon)
                            os.remove(f'guild_{ticket_name}.txt')
                            return
                        if m.component.custom_id == f"deny_avignon":
                            embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Вступление в организацию отклонено', colour=0x2f3136)
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
                            clsembed=discord.Embed(title="📞 Ответ от организации \"Авиньон\"", description=f'Ваша заявка на вступление в организацию {name} отклонена главой организации `{m.author}`.', colour = 0x2f3136)
                            clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                            clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                            await memberop.send(embed = clsembed)
                            os.remove(f'guild_{ticket_name}.txt')
                            return
        if inter.component.custom_id == f"exit_avignon":
            name = '🗺️ `Авиньон`'
            ticket_name = 'avignon'
            guildownerid = '585492782827831326'
            guildroleid = '1080414446666645548'
            roleavignon = discord.utils.get(guild.roles,id=int(guildroleid))

            if roleavignon in memberop.roles:
                await inter.send(res, ephemeral = True)
                embed = discord.Embed(title='Игрок покинул вашу организацию', description=f'Игрок: {memberop} \nОрганизация: {name}.', color = 0x2f3136)
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/991308335506784276.webp?size=96&quality=lossless")
                embed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                phoenix = await self.client.fetch_user(int(guildownerid))
                memberop.remove_roles(roleavignon)
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


        if inter.component.custom_id == "guard":
            if memberop.id in guildmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:
                chooseemb = discord.Embed(title='Выберите тип заявки', color = 0x2f3136)
                row = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Вступление в организацию',
                        custom_id = 'enter_guard',
                        emoji= '<:enter:991308332906328125>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Выход из организации',
                        custom_id = 'exit_guard',
                        emoji= '<:exit:991308335506784276>'
                    )
                view=View()
                view.add_item(row)
                view.add_item(row2)
                await inter.send(embed=chooseemb, view = view, ephemeral = True)

        if inter.component.custom_id == "enter_guard":
            if memberop.id in guildmembers:
                resno = '<:phoenix_warn:953725334736502784> У вас уже есть открытое обращение. Вы не можете открыть новое обращение, пока предыдущее не будет закрыто.'
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:
                name = '🏹 `Гвардия`'
                ticket_name = 'guard'
                guildownerid = '953687436725211257'
                guildroleid = '1128764905063985232'

                await inter.send(res, ephemeral = True)
                counterguild += 1
                guildmembers.append(memberop.id)
                owner = await self.client.fetch_user(int(guildownerid))
                channel2 = await guild.create_text_channel(f"guildjoin {ticket_num}", category = mainCategory)
                embinfo = discord.Embed(title='Информация об обращении', description=f'**Автор:** <:member:979406123587223562> `{memberop}` \n **ID обращения:** `{ticket_num}` \n\n**Тип обращения:** <:blurplecertifiedmoderator:856563321541230602> `Вступление в организацию` \n**Организация:** {name}', color = 0x2f3136)
                await channel2.set_permissions(owner,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)
                await channel2.send(embed=embinfo)
                await channel2.send(embed=emb1)
                await channel2.send(embed=nhtrhtrjtremb1)
                row = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Одобрить заявку',
                        custom_id = 'accept_guard',
                        emoji= '<:minecraft_accept:1080779491875491882>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Отклонить заявку',
                        custom_id = 'deny_guard',
                        emoji= '<:minecraft_deny:1080779495386140684>'
                    )
                view2=View()
                view2.add_item(row)
                view2.add_item(row2)
                msgtic = await channel2.send(embed=embed3, view=view2)
                delete = await channel2.send(content = f'{memberop.mention} {owner.mention}')
                await delete.delete()
                def check(m):
                    return m.message.id == msgtic.id and m.author.id == int(guildownerid)
                try:
                   m = await self.client.wait_for("button_click", check=check)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде тикетов") 
                else:
                    if m.component.custom_id == f"accept_guard":
                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Вступление в организацию одобрено', colour=0x2f3136)
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
                        clsembed=discord.Embed(title="📞 Ответ от организации \"Гвардия\"", description=f'Ваша заявка на вступление в организацию {name} одобрена главой организации `{m.author}`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        role = discord.utils.get(guild.roles,id=int(guildroleid)) 
                        await memberop.add_roles(role)
                        os.remove(f'guild_{ticket_name}.txt')
                        return
                    if m.component.custom_id == f"deny_guard":
                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Вступление в организацию отклонено', colour=0x2f3136)
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
                        clsembed=discord.Embed(title="📞 Ответ от организации \"Гвардия\"", description=f'Ваша заявка на вступление в организацию {name} отклонена главой организации `{m.author}`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        os.remove(f'guild_{ticket_name}.txt')
                        return
        if inter.component.custom_id == f"exit_guard":
            name = '🏹 `Гвардия`'
            ticket_name = 'guard'
            guildownerid = '953687436725211257'
            guildroleid = '1128764905063985232'

            if role in memberop.roles:
                await inter.send(res, ephemeral = True)
                embed = discord.Embed(title='Игрок покинул вашу организацию', description=f'Игрок: {memberop} \nОрганизация: {name}.', color = 0x2f3136)
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/991308335506784276.webp?size=96&quality=lossless")
                embed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                phoenix = await self.client.fetch_user(int(guildownerid))
                memberop.remove_roles(role)
                await phoenix.send(embed=embed)
                await logchannel.send(embed=embed)
            else:
                await inter.send(noguild, ephemeral = True)

        if inter.component.custom_id == "pehub":
            if memberop.id in guildmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:
                chooseemb = discord.Embed(title='Выберите тип заявки', color = 0x2f3136)
                row = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Вступление в организацию',
                        custom_id = 'enter_pehub',
                        emoji= '<:enter:991308332906328125>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Выход из организации',
                        custom_id = 'exit_pehub',
                        emoji= '<:exit:991308335506784276>'
                    )
                view=View()
                view.add_item(row)
                view.add_item(row2)
                await inter.send(embed=chooseemb, view = view, ephemeral = True)

        if inter.component.custom_id == "enter_pehub":
            if memberop.id in guildmembers:
                resno = '<:phoenix_warn:953725334736502784> У вас уже есть открытое обращение. Вы не можете открыть новое обращение, пока предыдущее не будет закрыто.'
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:
                name = '🤡 `PeHub`'
                ticket_name = 'pehub'
                guildownerid = '797939500412174396'
                guildroleid = '1132004725311672360'

                await inter.send(res, ephemeral = True)
                counterguild += 1
                guildmembers.append(memberop.id)
                owner = await self.client.fetch_user(int(guildownerid))
                channel2 = await guild.create_text_channel(f"guildjoin {ticket_num}", category = mainCategory)
                embinfo = discord.Embed(title='Информация об обращении', description=f'**Автор:** <:member:979406123587223562> `{memberop}` \n **ID обращения:** `{ticket_num}` \n\n**Тип обращения:** <:blurplecertifiedmoderator:856563321541230602> `Вступление в организацию` \n**Организация:** {name}', color = 0x2f3136)
                await channel2.set_permissions(owner,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)
                await channel2.send(embed=embinfo)
                await channel2.send(embed=emb1)
                await channel2.send(embed=nhtrhtrjtremb1)
                row = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Одобрить заявку',
                        custom_id = 'accept_pehub',
                        emoji= '<:minecraft_accept:1080779491875491882>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Отклонить заявку',
                        custom_id = 'deny_pehub',
                        emoji= '<:minecraft_deny:1080779495386140684>'
                    )
                view2=View()
                view2.add_item(row)
                view2.add_item(row2)
                msgtic = await channel2.send(embed=embed3, view=view2)
                delete = await channel2.send(content = f'{memberop.mention} {owner.mention}')
                await delete.delete()
                def check(m):
                    return m.message.id == msgtic.id and m.author.id == int(guildownerid)
                try:
                   m = await self.client.wait_for("button_click", check=check)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде тикетов") 
                else:
                    if m.component.custom_id == f"accept_pehub":
                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Вступление в организацию одобрено', colour=0x2f3136)
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
                        clsembed=discord.Embed(title="📞 Ответ от организации \"PeHub\"", description=f'Ваша заявка на вступление в организацию {name} одобрена главой организации `{m.author}`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        role = discord.utils.get(guild.roles,id=int(guildroleid)) 
                        await memberop.add_roles(role)
                        os.remove(f'guild_{ticket_name}.txt')
                        return
                    if m.component.custom_id == f"deny_pehub":
                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Вступление в организацию отклонено', colour=0x2f3136)
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
                        clsembed=discord.Embed(title="📞 Ответ от организации \"PeHub\"", description=f'Ваша заявка на вступление в организацию {name} отклонена главой организации `{m.author}`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        os.remove(f'guild_{ticket_name}.txt')
                        return
        if inter.component.custom_id == f"exit_pehub":
            name = '🤡 `PeHub`'
            ticket_name = 'pehub'
            guildownerid = '797939500412174396'
            guildroleid = '1132004725311672360'

            if role in memberop.roles:
                await inter.send(res, ephemeral = True)
                embed = discord.Embed(title='Игрок покинул вашу организацию', description=f'Игрок: {memberop} \nОрганизация: {name}.', color = 0x2f3136)
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/991308335506784276.webp?size=96&quality=lossless")
                embed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                phoenix = await self.client.fetch_user(int(guildownerid))
                memberop.remove_roles(role)
                await phoenix.send(embed=embed)
                await logchannel.send(embed=embed)
            else:
                await inter.send(noguild, ephemeral = True)

        if inter.component.custom_id == "newguild":
            if memberop.id in guildmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in guildmembers:
                await inter.send(res, ephemeral = True)
                counterguild += 1
                guildmembers.append(memberop.id)
                mainCategory = discord.utils.get(guild.categories, id=939513361425657947) #ID категории, где будут создаваться тикеты.
                channel2 = await guild.create_text_channel(f"guildcreate {ticket_num}", category = mainCategory)
                modrole = discord.utils.get(guild.roles,id=939476433196171324) #ID роли модератора
                await channel2.set_permissions(modrole,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)
                embinfo = discord.Embed(title='<:info:871310064135327775> Информация об обращении', description=f'**Автор:** <:member:1105878287978340415> `{memberop}` \n **ID обращения:** `{ticket_num}` \n\n**Тип обращения:** <:invite:1105878276242673725> `Создание организации`.', color = 0x2f3136)
                emb1 = discord.Embed(title='Добро пожаловать в службу поддержки.', description='Для создания вашей организации, отправьте соообщение по следующей форме заполнения.: \n1) Название организации. \n2) Описание организации. \n3) Эмодзи для кнопки вступления в организацию. \n 4) Цвет роли организации (Форматом HEX). 5) Герб организации (https://minecraft.tools/en/banner.php)', color = 0x2f3136)
                nhtrhtrjtremb1 = discord.Embed(title='Когда мне ответят?', description=" Обращения разбираются в порядке очереди. В среднем обращения разбираются от 1 до 3-х часов в рабочие дни с 10:00 по 00:00. В выходные время ответа может быть дольше, но не более 9-ти часов. \n\nЕсли с момента отправки последнего сообщения прошло более 3-х часов, а вам не ответили - можете упомянуть <@&939476433196171324>. \nЕсли прошло более 6-ти часов - упоминайте <@&922561682780332102>.", color = 0x2f3136)
                embed3 = discord.Embed(title='', description='<:info:871310064135327775> Обращения закрываются сотрудниками кнопкой ниже.', color = 0x2f3136)
                await channel2.send(embed=embinfo)
                await channel2.send(embed=emb1)
                await channel2.send(embed=nhtrhtrjtremb1)
                row = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Закрыть обращение',
                        custom_id = 'accept_guild',
                        emoji= '<:blurplelock:856563321321816104>'
                    )
                view2=View()
                view2.add_item(row)
                msgtic = await channel2.send(embed=embed3, view=view2)
                delete = await channel2.send(content = f'{memberop.mention}')
                await delete.delete()
                def check(m):
                    return m.message.id == msgtic.id and m.author.guild_permissions.manage_messages == True
                try:
                   m = await self.client.wait_for("button_click", check=check)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде тикетов") 
                else:
                    if m.component.custom_id == "accept_guild":
                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Обращение закрыто.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Тип обращения:', value=f'<:invite:1105878276242673725> `Создание организации`')
                        embedth.add_field(name='Сотрудник:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор:', value=f'<:member:979406123587223562> `{memberop}`')  
                        with open(f"newguild.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")      
                        await logchannel.send(embed=embedth,file=File(f'newguild.txt'))
                        guildmembers.remove(memberop.id)
                        await channel2.delete()
                        clsembed=discord.Embed(title="📞 Поддержка проекта", description=f'Приветствую. \nВаше обращение закрыто сотрудником `{m.author}`. \nВы можете запросить файл с содержанием вашего обращения в течение 3-х дней с момента закрытия обращения. Для этого обратитесь к руководителю проекта `Найт#0550`, предъявив ID вашего обращения. \n\nID: `{ticket_num}` \nТип обращения: <:phoenix_plus:953725336061886505> `Создание организации`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1105878293187678208.webp?size=96&quality=lossless")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        os.remove(f'newguild.txt')
                        return   

def setup(client):
    client.add_cog(GuildButtonClick(client))