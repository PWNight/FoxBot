import disnake as discord
from disnake.ext import commands
from disnake.utils import get
from api.check import block
from api.server import base, main

class DataBase(commands.Cog):
    def __init__(self, client):
        self.client = client

    # ? --------------------------
    # ? | Запись При Старте Бота |
    # ? --------------------------

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.logger(self.__class__.__name__, 'cogs')
        for guild in self.client.guilds:
            if base.guild(guild) is None:
                base.send(f"INSERT INTO guilds VALUES ('{guild.id}', '{guild.name}', '{self.client.config.prefix}', '{self.client.config.lang}', NULL, NULL, NULL, NULL, NULL, 3, 'mute')")
                self.client.logger(f"Сервер {guild.name} был зарегистрирован в базе данных")
            else:
                pass
            
            for member in guild.members:
                if not member.bot:
                    try:
                        if base.user(member) is None:
                            base.send(f"INSERT INTO users VALUES ('{guild.id}', '{member}', {member.id}, 0, 0, 0)")
                            self.client.logger(f"Пользователь {member} был зарегистрирован в базе данных")
                        else:
                            pass
                    except:
                        continue

    # ? ---------------------------
    # ? | Присоединение к Гильдии |
    # ? ---------------------------

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for member in guild.members:
            if not member.bot:
                try:
                    if base.user(member) is None:
                        base.send(f"INSERT INTO users VALUES ('{guild.id}', '{member}', {member.id}, 0, 0, 0)")
                        self.client.logger(f"Пользователь {member} был зарегистрирован в базе данных")
                    else:
                        pass
                except:
                    continue

        if base.guild(guild) is None:
            base.send(f"INSERT INTO guilds VALUES ('{guild.id}', '{guild.name}', '{self.client.config.prefix}', '{self.client.config.lang}', NULL, NULL, NULL, NULL, NULL, 3, 'mute')")
            self.client.logger(f"Сервер {guild.name} был зарегистрирован в базе данных")
        else:
            pass

    # ? -----------------------
    # ? | Удаление из Гильдии |
    # ? -----------------------

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        for member in guild.members:
            try:
                if base.user(member) is not None:
                    base.send(f"DELETE FROM users WHERE guild = {guild.id}")
                    self.client.logger(f"Пользователь {member} был удалён из базы данных")
                else:
                    pass
            except:
                continue

        if base.guild(guild) is not None:
            base.send(f"DELETE FROM guilds WHERE guild = {guild.id}")
            self.client.logger(f"Сервер {guild.name} был удален из базы данных")
        else:
            pass

    # ? ---------------------------
    # ? | Присоединение Участника |
    # ? ---------------------------

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member.bot:
            if base.guild(member.guild)[5] is not None:
                role = get(member.guild.roles, id = base.guild(member.guild)[5])
                await member.add_roles(role)
            else:
                pass

            if base.user(member) is None:
                base.send(f"INSERT INTO users VALUES ('{member.guild.id}', '{member}', {member.id}, 0, 0, 0)")
                self.client.logger(f"Пользователь {member} был зарегистрирован в базе данных")                  
            else:
                pass

    # ? ----------------------
    # ? | Удаление Участника |
    # ? ----------------------

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if base.user(member) is not None:
            base.send(f"DELETE FROM users WHERE guild = {member.guild.id} AND id = {member.id}")
            self.client.logger(f"Пользователь {member} был удалён из базы данных")
        else:
            pass

def setup(client):
    client.add_cog(DataBase(client))