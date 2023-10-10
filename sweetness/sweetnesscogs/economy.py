import pymongo
import disnake
import asyncio
import datetime
import json
import random
import time
from disnake import Localized
from random import randint
from disnake.ext import commands
from disnake.enums import ButtonStyle, TextInputStyle
import imghdr
import requests

intermessage_id = {}
profile_user = {}
summa = {}

cluster = pymongo.MongoClient(f"mongodb://127.0.0.1/myFirstDatabase?retryWrites=true&w=majority")

files = cluster.sweetness.files
economy = cluster.sweetness.economy

def hex_to_rgb(value):
    value = value.lstrip('#')
    RGB = list(tuple(int(value[i:i + len(value) // 3], 16) for i in range(0, len(value), len(value) // 3)))
    return (RGB[0]<<16) + (RGB[1]<<8) + RGB[2]

min = 60
hour = 60 * 60
day = 60 * 60 * 24

class BalanceView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        
        shop_data = files.find_one({"_id": "shop"})
        emoji_take = shop_data.get("emoji_take", "<:dney:1153488333570314290>") if shop_data else "<:dney:1153488333570314290>"
        
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label='Купить валюту', emoji=emoji_take, url="https://discord.com/channels/1143903608946045048/1143903610489536620"))
        self.add_item(MainProfileButtons())


class BalanceBack(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="Назад", custom_id="back_balance", emoji=f'{files.find_one({"_id": "back"})["emoji_take"]}'))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="Выход", custom_id="exit_profile", emoji=f'{files.find_one({"_id": "basket"})["emoji_take"]}'))

class InformationProfile(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="Назад", custom_id="back_balance", emoji=f'{files.find_one({"_id": "back"})["emoji_take"]}'))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="Выход", custom_id="exit_profile", emoji=f'{files.find_one({"_id": "basket"})["emoji_take"]}'))

class DuelButton(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="Принять", custom_id="yesduel", emoji=f'{files.find_one({"_id": "accept"})["emoji_take"]}'))

class Orel(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="Присоединиться", custom_id="invite_orel", emoji=f'{files.find_one({"_id": "duel"})["emoji_take"]}'))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="Удалить", custom_id="delete", emoji=f'{files.find_one({"_id": "basket"})["emoji_take"]}'))

class Reshka(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="Присоединиться", custom_id="invite_reshka", emoji=f'{files.find_one({"_id": "duel"})["emoji_take"]}'))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="Удалить", custom_id="delete", emoji=f'{files.find_one({"_id": "basket"})["emoji_take"]}'))

class MainProfileButtons(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Другое",
            options = [
                disnake.SelectOption(label="Информация", description="Информация", value = "information_user", emoji=f'{files.find_one({"_id": "information"})["emoji_take"]}'),
                disnake.SelectOption(label="Доходы", description="Доходы", value = "doxod", emoji=f'{files.find_one({"_id": "slide_u"})["emoji_take"]}'),
                disnake.SelectOption(label="Расходы", description="Расходы", value = "rasxod", emoji=f'{files.find_one({"_id": "slide_d"})["emoji_take"]}'),
                disnake.SelectOption(label="Выход", description="Удалить это сообщение", value = "exit_role", emoji=f'{files.find_one({"_id": "basket"})["emoji_take"]}'),
            ],
        )

class economycog(commands.Cog):
    def __init__(self, bot: commands.Bot(intents = disnake.Intents.all(), command_prefix="!")):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def asd(self, inter):
        await inter.message.delete()
        embed = disnake.Embed(color = 3092790, description = '**Уважаемые участники,**\n\nДоброго времени суток! Мы рады поделиться с вами захватывающей **новостью** на нашем сервере. Мы представляем вам **нового экономического бота**, который обогатит ваш опыт в нашем сообществе. Этот бот предоставляет множество уникальных **команд и функций**, которые позволят вам разнообразить свой виртуальный мир.\n\nВ честь этой **важной новости**, мы предоставляем вам эксклюзивный **промокод "SweetnessBotUpdateWave"**, который дарит вам целых **1500 серверных монет**. С этой валютой у вас появляется множество **возможностей**: создайте стильную **лав-руму**, сохраните монеты для будущих покупок\n\nНе упустите этот **шанс** улучшить ваше виртуальное присутствие на сервере и создать уникальные впечатления. **Спасибо** вам за ваше активное участие в жизни сообщества!\n\nПриятного **времяпрепровождения** на **сервере**.')
        embed.set_author(name = inter.author, icon_url = inter.author.display_avatar.url)
        embed.set_thumbnail(url = inter.guild.icon.url)
        await inter.send(content = "@everyone", embed = embed)

    @commands.slash_command(description = "Проверить баланс")
    async def balance(self, inter, пользователь:disnake.Member = None):
        if пользователь == inter.author or пользователь == None: 
            пользователь = inter.author

        profile_user[inter.author.id] = пользователь.id

        if cluster.sweetness.economy.count_documents({"_id": str(пользователь.id)}) == 0: 
            cluster.sweetness.economy.insert_one({"_id": str(пользователь.id), "balance": 0})

        if cluster.sweetness.donate.count_documents({"_id": str(пользователь.id)}) == 0: 
            cluster.sweetness.donate.insert_one({"_id": str(пользователь.id), "donate_balance": 0})

        embed = disnake.Embed(color = 3092790)
        embed.set_author(name = f"Текущий баланс — {пользователь}", icon_url = inter.guild.icon.url)
        embed.add_field(name = f"<:amitobal:1158567849707716708> **Баланс:**", value = f'```{cluster.sweetness.economy.find_one({"_id": str(пользователь.id)})["balance"]}```')
        embed.add_field(name = f"<:donateamito:1158567848080310343> **Донат:**", value = f'```{cluster.sweetness.donate.find_one({"_id": str(пользователь.id)})["donate_balance"]}```')
        embed.set_footer(text = f"Запросил(а) {inter.author}", icon_url = inter.author.display_avatar.url)
        embed.set_thumbnail(url=пользователь.display_avatar.url)
        await inter.send(inter.author.mention, embed = embed, view = BalanceView())

    @commands.slash_command(description = "Посмотреть количество времени, которое вы просидели в войсе")
    async def online(inter, пользователь:disnake.Member = None):
        if пользователь == inter.author or пользователь == None:
            пользователь = inter.author

        if cluster.sweetness.online.count_documents({"_id": str(пользователь.id)}) == 0:
            cluster.sweetness.online.insert_one({"_id": str(пользователь.id),"online": 0})

        if cluster.sweetness.day.count_documents({"_id": str(пользователь.id)}) == 0:
            cluster.sweetness.day.insert_one({"_id": str(пользователь.id),"day": 0})
 
        online = cluster.sweetness.online.find_one({"_id": str(пользователь.id)})["online"]
        days = cluster.sweetness.day.find_one({"_id": str(пользователь.id)})["day"]
        
        embed = disnake.Embed(color = 3092790)
        embed.set_author(name = f"Голосовой онлайн — {пользователь} | {inter.guild.name}", icon_url = inter.guild.icon.url)
        embed.add_field(name = f"<:date:1117749277402349608> **За все время:**", value = f"```{online // 86400}д. {online // hour}ч. {(online - (online // hour * hour)) // 60}м. {online - ((online // hour * hour) + ((online - (online // hour * hour)) // 60 * min))}с.```")
        embed.add_field(name = f":date: **За неделю:**", value = f"```{days // hour}ч. {(days - (days // hour * hour)) // 60}м. {days - ((days // hour * hour) + ((days - (days // hour * hour)) // 60 * min))}с.```")
        embed.set_thumbnail(url = пользователь.display_avatar.url)
        embed.set_footer(text = f"Запросил(а) {inter.author}", icon_url = inter.author.display_avatar.url)
        await inter.send(embed = embed)

    @commands.slash_command(description = "Посмотреть аватар")
    async def avatar(inter, member:disnake.Member):
        embed = disnake.Embed(description=f"**Аватар пользователя** {member.mention}",color=3092790)
        embed.set_author(name = inter.author, icon_url = inter.author.display_avatar.url)
        embed.set_image(url = member.display_avatar.url)
        await inter.send(embed = embed)

    @commands.slash_command(description="Посмотреть баннер")
    async def banner(self, inter, member: disnake.Member):
        req = await self.bot.http.request(disnake.http.Route("GET", "/users/{uid}", uid=member.id))
        banner_id = req["banner"]
        if banner_id:
            banner_url = f"https://cdn.discordapp.com/banners/{member.id}/{banner_id}"
            response = requests.get(banner_url)
            if response.status_code == 200:
                banner_type = imghdr.what(None, h=response.content)
                if banner_type == "gif":
                    banner_url += ".gif"
                elif banner_type == "png":
                    banner_url += ".png"
                else:
                    await inter.send("Не удалось определить тип баннера.")
                    return
                embed = disnake.Embed(color=3092790)
                embed.set_author(name=f"Баннер пользователя {member}", icon_url = member.guild.icon.url)
                embed.set_footer(text = f"Запросил(а) {inter.author}", icon_url = inter.author.display_avatar.url)
                embed.set_image(url=banner_url)
                await inter.send(embed=embed)
            else:
                await inter.send("Не удалось загрузить баннер.")
        else:
            await inter.send("У данного пользователя нет баннера.")

    @commands.slash_command(description = "Бросить вызов на бабки")
    async def duel(self, inter, ставка:int, пользователь: disnake.Member):

        if cluster.sweetness.economy.count_documents({"_id": str(inter.author.id)}) == 0:
            cluster.sweetness.economy.insert_one({"_id": str(inter.author.id), "balance": 0})

        if cluster.sweetness.economy.count_documents({"_id": str(пользователь.id)}) == 0:
            cluster.sweetness.economy.insert_one({"_id": str(пользователь.id), "balance": 0})

        embed = disnake.Embed(color=3092790)
        embed.set_thumbnail(url = inter.author.display_avatar.url)
        embed.set_author(name = f"Дуэль {inter.guild}", icon_url = inter.guild.icon.url)

        if ставка < 0:
            embed.description=f"{inter.author.mention}, **Нельзя** указать сумму **ниже ноля**"
            return await inter.send(ephemeral = True, embed=embed)

        elif ставка > 4999:
            embed.description=f"{inter.author.mention}, **Нельзя** указать **сумму** больше 4999 <:amitobal:1158567849707716708>"
            return await inter.send(ephemeral = True, embed=embed)

        elif ставка < 50:
            embed.description=f"{inter.author.mention}, **Нельзя** указать **сумму ниже** 50 <:amitobal:1158567849707716708>"
            return await inter.send(ephemeral = True, embed=embed)

        elif ставка > int(economy.find_one({"_id": str(inter.author.id)})["balance"]):
            embed.description=f"{inter.author.mention}, У **Вас** на балансе недостаточно средств!"
            return await inter.send(ephemeral = True, embed=embed)

        elif ставка > int(economy.find_one({"_id": str(пользователь.id)})["balance"]):
            embed.description=f"У {пользователь.mention} на балансе **недостаточно средств**"
            return await inter.send(ephemeral = True, embed=embed)

        embed.description = f"{inter.author.mention} **Вызывает** на дуэль {пользователь.mention}, " \
                            f"**воспользуйтесь** реакциями для ответа\nСтавка: **{ставка}** <:amitobal:1158567849707716708> "
        await inter.send(пользователь.mention, embed=embed, view=DuelButton())
        intermessage_id[пользователь.id] = inter.author.id
        summa[пользователь.id] = ставка

    @commands.slash_command(description="Подбросить монетку")
    async def flip(self, inter, ставка: int,
                   выбери: str = commands.Param(choices=[Localized("Орел", key="A"), Localized("Решка", key="A")])):

        if economy.count_documents({"_id": str(inter.author.id)}) == 0:
            economy.insert_one({"_id": str(inter.author.id), "balance": 0})

        embed = disnake.Embed(description=f"{inter.author.mention}, **Нельзя** указать **сумму** больше 4999 <:amitobal:1158567849707716708> ", color=3092790)
        embed.set_thumbnail(url = inter.author.display_avatar.url)
        embed.set_author(name = "Орел и Решка", icon_url = inter.author.display_avatar.url)

        if ставка < 0:
            embed.description=f"{inter.author.mention}, **Нельзя** указать сумму **ниже ноля**"
            return await inter.send(embed=embed)

        elif ставка > 4999:
            embed.description=f"{inter.author.mention}, **Нельзя** указать **сумму** больше 4999 <:amitobal:1158567849707716708>"
            return await inter.send(embed=embed)

        elif ставка < 50:
            embed.description=f"{inter.author.mention}, **Нельзя** указать **сумму ниже** 50 <:amitobal:1158567849707716708>"
            return await inter.send(embed=embed)

        elif ставка > int(economy.find_one({"_id": str(inter.author.id)})["balance"]):
            embed.description=f"{inter.author.mention}, У **Вас** на балансе недостаточно средств!"
            return await inter.send(embed=embed)

        embed.description=f"{inter.author.mention}, **Вы** успешно создали игру **Орел и Решка**"
        await inter.send(ephemeral=True, embed=embed)

        if выбери == "Орел":
            embed.description=f"{inter.author.mention}, ставит {ставка}<:amitobal:1158567849707716708>  на **Орел!**\nЧтобы принять **вызов** нажми на кнопку ниже."
            msg = await inter.channel.send(inter.author.mention, embed=embed, view=Orel())

        if выбери == "Решка":
            embed.description=f"{inter.author.mention}, ставит {ставка}<:amitobal:1158567849707716708>  на **Решка!**\nЧтобы принять вызов нажми на кнопку ниже."
            msg = await inter.channel.send(inter.author.mention, embed=embed, view=Reshka())

        intermessage_id[msg.id] = int(inter.author.id)
        summa[msg.id] = ставка

    @commands.slash_command(description = 'Передать валюту пользователю')
    async def give(self, inter, пользователь: disnake.Member, сумма):

        await inter.response.defer()

        embed = disnake.Embed(color = 3092790)
        embed.set_thumbnail(url = inter.author.display_avatar.url)
        embed.set_author(name = f"Передать валюту | {inter.guild.name}", icon_url = inter.guild.icon.url)

        if пользователь == inter.author:
            embed.description = f'{inter.author.mention}, **Вы** не можете передать валюту **самому себе!**'
            return await inter.send(embed = embed)

        if int(сумма) > int(economy.find_one({'_id': str(inter.author.id)})['balance']):
            embed.description = f'{inter.author.mention}, У **Вас** на балансе **недостаточно средств** для совершения этой **операции**.'
            return await inter.send(embed = embed)

        if int(сумма) < 0 or int(сумма) == 0:
            embed.description = f'{inter.author.mention}, **Нельзя** перевести **отрицитательную сумму** или сумму которая **равна нулю**.'
            return await inter.send(embed = embed)
        
        db = cluster.sweetness
        history_transactions = db.history_transactions
        history = db.history
        history_win = db.history_win

        if economy.count_documents({"_id": str(inter.author.id)}) == 0:
            economy.insert_one({"_id": str(inter.author.id), "balance": 0})
            
        if economy.count_documents({"_id": str(пользователь.id)}) == 0:
            economy.insert_one({"_id": str(пользователь.id),"balance": 0})

        economy.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": -int(сумма)}})
        economy.update_one({"_id": str(пользователь.id)}, {"$inc": {"balance": +int(сумма)}})

        if history.count_documents({"_id": str(пользователь.id)}) == 0: 
            history.insert_one({"_id": str(пользователь.id), "casino": 0, "items": 0, "roles": 0, "pay": 0, "loverooms": 0, "clan": 0})
        if history.count_documents({"_id": str(inter.author.id)}) == 0: 
            history.insert_one({"_id": str(inter.author.id), "casino": 0, "items": 0, "roles": 0, "pay": 0, "loverooms": 0, "clan": 0})

        if history_transactions.count_documents({"_id": str(inter.author.id)}) == 0:
            history_transactions.insert_one({"_id": str(inter.author.id), "tip_data": [], "msg_sum": [], "moderator": [], "perevodov": 0, "pereveli": 0})
        if history_transactions.count_documents({"_id": str(пользователь.id)}) == 0:
            history_transactions.insert_one({"_id": str(пользователь.id), "tip_data": [], "msg_sum": [], "moderator": [], "perevodov": 0, "pereveli": 0})

        if history.count_documents({"_id": str(inter.author.id)}) == 0: 
            history.insert_one({"_id": str(inter.author.id), "casino": 0, "items": 0, "roles": 0, "pay": 0, "loverooms": 0, "clan": 0})

        if history_win.count_documents({"_id": str(пользователь.id)}) == 0:
            history_win.insert_one({"_id": str(пользователь.id), "active": 0, "giveaway": 0, "roles": 0, "promocode": 0, "clan": 0, "gifts": 0, "casino": 0, "transfer": 0, "events": 0})

        history_transactions.update_one({"_id": str(inter.author.id)}, {"$push": {"tip_data": f"Перевел | `{datetime.datetime.now().strftime('%d.%m.%Y')}`"}})
        history_transactions.update_one({"_id": str(inter.author.id)}, {"$push": {"msg_sum": f"None | {сумма} <:amitobal:1158567849707716708>"}})
        history_transactions.update_one({"_id": str(inter.author.id)}, {"$push": {"moderator": int(пользователь.id)}})

        history_transactions.update_one({"_id": str(пользователь.id)}, {"$push": {"tip_data": f"Перевод | `{datetime.datetime.now().strftime('%d.%m.%Y')}`"}})
        history_transactions.update_one({"_id": str(пользователь.id)}, {"$push": {"msg_sum": f"None | {сумма} <:amitobal:1158567849707716708>"}})
        history_transactions.update_one({"_id": str(пользователь.id)}, {"$push": {"moderator": int(inter.author.id)}})

        history_transactions.update_one({"_id": str(inter.author.id)}, {"$inc": {"perevodov": +int(1)}})
        history_transactions.update_one({"_id": str(пользователь.id)}, {"$inc": {"pereveli": +int(1)}})

        history.update_one({"_id": str(inter.author.id)}, {"$inc": {"pay": +int(сумма)}})
        history_win.update_one({"_id": str(пользователь.id)}, {"$inc": {"transfer": +int(сумма)}})

        embed.description=f'{inter.author.mention} **Передал(а)** {пользователь.mention} **{int(сумма)}** <:amitobal:1158567849707716708>'
        await inter.send(content = пользователь.mention, embed = embed)

    @commands.Cog.listener()
    async def on_dropdown(self, inter):
        custom_id = inter.values[0]

        if custom_id == "information_user":
            if inter.message.content != inter.author.mention:
                embed = disnake.Embed(description=f"{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**", color=3092790)
                embed.set_author(name = "Информация", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url=inter.author.display_avatar.url)
                return await inter.send(ephemeral=True, embed=embed)

            пользователь = disnake.utils.get(inter.guild.members, id=int(profile_user[inter.author.id]))

            await inter.response.defer()

            db = cluster.sweetness
            message = db.message
            online = db.online

            if economy.count_documents({"_id": str(пользователь.id)}) == 0: 
                economy.insert_one({"_id": str(пользователь.id), "balance": 0})
            if online.count_documents({"_id": str(пользователь.id)}) == 0: 
                online.insert_one({"_id": str(пользователь.id), "online": 0})
            if message.count_documents({"_id": str(пользователь.id)}) == 0: 
                message.insert_one({"_id": str(пользователь.id), "message_count": 0})

            topbalance = next((index + 1 for index, x in enumerate(economy.find().sort("balance", -1)) if str(x["_id"]) == str(пользователь.id)), 0)
            topmsg = next((index + 1 for index, x in enumerate(message.find().sort("message_count", -1)) if str(x["_id"]) == str(пользователь.id)), 0)
            topvoice = next((index + 1 for index, x in enumerate(online.find().sort("online", -1)) if str(x["_id"]) == str(пользователь.id)), 0)

            joined = str(int(пользователь.joined_at.timestamp()))
            created = str(int(пользователь.created_at.timestamp()))

            balance = economy.find_one({"_id": str(пользователь.id)})["balance"]
            message = message.find_one({"_id": str(пользователь.id)})["message_count"]
            online = online.find_one({"_id": str(пользователь.id)})["online"]

            point = "<:to4kaaa:948159896979922966>"

            embed = disnake.Embed(description=f"{point} ID: **{пользователь.id}**", color=3092790)
            embed.set_thumbnail(url=inter.guild.icon.url)
            embed.set_author(name = f"Карточка пользователя — {пользователь}", icon_url = пользователь.display_avatar.url)

            embed.add_field(name="<:amitobal:1158567849707716708> Баланс", value=f"```{balance}```")
            embed.add_field(name="<:message1:1139168204191694878> Сообщений", value=f"```{message}```")
            embed.add_field(name="<:online:1139167847982059561> Онлайн", value=f"```{online // hour}ч. {(online - (online // hour * hour)) // 60}м. {online - ((online // hour * hour) + ((online - (online // hour * hour)) // 60 * min))}с.```")

            mb = len(inter.guild.members)
            value = f"> <:online:1139167847982059561> По войсу **{topvoice}** из **{mb}**\n \
            > <:message1:1139168204191694878> По сообщениям **{topmsg}** из **{mb}**\n> <:amitobal:1158567849707716708> По балансу **{topbalance}** из **{mb}**"
            embed.add_field(name="<:pencil1:1139168201079533689> Создал аккаунт", value=f'<t:{created}> (<t:{created}:R>)')
            embed.add_field(name="<:date1:1139169091840655421> Присоединился", value=f'<t:{joined}> (<t:{joined}:R>)')
            embed.add_field(name="<:top1:1139161095265853460> Место в топе", value=value, inline = True)
            await inter.message.edit(embed=embed, view = BalanceBack())

        if custom_id == "rasxod":
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(color = 3092790)
                embed.set_author(name = "Расход", icon_url = inter.guild.icon.url)
                embed.description = f"{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**"
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            
            пользователь = disnake.utils.get(inter.guild.members, id=int(profile_user[inter.author.id]))
            if cluster.sweetness.history.count_documents({"_id": str(пользователь.id)}) == 0: 
                cluster.sweetness.history.insert_one({"_id": str(пользователь.id), "casino": 0, "items": 0, "roles": 0, "pay": 0, "loverooms": 0, "clan": 0})

            expenses = cluster.sweetness.history.find_one({"_id": str(пользователь.id)})

            casino = expenses["casino"]
            items = expenses["items"]
            roles = expenses["roles"]
            transfer = expenses["pay"]
            loverooms = expenses["loverooms"]
            clan = expenses["clan"]
            general = int(casino) + int(items) + int(roles) + int(roles) + int(transfer) + int(loverooms) + int(clan)
            embed = disnake.Embed(title = f"Расходы пользователя {пользователь}", color = 3092790)
            if casino == 0:
                casino_percent = 0
            else:
                casino_percent = 100 * float(casino) / float(general)
            if items == 0:
                items_percent = 0
            else:
                items_percent = 100 * float(items) / float(general)
            if roles == 0:
                roles_percent = 0
            else:
                roles_percent = 100 * float(roles) / float(general)
            if transfer == 0:
                transfer_percent = 0
            else:
                transfer_percent = 100 * float(transfer) / float(general)
            if loverooms == 0:
                loverooms_percent = 0
            else:
                loverooms_percent = 100 * float(loverooms) / float(general)
            if clan == 0:
                clan_percent = 0
            else:
                clan_percent = 100 * float(clan) / float(general)

            embed.add_field(name = "> Поражения в играх", value = f"```{casino} 💰 ({casino_percent:.2f}%)```")
            embed.add_field(name = "> Кланы", value = f"```{clan} 💰 ({clan_percent:.2f}%)```")
            embed.add_field(name = "> Лаврумы", value = f"```{loverooms} 💰 ({loverooms_percent:.2f}%)```")
            embed.add_field(name = "> Личные роли", value = f"```{roles} 💰 ({roles_percent:.2f}%)```")
            embed.add_field(name = "> Переводы", value = f"```{transfer} 💰 ({transfer_percent:.2f}%)```")
            embed.add_field(name = "> Покупки товаров", value = f"```{items} 💰 ({items_percent:.2f}%)```")
            embed.set_footer(text = f"Общие расходы {general} 💰", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = пользователь.display_avatar.url)
            await inter.response.edit_message(embed = embed, view = BalanceBack())
        
        if custom_id == "doxod":
            if inter.message.content != inter.author.mention:
                embed = disnake.Embed(color=3092790)
                embed.set_author(name = "Доход", icon_url = inter.guild.icon.url)
                embed.description = f"{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**"
                embed.set_thumbnail(url=inter.author.display_avatar.url)
                return await inter.send(ephemeral=True, embed=embed)
            
            пользователь = disnake.utils.get(inter.guild.members, id=int(profile_user[inter.author.id]))
            if cluster.sweetness.history_win.count_documents({"_id": str(пользователь.id)}) == 0:
                cluster.sweetness.history_win.insert_one({
                    "_id": str(пользователь.id),
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

            income = cluster.sweetness.history_win.find_one({"_id": str(пользователь.id)})

            active = income["active"]
            giveaway = income["giveaway"]
            roles = income["roles"]
            promocode = income["promocode"]
            clan = income["clan"]
            gifts = income["gifts"]
            casino = income["casino"]
            transfer = income["transfer"]
            events = income["events"]
            general = int(active) + int(giveaway) + int(roles) + int(promocode) + int(clan) + int(gifts) + int(casino) + int(transfer) + int(events)

            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = f"Доходы пользователя {пользователь} | {inter.guild.name}", icon_url = inter.guild.icon.url)
            if active == 0:
                active_percent = 0
            else:
                active_percent = 100 * float(active) / float(general)
            if giveaway == 0:
                giveaway_procent = 0
            else:
                giveaway_procent = 100 * float(giveaway) / float(general)
            if roles == 0:
                roles_percent = 0
            else:
                roles_percent = 100 * float(roles) / float(general)
            if promocode == 0:
                promocode_percent = 0
            else:
                promocode_percent = 100 * float(promocode) / float(general)
            if clan == 0:
                clan_percent = 0
            else:
                clan_percent = 100 * float(clan) / float(general)
            if gifts == 0:
                gifts_percent = 0
            else:
                gifts_percent = 100 * float(gifts) / float(general)
            if casino == 0:
                casino_percent = 0
            else:
                casino_percent = 100 * float(casino) / float(general)
            if transfer == 0:
                transfer_percent = 0
            else:
                transfer_percent = 100 * float(transfer) / float(general)
            if events == 0:
                events_percent = 0
            else: 
                events_percent = 100 * float(events) / float(general)

            embed.add_field(name = "> Ивенты", value = f"```{events} 💰 ({events_percent:.2f}%)```")
            embed.add_field(name = "> Розыгрыши", value = f"```{giveaway} 💰 ({giveaway_procent:.2f}%)```")
            embed.add_field(name = "> Промокоды", value = f"```{promocode} 💰 ({promocode_percent:.2f}%)```")
            embed.add_field(name = "> Кланы", value = f"```{clan} 💰 ({clan_percent:.2f}%)```")
            embed.add_field(name = "> Временные награды", value = f"```{gifts} 💰 ({gifts_percent:.2f}%)```")
            embed.add_field(name = "> Актив", value = f"```{active} 💰 ({active_percent:.2f}%)```")
            embed.add_field(name = "> Переводы", value = f"```{transfer} 💰 ({transfer_percent:.2f}%)```")
            embed.add_field(name = "> Продажа ролей", value = f"```{roles} 💰 ({roles_percent:.2f}%)```")
            embed.add_field(name = "> Победы в играх", value = f"```{casino} 💰 ({casino_percent:.2f}%)```")

            embed.set_footer(text = f"Общие доходы {general} 💰", icon_url = inter.guild.icon.url)

            embed.set_thumbnail(url=пользователь.display_avatar.url)
            await inter.response.edit_message(embed=embed, view=BalanceBack())

    @commands.Cog.listener()
    async def on_button_click(self, inter):

        custom_id = inter.component.custom_id

        if custom_id == "back_balance":
            пользователь = disnake.utils.get(inter.guild.members, id = int(profile_user[inter.author.id]))
            
            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = f"Текущий баланс — {пользователь} | {inter.guild.name}", icon_url = inter.guild.icon.url)
            embed.add_field(name = f"<:amitobal:1158567849707716708> **Баланс:**", value = f'```{economy.find_one({"_id": str(пользователь.id)})["balance"]}```')
            embed.set_footer(text = f"Запросил(а) {inter.author}", icon_url = inter.author.display_avatar.url)
            embed.set_thumbnail(url=пользователь.display_avatar.url)
            await inter.response.edit_message(embed = embed, view = BalanceView())

        if custom_id[:6] == "invite":
            пользователь = intermessage_id[inter.message.id]

            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = f"Орел и Решка | {inter.guild.name}", icon_url = inter.guild.icon.url)

            if пользователь == inter.author.id:
                embed.description = f"{inter.author.mention}, **Вы** не можете принять свою же **ставку!**"
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)

            number = randint(1, 2)
            ставка = int(summa[inter.message.id])

            if custom_id == "invite_orel":
                #пользователь = "Орел"
                if int(ставка) > int(economy.find_one({"_id": str(inter.author.id)})["balance"]):
                    embed.description = f"{inter.author.mention}, У **Вас** на балансе недостаточно средств!"
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    return await inter.send(ephemeral = True, embed = embed)
                if int(ставка) > int(economy.find_one({"_id": str(пользователь)})["balance"]):
                    embed.description = f"У <@{пользователь}> на балансе недостаточно средств!"
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    return await inter.send(ephemeral = True, embed = embed)
                if number == 1:
                
                    economy.update_one({"_id": str(пользователь)}, {"$inc": {"balance": -int(ставка)}})
                    economy.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": +int(ставка)}})

                    cluster.sweetness.history.update_one({"_id": str(пользователь)}, {"$inc": {"casino": +int(ставка)}})
                    cluster.sweetness.history_win.update_one({"_id": str(inter.author.id)}, {"$inc": {"casino": +int(ставка)}})

                    embed.description = f"**Орел** — <@{пользователь}>\n**Решка** — {inter.author.mention}"
                    embed.set_image(url = "https://media.discordapp.net/attachments/871820381797908500/877885522356351027/90970bf6eb2dd868.gif") # Решка
                    await inter.message.edit(embed = embed, components=[])
                    await asyncio.sleep(5)
                    embed = disnake.Embed(description=f"В битве между {inter.author.mention} и <@{пользователь}>\n**стал победителем** {inter.author.mention}, его выигрыш {int(ставка)} <:amitobal:1158567849707716708> ",color=3092790)
                    embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/1134137639428173884/1146123478559371424/duel.png")
                    embed.set_author(name = f"Орел и Решка | {inter.guild.name}", icon_url = inter.guild.icon.url)
                    return await inter.message.edit(embed = embed)
                elif number == 2:
                    
                    economy.update_one({"_id": str(пользователь)}, {"$inc": {"balance": +int(ставка)}})
                    economy.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": -int(ставка)}})

                    cluster.sweetness.history_win.update_one({"_id": str(пользователь)}, {"$inc": {"casino": +int(ставка)}})
                    cluster.sweetness.history.update_one({"_id": str(inter.author.id)}, {"$inc": {"casino": +int(ставка)}})

                    embed.description = f"**Орел** — <@{пользователь}>\n**Решка** — {inter.author.mention}"
                    embed.set_image(url = "https://media.discordapp.net/attachments/871820381797908500/877885120244224031/e286ab8ddbf4c2af.gif") # Орёл
                    await inter.message.edit(embed = embed, components=[])
                    await asyncio.sleep(5)
                    embed = disnake.Embed(description=f"В битве между {inter.author.mention} и <@{пользователь}>\n**стал победителем** <@{пользователь}>, его выигрыш {int(ставка)} <:amitobal:1158567849707716708> ",color=3092790)
                    embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/1134137639428173884/1146123478559371424/duel.png")
                    embed.set_author(name = f"Орел и Решка | {inter.guild.name}", icon_url = inter.guild.icon.url)
                    return await inter.message.edit(embed = embed)
            if custom_id == "invite_reshka":
                #пользователь = "Решка"
                if int(ставка) > int(economy.find_one({"_id": str(inter.author.id)})["balance"]):
                    embed.description = f"{inter.author.mention}, У **Вас** на балансе недостаточно средств!"
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    return await inter.send(ephemeral = True, embed = embed)
                if int(ставка) > int(economy.find_one({"_id": str(пользователь)})["balance"]):
                    embed.description = f"У <@{пользователь}> на балансе недостаточно средств!"
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    return await inter.send(ephemeral = True, embed = embed)
                if number == 1:
                
                    economy.update_one({"_id": str(пользователь)}, {"$inc": {"balance": +int(ставка)}})
                    economy.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": -int(ставка)}})

                    cluster.sweetness.history_win.update_one({"_id": str(пользователь)}, {"$inc": {"casino": +int(ставка)}})
                    cluster.sweetness.history.update_one({"_id": str(inter.author.id)}, {"$inc": {"casino": +int(ставка)}})

                    embed.description = f"**Решка** — <@{пользователь}>\n**Орёл** — {inter.author.mention}"
                    embed.set_image(url = "https://media.discordapp.net/attachments/871820381797908500/877885522356351027/90970bf6eb2dd868.gif") # Решка
                    await inter.message.edit(embed = embed, components=[])
                    await asyncio.sleep(5)
                    embed = disnake.Embed(description=f"В битве между {inter.author.mention} и <@{пользователь}>\n**стал победителем** <@{пользователь}>, его выигрыш {int(ставка)} <:amitobal:1158567849707716708> ",color=3092790)
                    embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/1134137639428173884/1146123478559371424/duel.png")
                    embed.set_author(name = f"Орел и Решка | {inter.guild.name}", icon_url = inter.guild.icon.url)
                    return await inter.message.edit(embed = embed)
                elif number == 2:
                    
                    economy.update_one({"_id": str(пользователь)}, {"$inc": {"balance": -int(ставка)}})
                    economy.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": +int(ставка)}})

                    cluster.sweetness.history.update_one({"_id": str(пользователь)}, {"$inc": {"casino": +int(ставка)}})
                    cluster.sweetness.history_win.update_one({"_id": str(inter.author.id)}, {"$inc": {"casino": +int(ставка)}})

                    embed.description = f"**Решка** — <@{пользователь}>\n**Орёл** — {inter.author.mention}"
                    embed.set_image(url = "https://media.discordapp.net/attachments/871820381797908500/877885120244224031/e286ab8ddbf4c2af.gif") # Орёл
                    await inter.message.edit(embed = embed, components=[])
                    await asyncio.sleep(5)
                    embed = disnake.Embed(description=f"В битве между {inter.author.mention} и <@{пользователь}>\n**стал победителем** {inter.author.mention}, его выигрыш {int(ставка)} <:amitobal:1158567849707716708> ",color=3092790)
                    embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/1134137639428173884/1146123478559371424/duel.png")
                    embed.set_author(name = f"Орел и Решка | {inter.guild.name}", icon_url = inter.guild.icon.url)
                    return await inter.message.edit(embed = embed)

        if inter.component.custom_id == "delete":
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description = f"{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**", color = 3092790)
                embed.set_author(name = "Удалить сообщение", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            
            await inter.message.delete()

        if inter.component.custom_id == "yesduel":
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description = f"{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**", color = 3092790)
                embed.set_author(name = f"Дуэли | {inter.guild.name}", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            
            пользователь = disnake.utils.get(inter.guild.members, id = int(intermessage_id[inter.author.id]))

            embed = disnake.Embed(description=f"### {inter.author.mention} сражается в дуэле с {пользователь.mention}", color = 3092790)
            embed.set_author(name = f"Дуэли | {inter.guild.name}", icon_url = inter.guild.icon.url)
            embed.set_image(url = random.choice(["https://imgur.com/z22DV5l.gif", "https://imgur.com/d6VxvxE.gif", "https://imgur.com/sMulajH.gif", "https://imgur.com/GQ6Fe8D.gif"]))
            await inter.message.edit(embed = embed, components = [])

            ставка = summa[inter.author.id]
            number = randint(1, 2)

            if number == 1:
                economy.update_one({"_id": str(пользователь.id)}, {"$inc": {"balance": -int(ставка)}})
                economy.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": +int(ставка)}})

                cluster.sweetness.history.update_one({"_id": str(пользователь.id)}, {"$inc": {"casino": -int(ставка)}})
                cluster.sweetness.history_win.update_one({"_id": str(inter.author.id)}, {"$inc": {"casino": +int(ставка)}})

            if number == 2:
                economy.update_one({"_id": str(пользователь.id)}, {"$inc": {"balance": +int(ставка)}})
                economy.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": -int(ставка)}})

                cluster.sweetness.history_win.update_one({"_id": str(пользователь.id)}, {"$inc": {"casino": +int(ставка)}})
                cluster.sweetness.history.update_one({"_id": str(inter.author.id)}, {"$inc": {"casino": -int(ставка)}})

            await asyncio.sleep(3)

            if number == 1:
                embed = disnake.Embed(color=3092790)
                embed.set_author(name = f"Дуэли | {inter.guild.name}", icon_url = inter.guild.icon.url)
                embed.description = f"**В битве** между {inter.author.mention} и {пользователь.mention} **стал победителем** {inter.author.mention}, его выигрыш {int(ставка)} <:amitobal:1158567849707716708> "
                embed.set_author(name = inter.author, icon_url = inter.author.display_avatar.url)
                await inter.message.edit(embed = embed)
                del intermessage_id[inter.author.id]
                del summa[inter.author.id]

            if number == 2:
                embed = disnake.Embed(color=3092790)
                embed.set_author(name = f"Дуэли | {inter.guild.name}", icon_url = inter.guild.icon.url)
                embed.description = f"**В битве** между {inter.author.mention} и {пользователь.mention} **стал победителем** {пользователь.mention}, его выигрыш {int(ставка)} <:amitobal:1158567849707716708> "
                await inter.message.edit(embed = embed)
                del intermessage_id[inter.author.id]
                del summa[inter.author.id]

def setup(bot): 
    bot.add_cog(economycog(bot))