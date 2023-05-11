import disnake as discord
from disnake.ext import commands
from api.server import main

class Mute(commands.Cog):

    def __init__(self, client):
        self.client = client     

    @commands.cooldown(1, 60, commands.BucketType.guild)       
    @commands.slash_command(name="таймаут", description="📛 Выдаёт тайм-аут указанному пользователю.", test_guilds=[921483461016031263])
    @commands.has_permissions(manage_messages=True)
    async def timeout(self, inter, member: discord.Member, time, *, reason):
        time_conversion = {
            "s": 1, 
            "m": 60, 
            "h": 3600, 
            "d": 86400, 
            "с": 1, 
            "м": 60, 
            "ч": 3600, 
            "д": 86400,
        }
        mute_time = int(time[0]) * time_conversion[time[-1]]
        if inter.author.top_role.position <= member.top_role.position:
            await inter.send(embed = main.deny(inter.guild, main.get_lang(inter.guild, "TOP")))        
        elif member == None:
            await inter.send(embed = main.deny(inter.guild, main.get_lang(inter.guild, "MUTE_NOARG")))
        elif member == inter.author:
            await inter.send(embed = main.deny(inter.guild, main.get_lang(inter.guild, "MUTE_AUTHOR")))
        elif reason == None:
            reason = ''
        else:
            try: 
                await member.timeout(duration=mute_time, reason=f'{reason} ({inter.author})')   
                await inter.send(embed = main.done(inter.guild, main.get_lang(inter.guild, "MUTE_SUCCESS").format(member.mention, inter.author.mention, reason, time)))
                await member.send(embed = main.warn(inter.guild, main.get_lang(inter.guild, "MUTE_MEMBER").format(inter.guild.name, inter.author, reason, time)))
            except:
                await inter.send(embed = main.deny(inter.guild, main.get_lang(inter.guild, "MUTE_ERROR")))

def setup(client):
    client.add_cog(Mute(client))        