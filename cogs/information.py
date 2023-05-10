import disnake as discord
from disnake.ext import commands
from api.check import block
from api.server import base, main
import calendar


class Info(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.logger(self.__class__.__name__, 'cogs')
        
    @commands.command(aliases=['si', 'server', 'сервер', 'серверинфо', 'сервер-инфо', 'си', 'сервак'])
    @block.block()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        guild_age = (ctx.message.created_at - guild.created_at).days
        created_at = int(guild.created_at.timestamp())
        color = discord.Color.green()

        user_count = len([x for x in ctx.guild.members if not x.bot])
        member_count = len(ctx.guild.members) # includes bots
        list_of_bots = len([bot for bot in ctx.guild.members if bot.bot])

        online_users = sum(member.status==discord.Status.online and not member.bot for member in ctx.guild.members)
        idle_users = sum(member.status==discord.Status.idle and not member.bot for member in ctx.guild.members)
        dnd_users = sum(member.status==discord.Status.dnd and not member.bot for member in ctx.guild.members)
        off_users = sum(member.status==discord.Status.offline and not member.bot for member in ctx.guild.members)

        total_text_channels = len(ctx.guild.text_channels)
        total_voice_channels = len(ctx.guild.voice_channels)
        total_channels = total_text_channels + total_voice_channels

        try:
            em = discord.Embed(description=' ', color=9579219)
            em.add_field(name=f'{main.get_lang(ctx.guild, "SI_MEMBER_TITLE")}', value=f'{main.get_lang(ctx.guild, "SI_MEMBER_DESC").format(member_count, user_count, list_of_bots)}', inline=True)
            em.add_field(name=f'{main.get_lang(ctx.guild, "SI_STATUS_TITLE")}', value=f'{main.get_lang(ctx.guild, "SI_STATUS_DESC").format(online_users, idle_users, dnd_users, off_users)}', inline=True)
            em.add_field(name=f'{main.get_lang(ctx.guild, "SI_CHANNEL_TITLE")}', value=f'{main.get_lang(ctx.guild, "SI_CHANNEL_ALL").format(total_channels, total_text_channels, total_voice_channels)}', inline=True)
            em.add_field(name=f'{main.get_lang(ctx.guild, "SI_OWNER")}', value=guild.owner.mention, inline=True)
            em.add_field(name=f'{main.get_lang(ctx.guild, "SI_LEVEL_CHECK")}', value=guild.verification_level, inline=True)
            em.add_field(name=f'{main.get_lang(ctx.guild, "SI_DATE")}', value=f'<t:{created_at}:D>', inline=True)
            em.set_thumbnail(url=ctx.guild.icon.url)
            em.set_author(name=f'{main.get_lang(ctx.guild, "SI_AUTHOR").format(guild.name)}')
            await ctx.send(embed=em)
        except:
            em = discord.Embed(description=' ', color=9579219)
            em.add_field(name=f'{main.get_lang(ctx.guild, "SI_MEMBER_TITLE")}', value=f'{main.get_lang(ctx.guild, "SI_MEMBER_DESC").format(member_count, user_count, list_of_bots)}', inline=True)
            em.add_field(name=f'{main.get_lang(ctx.guild, "SI_STATUS_TITLE")}', value=f'{main.get_lang(ctx.guild, "SI_STATUS_DESC").format(online_users, idle_users, dnd_users, off_users)}', inline=True)
            em.add_field(name=f'{main.get_lang(ctx.guild, "SI_CHANNEL_TITLE")}', value=f'{main.get_lang(ctx.guild, "SI_CHANNEL_ALL").format(total_channels, total_text_channels, total_voice_channels)}', inline=True)
            em.add_field(name=f'{main.get_lang(ctx.guild, "SI_OWNER")}', value=guild.owner.mention, inline=True)
            em.add_field(name=f'{main.get_lang(ctx.guild, "SI_LEVEL_CHECK")}', value=guild.verification_level, inline=True)
            em.add_field(name=f'{main.get_lang(ctx.guild, "SI_DATE")}', value=f'<t:{created_at}:D>', inline=True)
            em.set_author(name=f'{main.get_lang(ctx.guild, "SI_AUTHOR").format(guild.name)}')
            await ctx.send(embed=em)            

def setup(client):
    client.add_cog(Info(client))