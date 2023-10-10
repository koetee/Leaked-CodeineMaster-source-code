import pymongo
import disnake
import json
import datetime
from random import randint
from disnake.ext import commands

cluster = pymongo.MongoClient(f"mongodb://127.0.0.1/myFirstDatabase?retryWrites=true&w=majority")

files = cluster.sweetness.files

class GiftOpen(disnake.ui.View):

    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, emoji = ":3297blurpleone:1047233442363998280>", row = 0, custom_id = "1_gift"))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, emoji = "<:7036blurpletwo:1047233452522610789>", row = 0, custom_id = "2_gift"))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, emoji = "<:2742blurplethree:1047233465055182858>", row = 0, custom_id = "3_gift"))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.green, label = 'Посмотреть содержимое', custom_id = "info_gift", emoji = "<:INFO:824629055084298261>", row = 1))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.blurple, label = 'Хотите получать больше?', emoji = "<:buy1:1139161075552616530>", url = "https://discord.com/channels/1143903608946045048/1143903610489536620", row = 1))

class TimelyView(disnake.ui.View):

    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label = 'Хотите получать больше?', emoji = "<:buy1:1139161075552616530>", url = "https://discord.com/channels/1143903608946045048/1143903610489536620"))

class GiftsView(disnake.ui.View):

    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label = 'Получить подарок', custom_id = "take_gift", emoji = "<:giftbox:1110588981025972385>"))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label = 'Открыть подарок', custom_id = "see_gift", emoji = "<:giftbox:1110588981025972385>"))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.green, label = 'Посмотреть содержимое', custom_id = "info_gift", emoji = "<:INFO:824629055084298261>"))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.blurple, label = 'Хотите получать больше?', emoji = "<:buy1:1139161075552616530>", url = "https://discord.com/channels/1143903608946045048/1143903610489536620"))

class cog_gift(commands.Cog):
    def __init__(self, bot: commands.Bot(intents = disnake.Intents.all(), command_prefix="gifts!")):
        self.bot = bot
        
    @commands.slash_command(description = "Получить награду(раз в 12 часов)")
    async def timely(self, inter):
        if cluster.sweetness.gifts.count_documents({"_id": str(inter.author.id)}) == 0:
            cluster.sweetness.gifts.insert_one({"_id": str(inter.author.id), "timely": datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=5)})

        date_timely = cluster.sweetness.gifts.find_one({'_id': str(inter.author.id)})['timely']
        if date_timely > datetime.datetime.now():

            sec = date_timely - datetime.datetime.now()
            hours = (str(sec.seconds // 3600).split('.')[0])
            minutes = (str((sec.seconds % 3600) // 60).split('.')[0])
            seconds = (str(sec.seconds % 60).split('.')[0])

            embed = disnake.Embed(description=f"{inter.author.mention}, **Вы** уже **получали бонус**, приходите снова через **{hours}ч. {minutes}м. {seconds}с.**", color=3092790)
            embed.set_author(name = f"Временная награда | {inter.guild.name}", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            return await inter.send(embed = embed, ephemeral=True)
        
        new_date = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(hours=12)
        cluster.sweetness.gifts.update_one({'_id': str(inter.author.id)}, {'$set': {'timely': new_date}}, upsert = True)

        number = randint(25, 50)
        number_main = 0

        database = cluster.sweetness.sponsor
        groups = database.find()
        sponsors = []
        for group in groups:
            member = disnake.utils.get(inter.guild.members, id = int(group['_id']))
            if not member == None:
                sponsors.append(member.id)

        fast = database.find_one({'_id': str(inter.author.id)})

        if not inter.author.id in sponsors:
            up = "x1"
        else:
            x = fast['timely']
            number_main += number * int(x)
            up = f"x{x}"

        if number_main == 0:
            number_main += number

        embed = disnake.Embed(title = f"Временная награда — {inter.author}", description = f"{inter.author.mention}, **Вы** успешно **получили бонус** в размере **{number_main}** <:amitobal:1158567849707716708>", color = 3092790)
        embed.set_footer(text = f"Возвращайтесь через 12 часов | Умножение: {up}")
        embed.set_thumbnail(url = inter.author.display_avatar.url)
        await inter.send(embed = embed, view = TimelyView())

        if cluster.sweetness.economy.count_documents({"_id": str(inter.author.id)}) == 0:
            cluster.sweetness.economy.insert_one({"_id": str(inter.author.id),"balance": 0})
        if cluster.sweetness.count.count_documents({"_id": str(inter.author.id)}) == 0:
            cluster.sweetness.count.insert_one({"_id": str(inter.author.id), "daily": 0})
            
        cluster.sweetness.count.update_one({"_id": str(inter.author.id)}, {"$inc": {"daily": +1}})
        cluster.sweetness.economy.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": +int(number_main)}})

    @commands.slash_command(description = "Подарки")
    async def gift(self, inter):
        embed = disnake.Embed(description = f"{inter.author.mention}, **Выберите** действие", color = 3092790)
        embed.set_author(name = f"Подарки — {inter.author}", icon_url=inter.guild.icon.url)
        embed.set_thumbnail(url = inter.author.display_avatar.url)
        await inter.send(embed = embed, view = GiftsView())

    @commands.Cog.listener()
    async def on_button_click(self, inter):
    
        custom_id = inter.component.custom_id

        if custom_id.endswith("gift"):
            if custom_id == "take_gift":

                if cluster.sweetness.gift.count_documents({"_id": str(inter.author.id)}) == 0:
                    cluster.sweetness.gift.insert_one({"_id": str(inter.author.id), "gift": datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=5), "count": 0})

                date_timely = cluster.sweetness.gift.find_one({'_id': str(inter.author.id)})['gift']
                if date_timely > datetime.datetime.now():

                    sec = date_timely - datetime.datetime.now()
                    hours = (str(sec.seconds // 3600).split('.')[0])
                    minutes = (str((sec.seconds % 3600) // 60).split('.')[0])
                    seconds = (str(sec.seconds % 60).split('.')[0])

                    embed = disnake.Embed(description=f"{inter.author.mention}, **Вы** уже **получали бонус**, приходите снова через **{hours}ч. {minutes}м. {seconds}с.**", color=3092790)
                    embed.set_author(name = f"Подарки | {inter.guild.name}", icon_url = inter.guild.icon.url)
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    return await inter.send(embed = embed, ephemeral=True)

                new_date = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(hours=12)
                cluster.sweetness.gift.update_one({'_id': str(inter.author.id)}, {'$set': {'gift': new_date}}, upsert = True)

                if cluster.sweetness.count_gift.count_documents({"_id": str(inter.author.id)}) == 0:
                    cluster.sweetness.count_gift.insert_one({"_id": str(inter.author.id), "daily": 0})

                cluster.sweetness.count_gift.update_one({"_id": str(inter.author.id)}, {"$inc": {"daily": +1}})
                cluster.sweetness.gift.update_one({"_id": str(inter.author.id)}, {"$inc": {"count": +1}})

                embed = disnake.Embed(description = f"{inter.author.mention}, **Вы** успешно **получили подарок**", color = 3092790)
                embed.set_author(name = f"Подарки — {inter.author}", icon_url=inter.guild.icon.url)
                embed.set_footer(text = f"Возвращайтесь через 24 часа")
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.response.edit_message(embed = embed, view = GiftsView())

            if custom_id == 'see_gift':
                embed = disnake.Embed(color = 3092790)
                embed.set_author(name = f"Открыть подарок | {inter.guild.name}", icon_url = inter.guild.icon.url)
                embed.description = f"### {inter.author.mention}, Выберите подарок, в котором, по вашему мнению, скрывается ценный приз."
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.response.edit_message(file = disnake.File("podarki.png"), embed = embed, view = GiftOpen())

            if custom_id == 'info_gift':
                embed = disnake.Embed(color = 3092790)
                embed.set_author(name = f"Содержимое подарка | {inter.guild.name}", icon_url = inter.guild.icon.url)
                embed.description = "- Что может выпасть из подарка:\n * Личная комната\n * Монеты 100\n * Монеты 250\n * Монеты 350\n * Монеты 500\n * Кейс"
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            await inter.response.defer()
            case_count = cluster.sweetness.gift.find_one({'_id': str(inter.author.id)})['count']

            if 1 > int(case_count) or 1 < 1:
                embed = disnake.Embed(title=f'Открытие подарка — {inter.author}', description=f'{inter.author.mention}, {"У Вас нету столько подарков!" if 1 > int(case_count) else "Нельзя открыть отрицательное число кейсов!"}', color=3092790)
                embed.set_thumbnail(url=inter.author.display_avatar.url)
                embed.set_footer(text=f'Запросил(а) {inter.author}', icon_url=inter.author.display_avatar.url)
                return await inter.send(content=inter.author.mention, ephemeral=True, embed=embed)

            cluster.sweetness.gift.update_one(
                {'_id': str(inter.author.id)},
                {'$inc': {'count': -1}}
            )

            number_of_random = randint(0, 10000)
            prize = ""

            if number_of_random > 10000:
                prize = "Монетки 100"
            elif number_of_random > 8000:
                prize = "Монетки 250"
            elif number_of_random > 4000:
                prize = "Монетки 350"
            else:
                prize = "Монетки 500"
            input = datetime.datetime.now()
            data = int(input.timestamp())
            cluster.sweetness.history_gift.update_one({"_id": str(inter.author.id)}, {"$push": {"data": f"<t:{data}:F>"}})

            if prize == "Монетки 100":
                cluster.sweetness.history_gift.update_one({"_id": str(inter.author.id)}, {"$push": {"prize": f"Монетки 100"}})
                cluster.sweetness.economy.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": +200}})
            elif prize == "Монетки 250":
                cluster.sweetness.history_gift.update_one({"_id": str(inter.author.id)}, {"$push": {"prize": f"Монетки 250"}})
                cluster.sweetness.economy.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": +250}})
            elif prize == "Монетки 350":
                cluster.sweetness.history_gift.update_one({"_id": str(inter.author.id)}, {"$push": {"prize": f"Монетки 350"}})
                cluster.sweetness.economy.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": +350}})
            elif prize == "Монетки 500":
                cluster.sweetness.history_gift.update_one({"_id": str(inter.author.id)}, {"$push": {"prize": f"Монетки 500"}})
                cluster.sweetness.economy.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": +500}})

            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = f"Открыть подарок | {inter.guild.name}", icon_url = inter.guild.icon.url)
            
            embed.set_thumbnail(url = inter.author.display_avatar.url)

            if custom_id == "1_gift":
                embed.description = f"### {inter.author.mention}, Вы успешно открыли первый подарок и вам выпало {prize}"
            elif custom_id == "2_gift":
                embed.description = f"### {inter.author.mention}, Вы успешно открыли первый подарок и вам выпало {prize}"
            elif custom_id == "3_gift":
                embed.description = f"### {inter.author.mention}, Вы успешно открыли первый подарок и вам выпало {prize}"

            await inter.message.edit(attachments = None, embed = embed, components = [])

def setup(bot): 
    bot.add_cog(cog_gift(bot))