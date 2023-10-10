import pymongo
import disnake
import json
from disnake.utils import get
from disnake.ext import commands

cluster = pymongo.MongoClient(f"mongodb://127.0.0.1/myFirstDatabase?retryWrites=true&w=majority")

files = cluster.sweetness.files

class promocodes(commands.Cog):
    def __init__(self, bot: commands.Bot(intents=disnake.Intents.all(), command_prefix = "test!")):
        self.bot = bot
    @commands.slash_command(name = 'promo', description="Активировать промокод")
    async def promo(inter, название):

        promocodes = len(cluster.sweetness.server_settings.find_one({'_id': str(inter.guild.id)})['promocodes'])

        embed = disnake.Embed(color=3092790).set_author(name = f"Промокоды | {inter.guild.name}", icon_url = inter.guild.icon.url).set_footer(text = f"Всего на сервере {promocodes} промокодов", icon_url = inter.guild.icon.url)
        if название == "update":
            embed.description = f"{inter.author.mention}, Такого **промокода не существует**!"
            return await inter.send(ephemeral = True, embed = embed)
        
        if название in cluster.sweetness.server_settings.find_one({'_id': str(inter.guild.id)})['promocodes']:

            result = cluster.sweetness.promocode.find_one({'_id': str(название)})

            count = result['sum']

            if cluster.sweetness.promocode.count_documents({"_id": str(inter.author.id)}) == 0: 
                cluster.sweetness.promocode.insert_one({"_id": str(inter.author.id), "activated_promo": []})

            if cluster.sweetness.economy.count_documents({"_id": str(inter.author.id)}) == 0:
                cluster.sweetness.economy.insert_one({"_id": str(inter.author.id), "balance": 0})

            if cluster.sweetness.history_win.count_documents({"_id": str(inter.author.id)}) == 0:
                cluster.sweetness.history_win.insert_one({
                    "_id": str(inter.author.id),
                    "active": 0,
                    "giveaway": 0,
                    "roles": 0,
                    "promocode": 0,
                    "clan": 0,
                    "gifts": 0,
                    "casino": 0,
                    "transfer": 0,
                    "events": 0
                })

            cluster.sweetness.history_win.update_one({"_id": str(inter.author.id)}, {"$inc": {"promocode": +int(count)}})

            if название in cluster.sweetness.promocode.find_one({'_id': str(inter.author.id)})['activated_promo']: 
                embed.description=f'{inter.author.mention}, **Вы** уже активировали этот промокод!'
                return await inter.send(embed = embed)
            
            if cluster.sweetness.promocode.find_one({'_id': str(название)})['activations'] == 0:
                embed.description = f'{inter.author.mention}, **Этот** промокод больше не активен, так как количество использований, этого промокода, было исчерпано.'
                return await inter.send(embed = embed)
            
            cluster.sweetness.economy.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": +int(count)}})
            
            cluster.sweetness.promocode.update_one({"_id": str(inter.author.id)}, {"$push": {"activated_promo": str(название)}})
            cluster.sweetness.promocode.update_one({"_id": str(название)}, {"$inc": {"activations": -1}})

            activations = result['activations']

            embed.description=f'{inter.author.mention}, **Вы** успешно **активировали** промокод `{название}` и **получили** на свой счёт **{count}** <:amitobal:1158567849707716708>\n \
            Этот промокод можно будет ввести ещё {activations} раз'
            return await inter.send(ephemeral = True, embed = embed)

        else:
            embed.description = f"{inter.author.mention}, Такого **промокода не существует**!"
            return await inter.send(ephemeral = True, embed = embed)

    @commands.slash_command(name = 'addpromo',description="Добавить новый промокод")
    async def addpromo(inter, название, активации: int, сумма: int):
        embed = disnake.Embed(title = f"Добавить промокод", color = 3092790)

        if inter.author.id in [355027475870253058, 284010976313868288, 849353684249083914]:

            if cluster.sweetness.server_settings.count_documents({"_id": str(inter.guild.id)}) == 0:
                cluster.sweetness.server_settings.insert_one({"_id": str(inter.guild.id), "promocodes": []})

            cluster.sweetness.server_settings.update_one({"_id": str(inter.guild.id)}, {"$push": {"promocodes": str(название)}})
            cluster.sweetness.promocode.update_one({'_id': str(название)}, {'$set': {'activations': int(активации)}}, upsert = True)
            cluster.sweetness.promocode.update_one({'_id': str(название)}, {'$set': {'sum': int(сумма)}}, upsert = True)
            
            embed.description = f"{inter.author.mention}, **Вы** успешно добавили промокод **{название}**"
            await inter.send(embed = embed)

        else:

            await inter.send(embed = disnake.Embed(color = 3092790, description = 'У вас недостаточно прав на выполнение этой команды!', ))
    
    @commands.slash_command(name = 'removepromo', description="Удалить промокод")
    async def removepromo(inter, название):
        if inter.author.id in [854328227077160982, 673700626525454397, 849353684249083914]:
            cluster.sweetness.promocode.delete_one({'_id': str(название)})
            cluster.sweetness.server_settings.update_one({"_id": str(inter.guild.id)}, {"$pull": {"promocodes": str(название)}})

            await inter.send(embed = disnake.Embed(description = f'Вы успешно удалили промокод **{название}**', color = 3092790, ))

        else:

            embed = disnake.Embed(color = 3092790, description = f'{inter.author.mention}, У **Вас** недостаточно прав на выполнение этой команды!')
            await inter.send(embed = embed)
            
def setup(bot): 
    bot.add_cog(promocodes(bot))