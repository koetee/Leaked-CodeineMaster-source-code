import pymongo
import disnake
import json
from disnake.ext import commands
from disnake.utils import get
from disnake.enums import ButtonStyle, TextInputStyle
from collections import OrderedDict

cluster = pymongo.MongoClient(f"mongodb://127.0.0.1/myFirstDatabase?retryWrites=true&w=majority")

files = cluster.sweetness.files

rolebutton = {}
roleyes = {}
currentShopTopPage = {}
hour = 60 * 60

class AcceptShopRole(disnake.ui.View):
    def __init__(self, id_owner):
        super().__init__()
        self.author = id_owner
    @disnake.ui.button(style = ButtonStyle.secondary, emoji=f"asdad")
    async def one_buy(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.author.id != self.author:
            return await inter.send(f"{inter.author.mention}, **Вы** не можете использовать **чужие кнопки**!", ephemeral=True)
        
        embed = disnake.Embed(color = 3092790)
        embed.set_author(name = f"Купить роль | {inter.guild.name}", icon_url = inter.guild.icon.url)
        embed.set_thumbnail(url = inter.author.display_avatar.url)

        role = disnake.utils.get(inter.guild.roles, id = int(roleyes[inter.author.id]))
        role_collection = cluster.sweetness.role
        role_buy = cluster.sweetness.role_buy
        economy_collection = cluster.sweetness.economy
        id_author = inter.author.id
        
        if int(economy_collection.find_one({"_id": str(inter.author.id)})["balance"]) < int(role_collection.find_one({'_id': str(roleyes[inter.author.id])})['cost']): 
            embed.description = f'{inter.author.mention}, у **Вас** на балансе недостаточно <:amitobal:1158567849707716708>'
            return await inter.message.edit(embed = embed, view = ShopBack())
        
        if role in inter.author.roles: 
            embed.description = f'{inter.author.mention}, у **Вас** уже есть эта роль!'
            return await inter.response.edit_message(embed = embed, view = ShopBack())
        
        role_collection.update_one({"_id": str(roleyes[inter.author.id])}, {"$inc": {"buy": +1}})
        role_buy.update_one({"_id": str(roleyes[inter.author.id])}, {"$inc": {"buy": +1}}, upsert=True)

        embed.description = f'{inter.author.mention}, **Вы** успешно приобрели роль <@&{role.id}>'
        await inter.response.edit_message(embed = embed, view = ShopBack())
        
        cluster.sweetness.history.update_one({'_id': str(inter .author.id)}, {'$inc': {'roles': +int(role_collection.find_one({'_id': str(roleyes[inter.author.id])})['cost'])}})
        economy_collection.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": -int(role_collection.find_one({'_id': str(roleyes[inter.author.id])})['cost'])}})

        plus_biz = int(role_collection.find_one({'_id': str(roleyes[inter.author.id])})['cost']) // 1.7
        economy_collection.update_one({"_id": str(role_collection.find_one({'_id': str(roleyes[inter.author.id])})['author'])}, {"$inc": {"balance": +int(plus_biz)}})
        await inter.author.add_roles(role)
    @disnake.ui.button(style = ButtonStyle.secondary, emoji=f"asdad", custom_id = 'shopback')
    async def second_buy(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        pass

class MenuShopDropdown(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Выберите опции",
            options = [
                disnake.SelectOption(label="Сначала старые", value = "old_sort_shop", description="Сортировка ролей", emoji="<:filter:1146119684878520350>"),
                disnake.SelectOption(label="Сначала новые", value = "new_sort_shop", description="Сортировка ролей", emoji="<:filter:1146119684878520350>"),
                disnake.SelectOption(label="Сначала дорогие", value = "major_sort_shop", description="Сортировка ролей", emoji="<:filter:1146119684878520350>"),
                disnake.SelectOption(label="Сначала дешевые", value = "cheap_sort_shop", description="Сортировка ролей", emoji="<:filter:1146119684878520350>"),
                disnake.SelectOption(label="Сначала популярные", value = "popular_sort_shop", description="Сортировка ролей", emoji="<:filter:1146119684878520350>"),
                disnake.SelectOption(label="Сначала непопулярные", value = "not_pupular_sort_shop", description="Сортировка ролей", emoji="<:filter:1146119684878520350>"),
            ],
        )

class ShopList(disnake.ui.View):

    def __init__(self, author: int, role_count):
        super().__init__()
        if role_count > 1:
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="1", custom_id="shop_one_buy", emoji=f"{files.find_one({'_id': 'buy'})['emoji_take']}"))
        if role_count > 2:
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="2", custom_id="shop_two_buy", emoji=f"{files.find_one({'_id': 'buy'})['emoji_take']}"))
        else:
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="2", custom_id="shop_two_buy", emoji=f"{files.find_one({'_id': 'buy'})['emoji_take']}", disabled = True))
        if role_count > 3:
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="3", custom_id="shop_three_buy", emoji=f"{files.find_one({'_id': 'buy'})['emoji_take']}"))
        else:
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="3", custom_id="shop_three_buy", emoji=f"{files.find_one({'_id': 'buy'})['emoji_take']}", disabled = True))
        if role_count > 4:
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="4", custom_id="shop_four_buy", emoji=f"{files.find_one({'_id': 'buy'})['emoji_take']}"))
        else:
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="4", custom_id="shop_four_buy", emoji=f"{files.find_one({'_id': 'buy'})['emoji_take']}", disabled = True))
        if role_count > 5:
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="5", custom_id="shop_five_buy", emoji=f"{files.find_one({'_id': 'buy'})['emoji_take']}"))
        else:
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="5", custom_id="shop_five_buy", emoji=f"{files.find_one({'_id': 'buy'})['emoji_take']}", disabled = True))

        self.add_item(MenuShopDropdown())

        if not str(author) in currentShopTopPage or currentShopTopPage[str(author)] == 0:
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="shop_first_page", emoji=f"{files.find_one({'_id': 'double_left'})['emoji_take']}", disabled = True))
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="shop_prev_page", emoji=f"{files.find_one({'_id': 'left'})['emoji_take']}", disabled = True))
        else:
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="shop_first_page", emoji=f"{files.find_one({'_id': 'double_left'})['emoji_take']}"))
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="shop_prev_page", emoji=f"{files.find_one({'_id': 'left'})['emoji_take']}"))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="shop_exit", emoji=f"{files.find_one({'_id': 'basket'})['emoji_take']}"))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="shop_right_page", emoji=f"{files.find_one({'_id': 'right'})['emoji_take']}"))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="shop_last_page", emoji=f"{files.find_one({'_id': 'double_right'})['emoji_take']}"))

class ShopBack(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="shop_back", emoji="<:back1:1111712230363373700>", row = 0))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="exit_profile", emoji="<:close:1092013516392767528>", row = 0))

class shopcog(commands.Cog):
    def __init__(self, bot: commands.Bot(intents=disnake.Intents.all(), command_prefix = "!")):
        self.bot = bot

    @commands.slash_command(description="Магазин")
    async def shop(self, inter):
        if cluster.sweetness.role.count_documents({"_id": 1230}) == 0:
            cluster.sweetness.role.insert_one({"_id": 1230, "roleshop": []})

        roleshop_collection = cluster.sweetness.role
        roleshop_data = roleshop_collection.find_one({"_id": 1230})

        roleshop = roleshop_data["roleshop"]
        role_count = 1
        embed = disnake.Embed(color=3092790)
        embed.set_thumbnail(url=inter.author.display_avatar.url)
        embed.set_author(name = f"Магазин Ролей | {inter.guild.name}", icon_url = inter.guild.icon.url)
        embed.description = ""

        role_ids = [str(role_id) for role_id in roleshop[:5]]
        role_data_ordered = OrderedDict()

        for role_id in role_ids:
            role_data = roleshop_collection.find_one({"_id": role_id})
            role_data_ordered[role_id] = role_data

        for role_id, role in role_data_ordered.items():
            role_author = role["author"]
            role_cost = role["cost"]
            role_buy = role["buy"]
            embed.description += (
                f"> **#{role_count} **<@&{role_id}>\n> **Продавец**: <@{role_author}>\n> **Цена: {role_cost}**\n> **Куплена раз**: {role_buy}\n\n"
            )
            role_count += 1

        currentShopTopPage[str(inter.author.id)] = 0
        await inter.send(inter.author.mention, embed=embed, view=ShopList(inter.author, role_count))

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        custom_id = inter.component.custom_id
        if custom_id[:4] == "shop":
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description=f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color=3092790)
                embed.set_thumbnail(url=inter.author.display_avatar.url)
                embed.set_author(name = f"Магазин Ролей | {inter.guild.name}", icon_url = inter.guild.icon.url)
                return await inter.send(ephemeral=True, embed=embed)
            
            roleshop_collection = cluster.sweetness.role
            roleshop_data = roleshop_collection.find_one({"_id": 1230})
            roleshop = roleshop_data["roleshop"]
            role_count = 1
            items_per_page = 5

            embed = disnake.Embed(color=3092790, description="")
            embed.set_thumbnail(url=inter.author.display_avatar.url)
            embed.set_author(name = f"Магазин Ролей | {inter.guild.name}", icon_url = inter.guild.icon.url)
            embed.description = ""

            if custom_id == "shop_back":
                role_ids = [str(role_id) for role_id in roleshop[:5]]
                role_data_ordered = OrderedDict()

                for role_id in role_ids:
                    role_data = roleshop_collection.find_one({"_id": role_id})
                    role_data_ordered[role_id] = role_data

                for role_id, role in role_data_ordered.items():
                    role_author = role["author"]
                    role_cost = role["cost"]
                    role_buy = role["buy"]
                    embed.description += (
                        f"> **#{role_count} **<@&{role_id}>\n> **Продавец**: <@{role_author}>\n> **Цена: {role_cost}**\n> **Куплена раз**: {role_buy}\n\n"
                    )
                    role_count += 1

                currentShopTopPage[str(inter.author.id)] = 0
                await inter.response.edit_message(embed=embed, view=ShopList(inter.author, role_count))
            elif custom_id == "shop_exit":
                return await inter.message.delete()
            elif custom_id == "shop_other_page":
                pass
            elif custom_id.endswith("buy"):
                id_mapping = {
                    "shop_one_buy": 0,
                    "shop_two_buy": 1,
                    "shop_three_buy": 2,
                    "shop_four_buy": 3,
                    "shop_five_buy": 4
                }
                id = id_mapping.get(custom_id)
    
                if id is not None:
                    page_number = (currentShopTopPage[str(inter.author.id)] + 1 // 5)

                    role_index = (page_number) * 5 + id

                    if role_index < len(roleshop):
                        role_id = roleshop[role_index]
                        role_cost = cluster.sweetness.role.find_one({'_id': str(role_id)})['cost']

                        roleyes[inter.author.id] = role_id

                        embed = disnake.Embed(
                            description=f"{inter.author.mention}, **Вы уверены**, что Вы хотите **купить** роль <@&{role_id}> за **{role_cost}** <:amitobal:1158567849707716708> ?\n"
                                        f"Для **согласия** нажмите на {files.find_one({'_id': 'accept'})['emoji_take']}, для **отказа** на {files.find_one({'_id': 'decline'})['emoji_take']}",
                            color=3092790
                        )
                        embed.set_thumbnail(url = inter.author.display_avatar.url)
                        await inter.response.edit_message(embed = embed, view = AcceptShopRole(inter.author.id))

            else:
                # Разделение списка на страницы
                pages = [roleshop[i:i + items_per_page] for i in range(0, len(roleshop), items_per_page)]

                currentShopTopPage.setdefault(str(inter.author.id), 0)

                if custom_id == 'shop_first_page':
                    currentShopTopPage[str(inter.author.id)] = 0
                elif custom_id == 'shop_prev_page':
                    if currentShopTopPage[str(inter.author.id)] > 0:
                        currentShopTopPage[str(inter.author.id)] -= 1
                elif custom_id == 'shop_right_page':
                    if currentShopTopPage[str(inter.author.id)] < len(pages) - 1:
                        currentShopTopPage[str(inter.author.id)] += 1
                elif custom_id == 'shop_last_page':
                    currentShopTopPage[str(inter.author.id)] = len(pages) - 1

                role_ids = [str(role_id) for role_id in pages[currentShopTopPage[str(inter.author.id)]]]

                role_data_ordered = {}

                for role_id in role_ids:
                    role_data = roleshop_collection.find_one({"_id": role_id})
                    role_data_ordered[role_id] = role_data

                for role_id, role in role_data_ordered.items():
                    role_author = role["author"]
                    role_cost = role["cost"]
                    role_buy = role["buy"]
                    embed.description += (
                        f"> **#{role_count} **<@&{role_id}>\n> **Продавец**: <@{role_author}>\n> **Цена: {role_cost}**\n> **Куплена раз**: {role_buy}\n\n"
                    )
                    role_count += 1

                return await inter.response.edit_message(content = inter.author.mention, embed = embed, view = ShopList(inter.author.id, role_count))

    @commands.Cog.listener()
    async def on_dropdown(self, inter):
        custom_id = inter.values[0]

        if custom_id[-9:] == 'sort_shop':
            await inter.response.defer()

            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description=f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color=3092790)
                embed.set_author(name = f"Магазин Ролей | {inter.guild.name}", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url=inter.author.display_avatar.url)
                return await inter.send(ephemeral=True, embed=embed)

            roleshop_collection = cluster.sweetness.role
            roleshop_data = roleshop_collection.find_one({"_id": 1230})
            roleshop = roleshop_data["roleshop"]
            embed = disnake.Embed(color=3092790, description="")
            embed.set_thumbnail(url=inter.author.display_avatar.url)
            embed.set_author(name = f"Магазин Ролей | {inter.guild.name}", icon_url = inter.guild.icon.url)

            embed.set_footer(text=f"Страница 1 из {len(roleshop_collection.find_one({'_id': 1230})['roleshop']) // 5 + 1}")

            if custom_id == 'old_sort_shop':
                role_count = 1
                role_ids = [str(role_id) for role_id in roleshop[:5]]
                role_data_ordered = OrderedDict()

                for role_id in role_ids:
                    role_data = roleshop_collection.find_one({"_id": role_id})
                    role_data_ordered[role_id] = role_data

                for role_id, role in role_data_ordered.items():
                    role_author = role["author"]
                    role_cost = role["cost"]
                    role_buy = role["buy"]
                    embed.description += (
                        f"> **#{role_count} **<@&{role_id}>\n> **Продавец**: <@{role_author}>\n> **Цена: {role_cost}**\n> **Куплена раз**: {role_buy}\n\n"
                    )
                    role_count += 1

                currentShopTopPage[str(inter.author.id)] = 0

            elif custom_id == 'major_sort_shop':
                pipeline = [
                    {"$sort": {"cost": -1}},
                ]
                role_count = 1
                roles = list(roleshop_collection.aggregate(pipeline))
                for role in roles:
                    try:
                        role_data = roleshop_collection.find_one({"_id": str(role['_id'])})
                        embed.description += f"> **#{role_count} — **<@&{role['_id']}>\n**Продавец**: <@{role_data['author']}>\n**Цена: {role_data['cost']}** \n**Куплена раз**: {role_data['buy']}\n\n"
                        role_count += 1
                        if role_count > 5:
                            break
                    except:
                        pass

            elif custom_id == 'cheap_sort_shop':
                pipeline = [
                    {"$sort": {"cost": 1}},
                ]
                role_count = 1
                roles = list(roleshop_collection.aggregate(pipeline))
                for role in roles:
                    try:
                        role_data = roleshop_collection.find_one({"_id": str(role['_id'])})
                        embed.description += f"> **#{role_count} — **<@&{role['_id']}>\n**Продавец**: <@{role_data['author']}>\n**Цена: {role_data['cost']}** \n**Куплена раз**: {role_data['buy']}\n\n"
                        role_count += 1
                        if role_count > 5:
                            break
                    except:
                        pass
            elif custom_id in ['new_sort_shop']:
                sort_order = 1
                sort_key = 'buy'
                roleshop_data = roleshop_collection.find_one({'_id': 1230})
                roleshop = roleshop_data['roleshop']

                role_ids = [str(role_id) for role_id in roleshop]
                role_data = roleshop_collection.find({"_id": {"$in": role_ids}, "buy": {"$exists": True}}).sort(sort_key, sort_order).limit(5)
                role_count = 1
                for x in role_data:
                    role_id = str(x['_id'])
                    role_member = disnake.utils.get(inter.guild.members, id=int(role_id))
                    if not role_member:
                        embed.description += f"> **#{role_count} — **<@&{role_id}>\n**Продавец**: <@{x['author']}>\n**Цена: {x['cost']}** \n**Куплена раз**: {x['buy']}\n\n"
                        role_count += 1
                        if role_count > 5:
                            break

            elif custom_id in ['popular_sort_shop', 'not_pupular_sort_shop']:
                sort_order = -1 if custom_id == 'popular_sort_shop' else 1
                sort_key = 'buy'
                roleshop_data = roleshop_collection.find_one({'_id': 1230})
                roleshop = roleshop_data['roleshop']

                role_ids = [str(role_id) for role_id in roleshop]
                role_data = roleshop_collection.find({"_id": {"$in": role_ids}, "buy": {"$exists": True}}).sort(sort_key, sort_order).limit(5)
                role_count = 1
                for x in role_data:
                    role_id = str(x['_id'])
                    role_member = disnake.utils.get(inter.guild.members, id=int(role_id))
                    if not role_member:
                        embed.description += f"> **#{role_count} — **<@&{role_id}>\n**Продавец**: <@{x['author']}>\n**Цена: {x['cost']}** \n**Куплена раз**: {x['buy']}\n\n"
                        role_count += 1
                        if role_count > 5:
                            break

            return await inter.message.edit(embed=embed, view=ShopList(inter.author, role_count))

def setup(bot):
    bot.add_cog(shopcog(bot))