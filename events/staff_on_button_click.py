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

class StaffButtonClick(commands.Cog):
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
        
        #Текстовая информация для тикетов.
        res = '<:evilsmile:1105881397597585500> Обращение создано. Ожидайте пинга в нужном канале.'
        resno = '<:error:1105878281246482484> У вас уже есть открытое обращение. Вы не можете открыть обращение, пока предыдущее не будет закрыто.'
        memberop = inter.author
        emb1 = discord.Embed(title='Добро пожаловать в службу набора кадров.', description='Чтобы получить ответ как можно быстрее, опишите суть вашей жалобы по следующей форме заполнения: \n1) Ваш никнейм. \n2) Никнейм нарушителя. \n3) Нарушенное правило.\n4) Подробность нарушения. \n5) Доказательства нарушения.', color = 0x2f3136)
        responceemb = discord.Embed(title='Когда мне ответят?', description=" Обращения разбираются в порядке очереди. В среднем обращения разбираются от 1 до 3-х часов в рабочие дни с 10:00 по 00:00. В выходные время ответа может быть дольше, но не более 9-ти часов. \n\nЕсли с момента отправки последнего сообщения прошло более 3-х часов, а вам не ответили - можете упомянуть <@&939476433196171324>. \nЕсли прошло более 6-ти часов - упоминайте <@&922561682780332102>.", color = 0x2f3136)
        buttonembed = discord.Embed(title='', description='<:info:871310064135327775> Обращения закрываются сотрудниками кнопкой ниже.', color = 0x2f3136)
        if inter.component.custom_id == "nabor_kadrov":
            if memberop.id in voprosmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in voprosmembers:
                chooseemb = discord.Embed(title='Выберите интересующее вас направление', color = 0x607aff)
                row = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Модерация',
                        custom_id = 'nabor_moder',
                        emoji= '💬'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Ивенты',
                        custom_id = 'nabor_events',
                        emoji= '🎭'
                    )
                row3 = Button(
                        style = discord.ButtonStyle.gray,
                        label = 'Редакция',
                        custom_id = 'nabor_edit',
                        emoji= '📝'
                    )
                view=View()
                view.add_item(row)
                view.add_item(row2)
                view.add_item(row3)
                await inter.send(embed=chooseemb, view = view, ephemeral = True)
                return

        if inter.component.custom_id == "nabor_moder":
            if memberop.id in voprosmembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in voprosmembers:
                global countervopros
                countervopros += 1
                voprosmembers.append(memberop.id)
                ticket_type = '💬 `Заявка в направление модерации`'
                ticket_systemname= 'nabor_moder'
                mainCategory = mainCategory
                channel2 = await guild.create_text_channel(f"ticket {ticket_num}", category = mainCategory)
                await channel2.set_permissions(memberop,send_messages=True,read_messages=True,read_message_history=True)
                await channel2.set_permissions(guild.default_role,send_messages=False,read_messages=False,read_message_history=False)

                embinfo = discord.Embed(title='<:info:871310064135327775> Информация об обращении', description=f'**Автор:** <:member:1105878287978340415> `{memberop}` \n **ID обращения:**  `{ticket_num}` \n\n**Тип обращения:** 💬 `Заявка в направление модерации`.', color = 0x2f3136)
                emb1 = emb1
                responceemb = responceemb
                buttonembed = buttonembed
                await channel2.send(embed=embinfo)
                await channel2.send(embed=emb1)
                await channel2.send(embed=responceemb)

                row = Button(
                        style = discord.ButtonStyle.grey,
                        label = 'Закрыть обращение',
                        custom_id = 'accept_nabor_moder',
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
                    if m.component.custom_id == "accept_nabor_moder":
                        pwnight = await self.client.fetch_user(int(660070694377357322))
                        embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Обращение закрыто.', colour=0x2f3136)
                        embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                        embedth.add_field(name='Тип обращения:', value=f'{ticket_type}')
                        embedth.add_field(name='Администратор:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                        embedth.add_field(name='Автор:', value=f'<:member:1105878287978340415> `{memberop}`')  

                        with open(f"{ticket_systemname}.txt", "a", encoding='utf8') as f:
                            async for msg12 in channel2.history(limit = 100):
                                f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")   
               
                        await pwnight.send(embed=embedth,file=File(f'{ticket_systemname}.txt'))
                        await channel2.delete()
                        clsembed=discord.Embed(title="\📞 Служба набора кадров.", description=f'Приветствую. \nВаше обращение закрыто администратором `{m.author}`. \nВы можете запросить файл с содержанием вашего обращения в течение 3-х дней с момента закрытия обращения. Для этого обратитесь к руководителю проекта `Найт#0550`, предъявив ID вашего обращения. \n\nID:  `{ticket_num}` \nСервер: <:discord:856561477033263124> `Discord`.\nТип обращения: <:report:1105878279736528977> `Жалоба`.', colour = 0x2f3136)
                        clsembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1105878293187678208.webp?size=96&quality=lossless")
                        clsembed.set_footer(text=f"FoxWorld ©️ 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                        await memberop.send(embed = clsembed)
                        
                        voprosmembers.remove(memberop.id)
                        os.remove(f'{ticket_systemname}.txt')
                        return
                    
def setup(client):
    client.add_cog(StaffButtonClick(client))