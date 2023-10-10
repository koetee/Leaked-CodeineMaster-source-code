import pymongo
import disnake
import datetime
import json
import re
from random import randint
from disnake.utils import get
from disnake.ext import commands
from disnake.enums import ButtonStyle, TextInputStyle
from disnake import utils, Embed
from PIL import Image, ImageDraw, ImageFont
from disnake import Localized

cluster = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/test?retryWrites=true&w=majority")

files = cluster.sweetness.files
database = cluster.sweetness

clan_invite = {}
clanshop = {}
profile_user = {}
currentClanTopPage = {}
currentRankChoice = {}
sort_clan_top = {}
clan_attack_choice = {}
clan_choice_hero = {}
clan_hero_cost = {}
clan_hero_name = {}
achievement = {}
achievement_reward = {}
selectTop = {}
currentTopPage = {}

min = 60
hour = 60 * 60
day = 60 * 60 * 24
async def get_member_ids(collection_name, key):
    membersID = []
    collection = database[collection_name]
    cursor = collection.find().sort(key, -1)
    for document in cursor:
        membersID.append(document["_id"])
    return membersID

def hex_to_rgb(value):
    value = value.lstrip('#')
    RGB = list(tuple(int(value[i:i + len(value) // 3], 16) for i in range(0, len(value), len(value) // 3)))
    return (RGB[0]<<16) + (RGB[1]<<8) + RGB[2]

class BackAchievements(disnake.ui.View):
    def __init__(self, пользователь, achiev):
        super().__init__()
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label = 'Вернуться назад', custom_id = 'achievements_main', emoji = '<:left:1138812764899520572>'))
        if cluster.sweetness.achievements.find_one({"_id": str(пользователь.id)})[f"{str(achiev)}"] == "NO":
            try:
                if cluster.sweetness.achievements_count.find_one({"_id": str(пользователь.id)})[f"{str(achiev)}"] == "YES":
                    self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label='Получить награду', custom_id='achievements_take_reward', emoji='<:gift:1136967445530284073>'))
            except:
                self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label='Получить награду', custom_id='achievements_take_reward', emoji='<:gift:1136967445530284073>', disabled=True))
        else:
            self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label='Получить награду', custom_id='achievements_take_reward', emoji='<:gift:1136967445530284073>', disabled=True))
        self.add_item(disnake.ui.Button(style = ButtonStyle.red, label = 'Выход', custom_id = 'exit_profile', emoji = '<:basket:1138812689502699680>'))

class ClanHeroBuy(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = ButtonStyle.green, label = 'Купить', custom_id = 'clan_buy_heroes', emoji = "<:zxc3:1009168371213926452>"))
        self.add_item(disnake.ui.Button(style = ButtonStyle.red, label = 'Отмена', custom_id = 'clan_back', emoji = '<:zxc2:1009168373936050206>'))

class ReportMenu(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = ButtonStyle.green, emoji = '<:zxc3:1009168371213926452>', custom_id = 'accept_one', row = 0))
        self.add_item(disnake.ui.Button(style = ButtonStyle.green, emoji = '<:zxc2:1009168373936050206>', custom_id = 'accept_two', row = 0))

class BallReportDisabled(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label = 'Вы успешно оставили отзыв', custom_id = 'ball_report', row = 0, disabled=True))

class BallReport(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label = 'Оставить отзыв', custom_id = 'ball_report', row = 0))
class ReportView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = ButtonStyle.green, label = 'Принять', custom_id = 'accept_report', emoji = '<:zxc3:1009168371213926452>'))
        self.add_item(disnake.ui.Button(style = ButtonStyle.red, label = 'Отклонить', custom_id = 'decline_report', emoji = "<:zxc2:1009168373936050206>"))


class Meet(disnake.ui.View):
    def __init__(self, invitelink):
        super().__init__()
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label = 'Присоединиться', url = str(invitelink)))

class ClanViewDropdown(disnake.ui.Select):
    def __init__(self, bot, clan_id):
        with open('clan_sweetness.json', 'r') as f:
            clan_data = json.load(f)

        guild = bot.get_guild(960579506425446472)

        guild_clans = clan_data.get(str(guild.id), {})

        options = []
        for clan_key, clan_value in guild_clans.items():
            if isinstance(clan_value, dict):
                try:
                    if not str(clan_key) == str(clan_id):
                        role = disnake.utils.get(guild.roles, id=int(clan_key))
                        clan_name = role.name
                        options.append(disnake.SelectOption(label=f"{clan_name}", value = f'{clan_key}_alliance', description=f"Сделать альянс с {clan_name}", emoji = '<:sort:1064936267533516861>'))
                except:
                    pass

        super().__init__(
            placeholder="Сделать альянс",
            options = options,
        )

class ClanAllianceView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Подтвердить", custom_id = 'clan_accept_alliance', emoji = '<:yes11:1096091626889302086>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Отказать", custom_id = 'clan_decline_alliance', emoji = '<:no1:1096087505159344138>'))

class ClanAlliance(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Сделать альянс (25000 💰 у обоих кланов)", custom_id = 'clan_create_alliance', emoji = '<:create:1140288843967381527>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Отправить поддержку", custom_id = 'clan_help_alliance', emoji = '<:help:1140288573891944579>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = "Меню", custom_id = 'clan_war', emoji = '<:menu1:1096091629393293494>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = "Выход", custom_id = 'clan_members_exit', emoji = '<:basket:1138812689502699680>', row = 1))


class ClanView(disnake.ui.View):
    def __init__(self, bot, clanxd):
        super().__init__()
        self.add_item(ClanViewDropdown(bot, clanxd))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = "Меню", custom_id = 'clan_war', emoji = '<:menu1:1096091629393293494>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = "Выход", custom_id = 'clan_members_exit', emoji = '<:basket:1138812689502699680>', row = 1))

class Achievements1Dropdown(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Выберите достижение",
            options = [
                disnake.SelectOption(label="Первобытное общество", description="25 участников в клане", value = '1_achiev'),
                disnake.SelectOption(label="Индустриальное общество", description="50 участников в клане", value = '2_achiev'),
                disnake.SelectOption(label="Постиндустриальное общество", description="100 участников в клане", value = '3_achiev'),
                disnake.SelectOption(label="Вот он - вкус победы", description="1 победа в клановой битве", value = '4_achiev'),
                disnake.SelectOption(label="Больше, мне нужно больше", description="5 побед в клановой битве", value = '5_achiev'),
                disnake.SelectOption(label="Вот он - вкус победы", description="10 побед в клановой битве", value = '6_achiev'),
                disnake.SelectOption(label="Главное не то, как ты бьешь, а как держишь удар", description="20 побед в клановой битве", value = '7_achiev'),
                disnake.SelectOption(label="Бро, тебе надо больше тренироваться", description="1000 часов в клановых войсах", value = '8_achiev'),
                disnake.SelectOption(label="Не суетись, всему своё время", description="5000 часов в клановых войсах", value = '9_achiev'),
                disnake.SelectOption(label="Клан отаку", description="10000 часов в клановых войсах", value = '10_achiev'),
                disnake.SelectOption(label="По лестнице к успеху", description="50000 часов в клановых войсах", value = '11_achiev'),
                disnake.SelectOption(label="Небоскрёб Прогресса", description="Заработайте 5 уровень в клане", value = '12_achiev'),
                disnake.SelectOption(label="Король Кланов", description="Заработайте 15 уровень в клане", value = '13_achiev'),
                disnake.SelectOption(label="Вершина Кланового Мира", description="Заработайте 30 уровень в клане", value = '14_achiev'),
                disnake.SelectOption(label="Первый союзник", description="Наймите 1 героя", value = '15_achiev'),
            ],
        )

class ClanQuest(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(Achievements1Dropdown())

        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label = 'Предыдущая', custom_id = 'achievements_next_0', emoji = '<:left:1138812764899520572>', disabled = True))
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label = 'Следующая', custom_id = 'achievements_next_2', emoji = '<:right:1138812810743259147>'))
        self.add_item(disnake.ui.Button(style = ButtonStyle.red, label = 'Выход', custom_id = 'clan_members_exit', emoji = '<:basket:1138812689502699680>'))

class Achievements2Dropdown(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Выберите достижение",
            options = [
                disnake.SelectOption(label="Служители Пятерых", description="Наймите 5 героев", value = '16_achiev'),
                disnake.SelectOption(label="Армия Великих Пятнадцати", description="Наймите 15 героев", value = '17_achiev'),
                disnake.SelectOption(label="Мастер Рекрутинга", description="Наймите 20 героев", value = '18_achiev'),
                disnake.SelectOption(label="Клановый союзник", description="Сделайте альянс кланов", value = '19_achiev'),
            ],
        )

class ClanQuest2(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(Achievements2Dropdown())

        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label = 'Предыдущая', custom_id = 'achievements_next_1', emoji = '<:left:1138812764899520572>'))
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label = 'Следующая', custom_id = 'achievements_next_3', emoji = '<:right:1138812810743259147>', disabled = True))
        self.add_item(disnake.ui.Button(style = ButtonStyle.red, label = 'Выход', custom_id = 'clan_members_exit', emoji = '<:basket:1138812689502699680>'))

class ClanAttack(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Подтвердить", custom_id = 'clan_accept_attack', emoji = '<:yes11:1096091626889302086>'))

        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = "Меню", custom_id = 'clan_war', emoji = '<:menu1:1096091629393293494>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = "Выход", custom_id = 'clan_members_exit', emoji = '<:basket:1138812689502699680>', row = 1))

class ClanZombieAttack(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Подтвердить", custom_id = 'clan_zombie_attack', emoji = '<:yes11:1096091626889302086>'))

        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = "Меню", custom_id = 'clan_war', emoji = '<:menu1:1096091629393293494>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = "Выход", custom_id = 'clan_members_exit', emoji = '<:basket:1138812689502699680>', row = 1))

class AttackZombieDropdown(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Выберите зомби",
            options = [
                disnake.SelectOption(label="Зомби 1-го уровня", description="Атаковать зомби 1-го уровня", value = 'clan_zombie_attack_1'),
                disnake.SelectOption(label="Зомби 2-го уровня", description="Атаковать зомби 2-го уровня", value = 'clan_zombie_attack_2'),
                disnake.SelectOption(label="Зомби 3-го уровня", description="Атаковать зомби 3-го уровня", value = 'clan_zombie_attack_3'),
                disnake.SelectOption(label="Зомби 4-го уровня", description="Атаковать зомби 4-го уровня", value = 'clan_zombie_attack_4'),
                disnake.SelectOption(label="Зомби 5-го уровня", description="Атаковать зомби 5-го уровня", value = 'clan_zombie_attack_5'),
                disnake.SelectOption(label="Зомби 6-го уровня", description="Атаковать зомби 6-го уровня", value = 'clan_zombie_attack_6'),
                disnake.SelectOption(label="Босс 7-го уровня", description="Атаковать босса 7-го уровня", value = 'clan_zombie_attack_7'),
            ],
        )

class AttackZombie(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(AttackZombieDropdown())
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = "Меню", custom_id = 'clan_war', emoji = '<:menu1:1096091629393293494>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = "Выход", custom_id = 'clan_members_exit', emoji = '<:basket:1138812689502699680>', row = 1))

class AttackClanDropdown(disnake.ui.Select):
    def __init__(self, bot, clan_id):
        with open('clan_sweetness.json', 'r') as f:
            clan_data = json.load(f)

        guild = bot.get_guild(960579506425446472)

        guild_clans = clan_data.get(str(guild.id), {})

        options = []
        for clan_key, clan_value in guild_clans.items():
            if isinstance(clan_value, dict):
                try:
                    if not str(clan_key) == str(clan_id):
                        role = disnake.utils.get(guild.roles, id=int(clan_key))

                        clan_name = role.name

                        options.append(disnake.SelectOption(label=f"{clan_name}", value = f'{clan_key}_clan_attack', description=f"Напасть на клан {clan_name}", emoji = '<:sort:1064936267533516861>'))
                except:
                    pass

        super().__init__(
            placeholder="Напасть на клан",
            options = options,
        )

class AttackClan(disnake.ui.View):
    def __init__(self, bot, clan_id):
        super().__init__()
        self.add_item(AttackClanDropdown(bot, clan_id))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = "Меню", custom_id = 'clan_war', emoji = '<:menu1:1096091629393293494>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = "Выход", custom_id = 'clan_members_exit', emoji = '<:basket:1138812689502699680>', row = 1))

class ClanSquad(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Герои клана", custom_id = 'clan_war_heroes', emoji = '<:heroes:1139674064856809524>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Армия клана", custom_id = 'clan_war_army', emoji = '<:staff:1096087520023945417>', disabled = True))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = "Меню", custom_id = 'clan_war', emoji = '<:menu1:1096091629393293494>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = "Выход", custom_id = 'clan_members_exit', emoji = '<:basket:1138812689502699680>', row = 1))

class ClanMap(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Атаковать зомби", custom_id = 'clan_attack_zombie', emoji = '<:kill:1140278179978813600>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Атаковать вражеский клан", custom_id = 'clan_attack_castle', emoji = '<:attack:1139675138334412880>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Отряд", custom_id = 'clan_war_settings', emoji = '<:staff:1096087520023945417>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = "Меню", custom_id = 'clan_war', emoji = '<:menu1:1096091629393293494>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = "Выход", custom_id = 'clan_members_exit', emoji = '<:basket:1138812689502699680>', row = 1))

class ClanVerbHero(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Найм", custom_id = 'clan_take_heroes', emoji = '<:get:1140280270256357396>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = "Меню", custom_id = 'clan_war', emoji = '<:menu1:1096091629393293494>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = "Выход", custom_id = 'clan_members_exit', emoji = '<:basket:1138812689502699680>', row = 1))

class ClanHeroesDropdown(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            options = [
                disnake.SelectOption(label="Дерил Диксон", value = 'clan_verb_1', description="Завербовать героя", emoji = '<:heroes:1139674064856809524>'),
                disnake.SelectOption(label="Девочка пост-эпохи", value = 'clan_verb_2', description="Завербовать героя", emoji = '<:heroes:1139674064856809524>'),
                disnake.SelectOption(label="Голобуй дротик", value = 'clan_verb_3', description="Завербовать героя", emoji = '<:heroes:1139674064856809524>'),
                disnake.SelectOption(label="Гробовщица", value = 'clan_verb_4', description="Завербовать героя", emoji = '<:heroes:1139674064856809524>'),
                disnake.SelectOption(label="Бритва", value = 'clan_verb_5', description="Завербовать героя", emoji = '<:heroes:1139674064856809524>'),
                disnake.SelectOption(label="Милитарист", value = 'clan_verb_6', description="Завербовать героя", emoji = '<:heroes:1139674064856809524>'),
                disnake.SelectOption(label="Железный страж", value = 'clan_verb_7', description="Завербовать героя", emoji = '<:heroes:1139674064856809524>'),
                disnake.SelectOption(label="Жнец", value = 'clan_verb_8', description="Завербовать героя", emoji = '<:heroes:1139674064856809524>'),
                disnake.SelectOption(label="Арсенал", value = 'clan_verb_9', description="Завербовать героя", emoji = '<:heroes:1139674064856809524>'),
                disnake.SelectOption(label="Разрушитель", value = 'clan_verb_10', description="Завербовать героя", emoji = '<:heroes:1139674064856809524>'),
                disnake.SelectOption(label="Вооружённый безумец", value = 'clan_verb_11', description="Завербовать героя", emoji = '<:heroes:1139674064856809524>'),
                disnake.SelectOption(label="Изгой", value = 'clan_verb_12', description="Завербовать героя", emoji = '<:heroes:1139674064856809524>'),
                disnake.SelectOption(label="Защитник рассвета", value = 'clan_verb_13', description="Завербовать героя", emoji = '<:heroes:1139674064856809524>'),
                disnake.SelectOption(label="Укротитель", value = 'clan_verb_14', description="Завербовать героя", emoji = '<:heroes:1139674064856809524>'),
                disnake.SelectOption(label="Ада", value = 'clan_verb_15', description="Завербовать героя", emoji = '<:heroes:1139674064856809524>'),
                disnake.SelectOption(label="Мегги Грин", value = 'clan_verb_16', description="Завербовать героя", emoji = '<:heroes:1139674064856809524>'),
            ],
        )


class ClanWar(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Отряд", custom_id = 'clan_war_settings', emoji = '<:staff:1096087520023945417>', row = 0))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Альянс", custom_id = 'clan_war_alliance', emoji = '<:alliance:1139674067067211919>', row = 0))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Герои", custom_id = 'clan_war_heroes', emoji = '<:heroes:1139674064856809524>', row = 0))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Квесты", custom_id = 'clan_war_quest', emoji = '<:achievements:1139674059156754492>', row = 0, disabled = True))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Щит", custom_id = 'clan_war_shield', emoji = '<:shield:1139675814791762071>', row = 0))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Карта кланов", custom_id = 'clan_map', emoji = '<:map:1139827653298360421>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Правила битвы", custom_id = 'clan_battle_rules', emoji = '<:map:1139827653298360421>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Магазин", custom_id = 'clan_war_shop', emoji = '<:shop1:1096087517150851223>', row = 1, disabled = True))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = "Меню", custom_id = 'clan_back', emoji = '<:menu1:1096091629393293494>', row = 2))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = "Выход", custom_id = 'clan_members_exit', emoji = '<:basket:1138812689502699680>', row = 2))

class ClanShield(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Подтвердить", custom_id = 'clan_accept_shield', emoji = '<:yes11:1096091626889302086>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = "Меню", custom_id = 'clan_war', emoji = '<:menu1:1096091629393293494>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = "Выход", custom_id = 'clan_members_exit', emoji = '<:basket:1138812689502699680>', row = 1))

class ClanWarHeroes(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(ClanHeroesDropdown())
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.green, label = "Список ваших героев", custom_id = 'clan_list_heroes', emoji = '<:menu1:1096091629393293494>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = "Меню", custom_id = 'clan_war', emoji = '<:menu1:1096091629393293494>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = "Выход", custom_id = 'clan_members_exit', emoji = '<:basket:1138812689502699680>', row = 1))

class ClanSystemRankAccept(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Подтвердить", custom_id = 'clan_accept_rank', emoji = '<:yes11:1096091626889302086>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Отказать", custom_id = 'clan_decline_rank', emoji = '<:no1:1096087505159344138>'))

        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = "Меню", custom_id = 'clan_system', emoji = '<:menu1:1096091629393293494>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = "Выход", custom_id = 'clan_members_exit', emoji = '<:basket:1138812689502699680>', row = 1))

class RankEdit(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Права заместителя", custom_id = 'clan_admin_rank', emoji = '<:owner:1096087506879008868>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Настройка лимитов", custom_id = 'clan_limit_rank', emoji = '<:staff:1096087520023945417>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Выдать ранг", custom_id = 'clan_add_rank', emoji = '<:plus:1135581260950020177>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Забрать ранг", custom_id = 'clan_remove_rank', emoji = '<:minus:1135581689536594050>'))

        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = "Меню", custom_id = 'clan_system', emoji = '<:menu1:1096091629393293494>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = "Выход", custom_id = 'clan_members_exit', emoji = '<:basket:1138812689502699680>', row = 1))

class ClanSystemEditDropdown(disnake.ui.Select):
    def __init__(self, ranks):
        options = []
        for rank in ranks:
            try:
                options.append(disnake.SelectOption(label=f"{rank}", value = f'{rank}_rank', description="Настроить ранг", emoji = '<:sort:1064936267533516861>'))
            except:
                pass

        if options == []:
            options.append(disnake.SelectOption(label=f"Отсутствуют", description="Отсутствуют", emoji = '<:sort:1064936267533516861>'))

        super().__init__(
            placeholder="Выберите ранг",
            options = options,
        )

class ClanSystemEdit(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Создать", custom_id = 'clan_create_rank', emoji = '<:plus:1135581260950020177>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Удалить", custom_id = 'clan_delete_rank', emoji = '<:minus:1135581689536594050>'))

        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = "Меню", custom_id = 'clan_system', emoji = '<:menu1:1096091629393293494>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = "Выход", custom_id = 'clan_members_exit', emoji = '<:basket:1138812689502699680>', row = 1))

class ClanSystem(disnake.ui.View):
    def __init__(self, rank):
        super().__init__()
        if rank == "Отсутствует":
            self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Управление", custom_id = 'clan_edit_rank', emoji = '<:dev:1135559157903261767>', disabled = True))
            self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Активировать систему рангов", custom_id = 'clan_system_rank', emoji = '<:rating:1135562565204844644>'))
        else:
            self.add_item(ClanSystemEditDropdown(rank))
            self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Управление", custom_id = 'clan_edit_rank', emoji = '<:dev:1135559157903261767>'))
            self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Активировать систему рангов", custom_id = 'clan_system_rank', emoji = '<:rating:1135562565204844644>', disabled = True))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = "Меню", custom_id = 'clan_back', emoji = '<:menu1:1096091629393293494>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = "Выход", custom_id = 'clan_members_exit', emoji = '<:basket:1138812689502699680>', row = 1))

class ClanMembersDropdown(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            options = [
                disnake.SelectOption(label="По возростанию рангов", value = 'clan_members_rang_asc', description="Фильтр: по возростанию рангов", emoji = '<:menu1:1096091629393293494>'),
                disnake.SelectOption(label="По убыванию рангов", value = 'clan_members_rang_desc', description="Фильтр: по убыванию рангов", emoji = '<:menu1:1096091629393293494>'),
                disnake.SelectOption(label="По возростанию онлайна", value = 'clan_members_online_asc', description="Фильтр: по возростанию онлайна", emoji = '<:menu1:1096091629393293494>'),
                disnake.SelectOption(label="По убыванию онлайна", value = 'clan_members_online_desc', description="Фильтр: по убыванию онлайна", emoji = '<:menu1:1096091629393293494>'),
                disnake.SelectOption(label="По возростанию времени", value = 'clan_members_time_asc', description="Фильтр: по возростанию времени", emoji = '<:menu1:1096091629393293494>'),
                disnake.SelectOption(label="По убыванию времени", value = 'clan_members_time_desc', description="Фильтр: по убыванию времени", emoji = '<:menu1:1096091629393293494>'),
            ],
        )

class ClanMembers(disnake.ui.View):
    def __init__(self, author: int):
        super().__init__()
        self.add_item(ClanMembersDropdown())

        if not str(author) in currentClanTopPage or currentClanTopPage[str(author)] == 0:
            self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'clan_members_first_page', emoji = '<:back:1008774480778252539>', disabled = True, row = 1))
            self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'clan_members_prev_page', emoji = '<:zxc5:1009168367342587915>', disabled = True, row = 1))
        else:
            self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'clan_members_first_page', emoji = '<:back:1008774480778252539>', row = 1))
            self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'clan_members_prev_page', emoji = '<:zxc5:1009168367342587915>', row = 1))

        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, custom_id = 'clan_members_exit', emoji = '<:basket:1138812689502699680>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'clan_members_right_page', emoji = '<:zxc4:1009168369112600728>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'clan_members_last_page', emoji = '<:zxc7:1009168365627125861>', row = 1))

        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = 'Меню', custom_id = 'clan_back', emoji = '<:menu1:1096091629393293494>', row = 2))

class ClanTopShopDropdown(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            options = [
                disnake.SelectOption(label="По возростанию рангов", value = 'clan_top_rang_asc', description="Фильтр: по возростанию рангов", emoji = '<:menu1:1096091629393293494>'),
                disnake.SelectOption(label="По убыванию рангов", value = 'clan_top_rang_desc', description="Фильтр: по убыванию рангов", emoji = '<:menu1:1096091629393293494>'),
                disnake.SelectOption(label="По возростанию онлайна", value = 'clan_top_online_asc', description="Фильтр: по возростанию онлайна", emoji = '<:menu1:1096091629393293494>'),
                disnake.SelectOption(label="По убыванию онлайна", value = 'clan_top_online_desc', description="Фильтр: по убыванию онлайна", emoji = '<:menu1:1096091629393293494>'),
                disnake.SelectOption(label="По возростанию времени", value = 'clan_top_time_asc', description="Фильтр: по возростанию времени", emoji = '<:menu1:1096091629393293494>'),
                disnake.SelectOption(label="По убыванию времени", value = 'clan_top_time_desc', description="Фильтр: по убыванию времени", emoji = '<:menu1:1096091629393293494>'),
            ],
        )

class ClanTopShop(disnake.ui.View):
    def __init__(self, author: int):
        super().__init__()
        self.add_item(ClanTopShopDropdown())

        if not str(author) in currentClanTopPage or currentClanTopPage[str(author)] == 0:
            self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'clan_top_first_page', emoji = '<:back:1008774480778252539>', disabled = True))
            self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'clan_top_prev_page', emoji = '<:zxc5:1009168367342587915>', disabled = True))
        else:
            self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'clan_top_first_page', emoji = '<:back:1008774480778252539>'))
            self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'clan_top_prev_page', emoji = '<:zxc5:1009168367342587915>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, custom_id = 'clan_top_exit', emoji = '<:basket:1138812689502699680>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'clan_top_right_page', emoji = '<:zxc4:1009168369112600728>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'clan_top_last_page', emoji = '<:zxc7:1009168365627125861>'))

class ClanDelete(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'clan_delete', emoji = '<:yes11:1096091626889302086>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'clan_back',  emoji = '<:no1:1096087505159344138>'))

class ClanAccept(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Отправить заявку", custom_id = 'clan_join', emoji = '<:invitation:1145676358916255874>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = "Отправить жалобу", custom_id = 'clan_report', emoji = '<:report:1142856573992042496>'))

class ClanChoice(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Эмбед", custom_id = 'clan_embed', emoji = '<:11:1096126530247204966>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Требования", custom_id = 'clan_request', emoji = '<:21:1096126528670138469>'))

class ClanJoin(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Принять", custom_id = 'clan_accept', emoji = '<:yes11:1096091626889302086>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Отклонить", custom_id = 'clan_decline', emoji = '<:no1:1096087505159344138>'))

class Disabled(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Принять", emoji = '<:yes11:1096091626889302086>', disabled = True))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Отклонить", emoji = '<:no1:1096087505159344138>', disabled = True))

class ClanEmbed(disnake.ui.View):
    def __init__(self, title_clan, desc_clan, image, bot):
        super().__init__()
        self.title_clan = title_clan
        self.desc_clan = desc_clan
        self.image = image
        self.bot = bot

    @disnake.ui.button(style = ButtonStyle.secondary, label = "Подтвердить", custom_id = 'accept_nabor', emoji = '<:yes11:1096091626889302086>')
    async def button_1(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        with open('clan_sweetness.json','r', encoding='utf-8') as f:
            clan = json.load(f)

        clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
        channel = database.clan.find_one({'_id': str(clanxd)})['channel_1']

        embed = disnake.Embed(title = f"{self.title_clan.content}", description = f"> {self.desc_clan.content}", color = 3092790)
        try:
            for attach in self.image.attachments:
                embed.set_image(url = str(attach))
        except:
            embed.set_image(url = self.image.content)
        await self.bot.get_channel(channel).purge(limit = 4)
        msg = await self.bot.get_channel(channel).send(embed = embed, view = ClanAccept())
        database.clan.update_one({'_id': str(msg.id)}, {'$set': {'clan': clanxd}}, upsert = True)

        for child in self.children:
            if isinstance(child, disnake.ui.Button): 
                child.disabled = True

        await inter.response.edit_message(view=self)

    @disnake.ui.button(style = ButtonStyle.secondary, label = "Отмена", emoji = '<:no1:1096087505159344138>')
    async def button_2(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.message.delete()

class ClanNabor(disnake.ui.View):
    def __init__(self, clan_name, desc_clan, request, propositions, peoples, image, bot):
        super().__init__()
        self.clan_name = clan_name
        self.desc_clan = desc_clan
        self.request = request
        self.propositions = propositions
        self.peoples = peoples
        self.image = image
        self.bot = bot

    @disnake.ui.button(style = ButtonStyle.secondary, label = "Подтвердить", custom_id = 'accept_nabor', emoji = '<:yes11:1096091626889302086>')
    async def button_1(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        embed = disnake.Embed(title = f"Набор в клан {self.clan_name}", description = f"> {self.desc_clan.content}", color = 3092790)
        try:
            for attach in self.image.attachments:
                embed.set_image(url = str(attach))
        except:
            embed.set_image(url = self.image.content)

        embed.add_field(name = "Что требуется от вас", value = f"{self.request.content}", inline = False)
        embed.add_field(name = "Что мы можем вам дать", value = f"{self.propositions.content}", inline = False)
        embed.add_field(name = "По поводу вступления в клан", value = f"{self.peoples.content}", inline = False)
        await self.bot.get_channel( ).send(embed = embed)

        for child in self.children:
            if isinstance(child, disnake.ui.Button):
                child.disabled = True

        await inter.message.edit(view=self)
        embed = disnake.Embed(title = "Пост в канал #поиск", description = f"{inter.author.mention}, **Ваш** пост о **наборе** участников успешно отправлен", color = 3092790)
        embed.set_thumbnail(url = inter.author.display_avatar.url)
        await inter.send(embed = embed)
    @disnake.ui.button(style = ButtonStyle.secondary, label = "Отмена", custom_id = 'clan_back', emoji = '<:no1:1096087505159344138>')
    async def button_2(self, button: disnake.ui.Button, inter: disnake.MessageInteraction): pass

class ClanShopAccept(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'yesshop', emoji = '<:yes11:1096091626889302086>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = 'Меню', custom_id = 'clan_back', emoji = '<:menu1:1096091629393293494>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = 'Выход', custom_id = 'clan_exit', emoji = '<:basket:1138812689502699680>'))

class ClanAdmin(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Добавить', custom_id = 'clan_add_admin', emoji = '<:plus1:1096093185282945074>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Удалить', custom_id = 'clan_remove_admin', emoji = '<:minus1:1096093188013441184>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = 'Меню', custom_id = 'clan_back', emoji = '<:menu1:1096091629393293494>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = 'Выход', custom_id = 'clan_exit', emoji = '<:basket:1138812689502699680>'))

class ClanBan(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Добавить', custom_id = 'clan_add_ban', emoji = '<:plus1:1096093185282945074>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Удалить', custom_id = 'clan_remove_ban', emoji = '<:minus1:1096093188013441184>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = 'Меню', custom_id = 'clan_back', emoji = '<:menu1:1096091629393293494>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = 'Выход', custom_id = 'clan_exit', emoji = '<:basket:1138812689502699680>'))

class ProfileClanView(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Управление', custom_id = 'clan_manage', emoji = '<:dev:1135559157903261767>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Участники клана', custom_id = 'clan_members', emoji = '<:staff:1096087520023945417>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Покинуть клан', custom_id = 'clan_leave', emoji = '<:exit1:1096087549597990922>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Система рангов', custom_id = 'clan_system', emoji = '<:star:1139827652010709092>', row = 2))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Карта кланов⠀', custom_id = 'clan_map', emoji = '<:map:1139827653298360421>', row = 2))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Война кланов', custom_id = 'clan_war', emoji = '<:war:1139827649800319016>', row = 2))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Достижения', custom_id = 'achievements_main', emoji = '<:achievements:1096087534913728552>', row = 3))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, custom_id = 'clan_exit', emoji = '<:basket:1138812689502699680>', row = 3))

class ClanInvite(disnake.ui.View):
    def __init__(self, clan_owner, bot, name): 
        super().__init__()
        self.clan_owner = clan_owner
        self.bot = bot
        self.name = name

    @disnake.ui.button(style = ButtonStyle.secondary, custom_id = 'yes_invite', emoji = '<:yes11:1096091626889302086>')
    async def button_1(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        with open('clan_sweetness.json','r', encoding='utf-8') as f:
            clan = json.load(f)

        clanxd = clan[str(960579506425446472)][str(self.clan_owner.id)]
        role_id = int(clan[str(960579506425446472)][str(clanxd)]['Role'])

        clan_invite[str(inter.author.id)] = int(role_id)
        msg = await self.bot.get_channel(961617052085415956).send(inter.author.id)

        cluster.sweetness.clan.update_one({'_id': str(inter.author.id)}, {'$set': {'rank': f'Участник'}}, upsert = True)

        embed = disnake.Embed(description = f'### > {inter.author.mention} теперь ты в клане **{self.name}**!', color = 3092790)
        embed.set_author(name = f"Кланы | {self.bot.get_guild(960579506425446472).name}", icon_url = self.bot.get_guild(960579506425446472).icon.url)
        embed.set_footer(text = f"Добавил в клан: {self.clan_owner}", icon_url = inter.author.display_avatar.url)
        embed.set_image(url = "https://media.discordapp.net/attachments/1146880953743061143/1147985480131031050/file.jpg?width=676&height=676")
        await inter.response.edit_message(embed = embed, components = [])

        embed = disnake.Embed(description = f'### > Добро пожаловать в клан <@&{role_id}>', color = 3092790)
        embed.set_author(name = f"Кланы | {self.bot.get_guild(960579506425446472).name}", icon_url = self.bot.get_guild(960579506425446472).icon.url)
        embed.set_thumbnail(url = inter.author.display_avatar.url)
        embed.set_footer(text = f"Добавил в клан: {self.clan_owner}", icon_url = self.clan_owner.display_avatar.url)
        await self.bot.get_channel(int(clan[str(960579506425446472)][str(clanxd)]['TextChannel'])).send(inter.author.mention, embed = embed)

        input = datetime.datetime.now()
        data = int(input.timestamp())
        cluster.sweetness.clan.update_one({'_id': str(inter.author.id)}, {'$set': {'tip_data': f'<t:{data}:F>'}}, upsert = True)

        clan[str(960579506425446472)][str(clanxd)]['ClanMembers'] += 1
        clan[str(960579506425446472)][str(inter.author.id)] = clanxd
        with open('clan_sweetness.json','w') as f:
            json.dump(clan,f)

    @disnake.ui.button(style = ButtonStyle.secondary, custom_id = 'no_invite', emoji = '<:no1:1096087505159344138>')
    async def button_2(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        embed = disnake.Embed(title = "Клан", description = f'У {inter.author.mention} уже есть клан!', color = 3092790)
        await inter.message.edit(embed = embed)

class ClanManageDropdown(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            options = [
                disnake.SelectOption(label="Положить на депозит", value = 'clan_deposit', description="Доступно для всех", emoji = '<:take:1096087521978486894>'),
                disnake.SelectOption(label="Клановый онлайн", value = 'clan_online', description="Доступно для всех", emoji = '<:microphone:1140294304556908695>'),
                disnake.SelectOption(label="Топ онлайна", value = 'clan_top', description="Доступно для всех", emoji = '<:microphone:1140294304556908695>'),
                disnake.SelectOption(label="Добавить/Удалить заместителя", value = 'clan_admin', description="Доступно только для владельцев", emoji = '<:plus1:1096093185282945074>'),
                disnake.SelectOption(label="Добавить/Изменить описание", value = 'clan_desc', description="Доступно только для старших", emoji = '<:msg:1096090258107539486>'),
                disnake.SelectOption(label="Добавить/Изменить аватар", value = 'clan_avatar', description="Доступно только для старших", emoji = '<:clan_role:1096087544715825184>'),
                disnake.SelectOption(label="Забанить/Разбанить участника", value = 'clan_ban', description="Доступно только для старших", emoji = '<:unavailable:1096087529243037828>'),
                disnake.SelectOption(label="Список депозита", value = 'clan_list_of_deposit', description="Доступно для всех", emoji = '<:bank:1096087553469333614>'),
                disnake.SelectOption(label="Список ЧС клана", value = 'clan_blacklist', description="Доступно для всех", emoji = '<:list_fail:1096087494036029460>'),
                disnake.SelectOption(label="Клановый магазин", value = 'clan_shop', description="Доступно для всех", emoji = '<:shop1:1096087517150851223>'),
                disnake.SelectOption(label="Установить требования", value = 'clan_send', description="Доступно для владельцев", emoji = '<:edit1:1096092966570971218>'),
                disnake.SelectOption(label="Пост о наборе", value = 'clan_post', description="Доступно для владельцев", emoji = '<:send:1138558137373315185>'),
                disnake.SelectOption(label="Передать владельца клана", value = 'clan_owner', description="Доступно только для владельца", emoji = '<:owner:1096087506879008868>'),
                disnake.SelectOption(label="Вкл/Выкл режим собрания", value = 'clan_meet', description="Доступно только для старших", emoji = '<:meet:1096087500000333956>'),
                disnake.SelectOption(label="Удалить клан", value = 'clan_delete', description="Доступно для владельцев", emoji = '<:basket:1138812689502699680>'),
            ],
        )

class ClanManage(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ClanManageDropdown())
        self.add_item(disnake.ui.Button(style = ButtonStyle.green, label = 'Пригласить участника', custom_id = 'clan_invite', emoji = '<:invites:1096087491125203075>', row = 1))
        self.add_item(disnake.ui.Button(style = ButtonStyle.green, label = 'Выгнать участника', custom_id = 'clan_kick', emoji = '<:minus_man1:1096087502210744331>', row = 1))
        self.add_item(disnake.ui.Button(style = ButtonStyle.blurple, label = 'Вернуться в профиль', custom_id = 'clan_back', emoji = '<:back2:1096126812767125504>', row = 2))
        self.add_item(disnake.ui.Button(style = ButtonStyle.red, label = 'Закрыть', custom_id = 'clan_exit', emoji = '<:basket:1138812689502699680>', row = 2))

class ClanBack(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = ButtonStyle.blurple, label = 'Меню', custom_id = 'clan_back', emoji = '<:menu1:1096091629393293494>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = 'Выход', custom_id = 'clan_exit', emoji = '<:basket:1138812689502699680>'))

class ClanShop(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, custom_id = '1shop',emoji = '<:buy11:1147510217756643448>'))
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, custom_id = '2shop',emoji = '<:buy11:1147510217756643448>'))
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, custom_id = '3shop',emoji = '<:buy11:1147510217756643448>'))
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, custom_id = '4shop',emoji = '<:buy11:1147510217756643448>'))
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, custom_id = '5shop',emoji = '<:buy11:1147510217756643448>'))
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, custom_id = '6shop',emoji = '<:buy11:1147510217756643448>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = 'Меню', custom_id = 'clan_back', emoji = '<:menu1:1096091629393293494>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, label = 'Выход', custom_id = 'clan_exit', emoji = '<:basket:1138812689502699680>'))

class ClanProfileCog(commands.Cog):
    def __init__(self, bot: commands.Bot(intents = disnake.Intents.all(), command_prefix = 'test!')):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.bot.process_commands(message)

        if message.author.id == 992089934213152848:
            if message.channel.id == 961617052085415956:
                if not disnake.utils.get(message.guild.members, id = int(message.content)) == None:
                    member = disnake.utils.get(message.guild.members, id = int(message.content))
                    await member.add_roles(disnake.utils.get(message.guild.roles, id = 961529522082185226))

                    role = disnake.utils.get(message.guild.roles, id = int(clan_invite[str(message.content)]))
                    await member.add_roles(role)
                    return await message.delete()
                
        if message.author.bot:
            return

    @commands.slash_command(description='Профиль')
    async def clan_profile(self, inter, пользователь: disnake.Member = None):
        await inter.response.defer()

        if пользователь == inter.author or пользователь == None:
            пользователь = inter.author

        profile_user[inter.author.id] = пользователь.id

        with open('clan_sweetness.json', 'r', encoding='utf-8') as f:
            clan = json.load(f)

        if str(пользователь.id) not in clan[str(inter.guild.id)]:
            clan[str(inter.guild.id)][str(пользователь.id)] = 'Отсутствует'
            with open('clan_sweetness.json', 'w') as f:
                json.dump(clan, f)

        embed = disnake.Embed(color = 3092790)
        embed.set_author(name = "Клановый профиль", icon_url = inter.guild.icon.url)
        embed.set_thumbnail(url=inter.author.display_avatar.url)

        if clan[str(inter.guild.id)][str(пользователь.id)] == 'Отсутствует':
            embed.description=f'{inter.author.mention}, у {пользователь.mention} нету клана!'
            return await inter.send(embed=embed, ephemeral=True)

        clanxd = clan[str(inter.guild.id)][str(пользователь.id)]
        if database.clan_online.count_documents({"_id": str(clanxd)}) == 0:
            database.clan_online.insert_one({"_id": str(clanxd), "clan_online": 0})

        if database.clan_rating.count_documents({"_id": str(clanxd)}) == 0:
            database.clan_rating.insert_one({"_id": str(clanxd), "rating": 0})

        if database.clan_alliance.count_documents({"_id": str(clanxd)}) == 0:
            database.clan_alliance.insert_one({"_id": str(clanxd), "alliance": "Отсутствует"})

        clan_take = clan[str(inter.guild.id)][str(clanxd)]
        clan_online = database.clan_online.find_one({'_id': str(clanxd)})['clan_online']
        clan_points = clan_online // 3600
        clan_level = clan_points // 20 + 1

        clan_take['Points'] = int(clan_points)
        clan_take['Level'] = int(clan_level)
        with open('clan_sweetness.json', 'w') as f:
            json.dump(clan, f)
        try:
            role = disnake.utils.get(inter.guild.roles, id=int(clan_take['Role']))
            clan_name = role.name
        except:
            embed.description=f'{inter.author.mention}, у **Вас** нету клана!'
            return await inter.send(embed=embed, ephemeral=True)
        clan_description = clan_take['Description']
        clan_owner = f"<@{clan_take['Owner']}>"
        clan_admins = ""

        for member in reversed(role.members):
            try:
                rank_member = cluster.sweetness.clan.find_one({'_id': str(member.id)})['rank']
                zam = cluster.sweetness.clan.find_one({'_id': str(rank_member)})['admin']

                if zam == "Присутствует" and member.id not in clan_take['Admin']:
                    clan_take['Admin'].append(member.id)
                    with open('clan_sweetness.json', 'w') as f:
                        json.dump(clan, f)
            except:
                pass

        if not clan_take['Admin']:
            clan_admins = "Отсутствуют"
        else:
            for admin in clan[str(inter.guild.id)][str(clanxd)]["Admin"]:
                clan_admins += f"<@{admin}>, "

        clan_role = f"<@&{clanxd}>"
        clan_id = clanxd
        clan_date = f"{clan_take['Time']}"
        clan_points = f"{clan_take['Points']}"
        clan_level = f"{clan_take['Level']}"
        clan_limit = f"{clan_take['Limit']}"
        clan_balance = f"{clan_take['Balance']}"
        clan_rating = database.clan_rating.find_one({'_id': str(clanxd)})['rating']
        clan_alliance = database.clan_alliance.find_one({'_id': str(clanxd)})['alliance']
        if not clan_alliance == "Отсутствует":
            clan_alliance = f"<@&{clan_alliance}>"

        role_take = disnake.utils.get(inter.guild.roles, id = int(clanxd))

        embed = disnake.Embed(
            description=f'# <:clan:1096087543398801601> Клан {clan_name}\n\n<:msg:1096090258107539486> **Описание**\n```{clan_description}``` \
                \n<:owner:1096087506879008868> **Владелец**: {clan_owner}\n<:admin_clan:1096090695888031794> **Заместители**: {clan_admins} \
                \n<:clan_role:1096087544715825184> **Роль:** {clan_role}\n<:calendar:1096087540261462127> **Дата создания:** {clan_date} \
                \n<:point:1096087512834912398> **Очки клана:** {clan_points}\n<:level:1096087492542857346> **Уровень клана:** {clan_level} \
                \n<:top:1096087524985810964> **Рейтинг клана:** {clan_rating} \
                \n<:alliance:1139674067067211919> **Альянс:** {clan_alliance} \
                \n<:id:1096087488625377421> **ID:** {clan_id}', color=3092790)
        embed.add_field(name='<:staff:1096087520023945417> Участники', value=f'```{len(role_take.members)}/{clan_limit}```')
        embed.add_field(name='<:coin1:1096094598507532479> Баланс', value=f'```{clan_balance}```')
        embed.add_field(name='<:microphone:1140294304556908695> Голосовой онлайн',
                        value=f'```🕓 {clan_online // hour}ч. {(clan_online - (clan_online // hour * hour)) // 60}м.```')

        clan_url = clan_take['Thumbnail']
        if clan_url != 'Отсутствует':
            embed.set_thumbnail(url=clan_url)

        await inter.send(inter.author.mention, embed=embed, view=ProfileClanView())
    
    @commands.Cog.listener()
    async def on_dropdown(self, inter):
        custom_id = inter.values[0]

        with open('clan_sweetness.json','r', encoding='utf-8') as f: 
            clan = json.load(f)
        if custom_id[-6:] == 'achiev':
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(title = f'Достижения кланов', color = 3092790)
                embed.description = f"{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**"
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)

            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
            clan_name = f"{role.name}"
            role_take = disnake.utils.get(inter.guild.roles, id = int(clanxd))
            clan_alliance = database.clan_alliance.find_one({'_id': str(clanxd)})['alliance']

            clan_online = database.clan_online.find_one({'_id': str(clanxd)})['clan_online']
            clan_points = clan_online // 3600
            clan_level = clan_points // 20 + 1

            embed = disnake.Embed(description = "", color = 3092790)
            embed.set_author(name = f"Ачивки клана — {clan_name} | {inter.guild.name}", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            match custom_id:
                case "1_achiev":
                    embed.description += "25 участников в клане"
                    embed.add_field(name=f"\n<:progress:1136957793480474664> Прогресс", value=f"```• [{len(role_take.members)}/25 уч.]```")
                    embed.add_field(name=f"\n<:gift:1136967445530284073> Награда", value=f"```500 💰```")
                case "2_achiev":
                    embed.description += "50 участников в клане"
                    embed.add_field(name=f"\n<:progress:1136957793480474664> Прогресс", value=f"```• [{len(role_take.members)}/50 уч.]```")
                    embed.add_field(name=f"\n<:gift:1136967445530284073> Награда", value=f"```2000 💰```")
                case "3_achiev":
                    embed.description += "100 участников в клане"
                    embed.add_field(name=f"\n<:progress:1136957793480474664> Прогресс", value=f"```• [{len(role_take.members)}/100 уч.]```")
                    embed.add_field(name=f"\n<:gift:1136967445530284073> Награда", value=f"```5000 💰```")
                case "4_achiev":
                    embed.description += "1 победа в клановой битве"
                    embed.add_field(name=f"\n<:progress:1136957793480474664> Прогресс", value=f"```• [{int(database.clan_win.find_one({'_id': str(clanxd)})['win'])}/1]```")
                    embed.add_field(name=f"\n<:gift:1136967445530284073> Награда", value=f"```500 💰```")
                case "5_achiev":
                    embed.description += "5 побед в клановой битве"
                    embed.add_field(name=f"\n<:progress:1136957793480474664> Прогресс", value=f"```• [{int(database.clan_win.find_one({'_id': str(clanxd)})['win'])}/5]```")
                    embed.add_field(name=f"\n<:gift:1136967445530284073> Награда", value=f"```1000 💰```")
                case "6_achiev":
                    embed.description += "10 побед в клановой бит"
                    embed.add_field(name=f"\n<:progress:1136957793480474664> Прогресс", value=f"```• [{int(database.clan_win.find_one({'_id': str(clanxd)})['win'])}/10]```")
                    embed.add_field(name=f"\n<:gift:1136967445530284073> Награда", value=f"```2000 💰```")
                case "7_achiev":
                    embed.description += "20 побед в клановой битве"
                    embed.add_field(name=f"\n<:progress:1136957793480474664> Прогресс", value=f"```• [{int(database.clan_win.find_one({'_id': str(clanxd)})['win'])}/25]```")
                    embed.add_field(name=f"\n<:gift:1136967445530284073> Награда", value=f"```5000 💰```")
                case "8_achiev":
                    embed.description += "1000 часов в клановых войсах"
                    embed.add_field(name=f"\n<:progress:1136957793480474664> Прогресс", value=f"```• [{int(database.clan_online.find_one({'_id': str(clanxd)})['clan_online'])}/36.000.00]```")
                    embed.add_field(name=f"\n<:gift:1136967445530284073> Награда", value=f"```1000 💰```")
                case "9_achiev":
                    embed.description += "5000 часов в клановых войсах"
                    embed.add_field(name=f"\n<:progress:1136957793480474664> Прогресс", value=f"```• [{int(database.clan_online.find_one({'_id': str(clanxd)})['clan_online'])}/180.000.00с.]```")
                    embed.add_field(name=f"\n<:gift:1136967445530284073> Награда", value=f"```5000 💰```")
                case "10_achiev":
                    embed.description += "10000 часов в клановых войсах"
                    embed.add_field(name=f"\n<:progress:1136957793480474664> Прогресс", value=f"```• [{int(database.clan_online.find_one({'_id': str(clanxd)})['clan_online'])}/360.000.00с.]```")
                    embed.add_field(name=f"\n<:gift:1136967445530284073> Награда", value=f"```10000 💰```")
                case "11_achiev":
                    embed.description += "50000 часов в клановых войсах"
                    embed.add_field(name=f"\n<:progress:1136957793480474664> Прогресс", value=f"```• [{int(database.clan_online.find_one({'_id': str(clanxd)})['clan_online'])}/180.000.000с.]```")
                    embed.add_field(name=f"\n<:gift:1136967445530284073> Награда", value=f"```50000 💰```")
                case "12_achiev":
                    embed.description += "Заработайте 5 уровень в клане"
                    embed.add_field(name=f"\n<:progress:1136957793480474664> Прогресс", value=f"```• [{int(clan_level)}/5 ур.]```")
                    embed.add_field(name=f"\n<:gift:1136967445530284073> Награда", value=f"```750 💰```")
                case "13_achiev":
                    embed.description += "Заработайте 15 уровень в клане"
                    embed.add_field(name=f"\n<:progress:1136957793480474664> Прогресс", value=f"```• [{int(clan_level)}/15 ур.]```")
                    embed.add_field(name=f"\n<:gift:1136967445530284073> Награда", value=f"```2500 💰```")
                case "14_achiev":
                    embed.description += "Заработайте 30 уровень в клане"
                    embed.add_field(name=f"\n<:progress:1136957793480474664> Прогресс", value=f"```• [{int(clan_level)}/30 ур.]```")
                    embed.add_field(name=f"\n<:gift:1136967445530284073> Награда", value=f"```5000 💰```")
                case "15_achiev":
                    embed.description += "Наймите 1 героя"
                    embed.add_field(name=f"\n<:progress:1136957793480474664> Прогресс", value=f"```• [{len(database.clan_heroes.find_one({'_id': str(clanxd)})['heroes'])}/1]```")
                    embed.add_field(name=f"\n<:gift:1136967445530284073> Награда", value=f"```5000 💰```")
                case "16_achiev":
                    embed.description += "Наймите 5 героев"
                    embed.add_field(name=f"\n<:progress:1136957793480474664> Прогресс", value=f"```• [{len(database.clan_heroes.find_one({'_id': str(clanxd)})['heroes'])}/5]```")
                    embed.add_field(name=f"\n<:gift:1136967445530284073> Награда", value=f"```25000 💰```")
                case "17_achiev":
                    embed.description += "Наймите 15 героев"
                    embed.add_field(name=f"\n<:progress:1136957793480474664> Прогресс", value=f"```• [{len(database.clan_heroes.find_one({'_id': str(clanxd)})['heroes'])}/15]```")
                    embed.add_field(name=f"\n<:gift:1136967445530284073> Награда", value=f"```75000 💰```")
                case "18_achiev":
                    embed.description += "Наймите 20 героев"
                    embed.add_field(name=f"\n<:progress:1136957793480474664> Прогресс", value=f"```• [{len(database.clan_heroes.find_one({'_id': str(clanxd)})['heroes'])}/20]```")
                    embed.add_field(name=f"\n<:gift:1136967445530284073> Награда", value=f"```150000 💰```")
                case "19_achiev":
                    embed.description += "Сделайте альянс кланов"
                    embed.add_field(name=f"\n<:progress:1136957793480474664> Прогресс", value=f"```• [{'1' if not str(database.clan_alliance.find_one({'_id': str(clanxd)})['alliance']) == 'Отсутствует' else '0'}/1]```")
                    embed.add_field(name=f"\n<:gift:1136967445530284073> Награда", value=f"```1000000 💰```")

            value_match = re.search(r'\d+', custom_id)
            id = int(value_match.group()) if value_match else 0
            achievement[str(inter.author.id)] = id
            
            value_match = re.search(r'\d+', embed.fields[1].value)
            reward_amount = int(value_match.group()) if value_match else 0
            achievement_reward[str(inter.author.id)] = reward_amount

            embed.set_footer(text = f"Запросил(а) {inter.author}", icon_url = inter.guild.icon.url)
            try:
                asfasf = cluster.sweetness.achievements.find_one({'_id': str(inter.author.id)})[f"{str(id)}"]
                await inter.response.edit_message(embed = embed, view = BackAchievements(inter.author, id))
            except:
                cluster.sweetness.achievements.update_one({'_id': str(inter.author.id)}, {'$set': {f"{str(id)}": "NO"}}, upsert = True)
                await inter.response.edit_message(embed = embed, view = BackAchievements(inter.author, id))

        if custom_id.endswith('alliance'):
            embed = disnake.Embed(color = 3092790)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            embed.set_author(name = f"Альянс", icon_url = inter.guild.icon.url)

            if not inter.message.content == inter.author.mention:
                embed.description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**'
                return await inter.send(ephemeral = True, embed = embed)

            role_alliance = disnake.utils.get(inter.guild.roles, id = int(custom_id[:-9]))
            clan_take_alliance = clan[str(inter.guild.id)][str(role_alliance.id)]

            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            clan_take = clan[str(inter.guild.id)][str(clanxd)]
            clan_name = disnake.utils.get(inter.guild.roles, id = int(clanxd))

            clan_owner = disnake.utils.get(inter.guild.members, id = int(clan_take_alliance['Owner']))

            clan_balance = f"{clan_take['Balance']}"
            if int(25000) > int(clan_balance):
                embed.description = f'{inter.author.mention}, У **Вашего** клана на балансе **недостаточно средств!**'
                return await inter.response.edit_message(embed = embed)
            
            clan_balance = f"{clan_take_alliance['Balance']}"
            if int(25000) > int(clan_balance):
                embed.description = f'{inter.author.mention}, У **Вашего** клана на балансе **недостаточно средств!**'
                return await inter.response.edit_message(embed = embed)

            embed.description = f'{inter.author.mention}, **Ваш запрос** на **создание альянса** был успешно отправлен **клан-лидеру** {clan_owner.mention}.'
            await inter.response.edit_message(embed = embed, view = ClanWar())

            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = f"Предложение Альянса", icon_url = inter.guild.icon.url)
            embed.description = f"{clan_owner.mention}, **Вам** поступила **заявка** от лидера {inter.author.mention} на **создание альянса** с кланом {clan_name.name}."
            msg = await clan_owner.send(content = clan_owner.mention, embed = embed, view = ClanAllianceView())
            database.channels.update_one({'_id': str(msg.id)}, {'$set': {'alliance': clan_take}}, upsert = True)

        if custom_id.startswith("clan_zombie_attack"):
            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
            clan_name = f"{role.name}"

            if cluster.sweetness.clan_attack.count_documents({"_id": str(clanxd)}) == 0:
                cluster.sweetness.clan_attack.insert_one({"_id": str(clanxd), "attack": "Можно", "time": datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=5)})

            clan_attack_choice[str(inter.author.id)] = str(custom_id[-1:])

            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = "Атаковать зомби", icon_url = inter.guild.icon.url)
            embed.description = f"{inter.author.mention}, **Вы** действительно хотите **атаковать** зомби {custom_id[-1:]}-ого уровня?\n\n**Следующее нападение будет доступно только через 30 минут**"
            return await inter.response.edit_message(embed = embed, view = ClanZombieAttack())

        if custom_id.endswith("_clan_attack"):
            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
            clan_name = f"{role.name}"

            if cluster.sweetness.clan_attack.count_documents({"_id": str(clanxd)}) == 0:
                cluster.sweetness.clan_attack.insert_one({"_id": str(clanxd), "attack": "Можно", "time": datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=5)})

            clan_attack_choice[str(inter.author.id)] = str(custom_id[:-12])

            if str(custom_id[:-12]) == str(clanxd):
                embed = disnake.Embed(color = 3092790)
                embed.set_author(name = "Атаковать клан", icon_url = inter.guild.icon.url)
                embed.description = f"{inter.author.mention}, **Вы** не можете атаковать свой клан"
                return await inter.response.edit_message(embed = embed, view = ClanAttack())
            
            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = "Атаковать клан", icon_url = inter.guild.icon.url)
            embed.description = f"{inter.author.mention}, **Вы** действительно хотите **атаковать** клан <@&{custom_id[:-12]}>?\n\n**Следующее нападение будет доступно только через 30 минут**"
            return await inter.response.edit_message(embed = embed, view = ClanAttack())
        
        if custom_id.startswith("clan_zombie"):
            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
            clan_name = f"{role.name}"

            if cluster.sweetness.clan_attack.count_documents({"_id": str(clanxd)}) == 0:
                cluster.sweetness.clan_attack.insert_one({"_id": str(clanxd), "attack": "Можно", "time": datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=5)})

            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = "Атаковать зомби", icon_url = inter.guild.icon.url)
            embed.description = f"{inter.author.mention}, **Вы** действительно хотите **атаковать** зомби {custom_id[-1:]}-ого уровня?\n\n**Следующее нападение будет доступно только через 30 минут**"
            return await inter.response.edit_message(embed = embed, view = ClanShield())

        if custom_id.startswith("clan_verb"):
            
            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
            clan_name = f"{role.name}"
            clan_hero_number = custom_id[10:]

            clan_choice_hero[str(inter.author.id)] = clan_hero_number

            return await inter.response.edit_message(attachments=None, file = disnake.File(f"clan_hero_{clan_hero_number}.jpg"), embed = None, view = ClanVerbHero())

        if custom_id.startswith("clan_members"):

            пользователь = utils.get(inter.guild.members, id=profile_user[inter.author.id])

            history_data = cluster.sweetness.history_case.find_one({"_id": str(пользователь.id)})

            membersID = []
            tip_data_clan = []
            member_data_clan = []
            tip_time_time = []

            items_per_page = 10
            for member in reversed(role.members):
                membersID.append(member.id)

            embed = Embed(color=3092790)
            embed.set_thumbnail(url=пользователь.display_avatar.url)
            embed.description = f"Общее количество участников - **{len(membersID)}**"

            items_per_page = 10

            if str(inter.author.id) not in sort_clan_top:
                sort_clan_top[str(inter.author.id)] = "Отсутствует"

            if custom_id == "clan_members_rang_asc":
                sort_clan_top[str(inter.author.id)] = "Ранги по возрастанию"
                reason = history_data.get("prize", ["-"])
                dates = cluster.sweetness.history_case.find_one({"_id": str(пользователь.id)})["data"]
                
                pattern = r"<t:(\d+):F>"
                timestamps = [int(re.search(pattern, date).group(1)) for date in dates]
                
                # Сортировка по возрастанию
                sorted_dates_asc = sorted(dates, key=lambda x: int(re.search(pattern, x).group(1)))
                tip_data = sorted_dates_asc

            elif custom_id == "clan_members_rang_desc":
                sort_clan_top[str(inter.author.id)] = "Ранги по убыванию"
                reason = history_data.get("prize", ["-"])
                dates = cluster.sweetness.history_case.find_one({"_id": str(пользователь.id)})["data"]
    
                pattern = r"<t:(\d+):F>"
                timestamps = [int(re.search(pattern, date).group(1)) for date in dates]
                
                sorted_dates_desc = sorted(dates, key=lambda x: int(re.search(pattern, x).group(1)), reverse=True)
                tip_data = sorted_dates_desc

            if custom_id == "clan_members_online_asc":
                sort_clan_top[str(inter.author.id)] = "Онлайн по возростанию"
                reason = history_data.get("prize", ["-"])
                dates = cluster.sweetness.history_case.find_one({"_id": str(пользователь.id)})["data"]
                
                pattern = r"<t:(\d+):F>"
                timestamps = [int(re.search(pattern, date).group(1)) for date in dates]
                
                # Сортировка по возрастанию
                sorted_dates_asc = sorted(dates, key=lambda x: int(re.search(pattern, x).group(1)))
                tip_data = sorted_dates_asc

            elif custom_id == "clan_members_online_desc":
                sort_clan_top[str(inter.author.id)] = "Онлайн по убыванию"
                reason = history_data.get("prize", ["-"])
                dates = cluster.sweetness.history_case.find_one({"_id": str(пользователь.id)})["data"]
    
                pattern = r"<t:(\d+):F>"
                timestamps = [int(re.search(pattern, date).group(1)) for date in dates]
                
                sorted_dates_desc = sorted(dates, key=lambda x: int(re.search(pattern, x).group(1)), reverse=True)
                tip_data = sorted_dates_desc

            elif custom_id == "clan_members_time_asc":
                sort_clan_top[str(inter.author.id)] = "Время по возрастанию"
                tip_data = history_data.get("data", ["-"])

                prizes = cluster.sweetness.clanonline.find_one({"_id": str(пользователь.id)})["online"]

                pattern = r'\d+'
                prize_values = [int(re.search(pattern, prize).group()) for prize in prizes]

                sorted_prizes_asc = [prize for _, prize in sorted(zip(prize_values, prizes))]

                reason = sorted_prizes_asc

            elif custom_id == "clan_members_time_desc":
                sort_clan_top[str(inter.author.id)] = "Время по убыванию"
                tip_data = history_data.get("data", ["-"])

                prizes = cluster.sweetness.history_case.find_one({"_id": str(пользователь.id)})["prize"]

                pattern = r'\d+'
                prize_values = [int(re.search(pattern, prize).group()) for prize in prizes]

                sorted_prizes_desc = [prize for _, prize in sorted(zip(prize_values, prizes), reverse=True)]

                reason = sorted_prizes_desc
            else:
                reason = history_data.get("prize", ["-"])
                tip_data = history_data.get("data", ["-"])

            if str(inter.author.id) not in currentClanTopPage:
                currentClanTopPage[str(inter.author.id)] = 0

            pages = [tip_data[i:i + items_per_page] for i in range(0, len(tip_data), items_per_page)]

            currentClanTopPage[str(inter.author.id)] = 0

            description = "\n".join(f"**{tip}**" for tip in pages[currentClanTopPage[str(inter.author.id)]])

            embed.add_field(name="`  Дата  `", value=description)

            pages1 = [reason[i:i + items_per_page] for i in range(0, len(reason), items_per_page)]
            description1 = "\n".join(reasons for reasons in pages1[currentClanTopPage[str(inter.author.id)]][:10])
            embed.add_field(name="`  Приз  `", value=description1)

            pages = [tip_data[i:i + items_per_page] for i in range(0, len(tip_data), items_per_page)]
            embed.set_footer(text=f"Страница {currentClanTopPage[str(inter.author.id)] + 1} из {len(pages)}",
                                icon_url="https://cdn.discordapp.com/attachments/1091732133111939135/1109845138764738653/menu.png")
            embed.set_author(name=f"История {пользователь} | {inter.guild}", icon_url=inter.guild.icon.url)
            await inter.response.edit_message(embed=embed, view=ClanTopShop(inter.author.id))

        #if custom_id.startswith("clan_top"):
#
        #    пользователь = utils.get(inter.guild.members, id=profile_user[inter.author.id])
#
        #    history_data = cluster.sweetness.history_case.find_one({"_id": str(пользователь.id)})
#
        #    embed = Embed(color=3092790)
        #    embed.set_thumbnail(url=пользователь.display_avatar.url)
        #    embed.description = f"За все время открыто кейсов: **{len(history_data['prize'])}**"
#
        #    items_per_page = 10
#
        #    if str(inter.author.id) not in sort_clan_top:
        #        sort_clan_top[str(inter.author.id)] = "Отсутствует"
#
        #    if custom_id == "clan_top_prize_asc":
        #        sort_clan_top[str(inter.author.id)] = "Призы по возрастанию"
        #        tip_data = history_data.get("data", ["-"])
#
        #        prizes = cluster.sweetness.history_case.find_one({"_id": str(пользователь.id)})["prize"]
#
        #        pattern = r'\d+'
        #        prize_values = [int(re.search(pattern, prize).group()) for prize in prizes]
#
        #        sorted_prizes_asc = [prize for _, prize in sorted(zip(prize_values, prizes))]
#
        #        reason = sorted_prizes_asc
#
        #    elif custom_id == "clan_top_prize_desc":
        #        sort_clan_top[str(inter.author.id)] = "Призы по убыванию"
        #        tip_data = history_data.get("data", ["-"])
#
        #        prizes = cluster.sweetness.history_case.find_one({"_id": str(пользователь.id)})["prize"]
#
        #        pattern = r'\d+'
        #        prize_values = [int(re.search(pattern, prize).group()) for prize in prizes]
#
        #        sorted_prizes_desc = [prize for _, prize in sorted(zip(prize_values, prizes), reverse=True)]
#
        #        reason = sorted_prizes_desc
        #    else:
        #        reason = history_data.get("prize", ["-"])
        #        tip_data = history_data.get("data", ["-"])
#
        #    if str(inter.author.id) not in currentClanTopPage:
        #        currentClanTopPage[str(inter.author.id)] = 0
#
        #    pages = [tip_data[i:i + items_per_page] for i in range(0, len(tip_data), items_per_page)]
#
        #    currentClanTopPage[str(inter.author.id)] = 0
#
        #    description = "\n".join(f"**{tip}**" for tip in pages[currentClanTopPage[str(inter.author.id)]])
#
        #    embed.add_field(name="`  Дата  `", value=description)
#
        #    pages1 = [reason[i:i + items_per_page] for i in range(0, len(reason), items_per_page)]
        #    description1 = "\n".join(reasons for reasons in pages1[currentClanTopPage[str(inter.author.id)]][:10])
        #    embed.add_field(name="`  Приз  `", value=description1)
#
        #    pages = [tip_data[i:i + items_per_page] for i in range(0, len(tip_data), items_per_page)]
        #    embed.set_footer(text=f"Страница {currentClanTopPage[str(inter.author.id)] + 1} из {len(pages)}",
        #                        icon_url="https://cdn.discordapp.com/attachments/1091732133111939135/1109845138764738653/menu.png")
        #    embed.set_author(name=f"История {пользователь} | {inter.guild}", icon_url=inter.guild.icon.url)
        #    await inter.response.edit_message(embed=embed, view=ClanTopShop(inter.author.id))

        if custom_id[-4:] == "rank":

            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
                embed.set_author(name = "Клан", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            
            currentRankChoice[str(inter.author.id)] = custom_id[:-5]

            embed = disnake.Embed(description = f'### > {inter.author.mention}, Выберите что вы хотите сделать', color = 3092790)
            embed.set_author(name = f"Управление рангом {custom_id[:-5]}", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            return await inter.response.edit_message(embed=embed, view = RankEdit())

        if custom_id[:4] == 'clan':

            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(title = 'Клан', description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            if clanxd == 'Отсутствует':
                embed = disnake.Embed(description = f'{inter.author.mention}, У **Вас** нету **клана**!', color = disnake.Color.red())
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.response.edit_message(ephemeral = True, embed = embed)
            
            if custom_id == 'clan_delete':
                if clan[str(inter.guild.id)][clanxd]['Owner'] == inter.author.id:
                    embed = disnake.Embed(color = 3092790, title = 'Удалить клан', description = f"{inter.author.mention}, **Вы** точно хотите удалить клан?!")
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    await inter.response.edit_message(embed = embed, view = ClanDelete())
                else:
                    embed = disnake.Embed(color = 3092790, title = 'Удалить клан', description = f"{inter.author.mention}, **Вы** не являетесь **Лидером** этого клана!")
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    await inter.response.edit_message(embed = embed, view = ClanBack())

            if custom_id == 'clan_owner':
                if clan[str(inter.guild.id)][clanxd]['Owner'] == inter.author.id:
                    clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
                    if clan[str(inter.guild.id)][str(clanxd)]['Owner'] == inter.author.id:
                        components = [disnake.ui.TextInput(label="Айди пользователя",placeholder="Например: 849353684249083914",custom_id = "Айди пользователя",style=disnake.TextInputStyle.paragraph, max_length=25)]
                        await inter.response.send_modal(title=f"Передать владельца клана",custom_id = "clan_owner", components=components)
                    else:
                        embed = disnake.Embed(color = 3092790, title = 'Передать владельца клана', description = f"{inter.author.mention}, **Вы** не являетесь **Лидером** этого клана!")
                        embed.set_thumbnail(url = inter.author.display_avatar.url)
                        await inter.response.edit_message(embed = embed, view = ClanBack())

            if custom_id == 'clan_admin':
                if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id:
                    embed = disnake.Embed(
                        title = f'Добавить/Удалить заместителя клана', color = 3092790,
                        description = f'Действие выполняет: {inter.author.mention}\n**Выберите** операцию',
                    ).set_thumbnail(url = inter.author.display_avatar.url)
                    await inter.response.edit_message(embed = embed, view = ClanAdmin())
                else:
                    embed = disnake.Embed(color = 3092790, title = 'Добавить/Удалить заместителя клана', description = f"{inter.author.mention}, **Вы** не являетесь **Лидером** этого клана!")
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    await inter.response.edit_message(embed = embed, view = ClanBack())
                    
            if custom_id == 'clan_ban':
                if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id or inter.author.id in clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin']:
                    embed = disnake.Embed(
                        title = f'Забанить/разбанить пользователя', color = 3092790,
                        description = f'Действие выполняет: {inter.author.mention}\n**Выберите** операцию ',
                    ).set_thumbnail(url = inter.author.display_avatar.url)
                    await inter.response.edit_message(embed = embed, view = ClanBan())
                else:
                    embed = disnake.Embed(color = 3092790, title = 'Добавить/Удалить заместителя клана', description = f"{inter.author.mention}, **Вы** не являетесь **Лидером/Замом** этого клана!")
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    await inter.response.edit_message(embed = embed, view = ClanBack())

            if custom_id == 'clan_desc':
                if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id:
                    components = [disnake.ui.TextInput(label="Описание",placeholder="Например: zxc clan",custom_id = "Описание",style=disnake.TextInputStyle.paragraph, max_length=350)]
                    return await inter.response.send_modal(title=f"Описание",custom_id = "clan_desc", components=components)
                if inter.author.id in clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin']:
                    components = [disnake.ui.TextInput(label="Описание",placeholder="Например: zxc clan",custom_id = "Описание",style=disnake.TextInputStyle.paragraph, max_length=350)]
                    return await inter.response.send_modal(title=f"Описание",custom_id = "clan_desc", components=components)
                else:
                    embed = disnake.Embed(color = 3092790, title = 'Добавить/Удалить заместителя клана', description = f"{inter.author.mention}, **Вы** не являетесь **Лидером/Замом** этого клана!")
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    await inter.response.edit_message(embed = embed, view = ClanBack())

            if custom_id == 'clan_avatar':
                if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id or inter.author.id in clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin']:
                    embed = disnake.Embed(
                        description = f"{inter.author.mention} отправьте новое **Фото** чтобы добавить/изменить аватарку **клана**",
                        color = 3092790,
                    ).set_thumbnail(url = inter.author.display_avatar.url).set_author(name = "Управление профилем", icon_url = inter.guild.icon.url)
                    await inter.response.edit_message(embed = embed, components = [])
    
                    def check(m):
                        return m.author.id == inter.author.id
    
                    image = await self.bot.wait_for("message", check = check)
    
                    try:
                        for attach in image.attachments:
                            clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Thumbnail'] = str(attach)
                            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
                            role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
                            clan_name = f"{role.name}"
                            await attach.save(f"clan_{clan_name}.png")
                            with open('clan_sweetness.json','w') as f: 
                                json.dump(clan,f)
                    except:
                        embed = disnake.Embed(
                            description = f"{inter.author.mention}, Возможно **Вы** не отправили **ссылку** на фотографию, а не прикрепили **аватар**",
                            color = 3092790,
                        ).set_thumbnail(url = inter.author.display_avatar.url).set_author(name = "Ошибка в управлении", icon_url = inter.guild.icon.url)
                        return await inter.message.edit(embed = embed, view = ClanBack())
    
                    embed = disnake.Embed(
                        color = 3092790, 
                        description = f"{inter.author.mention} **Вы** успешно **изменили** картинку в **профиле!**"
                    ).set_thumbnail(url = inter.author.display_avatar.url).set_author(name = "Управление профилем", icon_url = inter.guild.icon.url)
                    await inter.message.edit(embed = embed, view = ClanBack())
                else:
                    embed = disnake.Embed(color = 3092790, title = 'Добавить/Удалить заместителя клана', description = f"{inter.author.mention}, **Вы** не являетесь **Лидером/Замом** этого клана!")
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    await inter.response.edit_message(embed = embed, view = ClanBack())

            if custom_id == 'clan_meet':
                if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id or inter.author.id in clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin']:
                    if database.channels.count_documents({"_id": str(clan[str(inter.guild.id)][str(inter.author.id)])}) == 0: 
                        database.channels.insert_one({"_id": str(clan[str(inter.guild.id)][str(inter.author.id)]), "sobranie": 'Отсутствует'})

                    try:
                        channel = inter.author.voice.channel
                    except:
                        embed = disnake.Embed(description = f'{inter.author.mention}, Для **включения** режима собрания, **зайдите в голосовой канал**, где будет **проводиться собрание.**', color = 3092790)
                        embed.set_author(name = "Режим собрания", icon_url = inter.guild.icon.url)
                        embed.set_thumbnail(url = inter.author.display_avatar.url)
                        await inter.response.edit_message(embed = embed, view = ClanBack())

                    if database.channels.find_one({"_id": str(clan[str(inter.guild.id)][str(inter.author.id)])})['sobranie'] == 'Отсутствует':

                        embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно включили режим собрания.', color = 3092790)
                        embed.set_author(name = "Режим собрания", icon_url = inter.guild.icon.url)
                        embed.set_thumbnail(url = inter.author.display_avatar.url)
                        await inter.response.edit_message(embed = embed, view = ClanBack())

                        id_role = clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Role']
                        role = disnake.utils.get(inter.guild.roles, id = int(id_role))
                        await inter.author.voice.channel.set_permissions(role, speak = False, view_channel = True, connect = True)
                        database.channels.update_one({'_id': str(clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Role'])}, {'$set': {'sobranie': 'Присутствует'}}, upsert = True)

                        invitelink = await channel.create_invite(max_uses = 99)

                        for member in clan[str(inter.guild.id)]:
                            if clan[str(inter.guild.id)][str(member)] == str(clanxd):
                                try:
                                    member_take = disnake.utils.get(inter.guild.members, id = int(member))
                                    embed = disnake.Embed(description = f"<@{member}>, **Сейчас** в вашем клане будет проводиться собрание.\n\n**Для перехода в канал собрание, нажмите по кнопке ниже.**", color = 3092790)
                                    embed.set_author(name = f"Кланы | {inter.guild.name}", icon_url = inter.guild.icon.url)
                                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                                    await member_take.send(embed = embed, view = Meet(invitelink))
                                except:
                                    pass

                        for member in inter.author.voice.channel.members:
                            await member.move_to(member.voice.channel)
                    else:
                        embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно выключили режим собрания.', color = 3092790)
                        embed.set_author(name = "Режим собрания", icon_url = inter.guild.icon.url)
                        embed.set_thumbnail(url = inter.author.display_avatar.url)
                        await inter.response.edit_message(embed = embed, view = ClanBack())

                        role_id = clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Role']
                        role = disnake.utils.get(inter.guild.roles, id = int(role_id))

                        database.channels.update_one({'_id': str(clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Role'])}, {'$set': {'sobranie': 'Отсутствует'}}, upsert = True)

                        await inter.author.voice.channel.set_permissions(role, speak = True, view_channel = True, connect = True)

                        for member in clan[str(inter.guild.id)]:
                            if clan[str(inter.guild.id)][str(member)] == str(clanxd):
                                try:
                                    member_take = disnake.utils.get(inter.guild.members, id = int(member))
                                    embed = disnake.Embed(description = f"<@{member}>, **Собрание было отменено**\n\nПричина: `Санта карлос лох, смотрит сериал`", color = 3092790)
                                    embed.set_author(name = f"Кланы | {inter.guild.name}", icon_url = inter.guild.icon.url)
                                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                                    await member_take.send(embed = embed)
                                except:
                                    pass

                        for member in inter.author.voice.channel.members: 
                            await member.move_to(member.voice.channel)
                else:
                    embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** не можете** Включить/Выключить режим собрания** так как вы не являетесь **лидером клана!**', color = disnake.Color.red())
                    embed.set_author(name = "Режим собрания", icon_url = inter.guild.icon.url)
                    embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
                    return await inter.response.edit_message(embed = embed, view = ClanBack())

            if custom_id == 'clan_deposit':
                await inter.response.send_modal(title=f"Пополнить клан", custom_id = "pay_clan",components=[
                    disnake.ui.TextInput(label="Сумма",placeholder="Например: 1000",custom_id = "Сумма",style=disnake.TextInputStyle.short, max_length=25)])

            if custom_id == 'clan_online':
                if database.clanonline.count_documents({"_id": str(inter.author.id)}) == 0:
                    database.clanonline.insert_one({"_id": str(inter.author.id),"online": 0})

                N = database.clanonline.find_one({'_id': str(inter.author.id)})['online']

                clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
                role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
                clan_name = f"{role.name}"

                embed = disnake.Embed(color = 3092790)
                embed.add_field(name = "Кол-во времени в войсе:", value = f"```{N // hour}ч. {(N - (N // hour * hour)) // 60}м. {N - ((N // hour * hour) + ((N - (N // hour * hour)) // 60 * min))}с.```")
                embed.set_footer(text = f'Запросил(а) {inter.author}', icon_url = inter.author.display_avatar.url)
                embed.set_author(name = f"Клановый голосовой онлайн — {inter.author} | {clan_name}", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                await inter.response.edit_message(embed = embed, view = ClanBack())

            if custom_id == 'clan_send':
                embed = disnake.Embed(title = "Управление кланом", color = 3092790)
                embed.description = f'{inter.author.mention}, **Выберите** что вы хотите добавить/изменить'
                embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
                await inter.response.edit_message(embed = embed, view = ClanChoice())

            if custom_id == 'clan_post':
                embed = disnake.Embed(title = "Пост в канал #поиск", description = f'{inter.author.mention}, **Напишите** ниже **описание клана** которое будет опубликовано в посте', color = 3092790)
                embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
                await inter.send(embed = embed, components = [])
                def check(m): 
                    return m.author.id == inter.author.id
                try: 
                    desc_clan = await self.bot.wait_for("message", check = check, timeout = 500)
                except TimeoutError:
                    return
                embed = disnake.Embed(title = "Пост в канал #поиск", description = f'{inter.author.mention}, **Укажите** что **требуется** от нового **участника** клана', color = 3092790)
                embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
                await inter.send(embed = embed, components = [])
                def check(m): 
                    return m.author.id == inter.author.id
                try: 
                    request = await self.bot.wait_for("message", check = check, timeout = 500)
                except TimeoutError:
                    return
                embed = disnake.Embed(title = "Пост в канал #поиск", description = f'{inter.author.mention}, **Укажите** что **Вы** можете предоставить **новому участнику** клана', color = 3092790)
                embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
                await inter.send(embed = embed, components = [])
                def check(m): 
                    return m.author.id == inter.author.id
                try: 
                    propositions = await self.bot.wait_for("message", check = check, timeout = 500)
                except TimeoutError:
                    return
                embed = disnake.Embed(title = "Пост в канал #поиск", description = f'{inter.author.mention}, **Укажите** людей к которым обращаться по поводу **вступления** в клан', color = 3092790)
                embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
                await inter.send(embed = embed, components = [])
                def check(m): 
                    return m.author.id == inter.author.id
                try: 
                    peoples = await self.bot.wait_for("message", check = check, timeout = 500)
                except TimeoutError:
                    return
                embed = disnake.Embed(title = "Пост в канал #поиск", description = f'{inter.author.mention}, отправьте **Изображение**, которое хотите использовать в эмбеде.', color = 3092790)
                embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
                await inter.send(embed = embed)
                def check(m): 
                    return m.author.id == inter.author.id
                try:
                    image = await self.bot.wait_for("message", check = check, timeout = 500)
                except TimeoutError:
                    return

                clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
                role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
                clan_name = f"{role.name}"

                embed = disnake.Embed(title = f"Набор в клан {clan_name}", description = f"> {desc_clan.content}", color = 3092790)
                try:
                    for attach in image.attachments:
                        embed.set_image(url = str(attach))
                except:
                    embed.set_image(url = image.content)
                bot = self.bot
                embed.add_field(name = "Что требуется от вас", value = f"{request.content}", inline = False)
                embed.add_field(name = "Что мы можем вам дать", value = f"{propositions.content}", inline = False)
                embed.add_field(name = "По поводу вступления в клан", value = f"{peoples.content}", inline = False)
                await inter.send(embed = embed, view = ClanNabor(clan_name, desc_clan, request, propositions, peoples, image, bot))

            if custom_id[:8] == 'clan_top':
                idd = 1
                description = ''
                clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
                role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
                membersID = []
                for x in database.clanonline.find().sort("online",-1):
                    try:
                        member = disnake.utils.get(inter.guild.members, id = int(x['_id']))
                        for r in member.roles:
                            if r.id == role.id:
                                membersID.append(x['_id'])
                    except:
                        pass
                items_per_page = 10
                if not str(inter.author.id) in currentClanTopPage:
                    currentClanTopPage[str(inter.author.id)] = 0
                pages = [membersID[i:i + items_per_page] for i in range(0, len(membersID), items_per_page)]
                for member_id in pages[0]:
                    N = database.clanonline.find_one({'_id': str(member_id)})['online']
                    match idd:
                        case 1:
                            description += f"**<:11:1096126530247204966> — <@{member_id}>** <:microphone:1140294304556908695> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                        case 2:
                            description += f"**<:21:1096126528670138469> — <@{member_id}>** <:microphone:1140294304556908695> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                        case 3:
                            description += f"**<:31:1096126525683810465> — <@{member_id}>** <:microphone:1140294304556908695> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                        case 4:
                            description += f"**<:41:1096126532826697909> — <@{member_id}>** <:microphone:1140294304556908695> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                        case 5:
                            description += f"**<:51:1097534359675879515> — <@{member_id}>** <:microphone:1140294304556908695> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                        case 6:
                            description += f"**<:61:1107004738194653246> — <@{member_id}>** <:microphone:1140294304556908695> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                        case 7:
                            description += f"**<:71:1107004742326034593> — <@{member_id}>** <:microphone:1140294304556908695> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                        case 8:
                            description += f"**<:81:1107004743815008328> — <@{member_id}>** <:microphone:1140294304556908695> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                        case 9:
                            description += f"**<:91:1107004746822328350> — <@{member_id}>** <:microphone:1140294304556908695> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                        case 10:
                            description += f"**<:101:1107004740723802112> — <@{member_id}>** <:microphone:1140294304556908695> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    idd += 1
                    if idd > 10:
                        break
                embed = disnake.Embed(description = description, color = 3092790)
                embed.set_author(name = f"Топ по онлайну клана {role.name}", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_footer(text = f'Запросил(а) {inter.author}', icon_url = inter.author.display_avatar.url)
                return await inter.response.edit_message(content = inter.author.mention, embed = embed, view = ClanTopShop(inter.author.id))

            if custom_id == 'clan_shop':
                embed = disnake.Embed(color = 3092790)
                embed.set_author(name = f"Клановый магазин {inter.guild.name}", icon_url = inter.guild.icon.url)
                embed.add_field(name = '<:11:1096126530247204966> Добавить текстовый канал', value = '**Цена:** 2500 <:coin1:1096094598507532479>', inline = False)
                embed.add_field(name = '<:21:1096126528670138469> Добавить значок на роль', value = '**Цена:** 2500 <:coin1:1096094598507532479>', inline = False)
                embed.add_field(name = '<:31:1096126525683810465> Сменить название клана', value = '**Цена:** 1000 <:coin1:1096094598507532479>', inline = False)
                embed.add_field(name = '<:41:1096126532826697909> Изменить цвет', value = '**Цена:** 500 <:coin1:1096094598507532479>', inline = False)
                embed.add_field(name = '<:51:1097534359675879515> Добавить слоты в клан', value = '**Цена:** 250 за 1 слот <:coin1:1096094598507532479>', inline = False)
                embed.add_field(name = '<:61:1107004738194653246> Добавить голосовой канал', value = '**Цена:** 5000 <:coin1:1096094598507532479>', inline = False)
                await inter.response.edit_message(embed = embed, view = ClanShop())

            if custom_id == 'clan_list_of_deposit':
                top_users = {k: v for k, v in sorted(clan[str(inter.guild.id)][clan[str(inter.guild.id)][str(inter.author.id)]]['Deposit'].items(), key=lambda item: item[1], reverse=True)}
                names = ''
                idd = 1
                for postion, user in enumerate(top_users):
                    names += f'**{idd} — **<@!{user}> **{top_users[user]}** <:coin1:1096094598507532479>\n'
                    idd += 1
                embed = disnake.Embed(title="Список пожертвований на депозит клана", description = names, color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_footer(text = f"Всего на балансе клана {clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Balance']} <:coin1:1096094598507532479>")
                return await inter.response.edit_message(embed = embed, view = ClanBack())

            if custom_id == 'clan_blacklist':
                embed = disnake.Embed(color = 3092790, description = f"**Список ЧС клана** <@&{clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Role']}>: \n{' '.join([inter.guild.get_member(i).mention for i in clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['BanList']])} | **{' '.join([inter.guild.get_member(i).name for i in clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['BanList']])}**\n\n")
                return await inter.response.edit_message(embed = embed, view = ClanBack())

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        custom_id = inter.component.custom_id

        with open('clan_sweetness.json','r', encoding='utf-8') as f:
            clan = json.load(f)

        if custom_id == 'clan_accept':
            if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id or inter.author.id in clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin']:
                await inter.response.defer()
                member = disnake.utils.get(inter.guild.members, id = int(database.clan.find_one({'_id': str(inter.message.id)})['clan']))

                if not str(member.id) in clan[str(inter.guild.id)]:
                    clan[str(inter.guild.id)][str(member.id)] = 'Отсутствует'
                    with open('clan_sweetness.json', 'w') as f:
                        json.dump(clan,f)

                clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
                if clan[str(inter.guild.id)][str(clanxd)]['Limit'] == clan[str(inter.guild.id)][str(clanxd)]['ClanMembers']:
                    await inter.message.edit(view = Disabled())
                    embed = disnake.Embed(description = f'{inter.author.mention}, **Ваш** клан достиг **лимита участников**!', color = disnake.Color.red())
                    embed.set_author(name = f"Кланы {inter.guild.name}", icon_url = inter.guild.icon.url)
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    return await inter.send(ephemeral = True, embed = embed, view = ClanBack())

                if int(member.id) in clan[str(inter.guild.id)][str(clanxd)]['BanList']:
                    await inter.message.edit(view = Disabled())
                    embed = disnake.Embed(description = f'{inter.author.mention}, **Этот** пользователь находится в чёрном списке клана.', color = disnake.Color.red())
                    embed.set_author(name = f"Кланы {inter.guild.name}", icon_url = inter.guild.icon.url)
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    return await inter.send(ephemeral = True, embed = embed, view = ClanBack())

                if clan[str(inter.guild.id)][str(member.id)] == 'Отсутствует':
                    await inter.message.edit(view = Disabled())

                    clanxd = clan[str(960579506425446472)][str(inter.author.id)]
                    role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
                    role_id = int(clan[str(960579506425446472)][str(clanxd)]['Role'])

                    clan_invite[str(member.id)] = int(role_id)
                    msg = await self.bot.get_channel(1154463674346508390).send(member.id)

                    embed = disnake.Embed(description = f'{member.mention} теперь ты в клане **{role.name}**!', color = 3092790)
                    embed.set_author(url = "Клан", icon_url = inter.guild.icon.url)
                    embed.set_footer(text = f"Принял заявку: {inter.author}", icon_url = inter.author.display_avatar.url)
                    embed.set_image(url = "https://media.discordapp.net/attachments/1146880953743061143/1147985480131031050/file.jpg?width=676&height=676")
                    await member.send(embed = embed, components = [])

                    clan[str(960579506425446472)][str(clanxd)]['ClanMembers'] += 1
                    clan[str(960579506425446472)][str(member.id)] = clanxd
                    with open('clan_sweetness.json','w') as f:
                        json.dump(clan,f)

                    embed = disnake.Embed(description = f'Добро пожаловать в клан <@&{role_id}>', color = 3092790)
                    embed.set_author(name = f"Кланы {inter.guild.name}", icon_url = inter.guild.icon.url)
                    embed.set_footer(text = f"Принял заявку: {inter.author}", icon_url = inter.author.display_avatar.url)
                    return await self.bot.get_channel(int(clan[str(960579506425446472)][str(clanxd)]['TextChannel'])).send(member.mention, embed = embed)
                else:
                    await inter.message.edit(view = Disabled())
                    embed = disnake.Embed(description = f'У {member.mention} уже есть **клан**!', color = disnake.Color.red())
                    embed.set_author(name = f"Кланы {inter.guild.name}", icon_url = inter.guild.icon.url)
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    return await inter.send(ephemeral = True, embed = embed, view = ClanBack())

        if custom_id == 'clan_decline':
            if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id or inter.author.id in clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin']:
                return await inter.response.edit_message(components = [])

        if custom_id == "achievements_take_reward":
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description=f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color=3092790)
                embed.set_author(name = "Забрать награду", icon_url=inter.guild.icon.url)
                embed.set_thumbnail(url=inter.author.display_avatar.url)
                return await inter.send(ephemeral=True, embed=embed)
            
            achievements_reward = achievement_reward[str(inter.author.id)]
            achievements = achievement[str(inter.author.id)]

            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            clan[str(inter.guild.id)][clanxd]['Balance'] += int(achievements_reward)
            with open('clan_sweetness.json','w') as f:
                json.dump(clan,f)

            embed = disnake.Embed(description=f'{inter.author.mention}, **Вы** успешно **получили награду** за достижение в размере **{achievements_reward}** <:coin1:1096094598507532479>', color=3092790)
            embed.set_author(name = "Получить награду за достижение", icon_url=inter.guild.icon.url)
            embed.set_thumbnail(url=inter.author.display_avatar.url)
            await inter.response.edit_message(embed = embed, components = [])

            cluster.sweetness.achievements.update_one({'_id': str(inter.author.id)}, {'$set': {f'{str(achievements)}': "YES"}}, upsert = True)

        if custom_id.endswith('heroes'):
            guild = self.bot.get_guild(960579506425446472)
            embed = disnake.Embed(description="**Список ваших героев:**\n", color = 3092790)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            embed.set_author(name = f"Герои | {inter.guild.name}", icon_url = guild.icon.url)

            if not inter.message.content == inter.author.mention:
                embed.description = f"{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**"
                return await inter.send(ephemeral = True, embed = embed)
            
            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]

            if custom_id == "clan_list_heroes":
                for hero in cluster.sweetness.clan_heroes.find_one({"_id": str(clanxd)})["heroes"]:
                    embed.description += f"Герой: **{hero}** [Используется]\n"
                if len(cluster.sweetness.clan_heroes.find_one({"_id": str(clanxd)})["heroes"]) == 0:
                    embed.description += "Пусто"
                return await inter.response.edit_message(attachments = None, embed = embed, view = ClanBack())

            if custom_id == "clan_take_heroes":
                match int(clan_choice_hero[str(inter.author.id)]):
                    case 1:
                        clan_hero_cost[str(inter.author.id)] = 100000
                        clan_hero_name[str(inter.author.id)] = "Дерил Диксон"
                    case 2:
                        clan_hero_name[str(inter.author.id)] = "Девочка пост-эпохи"
                        clan_hero_cost[str(inter.author.id)] = 100000
                    case 3:
                        clan_hero_name[str(inter.author.id)] = "Голобуй дротик"
                        clan_hero_cost[str(inter.author.id)] = 100000
                    case 4:
                        clan_hero_name[str(inter.author.id)] = "Гробовщица"
                        clan_hero_cost[str(inter.author.id)] = 200000
                    case 5:
                        clan_hero_name[str(inter.author.id)] = "Бритва"
                        clan_hero_cost[str(inter.author.id)] = 300000
                    case 6:
                        clan_hero_name[str(inter.author.id)] = "Милитарист"
                        clan_hero_cost[str(inter.author.id)] = 400000
                    case 7:
                        clan_hero_name[str(inter.author.id)] = "Железный страж"
                        clan_hero_cost[str(inter.author.id)] = 500000
                    case 8:
                        clan_hero_name[str(inter.author.id)] = "Жнец"
                        clan_hero_cost[str(inter.author.id)] = 600000
                    case 9:
                        clan_hero_name[str(inter.author.id)] = "Арсенал"
                        clan_hero_cost[str(inter.author.id)] = 700000
                    case 10:
                        clan_hero_name[str(inter.author.id)] = "Разрушитель"
                        clan_hero_cost[str(inter.author.id)] = 800000
                    case 11:
                        clan_hero_name[str(inter.author.id)] = "Вооружённый безумец"
                        clan_hero_cost[str(inter.author.id)] = 900000
                    case 12:
                        clan_hero_name[str(inter.author.id)] = "Изгой"
                        clan_hero_cost[str(inter.author.id)] = 1000000
                    case 13:
                        clan_hero_name[str(inter.author.id)] = "Защитник рассвета"
                        clan_hero_cost[str(inter.author.id)] = 2000000
                    case 14:
                        clan_hero_name[str(inter.author.id)] = "Укротитель"
                        clan_hero_cost[str(inter.author.id)] = 3000000
                    case 15:
                        clan_hero_name[str(inter.author.id)] = "Ада"
                        clan_hero_cost[str(inter.author.id)] = 4000000
                    case 16:
                        clan_hero_name[str(inter.author.id)] = "Мегги Грин"
                        clan_hero_cost[str(inter.author.id)] = 5000000
                embed.description = f'{inter.author.mention}, **Вы** действительно хотите приобрести героя за **{clan_hero_cost[str(inter.author.id)]}** <:coin1:1096094598507532479>'
                return await inter.response.edit_message(attachments = None, embed = embed, view = ClanHeroBuy())
            if custom_id == "clan_buy_heroes":
                clan_take = clan[str(guild.id)][clanxd]
                clan_balance = f"{clan_take['Balance']}"
                channel = database.clan.find_one({'_id': str(clanxd)})['channel_3'] # news channel
                cost = clan_hero_cost[str(inter.author.id)]
                
                clan_hero = clan_hero_name[str(inter.author.id)]

                if str(clan_hero) in database.clan_heroes.find_one({'_id': str(clanxd)})['heroes']:
                    embed.description = f'{inter.author.mention}, **Вы** не можете приобрести героя, которого вы и так **купили**'
                    return await inter.response.edit_message(embed = embed)
                if cost > int(clan_balance):
                    embed.description = f'{inter.author.mention}, У **Вашего** клана на балансе **недостаточно средств!**'
                    return await inter.response.edit_message(embed = embed)

                database.clan_heroes.update_one({'_id': str(clanxd)}, {'$push': {'heroes': clan_hero}}, upsert = True)

                clan_take['Balance'] -= int(cost)
                with open('clan_sweetness.json','w') as f:
                    json.dump(clan,f)

                embed.description = f"### **Ваш** клан успешно **приобрел героя** {clan_hero} за **{cost}** <:coin1:1096094598507532479>"
                embed.set_footer(text = f"Приобрел героя: {inter.author}", icon_url = inter.author.display_avatar.url)
                embed.set_thumbnail("https://cdn.discordapp.com/attachments/1147505417417670726/1147515271934906408/battle_1_1.png")
                msg = await self.bot.get_channel(channel).send(f"<@&{clanxd}>", embed = embed)

                embed.description = f'{inter.author.mention}, **Вы** успешно приобрели героя {clan_hero} за **{cost}** <:coin1:1096094598507532479>'
                return await inter.response.edit_message(embed = embed, view = ClanBack())
            
        if custom_id.endswith('alliance'):
            guild = self.bot.get_guild(960579506425446472)
            embed = disnake.Embed(color = 3092790)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            embed.set_author(name = f"Альянс", icon_url = guild.icon.url)

            if not inter.message.content == inter.author.mention:
                embed.description = f"{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**"
                return await inter.send(ephemeral = True, embed = embed)
            
            clanxd = clan[str(guild.id)][str(inter.author.id)]
            clan_take = clan[str(guild.id)][clanxd]
            clan_balance = f"{clan_take['Balance']}"

            if custom_id == "clan_accept_alliance":

                await inter.message.edit(components = [])

                clan_balance = f"{clan_take['Balance']}"
                clan_alliance = database.channels.find_one({'_id': str(inter.message.id)})['alliance']
                clan_name = disnake.utils.get(guild.roles, id = int(clan_alliance["Role"]))
                clan_balance = f"{clan_take['Balance']}"

                clan_alliance_name = disnake.utils.get(guild.roles, id = int(clanxd))

                if int(25000) > int(clan_balance):
                    embed.description = f'{inter.author.mention}, У **Вашего** клана на балансе **недостаточно средств!**'
                    return await inter.send(embed = embed)

                clan_balance = f"{clan_alliance['Balance']}"
                if int(25000) > int(clan_balance):
                    embed.description = f'{inter.author.mention}, У **второго** клана на балансе **недостаточно средств!**'
                    return await inter.send(embed = embed)

                cluster.sweetness.clan_alliance.update_one({'_id': str(clanxd)}, {'$set': {'alliance': clan_alliance["Role"]}}, upsert = True)
                cluster.sweetness.clan_alliance.update_one({'_id': str(clan_alliance["Role"])}, {'$set': {'alliance': clanxd}}, upsert = True)

                embed.description = f"{inter.author.mention}, **Вы** успешно **создали** альянс с кланом **{clan_name}**"
                await inter.author.send(embed = embed)

                clan_owner = disnake.utils.get(guild.members, id = int(clan_alliance['Owner']))

                embed = disnake.Embed(color = 3092790)
                embed.set_thumbnail(url = clan_owner.display_avatar.url)
                embed.set_author(name = f"Предложение Альянса", icon_url = guild.icon.url)
                embed.description = f"{clan_owner.mention}, **Теперь** у вас есть **союз** с альянсом {clan_alliance_name.name} под **руководством лидера** {inter.author.mention}."
                await clan_owner.send(embed = embed)

                clan_take['Balance'] -= 25000
                clan_alliance['Balance'] -= 25000
                with open('clan_sweetness.json','w') as f:
                    json.dump(clan,f)

            if custom_id == "clan_war_alliance":
                if clan_take['Owner'] == inter.author.id:
                    embed.description = f"* {inter.author.mention}, **Выберите альянса**"
                    return await inter.response.edit_message(attachments = None, embed = embed, view = ClanAlliance())
            
            elif custom_id == "clan_create_alliance":
                embed.description = f'{inter.author.mention}, **Выберите** клан с которым **Вы** хотите заключить **альянс:**'
                return await inter.response.edit_message(embed = embed, view = ClanView(self.bot, clanxd))
        
        if custom_id == "clan_zombie_attack":
            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = f"Клановые Битвы | {inter.guild.name}", icon_url = inter.guild.icon.url)
            embed.set_thumbnail("https://cdn.discordapp.com/attachments/1147505417417670726/1147515271934906408/battle_1_1.png")

            if not inter.message.content == inter.author.mention:
                embed.description = f"{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**"
                return await inter.send(ephemeral = True, embed = embed)
            
            await inter.response.defer()
        
            clan_zombie = clan_attack_choice[str(inter.author.id)]
            
            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
            clan_name = f"{role.name}"
            role_take = disnake.utils.get(inter.guild.roles, id = int(clanxd))

            data_attack = database.clan_attack.find_one({'_id': str(clanxd)})['time']
            if not data_attack == "Можно":
                remaining_minutes = (data_attack - datetime.datetime.now()).total_seconds() // 60
                if not remaining_minutes < 1:
                    embed.description = f"{inter.author.mention}, **Вам** ещё стоит **подождать**\nСледущая атака будет доступна в: {data_attack}, прежде чем **нападать**"
                    return await inter.message.edit(embed = embed)

            cluster.sweetness.clan_attack.update_one({'_id': str(clanxd)}, {'$set': {'time': datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(minutes = 30)}}, upsert = True)
            cluster.sweetness.clan_zombie.update_one({'_id': str(clanxd)}, {'$set': {'target': clan_zombie, 'time': datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(minutes = 5)}}, upsert = True)
            news_channel = database.clan.find_one({'_id': str(clanxd)})['channel_3'] # news channel

            embed.description = f"### Ваш клан начал нападение на зомби {clan_zombie}-ого уровня! Войска прибудут через 5 минут в точку назначения."
            msg = await self.bot.get_channel(news_channel).send(f"<@&{clanxd}>", embed = embed)

            im = Image.open('clan_map_main.png')
            idd = 1
        
            guild_clans = clan.get(str(inter.guild.id), {})

            attackers = []
            defenders = []
            zombie_attackers = []
            for clan_key, clan_value in guild_clans.items():
                if isinstance(clan_value, dict):
                    try:
                        role = disnake.utils.get(inter.guild.roles, id=int(clan_key))
                        level = clan[str(inter.guild.id)][str(clan_key)]['Level']

                        if cluster.sweetness.clan_shield.count_documents({"_id": str(clan_key)}) == 0:
                            cluster.sweetness.clan_shield.insert_one({"_id": str(clan_key), "activate": "Отсутствует", "time": datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=5)})

                        shield = database.clan_shield.find_one({'_id': str(clan_key)})['activate']

                        match idd:
                            case 1:
                                coordinates = (540, 290)  # розовый
                                size = 18
                                fill = "#B684E8"
                                if shield == "YES":
                                    transparent_image1 = Image.open('shield_pink.png')
                                    im.paste(transparent_image1, (533, 185), transparent_image1)
                            case 2:
                                coordinates = (312, 177)  # синий замок (ОРАНЖЕВЫЙ)
                                size = 18
                                fill = "#D8904E"
                                if shield == "YES":
                                    transparent_image1 = Image.open('shield_orange.png')
                                    im.paste(transparent_image1, (303, 96), transparent_image1)
                            case 3:
                                coordinates = (790, 171)  # лайм
                                size = 18
                                fill = "#6BFF8C"
                                if shield == "YES":
                                    transparent_image1 = Image.open('shield_lime.png')
                                    im.paste(transparent_image1, (686, 143), transparent_image1)
                            case 4:
                                coordinates = (494, 365)  # АФРИКА (MAGNET)
                                size = 18
                                fill = "#BD1F58"
                                if shield == "YES":
                                    transparent_image1 = Image.open('shield_magenta.png')
                                    im.paste(transparent_image1, (378, 326), transparent_image1)
                            case 5:
                                coordinates = (779, 557)  # АЦТЕК (СИНИЙ)
                                size = 16
                                fill = "#2FDBBC"
                                if shield == "YES":
                                    transparent_image1 = Image.open('shield_aztec.png')
                                    im.paste(transparent_image1, (809, 493), transparent_image1)
                            case 6:
                                coordinates = (239, 442)  # КРАСНЫЙ
                                size = 18
                                fill = "#AF3A3A"
                                if shield == "YES":
                                    transparent_image1 = Image.open('shield_red.png')
                                    im.paste(transparent_image1, (246, 439), transparent_image1)
                            case 7:
                                coordinates = (137, 343)  # ФИОЛЕТОВЫЙ
                                size = 18
                                fill = "#8458FF"
                                if shield == "YES":
                                    transparent_image1 = Image.open('shield_purple.png')
                                    im.paste(transparent_image1, (116, 243), transparent_image1)
                            case 8:
                                coordinates = (769, 175)  # ЗЕЛЕНЫЙ
                                size = 18
                                fill = "#18D214"
                                if shield == "YES":
                                    transparent_image1 = Image.open('shield_green.png')
                                    im.paste(transparent_image1, (1, 182), transparent_image1)
                            case _:
                                coordinates = None
        
                        if coordinates:
                            if not database.clan_defender.count_documents({"_id": str(clan_key)}) == 0: 
                                defenders.append({"clanxd": clan_key, "position": coordinates})
                            if not database.clan_war.count_documents({"_id": str(clan_key)}) == 0: 
                                attackers.append({"clanxd": clan_key, "position": coordinates})
                            if not database.clan_zombie.count_documents({"_id": str(clan_key)}) == 0:
                                lvl = database.clan_zombie.find_one({'_id': str(clanxd)})['target']
                                match int(lvl):
                                    case 1:
                                        coords = (793, 493)
                                    case 2:
                                        coords = (274, 299)
                                    case 3:
                                        coords = (144, 137)
                                    case 4:
                                        coords = (636, 347)
                                    case 5:
                                        coords = (631, 345)
                                    case 6:
                                        coords = (711, 321)
                                    case 7:
                                        coords = (352, 389)
                                    case _:
                                        coords = None

                                zombie_attackers.append({"clanxd": clan_key, "position": coords, "position_clanxd": coordinates})

                            ImageDraw.Draw(im).text(coordinates, str(f"{role.name[:10]}\nУр. {level}"), font=ImageFont.truetype('Montserrat-Bold.ttf', encoding='UTF-8', size=size), fill=fill)
                        idd += 1
                    except:
                        pass
            for attacker in attackers:
                for defender in defenders:
                    attacker_cords = zombie_attackers.get("position")

                    draw = ImageDraw.Draw(im)
                    neon_color = (255, 0, 0)

                    draw.line((attacker_cords, defender_cords), fill=neon_color, width=3)

                    x, y = attacker_cords
                
                    y -= 40
                    
                    machine_cords = (x, y)

                    transparent_image1 = Image.open('machine.png')
                    im.paste(transparent_image1, (machine_cords), transparent_image1)

                    x, y = attacker_cords

                    x += 28
                    y -= 21
                    
                    text_cords = (x, y)

                    ImageDraw.Draw(im).text((text_cords), str(f"Идет атака"), font=ImageFont.truetype('Montserrat-Bold.ttf', encoding='UTF-8', size=15), fill=(255, 255, 255))

            for zombie in zombie_attackers:
                attacker_cords = zombie.get("position_clanxd")
                zombie_cords = zombie.get("position")

                draw = ImageDraw.Draw(im)
                neon_color = (255, 0, 0)

                draw.line((attacker_cords, zombie_cords), fill=neon_color, width=3)

                x, y = attacker_cords
            
                y -= 27
                
                machine_cords = (x, y)

                transparent_image1 = Image.open('machine.png')
                im.paste(transparent_image1, (machine_cords), transparent_image1)

                x, y = attacker_cords

                x += 28
                y -= 21
                
                text_cords = (x, y)

                ImageDraw.Draw(im).text((text_cords), str(f"Идет атака"), font=ImageFont.truetype('Montserrat-Bold.ttf', encoding='UTF-8', size=15), fill=(255, 255, 255)) 

            im.save('out_clan_map.png')
        
            await inter.message.edit(attachments = None, embed=None, file=disnake.File('out_clan_map.png'), view=ClanMap())

        if custom_id == "clan_accept_attack":
            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = f"Клановые Битвы | {inter.guild.name}", icon_url = inter.guild.icon.url)
            embed.set_thumbnail("https://cdn.discordapp.com/attachments/1147505417417670726/1147515271934906408/battle_1_1.png")

            if not inter.message.content == inter.author.mention:
                embed.description = f"{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**"
                return await inter.send(ephemeral = True, embed = embed)
            
            await inter.response.defer()
            with open('clan_sweetness.json', 'r') as f:
                clan_data = json.load(f)
        
            clan_choice = clan_attack_choice[str(inter.author.id)]
            shield = database.clan_shield.find_one({'_id': str(clan_choice)})['activate']
            clan_online = database.clan_online.find_one({'_id': str(clan_choice)})['clan_online']

            clan_points = clan_online // 3600
            clan_level = clan_points // 20 + 1
            if not int(clan_level) > 4:
                embed.description = f"{inter.author.mention}, **Вы** не можете напасть на **клан**, который **ниже 5 уровня.**"
                return await inter.message.edit(embed = embed)
            if not shield == "Отсутствует":
                embed.description = f"{inter.author.mention}, **Вы** не можете напасть на **клан**, который находится под **щитом.**"
                return await inter.message.edit(embed = embed)
            
            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
            clan_name = f"{role.name}"
            role_take = disnake.utils.get(inter.guild.roles, id = int(clanxd))

            shield = database.clan_shield.find_one({'_id': str(clanxd)})['activate']
            if not shield == "Отсутствует":
                embed.description = f"{inter.author.mention}, **Вы** не можете напасть на **клан**, **находясь** при этом под **щитом.**"
                return await inter.message.edit(embed = embed)
            data_attack = database.clan_attack.find_one({'_id': str(clanxd)})['time']
            if not data_attack == "Можно":
                remaining_minutes = (data_attack - datetime.datetime.now()).total_seconds() // 60
                if not remaining_minutes < 1:
                    embed.description = f"{inter.author.mention}, **Вам** ещё стоит **подождать**\nСледущая атака будет доступна в: {data_attack}, прежде чем **нападать**"
                    return await inter.message.edit(embed = embed)

            cluster.sweetness.clan_attack.update_one({'_id': str(clanxd)}, {'$set': {'time': datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(minutes = 120)}}, upsert = True)
            cluster.sweetness.clan_war.update_one({'_id': str(clanxd)}, {'$set': {'target': clan_choice, 'time': datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(minutes = 5)}}, upsert = True)
            cluster.sweetness.clan_defender.update_one({'_id': str(clan_choice)}, {'$set': {'attacker': clanxd}}, upsert = True)

            news_channel = database.clan.find_one({'_id': str(clan_choice)})['channel_3'] # news channel

            embed.description = f"### Ваш клан атакуют! Через 5 минут вражеские войска будут у вашего замка! Зайдите в голосовой канал, чтобы усилить защиту!"
            msg = await self.bot.get_channel(news_channel).send(f"<@&{clan_choice}>", embed = embed)

            news_channel = database.clan.find_one({'_id': str(clanxd)})['channel_3'] # news channel

            embed.description = f"### Ваш клан начал нападение на клан <@&{clan_choice}>! Войска прибудут через 5 минут в точку назначения."
            msg = await self.bot.get_channel(news_channel).send(f"<@&{clanxd}>", embed = embed)

            im = Image.open('clan_map_main.png')
            idd = 1
        
            guild_clans = clan_data.get(str(inter.guild.id), {})

            attackers = []
            defenders = []
            for clan_key, clan_value in guild_clans.items():
                if isinstance(clan_value, dict):
                    try:
                        role = disnake.utils.get(inter.guild.roles, id=int(clan_key))
                        level = clan[str(inter.guild.id)][str(clan_key)]['Level']

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
                            coordinates = (779, 557) # АЦТЕК (СИНИЙ)
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
                            if not database.clan_defender.count_documents({"_id": str(clan_key)}) == 0: 
                                defenders.append({"clanxd": clan_key, "position": coordinates})
                            if not database.clan_war.count_documents({"_id": str(clan_key)}) == 0: 
                                attackers.append({"clanxd": clan_key, "position": coordinates})
                            ImageDraw.Draw(im).text(coordinates, str(f"{role.name[:10]}\nУр. {level}"), font=ImageFont.truetype('Montserrat-Bold.ttf', encoding='UTF-8', size=size), fill=fill)
                        idd += 1
                    except:
                        pass
            for attacker in attackers:
                for defender in defenders:
                    attacker_cords = attacker.get("position")
                    defender_cords = defender.get("position")

                    draw = ImageDraw.Draw(im)
                    neon_color = (255, 0, 0)


                    draw.line((attacker_cords, defender_cords), fill=neon_color, width=3)

                    x, y = attacker_cords
                
                    y -= 40
                    
                    machine_cords = (x, y)

                    transparent_image1 = Image.open('machine.png')
                    im.paste(transparent_image1, (machine_cords), transparent_image1)

                    x, y = attacker_cords

                    x += 28
                    y -= 21
                    
                    text_cords = (x, y)

                    ImageDraw.Draw(im).text((text_cords), str(f"Идет атака"), font=ImageFont.truetype('Montserrat-Bold.ttf', encoding='UTF-8', size=15), fill=(255, 255, 255)) 

            im.save('out_clan_map.png')
        
            await inter.message.edit(attachments = None, embed=None, file=disnake.File('out_clan_map.png'), view=ClanMap())

        if custom_id == "clan_attack_zombie":
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(title = f'Атаковать зомби', color = 3092790)
                embed.description = f"{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**"
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            
            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = "Атаковать зомби", icon_url = inter.guild.icon.url)
            if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id or inter.author.id in clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin']:
                embed.description = f"{inter.author.mention}, Выберите, на какого зомби вы хотите напасть:"
                await inter.response.edit_message(content = inter.author.mention, embed = embed, view = AttackZombie())
            else:
                embed.description = f'### > {inter.author.mention}, У **Вас** недостаточно **прав** на выполнение **этой команды**'
                return await inter.send(ephemeral = True, embed = embed)
            
        if custom_id == "clan_attack_castle":
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(title = f'Атаковать клан', color = 3092790)
                embed.description = f"{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**"
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            
            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = "Атаковать клан", icon_url = inter.guild.icon.url)
            clan_id = clan[str(inter.guild.id)][str(inter.author.id)]
            if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id or inter.author.id in clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin']:
                embed.description = f"{inter.author.mention}, **Выберите**, на какой **клан** вы хотите **напасть**:"
                await inter.response.edit_message(content = inter.author.mention, embed = embed, view = AttackClan(self.bot, clan_id))
            else:
                embed.description = f'### > {inter.author.mention}, У **Вас** недостаточно **прав** на выполнение **этой команды**'
                return await inter.send(ephemeral = True, embed = embed)

        if custom_id == "clan_battle_rules":
            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = "Правила битвы кланов", icon_url = inter.guild.icon.url)
            embed.description = "**Для нападения** на зомби **можно** использовать **любой состав** армии. **При нападении** на зомби **союзный альянс** может отправить **подкрепление**.\n\
            **После завершения битвы** с зомби или вражеским кланом, армия переходит в **режим отдыха на 30 минут**.\n\n\
            **Общее количество доступных** героев составляет `20`. **Нельзя нападать** на вражеский клан, когда у него **активен барьер**.\n\n\
            **Примерные расценки на нападение:**\n \
            > Зомби **1-ого** уровня: 20000 Боевой Мощи.\n \
            > Зомби **2-ого** уровня: 100.000 Боевой Мощи.\n \
            > Зомби **3-ого** уровня: 1.000.000 Боевой Мощи.\n \
            > Зомби **4-ого** уровня: 10.000.000 Боевой Мощи.\n \
            > Зомби **5-ого** уровня: 45.000.000 Боевой Мощи.\n \
            > Зомби **6-ого** уровня: 100.000.000 Боевой Мощи.\n \
            > Босс **7-ого** уровня: 1.000.000.000 Боевой Мощи.\n\n* Боевая мощь зарабатывается различными способами: Найм героев, альянс кланов, участники клана в голосовых каналах, всего количество участников"
            await inter.send(ephemeral = True, embed = embed)

        if custom_id.startswith('achievements'):
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(title = f'Квесты кланов', color = 3092790)
                embed.description = f"{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**"
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)

            achievements_count = 0

            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
            clan_name = f"{role.name}"
            role_take = disnake.utils.get(inter.guild.roles, id = int(clanxd))
            clan_alliance = database.clan_alliance.find_one({'_id': str(clanxd)})['alliance']

            if database.clan_win.count_documents({"_id": str(clanxd)}) == 0:
                database.clan_win.insert_one({"_id": str(clanxd), "win": 0})
            if database.clan_online.count_documents({"_id": str(clanxd)}) == 0:
                database.clan_online.insert_one({"_id": str(clanxd), "clan_online": 0})
            if database.clan_heroes.count_documents({"_id": str(clanxd)}) == 0:
                database.clan_heroes.insert_one({"_id": str(clanxd), "heroes": []})
            if database.clan_rating.count_documents({"_id": str(clanxd)}) == 0:
                database.clan_rating.insert_one({"_id": str(clanxd), "rating": 0})

            clan_online = database.clan_online.find_one({'_id': str(clanxd)})['clan_online']
            clan_points = clan_online // 3600
            clan_level = clan_points // 20 + 1
            description = ""

            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = f"Ачивки клана — {clan_name} | {inter.guild.name}", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)

            if custom_id == 'achievements_next_1' or custom_id == "achievements_main":
                await inter.response.defer()

                if len(role_take.members) >= 25:
                    cluster.sweetness.achievements_count.update_one({'_id': str(inter.author.id)}, {'$set': {'1': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:check_mark:1066791513390075954> Первобытное общество\n'
                else:
                    description += '<:cross:1066791510877667428> Первобытное общество\n'
                if len(role_take.members) >= 50:
                    cluster.sweetness.achievements_count.update_one({'_id': str(inter.author.id)}, {'$set': {'2': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:check_mark:1066791513390075954> Индустриальное общество\n'
                else:
                    description += '<:cross:1066791510877667428> Индустриальное общество\n'
                if len(role_take.members) >= 100:
                    cluster.sweetness.achievements_count.update_one({'_id': str(inter.author.id)}, {'$set': {'3': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:check_mark:1066791513390075954> Постиндустриальное общество\n'
                else:
                    description += '<:cross:1066791510877667428> Постиндустриальное общество\n'

                if int(database.clan_win.find_one({'_id': str(clanxd)})['win']) >= 1:
                    cluster.sweetness.achievements_count.update_one({'_id': str(inter.author.id)}, {'$set': {'4': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:check_mark:1066791513390075954> Вот он - вкус победы!\n'
                else:
                    description += '<:cross:1066791510877667428> Вот он - вкус победы!\n'

                if int(database.clan_win.find_one({'_id': str(clanxd)})['win']) >= 5:
                    cluster.sweetness.achievements_count.update_one({'_id': str(inter.author.id)}, {'$set': {'5': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:check_mark:1066791513390075954> Больше, мне нужно больше!\n'
                else:
                    description += '<:cross:1066791510877667428> Больше, мне нужно больше!\n'

                if int(database.clan_win.find_one({'_id': str(clanxd)})['win']) >= 10:
                    cluster.sweetness.achievements_count.update_one({'_id': str(inter.author.id)}, {'$set': {'6': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:check_mark:1066791513390075954> Вот он - вкус победы!\n'
                else:
                    description += '<:cross:1066791510877667428> Вот он - вкус победы!\n'

                if int(database.clan_win.find_one({'_id': str(clanxd)})['win']) >= 20:
                    cluster.sweetness.achievements_count.update_one({'_id': str(inter.author.id)}, {'$set': {'7': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:check_mark:1066791513390075954> Главное не то, как ты бьешь, а как держишь удар!\n'
                else:
                    description += '<:cross:1066791510877667428> Главное не то, как ты бьешь, а как держишь удар!\n'
                    

                if int(database.clan_online.find_one({'_id': str(clanxd)})['clan_online']) >= 3600000:
                    cluster.sweetness.achievements_count.update_one({'_id': str(inter.author.id)}, {'$set': {'8': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:check_mark:1066791513390075954> Бро, тебе надо больше тренироваться!\n'
                else:
                    description += '<:cross:1066791510877667428> Бро, тебе надо больше тренироваться!\n'

                if int(database.clan_online.find_one({'_id': str(clanxd)})['clan_online']) >= 18000000:
                    cluster.sweetness.achievements_count.update_one({'_id': str(inter.author.id)}, {'$set': {'9': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:check_mark:1066791513390075954> Не суетись, всему своё время!\n'
                else:
                    description += '<:cross:1066791510877667428> Не суетись, всему своё время!\n'

                if int(database.clan_online.find_one({'_id': str(clanxd)})['clan_online']) >= 36000000:
                    cluster.sweetness.achievements_count.update_one({'_id': str(inter.author.id)}, {'$set': {'10': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:check_mark:1066791513390075954> Клан отаку!\n'
                else:
                    description += '<:cross:1066791510877667428> Клан отаку!\n'

                if int(database.clan_online.find_one({'_id': str(clanxd)})['clan_online']) >= 180000000:
                    cluster.sweetness.achievements_count.update_one({'_id': str(inter.author.id)}, {'$set': {'11': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:check_mark:1066791513390075954> По лестнице к успеху!\n'
                else:
                    description += '<:cross:1066791510877667428> По лестнице к успеху!\n'

                if int(clan_level) >= 5:
                    cluster.sweetness.achievements_count.update_one({'_id': str(inter.author.id)}, {'$set': {'12': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:check_mark:1066791513390075954> Небоскрёб Прогресса!\n'
                else:
                    description += '<:cross:1066791510877667428> Небоскрёб Прогресса!\n'


                if int(clan_level) >= 15:
                    cluster.sweetness.achievements_count.update_one({'_id': str(inter.author.id)}, {'$set': {'13': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:check_mark:1066791513390075954> Король Кланов!\n'
                else:
                    description += '<:cross:1066791510877667428> Король Кланов!\n'

                if int(clan_level) >= 30:
                    cluster.sweetness.achievements_count.update_one({'_id': str(inter.author.id)}, {'$set': {'14': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:check_mark:1066791513390075954> Вершина Кланового Мира!\n'
                else:
                    description += '<:cross:1066791510877667428> Вершина Кланового Мира!\n'

                if len(database.clan_heroes.find_one({'_id': str(clanxd)})['heroes']) >= 1:
                    cluster.sweetness.achievements_count.update_one({'_id': str(inter.author.id)}, {'$set': {'15': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:check_mark:1066791513390075954> Первый союзник!\n'
                else:
                    description += '<:cross:1066791510877667428> Первый союзник!\n'

                embed.description = f"Количество **выполненных достижений** на этой странице: **{achievements_count}**\n\n{description}"
                embed.set_footer(text = "Страница 1 из 2")
                await inter.message.edit(attachments=None, embed = embed, view = ClanQuest())
            if custom_id == 'achievements_next_2':
                await inter.response.defer()

                if len(database.clan_heroes.find_one({'_id': str(clanxd)})['heroes']) >= 5:
                    cluster.sweetness.achievements_count.update_one({'_id': str(inter.author.id)}, {'$set': {'16': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:check_mark:1066791513390075954> Служители Пятерых!\n'
                else:
                    description += '<:cross:1066791510877667428> Служители Пятерых!\n'
                if len(database.clan_heroes.find_one({'_id': str(clanxd)})['heroes']) >= 15:
                    cluster.sweetness.achievements_count.update_one({'_id': str(inter.author.id)}, {'$set': {'17': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:check_mark:1066791513390075954> Армия Великих Пятнадцати!\n'
                else:
                    description += '<:cross:1066791510877667428> Армия Великих Пятнадцати!\n'
                if len(database.clan_heroes.find_one({'_id': str(clanxd)})['heroes']) >= 20:
                    cluster.sweetness.achievements_count.update_one({'_id': str(inter.author.id)}, {'$set': {'18': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:check_mark:1066791513390075954> Мастер Рекрутинга!\n'
                else:
                    description += '<:cross:1066791510877667428> Мастер Рекрутинга!\n'
                if not str(database.clan_alliance.find_one({'_id': str(clanxd)})['alliance']) == "Отсутствует":
                    cluster.sweetness.achievements_count.update_one({'_id': str(inter.author.id)}, {'$set': {'20': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:check_mark:1066791513390075954> Клановый союзник!!\n'
                else:
                    description += '<:cross:1066791510877667428> Клановый союзник!\n'

                embed.description = f"Количество **выполненных достижений** на этой странице: **{achievements_count}**\n\n{description}"
                embed.set_footer(text = "Страница 2 из 2")
                await inter.message.edit(attachments=None, embed = embed, view = ClanQuest2())

        if custom_id == "clan_war_settings":
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_author(name = f"Клан", icon_url = inter.guild.icon.url)
                return await inter.send(ephemeral = True, embed = embed)
            
            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
            clan_name = f"{role.name}"
            rating = database.clan_rating.find_one({'_id': str(clanxd)})['rating']
            role_take = disnake.utils.get(inter.guild.roles, id = int(clanxd))

            embed = Embed(color=3092790)
            embed.set_thumbnail(url = inter.author.display_avatar.url)

            embed.add_field(name = "Рейтинг", value = f"```🏆 {rating}```")
            clan_heroes = len(cluster.sweetness.clan_heroes.find_one({'_id': str(clanxd)})['heroes'])
            voice_members = 1
            if int(clan_heroes) == 0:
                power = len(role_take.members) * 50 * voice_members
            else:
                for member in role_take.members:
                    try:
                        channel = member.voice.channel.id
                        voice_members += 1
                    except:
                        pass
                power_heroes = len(cluster.sweetness.clan_heroes.find_one({'_id': str(clanxd)})['heroes']) * 100
                power = len(role_take.members) * 50 * voice_members * int(power_heroes)
            embed.add_field(name = "Ваша боевая мощь клана:", value = f"```⚔️ {power}```")
            embed.add_field(name = "Герои клана:", value = f'```{len(cluster.sweetness.clan_heroes.find_one({"_id": str(clanxd)})["heroes"])}/16```')
            embed.add_field(name = "Армия:", value = f"```???/???```")
            embed.set_author(name = f"Отряд клана {clan_name}", icon_url = inter.guild.icon.url)
            return await inter.response.edit_message(attachments = None, embed = embed, view = ClanSquad())

        if custom_id.endswith("shield"):
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_author(name = f"Клан", icon_url = inter.guild.icon.url)
                return await inter.send(ephemeral = True, embed = embed)

            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
            clan_name = f"{role.name}"

            embed = disnake.Embed(color = 3092790)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            embed.set_author(name = f"Клановый щит {clan_name}", icon_url = inter.guild.icon.url)

            if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id or inter.author.id in clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin']:

                if not inter.message.content == inter.author.mention:
                    embed.description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**'
                    return await inter.send(ephemeral = True, embed = embed)

                if custom_id == "clan_war_shield":

                    if cluster.sweetness.clan_shield.count_documents({"_id": str(clanxd)}) == 0:
                        cluster.sweetness.clan_shield.insert_one({"_id": str(clanxd), "activate": "Отсутствует", "time": datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=5)})

                    data_shield = cluster.sweetness.clan_shield.find_one({'_id': str(clanxd)})['time']
                    remaining_days = (data_shield - datetime.datetime.now()).days
                    if data_shield > datetime.datetime.now():
                        sec = data_shield - datetime.datetime.now()

                        hours = sec // hour
                        minutes = (sec - (sec // hour * hour)) // 60
                        seconds = (str(sec.seconds % 60).split('.')[0])

                        embed.description=f"{inter.author.mention}, **Вы** уже **активировали** щит **ранее**, приходите снова через **{hours}ч. {minutes}м. {seconds}с.**"
                        return await inter.send(embed = embed, ephemeral=True)

                    embed.description = f"{inter.author.mention}, **Вы** действительно хотите **активировать** щит на **24 часа**? За **100.000** <:coin1:1096094598507532479>\n**Вы** не сможете ни **атаковать**, ни быть **атакованным**"
                    return await inter.response.edit_message(embed = embed, view = ClanShield())

                if custom_id == "clan_accept_shield":
                    clan_balance = f"{clan[str(inter.guild.id)][clanxd]['Balance']}"
                    if int(100000) > int(clan_balance):
                        embed = disnake.Embed(description = f'{inter.author.mention}, У **Вашего** клана на балансе **недостаточно средств!**', color = 3092790)
                        embed.set_author(name = f"Клан", icon_url = inter.guild.icon.url)
                        embed.set_thumbnail(url = inter.author.display_avatar.url)
                        return await inter.send(embed = embed)

                    new_date = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(days=1)
                    cluster.sweetness.clan_shield.update_one({'_id': str(clanxd)}, {'$set': {'time': new_date}}, upsert = True)
                    cluster.sweetness.clan_shield.update_one({'_id': str(clanxd)}, {'$set': {'activate': "YES"}}, upsert = True)

                    clan_take = clan[str(inter.guild.id)][clanxd]
                    clan_take['Balance'] -= 100000
                    with open('clan_sweetness.json','w') as f:
                        json.dump(clan,f)

                    embed.description = f"{inter.author.mention}, **Вы** успешно **активировали** щит на **24 часа** в клане **{clan_name}**"
                    return await inter.response.edit_message(embed = embed, view = ClanBack())
            else:
                embed.description = f'### > {inter.author.mention}, У **Вас** недостаточно **прав** на выполнение **этой команды**'
                return await inter.send(ephemeral = True, embed = embed)
            
        if custom_id == "clan_war_heroes":
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_author(name = f"Клан", icon_url = inter.guild.icon.url)
                return await inter.send(ephemeral = True, embed = embed)

            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
            clan_name = f"{role.name}"

            if database.clan_heroes.count_documents({"_id": str(inter.author.id)}) == 0: 
                database.clan_heroes.insert_one({"_id": str(inter.author.id), "alarm_sps": 0})

            return await inter.response.edit_message(attachments = None, embed = None, file = disnake.File("clan_heroes.png"), view = ClanWarHeroes())

        #if custom_id.startswith("clan_top"):
#
        #    if not inter.message.content == inter.author.mention:
        #        embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
        #        embed.set_thumbnail(url = inter.author.display_avatar.url)
        #        embed.set_author(name = f"Клан", icon_url = inter.guild.icon.url)
        #        return await inter.send(ephemeral = True, embed = embed)
#
        #    пользователь = utils.get(inter.guild.members, id=profile_user[inter.author.id])
#
        #    history_data = cluster.sweetness.history_case.find_one({"_id": str(пользователь.id)})
        #    
        #    N = database.clanonline.find_one({'_id': str(inter.author.id)})['online']
#
        #    embed = Embed(color=3092790)
        #    embed.set_thumbnail(url=пользователь.display_avatar.url)
        #    embed.description = f"Ваш онлайн в клане: **{N // hour}ч. {(N - (N // hour * hour)) // 60}м. {N - ((N // hour * hour) + ((N - (N // hour * hour)) // 60 * min))}с.**"
#
        #    items_per_page = 10
#
        #    if str(inter.author.id) not in sort_clan_top:
        #        sort_clan_top[str(inter.author.id)] = "Отсутствует"
#
        #    if sort_clan_top[str(inter.author.id)] == "Даты по возрастанию": # Проверка на фильтр сортировки по датам
        #        reason = history_data.get("prize", ["-"])
        #        dates = cluster.sweetness.history_case.find_one({"_id": str(пользователь.id)})["data"]
        #        
        #        pattern = r"<t:(\d+):F>"
        #        timestamps = [int(re.search(pattern, date).group(1)) for date in dates]
        #        
        #        # Сортировка по возрастанию
        #        sorted_dates_asc = sorted(dates, key=lambda x: int(re.search(pattern, x).group(1)))
        #        
        #        tip_data = sorted_dates_asc
        #    elif sort_clan_top[str(inter.author.id)] == "Даты по убыванию": # Проверка на фильтр сортировки по датам
        #        reason = history_data.get("prize", ["-"])
        #        dates = cluster.sweetness.history_case.find_one({"_id": str(пользователь.id)})["data"]
    #
        #        pattern = r"<t:(\d+):F>"
        #        timestamps = [int(re.search(pattern, date).group(1)) for date in dates]
        #        
        #        # Сортировка по убыванию
        #        sorted_dates_desc = sorted(dates, key=lambda x: int(re.search(pattern, x).group(1)), reverse=True)
        #        
        #        tip_data = sorted_dates_desc
        #    if sort_clan_top[str(inter.author.id)] == "Призы по возрастанию": # Проверка на фильтр сортировки по призам
        #        tip_data = history_data.get("data", ["-"])
#
        #        prizes = cluster.sweetness.history_case.find_one({"_id": str(пользователь.id)})["prize"]
#
        #        pattern = r'\d+'
        #        prize_values = [int(re.search(pattern, prize).group()) for prize in prizes]
#
        #        sorted_prizes_asc = [prize for _, prize in sorted(zip(prize_values, prizes))]
#
        #        reason = sorted_prizes_asc
        #    elif sort_clan_top[str(inter.author.id)] == "Призы по убыванию": # Проверка на фильтр сортировки по призам
        #        tip_data = history_data.get("data", ["-"])
#
        #        prizes = cluster.sweetness.history_case.find_one({"_id": str(пользователь.id)})["prize"]
#
        #        pattern = r'\d+'
        #        prize_values = [int(re.search(pattern, prize).group()) for prize in prizes]
#
        #        sorted_prizes_desc = [prize for _, prize in sorted(zip(prize_values, prizes), reverse=True)]
#
        #        reason = sorted_prizes_desc
        #    else:
        #        reason = history_data.get("prize", ["-"])
        #        tip_data = history_data.get("data", ["-"])
#
#
        #    if str(inter.author.id) not in currentClanTopPage:
        #        currentClanTopPage[str(inter.author.id)] = 0
#
        #    pages = [tip_data[i:i + items_per_page] for i in range(0, len(tip_data), items_per_page)]
#
        #    if custom_id == "case_history_first_page":
        #        currentClanTopPage[str(inter.author.id)] = 0
        #    elif custom_id == "case_history_prev_page" and currentClanTopPage[str(inter.author.id)] > 0:
        #        currentClanTopPage[str(inter.author.id)] -= 1
        #    elif custom_id == "case_history_exit":
        #        return await inter.message.delete()
        #    elif custom_id == "case_history_right_page":
        #        if currentClanTopPage[str(inter.author.id)] < len(pages) - 1:
        #            currentClanTopPage[str(inter.author.id)] += 1
        #    elif custom_id == "case_history_last_page":
        #        currentClanTopPage[str(inter.author.id)] = len(pages) - 1
#
        #    description = "\n".join(f"**{tip}**" for tip in pages[currentClanTopPage[str(inter.author.id)]])
#
        #    embed.add_field(name="`  Дата  `", value=description)
#
        #    pages1 = [reason[i:i + items_per_page] for i in range(0, len(reason), items_per_page)]
        #    description1 = "\n".join(reasons for reasons in pages1[currentClanTopPage[str(inter.author.id)]][:10])
        #    embed.add_field(name="`  Приз  `", value=description1)
#
        #    pages = [tip_data[i:i + items_per_page] for i in range(0, len(tip_data), items_per_page)]
        #    embed.set_footer(text=f"Страница {currentClanTopPage[str(inter.author.id)] + 1} из {len(pages)}",
        #                        icon_url="https://cdn.discordapp.com/attachments/1091732133111939135/1109845138764738653/menu.png")
        #    embed.set_author(name=f"История {пользователь} | {inter.guild}", icon_url=inter.guild.icon.url)
        #    await inter.response.edit_message(embed=embed, view=ClanTopShop(inter.author.id))
#
        #if custom_id.startswith("clan_top"):
        #    if not inter.message.content == inter.author.mention:
        #        embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
        #        embed.set_thumbnail(url = inter.author.display_avatar.url)
        #        embed.set_author(name = f"Клан", icon_url = inter.guild.icon.url)
        #        return await inter.send(ephemeral = True, embed = embed)
#
        #    пользователь = utils.get(inter.guild.members, id=profile_user[inter.author.id])
#
        #    history_data = cluster.sweetness.history_case.find_one({"_id": str(пользователь.id)})
#
        #    embed = Embed(color=3092790)
        #    embed.set_thumbnail(url=пользователь.display_avatar.url)
        #    embed.description = f"Ваш онлайн в клане: **{N // hour}ч. {(N - (N // hour * hour)) // 60}м. {N - ((N // hour * hour) + ((N - (N // hour * hour)) // 60 * min))}с.**"
#
        #    items_per_page = 10
#
        #    if str(inter.author.id) not in sort_clan_top:
        #        sort_clan_top[str(inter.author.id)] = "Отсутствует"
#
        #    if sort_clan_top[str(inter.author.id)] == "Даты по возрастанию": # Проверка на фильтр сортировки по датам
        #        reason = history_data.get("prize", ["-"])
        #        dates = cluster.sweetness.history_case.find_one({"_id": str(пользователь.id)})["data"]
        #        
        #        pattern = r"<t:(\d+):F>"
        #        timestamps = [int(re.search(pattern, date).group(1)) for date in dates]
        #        
        #        # Сортировка по возрастанию
        #        sorted_dates_asc = sorted(dates, key=lambda x: int(re.search(pattern, x).group(1)))
        #        
        #        tip_data = sorted_dates_asc
        #    elif sort_clan_top[str(inter.author.id)] == "Даты по убыванию": # Проверка на фильтр сортировки по датам
        #        reason = history_data.get("prize", ["-"])
        #        dates = cluster.sweetness.history_case.find_one({"_id": str(пользователь.id)})["data"]
    #
        #        pattern = r"<t:(\d+):F>"
        #        timestamps = [int(re.search(pattern, date).group(1)) for date in dates]
        #        
        #        # Сортировка по убыванию
        #        sorted_dates_desc = sorted(dates, key=lambda x: int(re.search(pattern, x).group(1)), reverse=True)
        #        
        #        tip_data = sorted_dates_desc
        #    if sort_clan_top[str(inter.author.id)] == "Призы по возрастанию": # Проверка на фильтр сортировки по призам
        #        tip_data = history_data.get("data", ["-"])
#
        #        prizes = cluster.sweetness.history_case.find_one({"_id": str(пользователь.id)})["prize"]
#
        #        pattern = r'\d+'
        #        prize_values = [int(re.search(pattern, prize).group()) for prize in prizes]
#
        #        sorted_prizes_asc = [prize for _, prize in sorted(zip(prize_values, prizes))]
#
        #        reason = sorted_prizes_asc
        #    elif sort_clan_top[str(inter.author.id)] == "Призы по убыванию": # Проверка на фильтр сортировки по призам
        #        tip_data = history_data.get("data", ["-"])
#
        #        prizes = cluster.sweetness.history_case.find_one({"_id": str(пользователь.id)})["prize"]
#
        #        pattern = r'\d+'
        #        prize_values = [int(re.search(pattern, prize).group()) for prize in prizes]
#
        #        sorted_prizes_desc = [prize for _, prize in sorted(zip(prize_values, prizes), reverse=True)]
#
        #        reason = sorted_prizes_desc
        #    else:
        #        reason = history_data.get("prize", ["-"])
        #        tip_data = history_data.get("data", ["-"])
#
#
        #    if str(inter.author.id) not in currentClanTopPage:
        #        currentClanTopPage[str(inter.author.id)] = 0
#
        #    pages = [tip_data[i:i + items_per_page] for i in range(0, len(tip_data), items_per_page)]
#
        #    if custom_id == "case_history_first_page":
        #        currentClanTopPage[str(inter.author.id)] = 0
        #    elif custom_id == "case_history_prev_page" and currentClanTopPage[str(inter.author.id)] > 0:
        #        currentClanTopPage[str(inter.author.id)] -= 1
        #    elif custom_id == "case_history_exit":
        #        return await inter.message.delete()
        #    elif custom_id == "case_history_right_page":
        #        if currentClanTopPage[str(inter.author.id)] < len(pages) - 1:
        #            currentClanTopPage[str(inter.author.id)] += 1
        #    elif custom_id == "case_history_last_page":
        #        currentClanTopPage[str(inter.author.id)] = len(pages) - 1
#
        #    description = "\n".join(f"**{tip}**" for tip in pages[currentClanTopPage[str(inter.author.id)]])
#
        #    embed.add_field(name="`  Дата  `", value=description)
#
        #    pages1 = [reason[i:i + items_per_page] for i in range(0, len(reason), items_per_page)]
        #    description1 = "\n".join(reasons for reasons in pages1[currentClanTopPage[str(inter.author.id)]][:10])
        #    embed.add_field(name="`  Приз  `", value=description1)
#
        #    pages = [tip_data[i:i + items_per_page] for i in range(0, len(tip_data), items_per_page)]
        #    embed.set_footer(text=f"Страница {currentClanTopPage[str(inter.author.id)] + 1} из {len(pages)}",
        #                        icon_url="https://cdn.discordapp.com/attachments/1091732133111939135/1109845138764738653/menu.png")
        #    embed.set_author(name=f"История {пользователь} | {inter.guild}", icon_url=inter.guild.icon.url)
        #    await inter.response.edit_message(embed=embed, view=ClanTopShop(inter.author.id))

        if custom_id == 'clan_join':
            try:
                if database.clan.count_documents({"_id": str(inter.author.id)}) == 0: 
                    database.clan.insert_one({"_id": str(inter.author.id), "alarm_sps": 0})

                clanxd = database.clan.find_one({'_id': str(inter.message.id)})['clan']

                request = database.clan.find_one({'_id': str(clanxd)})['trebovaniya'][0]
                request1 = database.clan.find_one({'_id': str(clanxd)})['trebovaniya'][1]
                request2 = database.clan.find_one({'_id': str(clanxd)})['trebovaniya'][2]
                request3 = database.clan.find_one({'_id': str(clanxd)})['trebovaniya'][3]
                request4 = database.clan.find_one({'_id': str(clanxd)})['trebovaniya'][4]
            except:
                embed = disnake.Embed(color = 3092790, description=f"{inter.author.mention}, **В этом клане не установлены вопросы для требований**, поэтому бот не может отправить окно с формой заявки")
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_author(name = "Ошибка", icon_url = inter.guild.icon.url)
                return await inter.response.send_message(embed = embed, ephemeral = True)
            
            try:
                return await inter.response.send_modal(title=f"Заявка на вступление",custom_id = "clan_join", components=[
                    disnake.ui.TextInput(label=request,custom_id = request,style=disnake.TextInputStyle.short),
                    disnake.ui.TextInput(label=request1,custom_id = request1,style=disnake.TextInputStyle.short),
                    disnake.ui.TextInput(label=request2,custom_id = request2,style=disnake.TextInputStyle.paragraph),
                    disnake.ui.TextInput(label=request3,custom_id = request3,style=disnake.TextInputStyle.paragraph),
                    disnake.ui.TextInput(label=request4,custom_id = request4,style=disnake.TextInputStyle.paragraph)])
            except:
                embed = disnake.Embed(color = 3092790, description=f"{inter.author.mention}, **В этом клане повторяются вопросы**, поэтому бот не может отправить окно с формой заявки")
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_author(name = "Ошибка", icon_url = inter.guild.icon.url)
                return await inter.response.send_message(embed = embed, ephemeral = True)

        if custom_id == "clan_report":
            id_message = str(inter.message.id)

            await inter.response.send_modal(title = "Отправить жалобу", custom_id = "report_activity", components = [
                disnake.ui.TextInput(label="Причина",custom_id = "Причина",style=disnake.TextInputStyle.paragraph, max_length=200)])
            
            modal_inter: disnake.ModalInteraction = await self.bot.wait_for("modal_submit",check=lambda i: i.custom_id == "report_activity" and i.author.id == inter.author.id)

            for key, value in modal_inter.text_values.items():
                reason = value

            number = randint(1, 15)

            embed = disnake.Embed(description="", color = 3092790)

            embed.set_author(name = "Клановые жалобы", icon_url = "https://cdn.discordapp.com/attachments/1125009710446288926/1142861099897716879/report.png")
            embed.add_field(name = "> Информация о истце:", value = f"⠀**Пользователь:** {inter.author.mention}\n⠀**ID:** {inter.author.id}", inline = True)
            embed.add_field(name = "> ID жалобы:", value = f"⠀**{number}**", inline = True)
            embed.add_field(name = "> Причина", value = f"```{reason}```", inline = False)
            msg = await self.bot.get_channel(1152307160097763358).send(content = "<@&1025807036799275141>", embed = embed, view = ReportView())
            
            cluster.sweetness.clan_report.update_one({'_id': str(msg.id)}, {'$set': {'user': inter.author.id}}, upsert = True)
            
            embed = disnake.Embed(color = 3092790, description=f"{inter.author.mention}, **Жалоба** была успешно **отправлена** на рассмотрение, под номером **{number}**")
            embed.set_author(name = "Клановые жалобы", icon_url = "https://cdn.discordapp.com/attachments/1125009710446288926/1142861099897716879/report.png")
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            return await modal_inter.response.send_message(embed = embed, ephemeral = True)

        if custom_id == 'ball_report':
            await inter.response.send_modal(title=f"Отзыв", custom_id = "review_report", components=[
                disnake.ui.TextInput(label=f"Текст", custom_id = f"Текст", style=disnake.TextInputStyle.paragraph, max_length=500)])

        if custom_id[-6:] == 'report':
            if custom_id == 'accept_report':
                embed = inter.message.embeds[0]
                embed.set_footer(text=f"Принял репорт - {inter.author} / id - {inter.author.id}", icon_url=inter.author.display_avatar.url)
                await inter.message.edit(embed=embed, components = [])
                number = randint(1000, 9999)

                category = disnake.utils.get(inter.guild.categories, id = 1025859125701259384)
                report_channel_text = await inter.guild.create_text_channel(name = f"💬・Жалоба ивенты {number}", category = category)
                report_channel_voice = await inter.guild.create_voice_channel(name = f"🚫・Жалоба ивенты {number}", category = category)
                await report_channel_voice.set_permissions(inter.author, connect = True, view_channel = True)

                user = disnake.utils.get(inter.guild.members, id = cluster.sweetness.clan_report.find_one({'_id': str(inter.message.id)})['user'])

                embed = disnake.Embed(title = "Clans Report", color = 3092790, description=f"{user.mention}, Ваша **жалоба** на клан была **Принята** старшим администратром, в скором **Времени** с вами свяжутся.")
                embed.set_thumbnail(url = user.display_avatar.url)
                embed.add_field(name = "Администратор", value = f"> {inter.author.mention}\n> {inter.author.id}")
                embed.set_footer(text = f"Сервер {inter.guild.name}", icon_url = inter.guild.icon.url)
                msg = await user.send(embed = embed)

                embed = disnake.Embed(description=f"<:zxc3:1009168371213926452> - завершить в пользу {user.mention} \
                                      \n<:zxc2:1009168373936050206> - отклонить жалобу {user.mention}", color = 3092790)
                embed.set_author(name = "Управление жалобой", icon_url = inter.guild.icon.url)
                embed.set_footer(text = f"Администратор - {inter.author} / id - {inter.author.id}", icon_url = inter.author.display_avatar.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                msg = await report_channel_text.send(inter.author.mention, embed = embed, view = ReportMenu())

                cluster.sweetness.clan_report.update_one({'_id': str(msg.id)}, {'$set': {'text_channel': report_channel_text.id}}, upsert = True)
                cluster.sweetness.clan_report.update_one({'_id': str(msg.id)}, {'$set': {'channel': report_channel_voice.id}}, upsert = True)
                cluster.sweetness.clan_report.update_one({'_id': str(msg.id)}, {'$set': {'user': user.id}}, upsert = True)
                
            if custom_id == 'decline_report':
                embed = inter.message.embeds[0]
                embed.set_footer(text=f"Отклонил репорт - {inter.author} / id - {inter.author.id}", icon_url=inter.author.display_avatar.url)
                await inter.message.edit(embed=embed, components = [])

            if custom_id == 'move_one_report':
                await inter.response.defer()
                report_channel_voice = cluster.sweetness.clan_report.find_one({'_id': str(inter.message.id)})['channel']
                user = disnake.utils.get(inter.guild.members, id = cluster.sweetness.clan_report.find_one({'_id': str(inter.message.id)})['user'])
                try:
                    await user.move_to(self.bot.get_channel(report_channel_voice))
                except:
                    embed = disnake.Embed(color = 3092790, description = f"{inter.author.mention}, **{user.mention}** находится не в голосовом канале")
                    embed.set_author(name = f"Репорты | {inter.guild.name}", icon_url = inter.guild.icon.url)
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    await inter.send(embed = embed)

        if custom_id == 'accept_one':
            user = disnake.utils.get(inter.guild.members, id = cluster.sweetness.clan_report.find_one({'_id': str(inter.message.id)})['user'])
            await inter.message.edit(components = [])
            try:
                embed = disnake.Embed(title = "Clans Report", color = 3092790, description=f"{user.mention}, **Разбор** Вашей жалобы **был** завершен в вашу пользу. В скором времени наказание будет выдано. Ожидайте ответа старшей администрации.\n\nОставьте **отзыв** администратору, который **занимался** Вашей **жалобой**")
                embed.set_thumbnail(url = user.display_avatar.url)
                embed.add_field(name = "Администратор", value = f"> {inter.author.mention}\n> {inter.author.id}")
                embed.set_footer(text = f"Сервер {inter.guild.name}", icon_url = inter.guild.icon.url)
                msg = await user.send(embed = embed, view = BallReport())
                cluster.sweetness.clan_report.update_one({'_id': str(msg.id)}, {'$set': {'moderator': int(inter.author.id)}}, upsert = True)
            except:
                pass

            report_channel_voice = self.bot.get_channel(cluster.sweetness.clan_report.find_one({'_id': str(inter.message.id)})['channel'])
            report_channel_text = self.bot.get_channel(cluster.sweetness.clan_report.find_one({'_id': str(inter.message.id)})['text_channel'])
            await report_channel_text.delete()
            await report_channel_voice.delete()

        if custom_id == 'accept_two':
            user = disnake.utils.get(inter.guild.members, id = cluster.sweetness.clan_report.find_one({'_id': str(inter.message.id)})['user'])
            await inter.message.edit(components = [])
            try:
                embed = disnake.Embed(title = "Clans Report", color = 3092790, description=f"{user.mention}, **Разбор** Вашей жалобы **был** завершен. Решением старшей администрации, жалоба была отклонена.\nОставьте **отзыв** администратору, который **занимался** Вашей **жалобой**")
                embed.set_thumbnail(url = user.display_avatar.url)
                embed.add_field(name = "Администратор", value = f"> {inter.author.mention}\n> {inter.author.id}")
                embed.set_footer(text = f"Сервер {inter.guild.name}", icon_url = inter.guild.icon.url)
                msg = await user.send(embed = embed, view = BallReport())
                cluster.sweetness.clan_report.update_one({'_id': str(msg.id)}, {'$set': {'moderator': int(inter.author.id)}}, upsert = True)
            except:
                pass

            report_channel_voice = self.bot.get_channel(cluster.sweetness.clan_report.find_one({'_id': str(inter.message.id)})['channel'])
            report_channel_text = self.bot.get_channel(cluster.sweetness.clan_report.find_one({'_id': str(inter.message.id)})['text_channel'])
            await report_channel_text.delete()
            await report_channel_voice.delete()

        if custom_id[-4:] == "rank":
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_author(name = f"Клан", icon_url = inter.guild.icon.url)
                return await inter.send(ephemeral = True, embed = embed)
            
            if not clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id or inter.author.id in clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin']:
                embed = disnake.Embed(description = f'### > {inter.author.mention}, У Вас недостаточно прав на выполнение этой команды', color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_author(name = f"Клан", icon_url = inter.guild.icon.url)
                return await inter.send(ephemeral = True, embed = embed)
                
            if custom_id == "clan_accept_rank":
                rang = currentRankChoice[str(inter.author.id)]

                database.clan.update_one({'_id': str(rang)}, {'$set': {'admin': 'Присутствует'}}, upsert = True)
                embed = disnake.Embed(description = f"### > {inter.author.mention}, Вы успешно выдали права заместителя рангу {rang}", color = 3092790)
                embed.set_author(name = f"Система рангов", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_footer(text = f'Выполнил(а) {inter.author}', icon_url = inter.author.display_avatar.url)
                return await inter.response.edit_message(content = inter.author.mention, embed = embed, view = ClanBack())
            
            if custom_id == "clan_decline_rank":
                rang = currentRankChoice[str(inter.author.id)]
                database.clan.update_one({'_id': str(rang)}, {'$set': {'admin': 'Отсутствует'}}, upsert = True)

                embed = disnake.Embed(description = f"### > {inter.author.mention}, вы успешно забрали права заместителя у ранга {rang}", color = 3092790)
                embed.set_author(name = f"Система рангов", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_footer(text = f'Выполнил(а) {inter.author}', icon_url = inter.author.display_avatar.url)
                return await inter.response.edit_message(content = inter.author.mention, embed = embed, view = ClanBack())
            
            пользователь = disnake.utils.get(inter.guild.members, id = profile_user[inter.author.id])
            clanxd = clan[str(inter.guild.id)][str(пользователь.id)]

            if custom_id == "clan_add_rank":
                rang = currentRankChoice[str(inter.author.id)]
                return await inter.response.send_modal(title=f"Выдать {rang}", custom_id = "clan_add_rank", components=[
                    disnake.ui.TextInput(label="Айди участника",placeholder="Например: 849353684249083914",custom_id = "Айди участника",style=disnake.TextInputStyle.short, max_length=25)])
            
            if custom_id == "clan_remove_rank":
                rang = currentRankChoice[str(inter.author.id)]
                return await inter.response.send_modal(title=f"Снять {rang}", custom_id = "clan_remove_rank", components=[
                    disnake.ui.TextInput(label="Айди участника",placeholder="Например: 849353684249083914",custom_id = "Айди участника",style=disnake.TextInputStyle.short, max_length=25)])

            try:
                rank = database.clan.find_one({'_id': str(clanxd)})['rank']
            except: 
                database.clan.update_one({'_id': str(clanxd)}, {'$set': {'rank': 'Отсутствует'}}, upsert = True)
                rank = database.clan.find_one({'_id': str(clanxd)})['rank']

            if custom_id == "clan_limit_rank":
                rang = currentRankChoice[str(inter.author.id)]
                return await inter.response.send_modal(title=f"Установить лимит на ранг {rang}", custom_id = "clan_limit_rank", components=[
                    disnake.ui.TextInput(label="Лимит",placeholder="Например: 5",custom_id = "Лимит",style=disnake.TextInputStyle.short, max_length=3)])
            
            if custom_id == "clan_admin_rank":
                rang = currentRankChoice[str(inter.author.id)]

                embed = disnake.Embed(description = f"### > {inter.author.mention}, Нужны ли {rang} рангу права заместителя?", color = 3092790)
                embed.set_author(name = f"Система рангов", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_footer(text = f'Выполнил(а) {inter.author}', icon_url = inter.author.display_avatar.url)
                return await inter.response.edit_message(content = inter.author.mention, embed = embed, view = ClanSystemRankAccept())
            
            if custom_id == "clan_create_rank":
                return await inter.response.send_modal(title=f"Создать ранг",custom_id = "clan_create_rank", components=[
                    disnake.ui.TextInput(label="Название",placeholder="Например: zxc",custom_id = "Название",style=disnake.TextInputStyle.short, max_length=25)])
            
            if custom_id == "clan_delete_rank":
                return await inter.response.send_modal(title=f"Удалить ранг",custom_id = "clan_delete_rank", components=[
                    disnake.ui.TextInput(label="Название",placeholder="Например: zxc",custom_id = "Название",style=disnake.TextInputStyle.short, max_length=25)])

            if custom_id == "clan_edit_rank":
                embed = disnake.Embed(description = f"### > {inter.author.mention}, Тут **Вы** можете **создавать** новые ранги или же **управлять** уже созданными.", color = 3092790)
                embed.set_author(name = f"Система рангов", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_footer(text = f'Выполнил(а) {inter.author}', icon_url = inter.author.display_avatar.url)
                return await inter.response.edit_message(content = inter.author.mention, embed = embed, view = ClanSystemEdit())

            if custom_id == "clan_system_rank":
                database.clan.update_one({'_id': str(clanxd)}, {'$set': {'rank': []}}, upsert = True)
                rank = database.clan.find_one({'_id': str(clanxd)})['rank']
                embed = disnake.Embed(description = f"### > {inter.author.mention}, **Вы** успешно активировали **систему рангов**, теперь вы можете нажать на кнопку **управление**", color = 3092790)
                embed.set_author(name = f"Система рангов", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_footer(text = f'Активировал(а) {inter.author}', icon_url = inter.author.display_avatar.url)
                return await inter.response.edit_message(content = inter.author.mention, embed = embed, view = ClanSystem(rank))

        if custom_id[:8] == 'clan_top':
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_author(name = f"Клан", icon_url = inter.guild.icon.url)
                return await inter.send(ephemeral = True, embed = embed)

            idd = 1
            description = ''
            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
            membersID = []
            for x in database.clanonline.find().sort("online",-1):
                try:
                    member = disnake.utils.get(inter.guild.members, id = int(x['_id']))
                    for r in member.roles:
                        if r.id == role.id:
                            membersID.append(x['_id'])
                except:
                    pass

            items_per_page = 10

            pages = [membersID[i:i + items_per_page] for i in range(0, len(membersID), items_per_page)]
            if not str(inter.author.id) in currentClanTopPage:
                currentClanTopPage[str(inter.author.id)] = 0
            match custom_id:
                case 'clan_top_first_page':
                    currentClanTopPage[str(inter.author.id)] = 0
                case 'clan_top_prev_page' if currentClanTopPage[str(inter.author.id)] > 0:
                    currentClanTopPage[str(inter.author.id)] -= 1
                case 'clan_top_exit':
                    await inter.message.delete()
                case 'clan_top_right_page' if currentClanTopPage[str(inter.author.id)] < len(pages) - 1:
                    currentClanTopPage[str(inter.author.id)] += 1
                case 'clan_top_last_page':
                    currentClanTopPage[str(inter.author.id)] = len(pages) - 1
            for member_id in pages[currentClanTopPage[str(inter.author.id)]]:
                N = database.clanonline.find_one({'_id': str(member_id)})['online']
                match idd:
                    case 1:
                        description += f"**<:11:1096126530247204966> — <@{member_id}>** <:microphone:1140294304556908695> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    case 2:
                        description += f"**<:21:1096126528670138469> — <@{member_id}>** <:microphone:1140294304556908695> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    case 3:
                        description += f"**<:31:1096126525683810465> — <@{member_id}>** <:microphone:1140294304556908695> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    case 4:
                        description += f"**<:41:1096126532826697909> — <@{member_id}>** <:microphone:1140294304556908695> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    case 5:
                        description += f"**<:51:1097534359675879515> — <@{member_id}>** <:microphone:1140294304556908695> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    case 6:
                        description += f"**<:61:1107004738194653246> — <@{member_id}>** <:microphone:1140294304556908695> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    case 7:
                        description += f"**<:71:1107004742326034593> — <@{member_id}>** <:microphone:1140294304556908695> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    case 8:
                        description += f"**<:81:1107004743815008328> — <@{member_id}>** <:microphone:1140294304556908695> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    case 9:
                        description += f"**<:91:1107004746822328350> — <@{member_id}>** <:microphone:1140294304556908695> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    case 10:
                        description += f"**<:101:1107004740723802112> — <@{member_id}>** <:microphone:1140294304556908695> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                idd += 1
                if idd > 10:
                    break
            embed = disnake.Embed(description = description, color = 3092790)
            embed.set_author(name = f"Топ по онлайну клана {role.name}", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            embed.set_footer(text = f'Запросил(а) {inter.author}', icon_url = inter.author.display_avatar.url)
            return await inter.response.edit_message(content = inter.author.mention, embed = embed, view = ClanTopShop(inter.author.id))

        if custom_id[-4:] == 'shop':
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_author(name = f"Клан", icon_url = inter.guild.icon.url)
                return await inter.send(ephemeral = True, embed = embed)
            
            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            clan_balance = f"{clan[str(inter.guild.id)][clanxd]['Balance']}"

            if inter.component.custom_id == 'yesshop':
                if clanshop[inter.author.id] == 1:
                    if int(2500) > int(clan_balance):
                        embed = disnake.Embed(description = f'{inter.author.mention}, У **Вашего** клана на балансе **недостаточно средств!**', color = 3092790)
                        embed.set_author(name = f"Клан", icon_url = inter.guild.icon.url)
                        embed.set_thumbnail(url = inter.author.display_avatar.url)
                        return await inter.send(embed = embed)
                    
                    return await inter.response.send_modal(title=f"Создать текстовый канал",custom_id = "create_text_channel", components=[
                        disnake.ui.TextInput(label="Название",placeholder="Например: zxc",custom_id = "Название",style=disnake.TextInputStyle.short, max_length=20)])

                if clanshop[inter.author.id] == 2:
                    if int(2500) > int(clan_balance):
                        embed = disnake.Embed(description = f'{inter.author.mention}, У **Вашего** клана на балансе **недостаточно средств!**', color = 3092790)
                        embed.set_author(name = f"Клан", icon_url = inter.guild.icon.url)
                        embed.set_thumbnail(url = inter.author.display_avatar.url)
                        return await inter.send(embed = embed)
                    
                    embed = disnake.Embed(description = f'{inter.author.mention}, **Скиньте** фотографию в чат, для того чтобы **поставить/изменить** иконку на роли!', color=3092790)
                    embed.set_author(name = f"Добавить иконку", icon_url = inter.guild.icon.url)
                    await inter.send(inter.author.mention, embed = embed)
                    def check(m):
                        return m.author.id == inter.author.id
                    try: 
                        image = await self.bot.wait_for("message", check = check, timeout = 60)
                    except TimeoutError:
                        return
                    role_id = clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Role']
                    role = disnake.utils.get(inter.guild.roles, id = int(role_id))
                    for attach in image.attachments:
                        await attach.save(f"icon_role.png")
                    with open(f'icon_role.png', "rb") as image:
                        img_byte = image.read()
                    emoji = await inter.guild.create_custom_emoji(name = 'xdd', image = img_byte)
                    try:
                        await role.edit(icon = emoji)
                    except:
                        embed = disnake.Embed(title = f"Добавить/Изменить иконку", description = f"{inter.author.mention}, **На сервере недостаточно бустов** для того чтобы добавить иконку на роль!", color = 3092790)
                        return await inter.response.edit_message(embed = embed)

                    await emoji.delete()

                    clan[str(inter.guild.id)][clan[str(inter.guild.id)][str(inter.author.id)]]['Limit'] += 1
                    clan[str(inter.guild.id)][clan[str(inter.guild.id)][str(inter.author.id)]]['Balance'] -= 2500
                    with open('clan_sweetness.json','w') as f: 
                        json.dump(clan,f)
                    embed = disnake.Embed(title = f"Добавить/Изменить иконку", description = f"{inter.author.mention}, **Вы** успешно добавили/изменили иконку **клана!**", color = 3092790)
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    await inter.send(embed = embed)
                
                if clanshop[inter.author.id] == 3:
                    if int(1000) > int(clan_balance):
                        embed = disnake.Embed(title = 'Клан', description = f'{inter.author.mention}, У **Вашего** клана на балансе **недостаточно средств!**', color = 3092790)
                        embed.set_thumbnail(url = inter.author.display_avatar.url)
                        return await inter.send(embed = embed)
                
                    return await inter.response.send_modal(title=f"Сменить название клана",custom_id = "change_name_clan", components=[disnake.ui.TextInput(label="Название",
                                                        placeholder="Например: zxc",custom_id = "Название",style=disnake.TextInputStyle.short, max_length=20)])

                if clanshop[inter.author.id] == 4:
                    if int(500) > int(clan_balance):
                        embed = disnake.Embed(title = 'Клан', description = f'{inter.author.mention}, У **Вашего** клана на балансе **недостаточно средств!**', color = 3092790)
                        embed.set_thumbnail(url = inter.author.display_avatar.url)
                        return await inter.response.edit_message(embed = embed, view = ClanBack())
                    
                    return await inter.response.send_modal(title=f"Изменить цвет",custom_id = "change_color", components=[disnake.ui.TextInput(label="Цвет",
                                                        placeholder="Например: #000001",custom_id = "Цвет",style=disnake.TextInputStyle.short, max_length=20)])
                
                if clanshop[inter.author.id] == 5:
                    return await inter.response.send_modal(title=f"Добаить лимит",custom_id = "limit_clan", components=[disnake.ui.TextInput(label="Число",
                                                        placeholder="Например: 10",custom_id = "Число",style=disnake.TextInputStyle.short, max_length=3)])

                if clanshop[inter.author.id] == 6:
                    if int(5000) > int(clan_balance):
                        embed = disnake.Embed(title = 'Клан', description = f'{inter.author.mention}, У **Вашего** клана на балансе **недостаточно средств!**', color = 3092790)
                        embed.set_thumbnail(url = inter.author.display_avatar.url)
                        return await inter.send(embed = embed)
                    
                    return await inter.response.send_modal(title=f"Создать голосовой канал",custom_id = "create_voice_channel", components=[disnake.ui.TextInput(label="Название",placeholder="Например: zxc",custom_id = "Название",style=disnake.TextInputStyle.short, max_length=20)])

            if custom_id == '1shop':
                clanshop[inter.author.id] = 1
                text = 'Добавить текстовый канал'
                count = 2500
            if custom_id == '2shop':
                clanshop[inter.author.id] = 2
                text = 'Добавить значок на роль'
                count = 2500
            if custom_id == '3shop':
                clanshop[inter.author.id] = 3
                text = 'Сменить название клана'
                count = 1000
            if custom_id == '4shop':
                clanshop[inter.author.id] = 4
                text = 'Изменить цвет'
                count = 500
            if custom_id == '5shop':
                clanshop[inter.author.id] = 5
                text = 'Добавить слоты в клан'
                count = 250
            if custom_id == '6shop':
                clanshop[inter.author.id] = 6
                text = 'Добавить голосовой канал'
                count = 5000

            embed = disnake.Embed(description = f'{inter.author.mention}, **Вы уверены**, что Вы хотите **{text}** за **{count}** <:coin1:1096094598507532479>?\nДля **согласия** нажмите на <:yes11:1096091626889302086>, для **отказа** на <:no1:1096087505159344138>', color = 3092790)
            embed.set_author(name = f"Клановый магазин {inter.guild.name}", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            await inter.response.edit_message(embed = embed, view = ClanShopAccept())

        if custom_id[:4] == 'clan':
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
                embed.set_author(name = f"Кланы {inter.guild.name}", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            
            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]

            if custom_id == "clan_invite":
                if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id or inter.author.id in clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin']:
                    components = [disnake.ui.TextInput(label = "Айди участника",placeholder="Например: 849353684249083914",custom_id = "Айди участника",style=disnake.TextInputStyle.short, max_length=25)]
                    await inter.response.send_modal(title = f"Пригласить участника", custom_id = "vidat_clan", components = components)
                else:
                    embed = disnake.Embed(color = 3092790, description = '**Вы** не являетесь **Лидером/Администратором** этого клана!')
                    embed.set_author(name = f"Пригласить в клан", icon_url = inter.guild.icon.url)
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    await inter.response.edit_message(embed = embed, view = ClanBack())
                
            if custom_id == "clan_kick":
                if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id or inter.author.id in clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin']:
                    components = [disnake.ui.TextInput(label = "Айди участника",placeholder="Например: 849353684249083914",custom_id = "Айди участника",style=disnake.TextInputStyle.short, max_length=25)]
                    await inter.response.send_modal(title = f"Выгнать участника", custom_id = "kick_clan", components = components)
                else: 
                    embed = disnake.Embed(color = 3092790, description = f"{inter.author.mention}, **Вы** не являетесь **Лидером** этого клана!")
                    embed.set_author(name = f"Пригласить в клан", icon_url = inter.guild.icon.url)
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    await inter.response.edit_message(embed = embed, view = ClanBack())

            if custom_id == "clan_war":
                clanxd = clan[str(inter.guild.id)][str(inter.author.id)]

                if cluster.sweetness.clan_heroes.count_documents({"_id": str(clanxd)}) == 0:
                    cluster.sweetness.clan_heroes.insert_one({"_id": str(clanxd), "heroes": []})   
                
                if database.clan_shield.count_documents({"_id": str(clanxd)}) == 0:
                    database.clan_shield.insert_one({"_id": str(clanxd), "activate": "Отсутствует", "time": datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=5)})
                    
                if database.clan_rating.count_documents({"_id": str(clanxd)}) == 0:
                    database.clan_rating.insert_one({"_id": str(clanxd), "rating": 0})

                shield = database.clan_shield.find_one({'_id': str(clanxd)})['activate']
                rating = database.clan_rating.find_one({'_id': str(clanxd)})['rating']

                embed = disnake.Embed(description = f'### {inter.author.mention}, Помните, что на ваш клан, могут напасть в любой момент.', color = 3092790)

                if shield == "YES":
                    date_shield = database.clan_shield.find_one({'_id': str(clanxd)})['time']
                    sec = date_shield - datetime.datetime.now()

                    days = (date_shield - datetime.datetime.now()).days
                    hours = (str(sec.seconds // 3600).split('.')[0])
                    minutes = (str((sec.seconds % 3600) // 60).split('.')[0])
                    seconds = (str(sec.seconds % 60).split('.')[0])

                    if date_shield > datetime.datetime.now():
                        sec = date_shield - datetime.datetime.now()
    
                    embed.add_field(name = "Щит ", value = f"```🛡️ {days}д. {hours}ч. {minutes}м. {seconds}с.```")
                else:
                    embed.add_field(name = "Щит", value = f"```🛡️ {shield}```")

                role_take = disnake.utils.get(inter.guild.roles, id = int(clanxd))

                embed.add_field(name = "Рейтинг", value = f"```🏆 {rating}```")
                clan_heroes = len(cluster.sweetness.clan_heroes.find_one({'_id': str(clanxd)})['heroes'])
                voice_members = 1
                if int(clan_heroes) == 0:
                    power = len(role_take.members) * 50 * voice_members
                else:
                    for member in role_take.members:
                        try:
                            channel = member.voice.channel.id
                            voice_members += 1
                        except:
                            pass
                    power_heroes = len(cluster.sweetness.clan_heroes.find_one({'_id': str(clanxd)})['heroes']) * 100
                    power = len(role_take.members) * 50 * voice_members * int(power_heroes)
                embed.add_field(name = "Ваша боевая мощь клана:", value = f"```⚔️ {power}```")
                embed.add_field(name = "Герои клана:", value = f'```{len(cluster.sweetness.clan_heroes.find_one({"_id": str(clanxd)})["heroes"])}/16```')
                embed.set_author(name = f"Битва кланов | {inter.guild.name}", icon_url = inter.guild.icon.url)
                embed.set_footer(text = f"Выполнил(а) {inter.author}",icon_url = inter.author.display_avatar.url)
                await inter.response.edit_message(attachments = None, embed = embed, view = ClanWar())

            if custom_id == "clan_map":
                with open('clan_sweetness.json', 'r') as f:
                    clan_data = json.load(f)
            
                im = Image.open('clan_map_main.png')
                idd = 1

                guild_clans = clan_data.get(str(inter.guild.id), {})

                attackers = []
                defenders = []
                zombie_attackers = []

                await inter.response.defer()

                for clan_key, clan_value in guild_clans.items():
                    if isinstance(clan_value, dict):
                        try:
                            role = disnake.utils.get(inter.guild.roles, id=int(clan_key))
                            level = clan[str(inter.guild.id)][str(clan_key)]['Level']

                            if cluster.sweetness.clan_shield.count_documents({"_id": str(clan_key)}) == 0:
                                cluster.sweetness.clan_shield.insert_one({"_id": str(clan_key), "activate": "Отсутствует", "time": datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=5)})

                            shield = database.clan_shield.find_one({'_id': str(clan_key)})['activate']

                            match idd:
                                case 1:
                                    coordinates = (540, 290)  # розовый
                                    size = 18
                                    fill = "#B684E8"
                                    if shield == "YES":
                                        transparent_image1 = Image.open('shield_pink.png')
                                        im.paste(transparent_image1, (533, 185), transparent_image1)
                                case 2:
                                    coordinates = (312, 177)  # синий замок (ОРАНЖЕВЫЙ)
                                    size = 18
                                    fill = "#D8904E"
                                    if shield == "YES":
                                        transparent_image1 = Image.open('shield_orange.png')
                                        im.paste(transparent_image1, (303, 96), transparent_image1)
                                case 3:
                                    coordinates = (790, 171)  # лайм
                                    size = 18
                                    fill = "#6BFF8C"
                                    if shield == "YES":
                                        transparent_image1 = Image.open('shield_lime.png')
                                        im.paste(transparent_image1, (686, 143), transparent_image1)
                                case 4:
                                    coordinates = (494, 365)  # АФРИКА (MAGNET)
                                    size = 18
                                    fill = "#BD1F58"
                                    if shield == "YES":
                                        transparent_image1 = Image.open('shield_magenta.png')
                                        im.paste(transparent_image1, (378, 326), transparent_image1)
                                case 5:
                                    coordinates = (779, 557)  # АЦТЕК (СИНИЙ)
                                    size = 16
                                    fill = "#2FDBBC"
                                    if shield == "YES":
                                        transparent_image1 = Image.open('shield_aztec.png')
                                        im.paste(transparent_image1, (809, 493), transparent_image1)
                                case 6:
                                    coordinates = (239, 442)  # КРАСНЫЙ
                                    size = 18
                                    fill = "#AF3A3A"
                                    if shield == "YES":
                                        transparent_image1 = Image.open('shield_red.png')
                                        im.paste(transparent_image1, (246, 439), transparent_image1)
                                case 7:
                                    coordinates = (137, 343)  # ФИОЛЕТОВЫЙ
                                    size = 18
                                    fill = "#8458FF"
                                    if shield == "YES":
                                        transparent_image1 = Image.open('shield_purple.png')
                                        im.paste(transparent_image1, (116, 243), transparent_image1)
                                case 8:
                                    coordinates = (769, 175)  # ЗЕЛЕНЫЙ
                                    size = 18
                                    fill = "#18D214"
                                    if shield == "YES":
                                        transparent_image1 = Image.open('shield_green.png')
                                        im.paste(transparent_image1, (1, 182), transparent_image1)
                                case _:
                                    coordinates = None

                            if coordinates:
                                if not database.clan_defender.count_documents({"_id": str(clan_key)}) == 0:
                                    defenders.append({"clanxd": clan_key, "position": coordinates})
                                if not database.clan_war.count_documents({"_id": str(clan_key)}) == 0: 
                                    attackers.append({"clanxd": clan_key, "position": coordinates})
                                if not database.clan_zombie.count_documents({"_id": str(clan_key)}) == 0:
                                    lvl = database.clan_zombie.find_one({'_id': str(clanxd)})['target']
                                    match int(lvl):
                                       case 1:
                                           coords = (793, 493)
                                       case 2:
                                           coords = (274, 299)
                                       case 3:
                                           coords = (144, 137)
                                       case 4:
                                           coords = (636, 347)
                                       case 5:
                                           coords = (631, 345)
                                       case 6:
                                           coords = (711, 321)
                                       case 7:
                                           coords = (352, 389)
                                       case _:
                                           coords = None

                                    zombie_attackers.append({"clanxd": clan_key, "position": coords, "position_clanxd": coordinates})

                                ImageDraw.Draw(im).text(coordinates, str(f"{role.name[:10]}\nУр. {level}"), font=ImageFont.truetype('Montserrat-Bold.ttf', encoding='UTF-8', size=size), fill=fill)
                            idd += 1

                        except:
                            pass
                try:
                    for attacker in attackers:
                        for defender in defenders:
                            attacker_cords = attacker_cords.get("position")

                            draw = ImageDraw.Draw(im)
                            neon_color = (255, 0, 0)

                            draw.line((attacker_cords, defender_cords), fill=neon_color, width=3)

                            x, y = attacker_cords

                            y -= 40

                            machine_cords = (x, y)

                            transparent_image1 = Image.open('machine.png')
                            im.paste(transparent_image1, (machine_cords), transparent_image1)

                            x, y = attacker_cords

                            x += 28
                            y -= 21

                            text_cords = (x, y)

                            ImageDraw.Draw(im).text((text_cords), str(f"Идет атака"), font=ImageFont.truetype('Montserrat-Bold.ttf', encoding='UTF-8', size=15), fill=(255, 255, 255))

                    for zombie in zombie_attackers:
                        attacker_cords = zombie.get("position_clanxd")
                        zombie_cords = zombie.get("position")

                        draw = ImageDraw.Draw(im)
                        neon_color = (255, 0, 0)

                        draw.line((attacker_cords, zombie_cords), fill=neon_color, width=3)

                        x, y = attacker_cords

                        y -= 27

                        machine_cords = (x, y)

                        transparent_image1 = Image.open('machine.png')
                        im.paste(transparent_image1, (machine_cords), transparent_image1)

                        x, y = attacker_cords

                        x += 28
                        y -= 21

                        text_cords = (x, y)

                        ImageDraw.Draw(im).text((text_cords), str(f"Идет атака"), font=ImageFont.truetype('Montserrat-Bold.ttf', encoding='UTF-8', size=15), fill=(255, 255, 255)) 
                except:
                    pass

                im.save('out_clan_map.png')
            
                await inter.message.edit(embed=None, file=disnake.File('out_clan_map.png'), view=ClanMap())

            if custom_id == "clan_system":
                try:
                    rank = database.clan.find_one({'_id': str(clanxd)})['rank']
                except:
                    database.clan.update_one({'_id': str(clanxd)}, {'$set': {'rank': 'Отсутствует'}}, upsert = True)
                    rank = database.clan.find_one({'_id': str(clanxd)})['rank']
                embed = disnake.Embed(description = f'### {inter.author.mention}, Добро пожаловать в систему кланов ранги\n> **Выберите действие**', color = 3092790)
                embed.set_author(name = f"Система рангов | {inter.guild.name}", icon_url = inter.guild.icon.url)
                embed.set_footer(text = f"Выполнил(а) {inter.author}",icon_url = inter.author.display_avatar.url)
                await inter.response.edit_message(embed = embed, view = ClanSystem(rank))

            if custom_id == 'clan_leave':
                clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
                if clan[str(inter.guild.id)][str(clanxd)]['Owner'] == inter.author.id:
                    embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** не можете покинуть клан, пока вы являетесь лидером клана!', color = disnake.Color.red())
                    embed.set_footer(text = f"Выполнил(а) {inter.author}",icon_url = inter.author.display_avatar.url)
                    return await inter.response.edit_message(embed = embed, view = ClanBack())
                else:
                    if inter.author.id in clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin']:
                        clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin'].remove(inter.author.id)
                        with open('clan_sweetness.json','w') as f:
                            json.dump(clan,f)
                        await inter.author.remove_roles(disnake.utils.get(inter.guild.roles, id = 961299056968237127))

                    await inter.author.remove_roles(disnake.utils.get(inter.guild.roles, id = clan[str(inter.guild.id)][str(clanxd)]['Role']))
                    await inter.author.remove_roles(disnake.utils.get(inter.guild.roles, id = 961529522082185226))
                    clan[str(inter.guild.id)][str(inter.author.id)] = 'Отсутствует'
                    clan[str(inter.guild.id)][str(clanxd)]['ClanMembers'] -= 1
                    with open('clan_sweetness.json','w') as f: 
                        json.dump(clan,f)

                    embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно покинули клан!', color = 3092790)
                    embed.set_author(name = "Покинуть клан", icon_url = inter.guild.icon.url)
                    embed.set_footer(text = f"Выполнил(а) {inter.author}",icon_url = inter.author.display_avatar.url)
                    await inter.response.edit_message(embed = embed, view = ClanBack())

            if custom_id == 'clan_delete':
                if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id:
                    id_role = clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Role']

                    embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно удалили клан!', color = 3092790)
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    embed.set_author(name = f"Удалить клан на сервере {inter.guild.name}", icon_url = inter.guild.icon.url)
                    await inter.response.edit_message(embed = embed, components = [])

                    category_id = database.clan.find_one({'_id': str(id_role)})['category']

                    category = disnake.utils.get(inter.guild.categories, id = int(category_id))
                    for channel in category.voice_channels:
                        await channel.delete()
                    for channel in category.text_channels:
                        await channel.delete()

                    await category.delete()
                    clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
                    for member in clan[str(inter.guild.id)].copy():
                        if clan[str(inter.guild.id)][str(member)] == str(clanxd):
                            try:
                                if clan[str(inter.guild.id)][str(clanxd)]['Owner'] == int(member):
                                    user = disnake.utils.get(inter.guild.members, id = int(member))
                                    role = disnake.utils.get(inter.guild.roles, id = 961296301901885531)
                                    await user.remove_roles(role)
                                if int(member) in clan[str(inter.guild.id)][str(clanxd)]['Admin']:
                                    await disnake.utils.get(inter.guild.members, id = int(member)).remove_roles(disnake.utils.get(inter.guild.roles, id = 961299056968237127))
                                else:
                                    await disnake.utils.get(inter.guild.members, id = int(member)).remove_roles(disnake.utils.get(inter.guild.roles, id = 961529522082185226))
                            except:
                                pass
                            del clan[str(inter.guild.id)][str(member)]
                            with open('clan_sweetness.json','w') as f: 
                                json.dump(clan,f)
                    database.clan.delete_one({'_id': str(clanxd)})

                    await disnake.utils.get(inter.guild.roles, id = int(id_role)).delete()

                    del clan[str(inter.guild.id)][str(clanxd)]
                    with open('clan_sweetness.json','w') as f:
                        json.dump(clan,f)

                    return await self.bot.get_channel(1026239319624667236).set_permissions(inter.author, view_channel=False, send_messages=False)

            if custom_id == 'clan_embed':
                embed = disnake.Embed(description = f'{inter.author.mention}, **Напишите** ниже **заголовок** которое будет опубликовано в посте', color = 3092790)
                embed.set_footer(text = f"Выполнил(а) {inter.author}",icon_url = inter.author.display_avatar.url)
                embed.set_author(name = "Установка эмбеда в требованиях", icon_url = inter.guild.icon.url)
                await inter.send(embed = embed, components = [])
                def check(m):
                    return m.author.id == inter.author.id
                try:
                    title_clan = await self.bot.wait_for("message", check = check, timeout = 500)
                except TimeoutError:
                    return
                embed = disnake.Embed(description = f'{inter.author.mention}, **Напишите** ниже **описание клана** которое будет опубликовано в посте', color = 3092790)
                embed.set_footer(text = f"Выполнил(а) {inter.author}",icon_url = inter.author.display_avatar.url)
                embed.set_author(name = "Установка эмбеда в требованиях", icon_url = inter.guild.icon.url)
                await inter.send(embed = embed, components = [])
                def check(m):
                    return m.author.id == inter.author.id
                try:
                    desc_clan = await self.bot.wait_for("message", check = check, timeout = 500)
                except TimeoutError:
                    return
                embed = disnake.Embed(description = f'{inter.author.mention}, **Прикрепите** ниже **фотографию для клана** которое будет опубликовано в эмбеде', color = 3092790)
                embed.set_author(name = "Установка эмбеда в требованиях", icon_url = inter.guild.icon.url)
                embed.set_footer(text = f"Выполнил(а) {inter.author}",icon_url = inter.author.display_avatar.url)
                await inter.send(embed = embed, components = [])
                def check(m):
                    return m.author.id == inter.author.id
                try:
                    image = await self.bot.wait_for("message", check = check, timeout = 500)
                except TimeoutError:
                    return

                embed123 = disnake.Embed(title = title_clan.content, description = f"> {desc_clan.content}", color = 3092790)
                try:
                    for attach in image.attachments:
                        embed123.set_image(url = str(attach))
                except:
                    embed123.set_image(url = str(image.content))
                bot = self.bot
                await inter.send(embed = embed123, view = ClanEmbed(title_clan, desc_clan, image, bot))

            if custom_id == 'clan_request':
                components = [
                    disnake.ui.TextInput(label="Первый вопрос",placeholder="Например: Расскажите о себе",custom_id = "Первый вопрос",style=disnake.TextInputStyle.paragraph, max_length=45),
                    disnake.ui.TextInput(label="Второй вопрос",placeholder="Например: Возраст",custom_id = "Второй вопрос",style=disnake.TextInputStyle.paragraph, max_length=45),
                    disnake.ui.TextInput(label="Третий вопрос",placeholder="Например: Имя",custom_id = "Третий вопрос",style=disnake.TextInputStyle.paragraph, max_length=45),
                    disnake.ui.TextInput(label="Четвертый вопрос",placeholder="Например: Часовой пояс",custom_id = "Четвертый вопрос",style=disnake.TextInputStyle.paragraph, max_length=45),
                    disnake.ui.TextInput(label="Пятый вопрос",placeholder="Например: Ммр в доте",custom_id = "Пятый вопрос",style=disnake.TextInputStyle.paragraph, max_length=45)]
                await inter.response.send_modal(title=f"Установить требования",custom_id = "clan_request", components=components)

            if custom_id == "clan_map":
                embed = disnake.Embed(description = f'### {inter.author.mention}, Добро пожаловать в систему кланов карты\n> **Карты кланов находятся в данный момент в разработке**', color = 3092790)
                embed.set_author(name = "Карта кланов", icon_url = inter.guild.icon.url)
                embed.set_footer(text = f"Выполнил(а) {inter.author}",icon_url = inter.author.display_avatar.url)
                await inter.response.edit_message(embed = embed, view = ClanBack())

            if custom_id == 'clan_add_ban':
                if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id:
                    components = [disnake.ui.TextInput(label="Айди участника",placeholder="Например: 849353684249083914",custom_id = "Айди участника",style=disnake.TextInputStyle.short, max_length=20)]
                    await inter.response.send_modal(title=f"Выдать бан",custom_id = "vidat_ban", components=components)
                else: 
                    embed = disnake.Embed(color = 3092790, description = f'{inter.author.mention}, **Вы** не являетесь **Лидером** этого клана!')
                    embed.set_author(name = f"Добавить админа", icon_url = inter.guild.icon.url)
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    await inter.response.edit_message(embed = embed, view = ClanBack())
            if custom_id == 'clan_remove_ban':
                if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id:
                    components = [disnake.ui.TextInput(label="Айди участника",placeholder="Например: 849353684249083914",custom_id = "Айди участника",style=disnake.TextInputStyle.short, max_length=20)]
                    await inter.response.send_modal(title=f"Разбанить участника",custom_id = "remove_ban", components=components)
                else: 
                    embed = disnake.Embed(color = 3092790, description = f'{inter.author.mention}, **Вы** не являетесь **Лидером** этого клана!')
                    embed.set_author(name = f"Удалить админа", icon_url = inter.guild.icon.url)
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    await inter.response.edit_message(embed = embed, view = ClanBack())

            if custom_id == 'clan_add_admin':
                if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id:
                    components = [disnake.ui.TextInput(label="Айди участника",placeholder="Например: 849353684249083914",custom_id = "Айди участника",style=disnake.TextInputStyle.short, max_length=20)]
                    await inter.response.send_modal(title=f"Выдать админа",custom_id = "vidat_admin", components=components)
                else: 
                    embed = disnake.Embed(color = 3092790, description = f'{inter.author.mention}, **Вы** не являетесь **Лидером** этого клана!')
                    embed.set_author(name = f"Добавить админа", icon_url = inter.guild.icon.url)
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    await inter.response.edit_message(embed = embed, view = ClanBack())
                    
            if custom_id == 'clan_remove_admin':
                if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id:
                    components = [disnake.ui.TextInput(label="Айди участника",placeholder="Например: 849353684249083914",custom_id = "Айди участника",style=disnake.TextInputStyle.short, max_length=20)]
                    await inter.response.send_modal(title=f"Забрать роль",custom_id = "remove_admin", components=components)
                else: 
                    embed = disnake.Embed(color = 3092790, description = f'{inter.author.mention}, **Вы** не являетесь **Лидером** этого клана!')
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    await inter.response.edit_message(embed = embed, view = ClanBack())

            if custom_id == 'clan_exit':
                await inter.message.delete()

            if custom_id.startswith('clan_members'):

                пользователь = disnake.utils.get(inter.guild.members, id = profile_user[inter.author.id])

                idd = 1
                clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
                role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))

                membersID = []
                tip_data_clan = []
                member_data_clan = []
                tip_time_time = []

                items_per_page = 10
                for member in reversed(role.members):
                    membersID.append(member.id)

                embed = disnake.Embed(description = f"Общее количество участником - **{len(membersID)}**", color = 3092790)
                pages = [membersID[i:i + items_per_page] for i in range(0, len(membersID), items_per_page)]

                if not str(inter.author.id) in currentClanTopPage:
                    currentClanTopPage[str(inter.author.id)] = 0
                if custom_id == 'clan_members_first_page':
                    currentClanTopPage[str(inter.author.id)] = 0
                if custom_id == 'clan_members_prev_page':
                    if currentClanTopPage[str(inter.author.id)] > 0:
                        currentClanTopPage[str(inter.author.id)] -= 1
                if custom_id == 'clan_members_exit':
                    return await inter.message.delete()
                if custom_id == 'clan_members_right_page':
                    if currentClanTopPage[str(inter.author.id)] < len(pages) - 1:
                        currentClanTopPage[str(inter.author.id)] += 1
                if custom_id == 'clan_members_last_page':
                    currentClanTopPage[str(inter.author.id)] = len(pages) - 1
                for member_id in pages[currentClanTopPage[str(inter.author.id)]]:
                    tip_data_clan.append(cluster.sweetness.clan.find_one({'_id': str(member_id)})['rank'])
                    tip_time_time.append(cluster.sweetness.clan.find_one({'_id': str(member_id)})['tip_data'])
                    member_data_clan.append(f"<@{member_id}>")
                    idd += 1
                    if idd > 10:
                        break

                embed.set_author(name = f"Участники клана {role.name}", icon_url = inter.guild.icon.url)
                tip_data = "\n".join(reason for reason in tip_data_clan)
                tip_time ="\n".join(reason for reason in tip_time_time)
                member_data = "\n".join(reason for reason in member_data_clan)
                embed.add_field(name = "Дата входа", value = f"{tip_time}")
                embed.add_field(name = "Тип", value = f"{tip_data}")
                embed.add_field(name = "Пользователь", value = f"{member_data}")
                embed.set_footer(text = f'Запросил(а) {inter.author}', icon_url = inter.author.display_avatar.url)
                return await inter.response.edit_message(content = inter.author.mention, embed = embed, view = ClanMembers(inter.author.id))

            if custom_id == 'clan_manage':

                clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
                role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
                clan_name = f"{role.name}"

                embed = disnake.Embed(description = f"{inter.author.mention}, **Выберите действие** над **кланом** <@&{clanxd}>", color = 3092790)
                embed.set_author(name = f"Управление кланом {clan_name}", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                await inter.response.edit_message(embed = embed, view = ClanManage())

            if custom_id == 'clan_back':
                пользователь = disnake.utils.get(inter.guild.members, id = int(profile_user[inter.author.id]))

                with open('clan_sweetness.json','r', encoding='utf-8') as f: 
                    clan = json.load(f)

                if not str(пользователь.id) in clan[str(inter.guild.id)]:
                    clan[str(inter.guild.id)][str(пользователь.id)] = 'Отсутствует'
                    with open('clan_sweetness.json','w') as f:
                        json.dump(clan,f)

                if пользователь == inter.author or пользователь == None:
                    if clan[str(inter.guild.id)][str(пользователь.id)] == 'Отсутствует':
                        embed = disnake.Embed(description = f'{inter.author.mention}, у **Вас** нету клана!', color = disnake.Color.red())
                        embed.set_author(name = f"Клановый профиль", icon_url = inter.guild.icon.url)
                        embed.set_thumbnail(url = inter.author.display_avatar.url)
                        return await inter.send(embed = embed, ephemeral = True)

                if clan[str(inter.guild.id)][str(пользователь.id)] == 'Отсутствует':
                    embed = disnake.Embed(description = f'{inter.author.mention}, у **{пользователь.mention}** нету клана!', color = disnake.Color.red())
                    embed.set_author(name = f"Клановый профиль", icon_url = inter.guild.icon.url)
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    return await inter.send(embed = embed, ephemeral = True)

                clanxd = clan[str(inter.guild.id)][str(пользователь.id)]
                if database.clan_online.count_documents({"_id": str(clanxd)}) == 0:
                    database.clan_online.insert_one({"_id": str(clanxd), "clan_online": 0})

                if database.clan_rating.count_documents({"_id": str(clanxd)}) == 0:
                    database.clan_rating.insert_one({"_id": str(clanxd), "rating": 0})

                clan_online = database.clan_online.find_one({'_id': str(clanxd)})['clan_online']

                clan_points = clan_online // 3600
                clan_level = clan_points // 20
                clan_level += 1

                clan[str(inter.guild.id)][clanxd]['Points'] = int(clan_points)
                clan[str(inter.guild.id)][clanxd]['Level'] = int(clan_level)
                with open('clan_sweetness.json','w') as f: 
                    json.dump(clan,f)

                role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
                clan_name = f"{role.name}"
                clan_description = clan[str(inter.guild.id)][clanxd]['Description']
                clan_owner = f"<@{clan[str(inter.guild.id)][clanxd]['Owner']}>"
                clan_admins = ""
                if clan[str(inter.guild.id)][str(clanxd)]['Admin'] == []:
                    clan_admins += "Отсутствуют"
                if not clan[str(inter.guild.id)][str(clanxd)]['Admin'] == []:
                    clan_admins += f'{" ".join([inter.guild.get_member(i).mention for i in clan[str(inter.guild.id)][str(clanxd)]["Admin"]])}'
                clan_role = f"<@&{clanxd}>"
                clan_id = clanxd
                clan_date = f"{clan[str(inter.guild.id)][clanxd]['Time']}"
                clan_points = f"{clan[str(inter.guild.id)][clanxd]['Points']}"

                clan_level = f"{clan[str(inter.guild.id)][clanxd]['Level']}"
                clan_limit = f"{clan[str(inter.guild.id)][clanxd]['Limit']}"
                clan_balance = f"{clan[str(inter.guild.id)][clanxd]['Balance']}"
                clan_rating = database.clan_rating.find_one({'_id': str(clanxd)})['rating']
                clan_alliance = database.clan_alliance.find_one({'_id': str(clanxd)})['alliance']
                if not clan_alliance == "Отсутствует":
                    clan_alliance = f"<@&{clan_alliance}>"

                role_take = disnake.utils.get(inter.guild.roles, id = int(clanxd))

                embed = disnake.Embed(
                    description=f'# <:clan:1096087543398801601> Клан {clan_name}\n\n<:msg:1096090258107539486> **Описание**\n```{clan_description}``` \
                        \n<:owner:1096087506879008868> **Владелец**: {clan_owner}\n<:admin_clan:1096090695888031794> **Заместители**: {clan_admins} \
                        \n<:clan_role:1096087544715825184> **Роль:** {clan_role}\n<:calendar:1096087540261462127> **Дата создания:** {clan_date} \
                        \n<:point:1096087512834912398> **Очки клана:** {clan_points}\n<:level:1096087492542857346> **Уровень клана:** {clan_level} \
                        \n<:top:1096087524985810964> **Рейтинг клана:** {clan_rating} \
                        \n<:alliance:1139674067067211919> **Альянс:** {clan_alliance} \
                        \n<:id:1096087488625377421> **ID:** {clan_id}', color=3092790)
                embed.add_field(name='<:staff:1096087520023945417> Участники', value=f'```{len(role_take.members)}/{clan_limit}```')
                embed.add_field(name = '<:coin1:1096094598507532479> <:to4kaa:981274474009743430> Баланс', value = f'```{clan_balance}```')
                embed.add_field(name = '<:microphone:1140294304556908695> <:to4kaa:981274474009743430> Голосовой онлайн', value = f'```🕓 {clan_online // hour}ч. {(clan_online - (clan_online // hour * hour)) // 60}м.```')

                clan_url = f"{clan[str(inter.guild.id)][clanxd]['Thumbnail']}"
                if not clan_url == 'Отсутствует':
                    embed.set_thumbnail(url = clan_url)
                else:
                    embed.set_thumbnail(None)

                await inter.response.edit_message(attachments = None, embed = embed, view = ProfileClanView())

    @commands.Cog.listener()
    async def on_modal_submit(self, inter):
        custom_id = inter.custom_id
        with open('clan_sweetness.json','r', encoding='utf-8') as f: 
            clan = json.load(f)
            
        if custom_id[-4:] == "rank":
            for key, value in inter.text_values.items():
                value = value

            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = "Система рангов", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            embed.set_footer(text = f'Выполнил(а) {inter.author}', icon_url = inter.author.display_avatar.url)

            if custom_id == "clan_add_rank":
                rang = currentRankChoice[str(inter.author.id)]

                database.clan.update_one({'_id': str(value)}, {'$set': {'rank': rang}}, upsert = True)
                embed.description = f"### > {inter.author.mention}, вы успешно выдали ранг `{rang}` <@{value}>"
                return await inter.response.edit_message(content = inter.author.mention, embed = embed, view = ClanBack())

            if custom_id == "clan_remove_rank":
                rang = currentRankChoice[str(inter.author.id)]

                database.clan.update_one({'_id': str(value)}, {'$set': {'rank': "Участник"}}, upsert = True)
                embed.description = f"### > {inter.author.mention}, вы успешно сняли ранг `{rang}` <@{value}>"
                return await inter.response.edit_message(content = inter.author.mention, embed = embed, view = ClanBack())

            if custom_id == "clan_limit_rank":
                rank = currentRankChoice[str(inter.author.id)]
                database.clan.update_one({'_id': str(rank)}, {'$set': {'limit': value}}, upsert = True)
                embed.description = f"> ### {inter.author.mention}, Вы успешно установили лимит **{value}** рангу {rank}"

            if custom_id == "clan_create_rank":
                database.clan.update_one({'_id': str(value)}, {'$set': {'limit': 5}}, upsert = True)
                database.clan.update_one({'_id': str(value)}, {'$set': {'admin': 'Отсутствуют'}}, upsert = True)
                database.clan.update_one({'_id': str(clanxd)}, {'$push': {'rank': value}}, upsert = True)
                embed.description = f"> ### {inter.author.mention}, Вы успешно создали ранг {value}"
            if custom_id == "clan_delete_rank":
                database.clan.update_one({'_id': str(clanxd)}, {'$pull': {'rank': value}}, upsert = True)
                database.clan.delete_one({'_id': str(value)})
                embed.description = f"> ### {inter.author.mention}, Вы успешно удалили ранг {value}"

            return await inter.response.edit_message(embed = embed, view = ClanBack())

        if custom_id == "change_color":
            for key, value in inter.text_values.items(): 
                value = value

            role_id = clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Role']
            role = disnake.utils.get(inter.guild.roles, id = int(role_id))
            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            clan[str(inter.guild.id)][clan[str(inter.guild.id)][str(inter.author.id)]]['Balance'] -= 500
            with open('clan_sweetness.json','w') as f:
                json.dump(clan,f)

            await role.edit(color = disnake.Color(hex_to_rgb(str(value))))

            embed = disnake.Embed( description = f'{inter.author.mention}, **Вы** успешно изменили **цвет клана!**', color = 3092790)
            embed.set_author(name = "Управление кланом", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            return await inter.response.edit_message(embed = embed, view = ClanBack())
        if custom_id == "limit_clan":
            for key, value in inter.text_values.items(): 
                value = value

            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            clan_balance = f"{clan[str(inter.guild.id)][clanxd]['Balance']}"
            need_balance = int(value) * 250

            if need_balance > int(clan_balance):
                embed = disnake.Embed(description = f'{inter.author.mention}, У **Вашего** клана на балансе **недостаточно средств!**', color = 3092790)
                embed.set_author(name = "Клан", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.response.edit_message(embed = embed, view = ClanBack())
            
            clan[str(inter.guild.id)][clan[str(inter.guild.id)][str(inter.author.id)]]['Limit'] += int(value)
            clan[str(inter.guild.id)][clan[str(inter.guild.id)][str(inter.author.id)]]['Balance'] -= need_balance
            with open('clan_sweetness.json','w') as f: 
                json.dump(clan,f)

            embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно приобрели **{value} слотов** в клан', color = 3092790)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            embed.set_author(name = f"Клановый магазин {inter.guild.name}", icon_url = inter.guild.icon.url)
            return await inter.response.edit_message(embed = embed, view = ClanBack())

        if custom_id == 'change_name_clan':
            for key, value in inter.text_values.items(): 
                value = value
            role_id = clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Role']
            role = disnake.utils.get(inter.guild.roles, id = int(role_id))
            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            clan[str(inter.guild.id)][clan[str(inter.guild.id)][str(inter.author.id)]]['Balance'] -= 1000
            with open('clan_sweetness.json','w') as f:
                json.dump(clan,f)
            await role.edit(name = value)
            MainCategory = disnake.utils.get(inter.guild.categories, id = int(database.clan.find_one({'_id': str(clanxd)})['category']))
            await MainCategory.edit(name = value)
            embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно изменили **название клана!**', color = 3092790)
            embed.set_author(name = "Управление кланом", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            return await inter.response.edit_message(embed = embed, view = ClanBack())
        
        if custom_id == 'clan_request':
            id = 0
            for key, value in inter.text_values.items(): 
                if id == 0:
                    trebovaniya = value
                if id == 1:
                    trebovaniya1 = value
                if id == 2:
                    trebovaniya2 = value
                if id == 3:
                    trebovaniya3 = value
                if id == 4:
                    trebovaniya4 = value
                id += 1

            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]

            database.clan.update_one({'_id': str(clanxd)}, {'$set': {'trebovaniya': []}}, upsert = True)
            database.clan.update_one({'_id': str(clanxd)}, {'$push': {'trebovaniya': trebovaniya}}, upsert = True)
            database.clan.update_one({'_id': str(clanxd)}, {'$push': {'trebovaniya': trebovaniya1}}, upsert = True)
            database.clan.update_one({'_id': str(clanxd)}, {'$push': {'trebovaniya': trebovaniya2}}, upsert = True)
            database.clan.update_one({'_id': str(clanxd)}, {'$push': {'trebovaniya': trebovaniya3}}, upsert = True)
            database.clan.update_one({'_id': str(clanxd)}, {'$push': {'trebovaniya': trebovaniya4}}, upsert = True)

            embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно установили требования', color = 3092790)
            embed.set_author(name = "Установка требований в клан:", icon_url = inter.guild.icon.url)
            embed.set_footer(text = f"Выполнил(а) {inter.author}",icon_url = inter.author.display_avatar.url)
            await inter.response.edit_message(embed = embed, view = ClanBack())

        if custom_id == 'clan_join':
            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = "Новая заявка в клан", icon_url = inter.guild.icon.url)

            for key, value in inter.text_values.items(): 
                embed.add_field(name = key.capitalize(), value=value, inline = False)
            
            clanxd = database.clan.find_one({'_id': str(inter.message.id)})['clan']
            channel = database.clan.find_one({'_id': str(clanxd)})['channel_2']

            embed.description = f"Поступила новая заявка в клан от: {inter.author.mention}"
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            msg = await self.bot.get_channel(channel).send(embed = embed, view = ClanJoin())
            database.clan.update_one({'_id': str(msg.id)}, {'$set': {'clan': inter.author.id}}, upsert = True)

            embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно **подали заявку** в клан <@&{clanxd}>!', color = 3092790)
            embed.set_author(name = "Подать заявку в клан", icon_url = inter.guild.icon.url)
            embed.set_footer(text = f"Выполнил(а) {inter.author}",icon_url = inter.author.display_avatar.url)
            await inter.send(ephemeral = True, embed = embed)

        if custom_id == 'clan_owner':
            for key, value in inter.text_values.items():
                member = disnake.utils.get(inter.guild.members, id = int(value))
            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            clan[str(inter.guild.id)][str(clanxd)]['Owner'] = member.id

            await inter.author.remove_roles(disnake.utils.get(inter.guild.roles, id = 961296301901885531))
            await member.add_roles(disnake.utils.get(inter.guild.roles, id = 961296301901885531))

            embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно передали **владельца клана** {member.mention}!', color = 3092790)
            embed.set_footer(text = f"Выполнил(а) {inter.author}",icon_url = inter.author.display_avatar.url)
            embed.set_author(name = "Передать владельца клана", icon_url = inter.guild.icon.url)
            await inter.response.edit_message(embed = embed)

            with open('clan_sweetness.json','w') as f: 
                json.dump(clan,f)

        if custom_id[-7:] == 'channel':
            for key, value in inter.text_values.items():
                name = value

            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            role_id = clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Role']
            role = disnake.utils.get(inter.guild.roles, id = int(role_id))

            if custom_id == 'create_voice_channel':
                MainCategory = disnake.utils.get(inter.guild.categories, id = int(database.clan.find_one({'_id': str(clanxd)})['category']))
                channel_1 = await inter.guild.create_voice_channel(name = f"💫・{name}", category = MainCategory)
                await channel_1.set_permissions(role, view_channel = True, connect = True)
                await channel_1.set_permissions(inter.guild.default_role, view_channel = True, connect = False)
                await channel_1.set_permissions(inter.guild.get_role(1001186408486141974), view_channel = False, connect = False) # Не допуск
                await channel_1.set_permissions(inter.guild.get_role(1001140364226347108), view_channel = False, connect = False) # Анверифи
                for admin in clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin']:
                    await channel_1.set_permissions(disnake.utils.get(inter.guild.members, id = int(admin)), manage_channels = True)
                clan_leader = clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner']
                await channel_1.set_permissions(disnake.utils.get(inter.guild.members, id = int(clan_leader)), manage_channels = True)
                await channel_1.set_permissions(inter.author, manage_channels = True)
                await channel_1.set_permissions(disnake.utils.get(inter.guild.roles, id = 1025807036799275141), move_members = True, deafen_members = True, mute_members = True, view_channel = True, connect = True)

                database.clan.update_one({'_id': str(clanxd)}, {'$set': {'voice_channels': []}}, upsert = True)
                database.clan.update_one({'_id': str(clanxd)}, {'$push': {'voice_channels': int(channel_1.id)}}, upsert = True)

                clan[str(inter.guild.id)][clan[str(inter.guild.id)][str(inter.author.id)]]['Balance'] -= 5000
                with open('clan_sweetness.json','w') as f:
                    json.dump(clan,f)

            if custom_id == 'create_text_channel':
                MainCategory = disnake.utils.get(inter.guild.categories, id = int(database.clan.find_one({'_id': str(clanxd)})['category']))
                channel_1 = await inter.guild.create_text_channel(name = f"💬・{name}", category = MainCategory)
                await channel_1.set_permissions(inter.guild.default_role, send_messages = False, view_channel = False)
                await channel_1.set_permissions(role, send_messages=True, view_channel = True)

                clan[str(inter.guild.id)][clan[str(inter.guild.id)][str(inter.author.id)]]['Balance'] -= 2500
                with open('clan_sweetness.json','w') as f:
                    json.dump(clan,f)

            embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно **добавили канал** под названием **{name}**', color = 3092790)
            embed.set_author(name = f"Кланы {inter.guild.name}", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            return await inter.response.edit_message(embed = embed)

        if custom_id == 'clan_avatar':
            for key, value in inter.text_values.items():
                site = value

            if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id:
                clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Thumbnail'] = site
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно добавили аватарку клана!', color = disnake.Color.green())
                embed.set_author(name = "Управление кланом", icon_url = inter.guild.icon.url)
                embed.set_footer(text = f"Выполнил(а) {inter.author}",icon_url = inter.author.display_avatar.url)
                await inter.send(embed = embed)
            else: 
                embed = disnake.Embed(color = 3092790)
                embed.set_author(name = f"Управление кланом {inter.guild.name}", icon_url = inter.guild.icon.url)
                embed.description = f"{inter.author.mention}, **Вы** не владеете этим кланом!"
                await inter.send(embed = embed)
                
            with open('clan_sweetness.json','w') as f: 
                json.dump(clan,f)
        
        if custom_id == 'clan_desc':
            for key, value in inter.text_values.items():
                описание = value
            if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id:
                clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Description'] = описание
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно добавили/изменили **описание клана**!', color = 3092790)
                embed.set_author(name = "Управление кланом", icon_url = inter.guild.icon.url)
                embed.set_footer(text = f"Выполнил(а) {inter.author}",icon_url = inter.author.display_avatar.url)
                await inter.send(embed = embed)
            else:
                embed = disnake.Embed(title = f'{inter.author.mention}, **Вы** не владеете этим кланом!', color = disnake.Color.red())
                embed.set_author(name = f"Кланы {inter.guild.name}", icon_url = inter.guild.icon.url)
                await inter.send(embed = embed)
            with open('clan_sweetness.json','w') as f:
                json.dump(clan,f)

        if custom_id[-3:] == 'ban':
            for key, value in inter.text_values.items():
                member = disnake.utils.get(inter.guild.members, id = int(value))

            if custom_id == 'vidat_ban':
                if not str(member.id) in clan[str(inter.guild.id)]:
                    clan[str(inter.guild.id)][str(member.id)] = 'Отсутствует'
                    with open('clan_sweetness.json','w') as f:
                        json.dump(clan,f)

                if clan[str(inter.guild.id)][str(member.id)] == 'Отсутствует':
                    embed = disnake.Embed(description = f'{inter.author.mention}, У **{member.id}** нету **клана**!', color = disnake.Color.red())
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    return await inter.response.edit_message(embed = embed)

                clanxd = clan[str(inter.guild.id)][str(inter.author.id)]

                if member == inter.author:
                    embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** не можете у себя **забрать доступ** в клан', color = disnake.Color.red())
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    return await inter.response.edit_message(embed = embed)

                if member.id in clan[str(inter.guild.id)][str(clanxd)]['BanList']:
                    embed = disnake.Embed(description = f'{inter.author.mention}, **Этот пользователь** и так **находится** в чёрном **списке клана**', color = disnake.Color.red())
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    return await inter.response.edit_message(embed = embed)
                
                clan[str(inter.guild.id)][str(member.id)] = 'Отсутствует'

                role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
                await member.remove_roles(role)

                clan[str(inter.guild.id)][str(clanxd)]['ClanMembers'] -= 1
                clan[str(inter.guild.id)][str(clanxd)]['BanList'].append(member.id)
                role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))
                await member.remove_roles(role)

                with open('clan_sweetness.json','w') as f:
                    json.dump(clan,f)

                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно забрали у {member.mention} доступ в клан', color = disnake.Color.green())
                embed.set_footer(text = f"Выполнил(а) {inter.author}",icon_url = inter.author.display_avatar.url)
                await inter.response.edit_message(embed = embed)
            if custom_id == 'remove_ban':
                if not str(member.id) in clan[str(inter.guild.id)]:
                    clan[str(inter.guild.id)][str(member.id)] = 'Отсутствует'
                    with open('clan_sweetness.json','w') as f:
                        json.dump(clan,f)

                clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
                clan[str(inter.guild.id)][str(clanxd)]['BanList'].remove(member.id)
                with open('clan_sweetness.json','w') as f:
                    json.dump(clan,f)

                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно выдали {member.mention} доступ в клан', color = disnake.Color.green())
                embed.set_footer(text = f"Выполнил(а) {inter.author}",icon_url = inter.author.display_avatar.url)
                await inter.response.edit_message(embed = embed)

        if custom_id[-5:] == 'admin':
            for key, value in inter.text_values.items():
                member = disnake.utils.get(inter.guild.members, id = int(value))

            if custom_id == 'vidat_admin':
                embed = disnake.Embed(color = 3092790, description = f"{inter.author.mention}, **У** {member.mention} нету клана!")
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_footer(text = f"Выполнил(а) {inter.author}",icon_url = inter.author.display_avatar.url)
                embed.set_author(name = f"Выдать заместителя", icon_url = inter.guild.icon.url)

                if int(member.id) == int(inter.author.id):
                    embed.description = f"{inter.author.mention}, **Вы** не можете выдать себе заместителя!"
                    return await inter.send(embed = embed)

                if not str(member.id) in clan[str(inter.guild.id)]:
                    embed.description = f"{inter.author.mention}, **У** {member.mention} нету клана!"
                    return await inter.send(embed = embed)

                if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin'] == 'Отсутствуют':
                
                    clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin'] = []
                    with open('clan_sweetness.json','w') as f:
                        json.dump(clan,f)

                cluster.sweetness.clan.update_one({'_id': str(member.id)}, {'$set': {'rank': f'Заместитель'}}, upsert = True)
                        
                clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin'].append(member.id)
                with open('clan_sweetness.json','w') as f:
                    json.dump(clan,f)

                embed.description = f'{inter.author.mention}, **Вы** успешно **назначили** на заместителя {member.mention}'
                await inter.response.edit_message(embed = embed)

                clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
                role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))

                await member.add_roles(disnake.utils.get(inter.guild.roles, id = 961299056968237127))

                embed = disnake.Embed(description = f'{inter.author.mention} Назначил вас заместителем клана **{role.name}**', color = 3092790)
                embed.set_author(name = f"Кланы {inter.guild.name}", icon_url = inter.guild.icon.url)
                await member.send(embed = embed)

            if custom_id == 'remove_admin':
                clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin'].remove(member.id)
                with open('clan_sweetness.json','w') as f: 
                    json.dump(clan,f)

                cluster.sweetness.clan.update_one({'_id': str(member.id)}, {'$set': {'rank': f"Участник"}}, upsert = True)

                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно сняли {member.mention} с **заместителя**', color = disnake.Color.green())
                embed.set_footer(text = f"Выполнил(а) {inter.author}",icon_url = inter.author.display_avatar.url)
                await inter.response.edit_message(embed = embed)

                clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
                role = disnake.utils.get(inter.guild.roles, id = int(clan[str(inter.guild.id)][str(clanxd)]['Role']))

                await member.remove_roles(disnake.utils.get(inter.guild.roles, id = 961299056968237127))

                embed = disnake.Embed(description = f'{inter.author.mention} Снял с вас заместителя клана **{role.name}**', color = disnake.Color.red())
                return await member.send(embed = embed)

        if custom_id == 'kick_clan':
            for key, value in inter.text_values.items():
                member = disnake.utils.get(inter.guild.members, id = int(value))

            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = "Выгнать из клана", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)

            clan[str(inter.guild.id)][str(value)] = 'Отсутствует'
            with open('clan_sweetness.json','w') as f:
                json.dump(clan,f)

            if clan[str(inter.guild.id)][str(inter.author.id)] == 'Отсутствует':
                embed.description = f'{inter.author.mention}, У **Вас** нету **клана**!'
                return await inter.response.edit_message(embed = embed)
            
            if member == inter.author:
                embed.description = f'{inter.author.mention}, **Вы** не можете выгнать **себя из клана**'
                return await inter.response.edit_message(embed = embed)
            
            if str(member.id) == str(clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner']):
                embed.description = f'{inter.author.mention}, **Вы** не можете выгнать **клан лидера**'
                return await inter.response.edit_message(embed = embed)
                
            if clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Owner'] == inter.author.id:
                clan[str(inter.guild.id)][str(member.id)] = 'Отсутствует'

                role_id = clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Role']
                role = disnake.utils.get(inter.guild.roles, id = int(role_id))
                await member.remove_roles(role)

                embed.description = f'{inter.author.mention}, **Вы** успешно выгнали <@{value}> из клана <@&{clan[str(inter.guild.id)][str(inter.author.id)]}>'
                await inter.response.edit_message(embed = embed, view = ClanBack())

                if member.id in clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin']:
                    await member.remove_roles(disnake.utils.get(inter.guild.roles, id = 961299056968237127))
                    clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin'].remove(member.id)
                    with open('clan_sweetness.json','w') as f:
                        json.dump(clan,f)

                return await member.remove_roles(disnake.utils.get(inter.guild.roles, id = 961529522082185226))
            
            if inter.author.id in clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin']:
                if member.id in clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Admin']:
                    embed.description = f'{inter.author.mention}, **Вы** не можете выгнать заместителя клана, являясь **заместилем клана**'
                    return await inter.response.edit_message(embed = embed)
                
                clan[str(inter.guild.id)][str(member.id)] = 'Отсутствует'

                role_id = clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Role']
                role = disnake.utils.get(inter.guild.roles, id = int(role_id))
                await member.remove_roles(role)

                embed.description = f'{inter.author.mention}, **Вы** успешно выгнали <@{value}> из клана <@&{clan[str(inter.guild.id)][str(inter.author.id)]}>'
                await inter.response.edit_message(embed = embed, view = ClanBack())

                return await member.remove_roles(disnake.utils.get(inter.guild.roles, id = 961529522082185226))





        if custom_id == "vidat_clan":
            for key, value in inter.text_values.items():
                member = disnake.utils.get(inter.guild.members, id = int(value))

            embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** не можете **пригласить себя** в клан!', color = 3092790)
            embed.set_author(name = f"Клан | {inter.guild.name}", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)

            try:
                if not str(member.id) in clan[str(inter.guild.id)]:
                    clan[str(inter.guild.id)][str(member.id)] = 'Отсутствует'
                    with open('clan_sweetness.json', 'w') as f:
                        json.dump(clan,f)
            except:
                embed.description = f'{inter.author.mention}, Пользователь не найден на сервере либо неправильно введен айди'
                return await inter.response.edit_message(embed = embed, view = ClanBack())

            if member == inter.author: 
                embed.description = f'{inter.author.mention}, **Вы** не можете **пригласить себя** в клан!'
                return await inter.response.edit_message(embed = embed, view = ClanBack())

            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            if clan[str(inter.guild.id)][str(clanxd)]['Limit'] == clan[str(inter.guild.id)][str(clanxd)]['ClanMembers']:
                embed.description = f'{inter.author.mention}, **Ваш** клан достиг **лимита участников**!'
                return await inter.response.edit_message(embed = embed, view = ClanBack())

            if int(member.id) in clan[str(inter.guild.id)][str(clanxd)]['BanList']: 
                embed.description = f'{inter.author.mention}, **Этот** пользователь находится в чёрном списке клана.'
                return await inter.response.edit_message(embed = embed, view = ClanBack())

            if clan[str(inter.guild.id)][str(member.id)] == 'Отсутствует':
                clan_owner = inter.author
                role_id = clan[str(inter.guild.id)][str(clan[str(inter.guild.id)][str(inter.author.id)])]['Role']
                role = disnake.utils.get(inter.guild.roles, id = int(role_id))
                name = role.name
                embed.description = f'{inter.author.mention} **предлагает** вам вступить в клан {name}, **воспользуйтесь кнопками** ниже для ответа'
                bot = self.bot
                try:
                    await member.send(embed = embed, view = ClanInvite(clan_owner, bot, name))
                except:
                    embed.description = f'{inter.author.mention}, **Невозможно** отправить **сообщение** {member.mention}'
                    return await inter.response.edit_message(embed = embed, view = ClanBack())

                embed.description = f'{inter.author.mention}, **Вы** успешно **пригласили в клан** {member.mention}'
                await inter.response.edit_message(embed = embed, view = ClanBack())
            else: 
                embed.description = f'У {member.mention} уже есть **клан**!'
                return await inter.response.edit_message(embed = embed, view = ClanBack())

        if custom_id == 'pay_clan':
            for key, value in inter.text_values.items():
                count = value

            embed = disnake.Embed(description=f'{inter.author.mention}, **Нельзя** указать сумму **ниже нуля**!', color=3092790)
            embed.set_thumbnail(url=inter.author.display_avatar.url)
            embed.set_author(name=f"Депозит | {inter.guild.name}", icon_url=inter.guild.icon.url)
            
            match int(count):
                case x if x < 0:
                    embed.description=f'{inter.author.mention}, **Нельзя** указать сумму **ниже нуля**!'
                    return await inter.response.edit_message(embed=embed, view=ClanBack())
                case 0:
                    embed.description=f'{inter.author.mention}, **Нельзя** равной **нулю**!'
                    return await inter.response.edit_message(embed=embed, view=ClanBack())
                case x if x > int(database.economy.find_one({"_id": str(inter.author.id)})["balance"]):
                    embed.description=f'{inter.author.mention}, у **Вас** на балансе недостаточно <:coin1:1096094598507532479>'
                    return await inter.response.edit_message(embed=embed, view=ClanBack())

            if clan[str(inter.guild.id)][str(inter.author.id)] == 'Отсутствует': 
                embed.description = f'{inter.author.mention}, у **Вас** нету **клана**!'
                return await inter.response.edit_message(embed = embed, view = ClanBack())

            clanxd = clan[str(inter.guild.id)][str(inter.author.id)]
            if not str(inter.author.id) in clan[str(inter.guild.id)][str(clanxd)]['Deposit']:
                clan[str(inter.guild.id)][str(clanxd)]['Deposit'][str(inter.author.id)] = {}
                clan[str(inter.guild.id)][str(clanxd)]['Deposit'][str(inter.author.id)] = 0
                with open('clan_sweetness.json','w') as f: 
                    json.dump(clan,f)

            database.economy.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": -int(count)}})
            clan[str(inter.guild.id)][str(clanxd)]['Deposit'][str(inter.author.id)] += int(count)
            clan[str(inter.guild.id)][str(clanxd)]['Balance'] += int(count)
            with open('clan_sweetness.json','w') as f:
                json.dump(clan,f)

            embed.description = f'{inter.author.mention}, **Вы** успешно **внесли** {count} <:coin1:1096094598507532479> на депозит клана!'
            return await inter.response.edit_message(embed = embed, view = ClanBack())
def setup(bot):
    bot.add_cog(ClanProfileCog(bot))