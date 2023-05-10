#import disnake as discord
#from disnake.ext import commands
#from api.check import utils, block
#from api.server import base, main
#
#
#class Notify(commands.Cog):
#
#    def __init__(self, client):
#        self.client = client
#
#    @commands.slash_command(name="notify", description="Публикует уведомление в одноимённом канале", test_guilds=[921483461016031263])
#    @block.block()
#    async def notify(self, inter, type:str, member: discord.Member = None, message:str):
#        if not member:
#            member = inter.author
#
#        embed = discord.Embed(color = 0xFFA500)
#        if type = :
#            embed.description = main.get_lang(inter.guild, "TICKLE_ARGS").format(inter.author.mention, member.mention)
#        else:
#            embed.description = main.get_lang(inter.guild, "TICKLE_NOARGS").format(inter.author.mention)
#        embed.set_image(url = random.choice(tickkle))
#
#        await inter.send(embed = embed)     
#
#
#def setup(client):
#    client.add_cog(Notify(client))