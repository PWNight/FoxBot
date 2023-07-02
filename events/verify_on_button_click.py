import disnake as discord
from disnake.ext import commands
import asyncio
import os
from disnake import File
from disnake.ui import Button, View
from api.server.dataIO import fileIO
from disnake import TextInputStyle

verifymembers = []
counterverify = 0

class VerifyButtonClick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        #Техническая информация для тикетов.
        guild = self.client.get_guild(inter.guild.id)
        logchannel = self.client.get_channel(1053188377651970098) # ID канала с логами.
        memberop = inter.author
        
        #Текстовая информация для тикетов.
        res = '<:evilsmile:1105881397597585500> Обращение создано. Ожидайте пинга в нужном канале.'
        resno = '<:error:1105878281246482484> У вас уже есть открытое обращение. Вы не можете открыть обращение, пока предыдущее не будет закрыто.'

        if inter.component.custom_id == "verify":
            if memberop.id in verifymembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in verifymembers:

                global counterverify
                counterverify += 1
                await inter.response.send_modal(
                    title=f"Заявка игрока {memberop.name}",
                    custom_id="verify_modal",
                    components=[
                        discord.ui.TextInput(
                            label="Ваш никнейм",
                            placeholder="Укажите ваш никнейм, с которого вы будете заходить на сервер.",
                            custom_id="Nickname",
                            style=TextInputStyle.short,
                            max_length=16,
                        ),
                        discord.ui.TextInput(
                            label="Ваш возраст",
                            placeholder="Укажите ваш возраст",
                            custom_id="Ago",
                            style=TextInputStyle.short,
                            max_length=2,
                        ),
                        discord.ui.TextInput(
                            label="Расскажите немного о себе",
                            placeholder="Это необходимо для знакомства с вами",
                            custom_id="About",
                            style=TextInputStyle.paragraph,
                        ),
                    ],
                )
                try:
                    inter: discord.ModalInteraction = await self.client.wait_for("modal_submit", check=lambda i: i.custom_id == "verify_modal" and i.author.id == inter.author.id)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде верификации")
                    return 
                else:
                    await inter.response.send_message(content='Заявка отправлена.', ephemeral = True)
                    embinfo = discord.Embed(title=f'<:info:871310064135327775> Информация о заявке игрока {memberop.name}', color = 0x2f3136)
                    for key, value in inter.text_values.items():
                        embinfo.add_field(name=key.capitalize(), value=value[:1024], inline=False)
                    row = Button(
                            style = discord.ButtonStyle.green,
                            label = 'Одобрить заявку',
                            custom_id = 'accept_verify',
                            emoji= '<:blurplelock:856563321321816104>'
                        )
                    row2 = Button(
                            style = discord.ButtonStyle.danger,
                            label = 'Отклонить заявку',
                            custom_id = 'deny_verify',
                            emoji= '<:blurplelock:856563321321816104>'
                        )
                    view2=View()
                    view2.add_item(row)
                    view2.add_item(row2)
                    msgtic = await logchannel.send(embed=embinfo, view=view2)
                    def check(m):
                        return m.message.id == msgtic.id and m.author.guild_permissions.manage_messages == True
                    try:
                       m = await self.client.wait_for("button_click", check=check)
                    except asyncio.TimeoutError:
                        print("Неизвестная ошибка в коде репортов") 
                    else:
                        if m.component.custom_id == "accept_report":
                            embedth = discord.Embed(title=f'<:blurplelock:856563321321816104> Репорт закрыт.', colour=0x2f3136)
                            embedth.add_field(name='ID:', value=f'`{ticket_num}`')
                            embedth.add_field(name='Закрыт сотрудником:', value=f'<:moderatorbadge:953725334518378616> `{m.author}`')
                            embedth.add_field(name='Открыт модератором:', value=f'<:member:979406123587223562> `{memberop}`')  
                            with open(f"report.txt", "a", encoding='utf8') as f:
                                async for msg12 in channel2.history(limit = 100):
                                    f.write(f"{msg12.created_at}:{msg12.author} ({msg12.author.id}): {msg12.content} \n")      
                            await logchannel.send(embed=embedth,file=File(f'report.txt'))
                            await channel2.delete()
                            clsembed=discord.Embed(title="\📞 Служба обработки репортов.", description=f'Приветствую, модератор. \nВаш репорт закрыт сотрудником `{m.author}`.', colour = 0x2f3136)
                            clsembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856561382484475904/979389736462458910/953725334627430411.png")
                            clsembed.set_footer(text="PhoenixWorld by Найт#0550", icon_url="https://cdn.discordapp.com/avatars/921482377505673267/c39980246a73cc64a1052c36a7a72c0a.png?size=1024")
                            await memberop.send(embed = clsembed)
                            os.remove(f'report.txt')
                            return

def setup(client):
    client.add_cog(VerifyButtonClick(client))