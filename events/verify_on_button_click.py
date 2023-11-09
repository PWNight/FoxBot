import disnake as discord
from disnake.ext import commands
import asyncio
from disnake.ui import Button, View
from disnake import TextInputStyle
from mctools import  RCONClient

verifymembers = []
counterverify = 0

class VerifyButtonClick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        #Техническая информация для тикетов.
        guild = self.client.get_guild(inter.guild.id)
        logchannel = self.client.get_channel(1126156262216843394) # ID канала с логами.
        memberop = inter.author
        guild = self.client.get_guild(921483461016031263)
        role = discord.utils.get(guild.roles, id=1172204202328592455)
        playerroleid = '1172204202328592455'
        playerrole = discord.utils.get(guild.roles,id=int(playerroleid)) 
        
        #Текстовая информация для тикетов.
        resno = '<:minecraft_deny:1080779495386140684> **У вас уже есть отправленная заявка.** \nОжидайте решения по предыдущей заявке, чтобы открыть новую.'
        already_player = '<:minecraft_deny:1080779495386140684> **Вы уже являетесь игроком сервера.** \nЕсли это ошибка - свяжитесь с руководством проекта.'
        maintenance = '<:minecraft_deny:1080779495386140684> **Служба верификации временно недоступна.** \nПричина: проведение технических работ. \nВ ближайшее время данная служба будет восстановлена.'

        if inter.component.custom_id == "maintenance":
            await inter.send(maintenance, ephemeral = True)
            return      
        if inter.component.custom_id == "verify":
            if memberop.id in verifymembers:
                await inter.send(resno, ephemeral = True)
                return
            if not memberop.id in verifymembers:
                if playerrole in memberop.roles: 
                    await inter.send(already_player, ephemeral = True)
                    return
                else:
                    global counterverify
                    counterverify += 1
                    await inter.response.send_modal(
                        title=f"Заявка игрока {memberop.name}",
                        custom_id="verify_modal",
                        components=[
                            discord.ui.TextInput(
                                label="Ваш никнейм",
                                placeholder="Укажите ваш игровой никнейм.",
                                custom_id="Никнейм",
                                style=TextInputStyle.short,
                                max_length=16,
                            ),
                            discord.ui.TextInput(
                                label="Ваш возраст",
                                placeholder="Укажите ваш возраст.",
                                custom_id="Возраст",
                                style=TextInputStyle.short,
                                max_length=2,
                            ),
                            discord.ui.TextInput(
                                label="Расскажите немного о себе",
                                placeholder="Напишите краткое описание вас и ваших увлечений.",
                                custom_id="Об игроке",
                                style=TextInputStyle.paragraph,
                            ),
                            discord.ui.TextInput(
                                label="Где вы узнали о нашем сервере?",
                                placeholder="Укажите соц.сеть, мониторинг или никнейм пригласившего.",
                                custom_id="Откуда игрок",
                                style=TextInputStyle.paragraph,
                            ),
                            discord.ui.TextInput(
                                label="Чем вы планируете заняться на сервере?",
                                placeholder="Построить крутой дом? Поучаствовать в ивентах? ",
                                custom_id="О деятельности",
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
                        await inter.response.send_message(content='<:minecraft_accept:1080779491875491882> **Ваша заявка была отправлена.** \nРешение по вашей заявке будет отправлено вам в ЛС.', ephemeral = True)
                        embinfo = discord.Embed(description=f"<:invite:1105878276242673725> Заявка пользователя {memberop.mention} ({memberop.display_name})", color = 0x2f3136)
                        for key, value in inter.text_values.items():
                            embinfo.add_field(name=key.capitalize(), value=value[:1024], inline=False)
                        row = Button(
                                style = discord.ButtonStyle.green,
                                label = 'Одобрить заявку',
                                custom_id = 'accept_verify',
                                emoji= '<:minecraft_accept:1080779491875491882>'
                            )
                        row2 = Button(
                                style = discord.ButtonStyle.danger,
                                label = 'Отклонить заявку',
                                custom_id = 'deny_verify',
                                emoji= '<:minecraft_deny:1080779495386140684>'
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
                            if m.component.custom_id == "accept_verify":
                                await msgtic.delete()
                                await memberop.add_roles(role)
                                pass
                                HOST = '135.181.126.159'
                                PORT = 25571
                                rcon = RCONClient(HOST, port = PORT)
                                if rcon.login('59d82888-5420-43b9-a58b-98c382061602'):
                                    rcon.command(f'easywl add {inter.text_values["Никнейм"]}')
                                    rcon.stop()
                                await memberop.edit(nick=f'{inter.text_values["Никнейм"]}')
                                embinfo = discord.Embed(description=f"<:invite:1105878276242673725> Заявка пользователя {memberop.mention} ({memberop.display_name}) \n\n**Статус заявки:** <:minecraft_accept:1080779491875491882> Принята \n**Принял заявку:** {m.author.mention}", color = 0x2f3136)
                                for key, value in inter.text_values.items():
                                    embinfo.add_field(name=key.capitalize(), value=value[:1024], inline=False)  
                                await logchannel.send(embed=embinfo)
                                clsembed=discord.Embed(title="Поддержка проекта FoxWorld", description=f'Приветствую! \nВаша заявка на наш сервер была одобрена Сотрудником {m.author.mention} ({m.author.display_name}). \nТеперь вы получили статус игрока нашего проекта и уже можете зайти на сервер. \n\nСчастливой игры! C любовью к своему делу, команда проекта FoxWorld.', colour = 0x2f3136)
                                clsembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1105891497255108679.webp?size=96&quality=lossless")
                                clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                                await memberop.send(embed = clsembed)
                                return
                            if m.component.custom_id == "deny_verify":
                                await msgtic.delete()
                                embinfo = discord.Embed(description=f"<:invite:1105878276242673725> Заявка пользователя {memberop.mention} ({memberop.display_name}) \n\n**Статус заявки:** <:minecraft_deny:1080779495386140684> Отклонена \n**Отклонил заявку:** {m.author.mention}", color = 0x2f3136)
                                for key, value in inter.text_values.items():
                                    embinfo.add_field(name=key.capitalize(), value=value[:1024], inline=False)  
                                await logchannel.send(embed=embinfo)
                                clsembed=discord.Embed(title="Поддержка проекта FoxWorld", description=f'Приветствую! \nВаша заявка на наш сервер была отклонена Сотрудником {m.author.mention} ({m.author.display_name}). \nВозможно, причиной отклонения послужило неправильно заполненное поле Никнейма. \n\nНе расстраивайтесь, вы можете узнать причину отклонения у одного из Сотрудников проекта, мы будем рады помочь вам! \n\nОжидаем вашего обращения! C любовью к своему делу, команда проекта FoxWorld.', colour = 0x2f3136)
                                clsembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1105891497255108679.webp?size=96&quality=lossless")
                                clsembed.set_footer(text=f"FoxWorld ©️ 2021 - 2023", icon_url="https://cdn.discordapp.com/attachments/939510519629479946/1019317064479035443/Fox5.png")
                                await memberop.send(embed = clsembed)
                                return

def setup(client):
    client.add_cog(VerifyButtonClick(client))