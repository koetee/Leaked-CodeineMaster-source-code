import pymongo
import disnake
import json
import datetime
from disnake.ext import commands
from disnake.enums import ButtonStyle, TextInputStyle
from PIL import Image, ImageDraw, ImageFont

cluster = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/test?retryWrites=true&w=majority")

files = cluster.sweetness.files
database = cluster.sweetness

class ClanView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Клановая карта", custom_id = 'map', emoji = '<:map:1139827653298360421>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Правила битв", custom_id = 'clan_battle_rules', emoji = '<:rules:1140330418546151464>'))

class clan_embed(commands.Cog):
    def __init__(self, bot: commands.Bot(intents = disnake.Intents.all(), command_prefix = 'embed!')):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def clan_embed(self, inter):
        await inter.message.delete()

        embed = disnake.Embed(color = 3092790)
        embed.set_image(url = "https://images-ext-1.discordapp.net/external/-ePJ8HGO6iO7DE0RPX26RQwR3Rv0H_vCfvTlMKAqKPw/https/media.tenor.com/4XzoCqoNqjQAAAAC/uzumaki-clan.gif?width=448&height=250")
        
        embed1 = disnake.Embed(title = f"                Кланы {inter.guild.name}", description = f"> Кланы представляют из себя организованные сообщества, где участники могут общаться, \
                               > договариваться о совместных играх, обмениваться опытом и советами, а также участвовать в масштабных турнирах и других игровых событиях.\n \
                               > Для получения своего клана, обратитесь к <@854328227077160982>.\n> <@&1128994817997807616> - Ответственные за кланы на сервере.", color = 3092790)
        embed1.set_image(url = "https://cdn.discordapp.com/attachments/1022766485954899989/1048367557691854949/1.png")
        
        embed2 = disnake.Embed(title = "                 Клановый бот", description="> `/clan_profile` — открыть клановый профиль и меню управления кланом\n**Внутри меню**: \
                               \n> `Управление` — перейти к панели настроек клана\n> `Участники` — просмотреть список участников клана\n> `Покинуть клан` — выйти из клана\n \
                               > `Выйти` — закрыть меню", color = 3092790)
        embed2.set_image(url = "https://cdn.discordapp.com/attachments/1022766485954899989/1048367557691854949/1.png")
        
        embed3 = disnake.Embed(title="             Панель настроек клана", description='> `Добавить заместителя` — добавить зама\n> `Добавить описание` — \
                               изменить описание в профиле клана\n> `Добавить аватар` — изменить аватар в клановом профиле\n> `Передать владельца` — передать права лидера\n > \
                               `Режим собрания` — отключить микрофоны участником в клан войсе\n> `Забанить участника` — внести в ЧС клана\n> `Пригласить участника` — отправить в ЛС приглашение\n> \
                               `Удалить участника` — изгнать пользователя из клана\n> `Список депозита` — посмотреть зачисления в казну\n> `Список ЧС клана` — просмотреть список банов клана\n>  \
                               `Положить на депозит` — пополнить баланс клана\n> `Клановый онлайн` — просмотреть онлайн участников\n> `Клановый магазин` — купить улучшения\n> \
                               `Установить требования` — отправить эмбед в канал "требования", настроить вопросы для заявок в клан\n> \
                               `Пост о наборе` — отправить в ⁠<#1128738075623829645> эмбед с рекламой клана\n> `Покинуть клан` — выйти из клана\n> \
                               `Удалить клан` — безвозвратно удалить клан', color = 3092790)
        embed3.set_image(url = "https://cdn.discordapp.com/attachments/1022766485954899989/1048367557691854949/1.png")

        embed4 = disnake.Embed(title="               Типы кланов", description="> Маленькие→ От **5** участников до **10**\n> Средние → От **11** участников до **25** \
                                \n> Большие → От **26** участников до **50**\n \
                               > Огромные → **51** участник и **более**", color = 3092790)
        embed4.set_image(url = "https://cdn.discordapp.com/attachments/1022766485954899989/1048367557691854949/1.png")

        embed5 = disnake.Embed(title="         Часовая норма для кланов  ", description="> Маленькие → от **10** до **30** ч.\n> Средние → от **10** до **50** ч.\n> Большие → от **50** до **100** ч.\n> Огромные → от **100** и **более** ч.", color = 3092790)
        embed5.set_image(url = "https://cdn.discordapp.com/attachments/1022766485954899989/1048367557691854949/1.png")

        await inter.send(embeds = [embed, embed1, embed2, embed3, embed4, embed5])

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def clan_system(self, inter):
        await inter.message.delete()

        embed = disnake.Embed(
            color = 3092790,
            description=
                "**Здесь** вы найдете **подробные правила** битвы кланов, а также **интерактивную карту клановой территории**. \
                \n\nПравила Битвы Кланов: \
                \n> В битве кланов можно использовать разнообразные составы армии для атаки зомби. \
                \n> Альянсы могут отправлять подкрепление в битву своим союзным кланам. \
                \n> По окончании битвы с зомби или другим кланом, армия отправляется в режим отдыха на 1 час. \
                \n\nИнтерактивная Карта: \
                \n> На интерактивной карте вы сможете наглядно увидеть распределение территории между кланами. \
                \n> Эта карта поможет вам строить стратегии и планировать атаки."
        )
        embed.set_author(name = f"Клановая мини-панель {inter.guild.name}", icon_url = inter.guild.icon.url)
        await inter.send(embed = embed, view = ClanView())

    @commands.Cog.listener()
    async def on_button_click(self, inter):

        custom_id = inter.component.custom_id

        with open('clan_sweetness.json','r', encoding='utf-8') as f:
            clan = json.load(f)

        if custom_id == "rules":

            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = "Правила битвы кланов", icon_url = inter.guild.icon.url)
            embed.description = "**Для нападения** на зомби **можно** использовать **любой состав** армии. **При нападении** на зомби **союзный альянс** может отправить **подкрепление**.\n\
            **После завершения битвы** с зомби или вражеским кланом, армия переходит в **режим отдыха на 1 час**.\n\n\
            **Общее количество доступных** героев составляет `16`. **Нельзя нападать** на вражеский клан, когда у него **активен барьер**.\n\n\
            **Примерные расценки на нападение:**\n\
            > Зомби **1-ого** уровня: **5** участников в голосовом канале, **1 герой**.\n\
            > Зомби **2-ого** уровня: **10** участников в голосовом канале, **2 героя**.\n\
            > Зомби **3-ого** уровня: **15** участников в голосовом канале, **4 героя**.\n\
            > Зомби **4-ого** уровня: **20** участников в голосовом канале, **6 героев**.\n\
            > Зомби **5-ого** уровня: **25** участников в голосовом канале, **9 героев**.\n\
            > Зомби **6-ого** уровня: **30** участников в голосовом канале, **12 героев**.\n\
            > Зомби **7-ого** уровня: **35** участников в голосовом канале, **16 героев**."
            await inter.send(ephemeral = True, embed = embed)

        if custom_id == "map":
            with open('clan_sweetness.json', 'r') as f:
                clan_data = json.load(f)
        
            im = Image.open('clan_map_main.png')
            idd = 1
        
            guild_clans = clan_data.get(str(inter.guild.id), {})

            for clan_key, clan_value in guild_clans.items():
                if isinstance(clan_value, dict):
                    try:
                        role = disnake.utils.get(inter.guild.roles, id=int(clan_key))
                        level = clan[str(inter.guild.id)][str(role.id)]['Level']

                        if cluster.sweetness.clan_shield.count_documents({"_id": str(clan_key)}) == 0:
                            cluster.sweetness.clan_shield.insert_one({"_id": str(clan_key), "activate": "Отсутствует", "time": datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=5)})

                        shield = database.clan_shield.find_one({'_id': str(clan_key)})['activate']

                        if idd == 1:
                            coordinates = (540, 290) # розовый
                            size = 18
                            fill = "#B684E8"
                            if shield == "YES":
                                transparent_image1 = Image.open('shield_pink.png')
                                im.paste(transparent_image1, (533, 185), transparent_image1)
                        elif idd == 2:
                            coordinates = (312, 177) # синий замок (ОРАНЖЕВЫЙ)
                            size = 18
                            fill = "#D8904E"
                            if shield == "YES":
                                transparent_image1 = Image.open('shield_orange.png')
                                im.paste(transparent_image1, (303, 96), transparent_image1)
                        elif idd == 3:
                            coordinates = (790, 171) # лайм
                            size = 18
                            fill = "#6BFF8C"
                            if shield == "YES":
                                transparent_image1 = Image.open('shield_lime.png')
                                im.paste(transparent_image1, (686, 143), transparent_image1)
                        elif idd == 4:
                            coordinates = (494, 365) # АФРИКА (MAGNET)
                            size = 18
                            fill = "#BD1F58"
                            if shield == "YES":
                                transparent_image1 = Image.open('shield_magenta.png')
                                im.paste(transparent_image1, (378, 326), transparent_image1)
                        elif idd == 5:
                            coordinates = (813, 557) # АЦТЕК (СИНИЙ)
                            size = 16
                            fill = "#2FDBBC"
                            if shield == "YES":
                                transparent_image1 = Image.open('shield_aztec.png')
                                im.paste(transparent_image1, (809, 493), transparent_image1)
                        elif idd == 6:
                            coordinates = (239, 442) # КРАСНЫЙ
                            size = 18
                            fill = "#AF3A3A"
                            if shield == "YES":
                                transparent_image1 = Image.open('shield_red.png')
                                im.paste(transparent_image1, (246, 439), transparent_image1)
                        elif idd == 7:
                            coordinates = (137, 343) # ФИОЛЕТОВЫЙ
                            size = 18
                            fill = "#8458FF"
                            if shield == "YES":
                                transparent_image1 = Image.open('shield_purple.png')
                                im.paste(transparent_image1, (116, 243), transparent_image1)
                        elif idd == 8:
                            coordinates = (769, 175) # ЗЕЛЕНЫЙ
                            size = 18
                            fill = "#18D214"
                            if shield == "YES":
                                transparent_image1 = Image.open('shield_green.png')
                                im.paste(transparent_image1, (1, 182), transparent_image1)
                        else:
                            coordinates = None
        
                        if coordinates:
                            ImageDraw.Draw(im).text(coordinates, str(f"{role.name[:10]}\nУр. {level}"), font=ImageFont.truetype('arial.ttf', encoding='UTF-8', size=size), fill=fill, stroke_width=2, stroke_fill='black')
        
                        idd += 1
                    except:
                        pass
                    
            im.save('out_clan_map.png')
        
            await inter.send(ephemeral = True, file=disnake.File('out_clan_map.png'))

def setup(bot):
    bot.add_cog(clan_embed(bot))