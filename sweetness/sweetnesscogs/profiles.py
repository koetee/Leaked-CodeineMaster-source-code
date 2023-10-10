import pymongo
import disnake
import json
import requests
import re
from disnake.utils import get
from disnake.ext import commands
from disnake import Localized
from disnake.enums import ButtonStyle, TextInputStyle
from PIL import Image, ImageDraw, ImageFont

intermessage_id = {}

cluster = pymongo.MongoClient(f"mongodb://127.0.0.1/myFirstDatabase?retryWrites=true&w=majority")

files = cluster.sweetness.files

database = cluster.sweetness

min = 60
hour = 60 * 60
day = 60 * 60 * 24
profile_user = {}
achievement_reward = {}
achievement = {}

class MarryYes(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, emoji=f'{files.find_one({"_id": "accept"})["emoji_take"]}', custom_id = 'yesmarry'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, emoji=f'{files.find_one({"_id": "decline"})["emoji_take"]}', custom_id = 'nomarry'))

class InformationProfile(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Назад', custom_id = 'back_profile', emoji=f'{files.find_one({"_id": "duel"})["emoji_take"]}'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Выход', custom_id = 'exit_profile', emoji=f'{files.find_one({"_id": "basket"})["emoji_take"]}'))

class BackAchievements(disnake.ui.View):
    def __init__(self, пользователь, achiev):
        super().__init__()
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label = 'Вернуться назад', custom_id = 'achievements_main', emoji=f'{files.find_one({"_id": "left"})["emoji_take"]}'))
        if database.achievements.find_one({"_id": str(пользователь.id)})[f"{str(achiev)}"] == "NO":
            try:
                if database.achievements_count.find_one({"_id": str(пользователь.id)})[f"{str(achiev)}"] == "YES":
                    self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label='Получить награду', custom_id='achievements_take_reward', emoji='<:gift:1136967445530284073>'))
            except:
                self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label='Получить награду', custom_id='achievements_take_reward', emoji='<:gift:1136967445530284073>', disabled=True))
        else:
            self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label='Получить награду', custom_id='achievements_take_reward', emoji='<:gift:1136967445530284073>', disabled=True))
        self.add_item(disnake.ui.Button(style = ButtonStyle.red, label = 'Выход', custom_id = 'exit_profile', emoji=f'{files.find_one({"_id": "basket"})["emoji_take"]}'))

class Achievements1Dropdown(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Выберите достижение",
            options = [
                disnake.SelectOption(label="Первые шаги", description="Напишите 30 сообщений или просидите 5 минут в войсе", value = '1_achiev'),
                disnake.SelectOption(label="Кто то сказал БУСТЕР?", description="Поддержите наш проект впервые с помощью буста", value = '2_achiev',),
                disnake.SelectOption(label="Бесплатно?!", description="Заберите ежедневные награды 5 раз", value = '3_achiev'),
                disnake.SelectOption(label="День сурка", description="Заберите ежедневные награды 15 раз", value = '4_achiev'),
                disnake.SelectOption(label="Ежедневный трудяга?!", description="Заберите ежедневные награды 30 раз", value = '5_achiev'),
                disnake.SelectOption(label="Свой среди своих", description="Отправьте 100 сообщений в пределах сервера", value = '6_achiev'),
                disnake.SelectOption(label="Произошла адаптация", description="Отправьте 500 сообщений в пределах сервера", value = '7_achiev'),
                disnake.SelectOption(label="Тысяча чертей! Тысяча сообщений!", description="Отправьте 1000 сообщений в пределах сервера", value = '8_achiev'),
                disnake.SelectOption(label="Буквенный абьюзер", description="Отправьте 5000 сообщений в пределах сервера", value = '9_achiev'),
                disnake.SelectOption(label="Клавиатурный чемпион", description="Отправьте 10.000 сообщений в пределах сервера", value = '10_achiev'),
                disnake.SelectOption(label="Клавиатурный червь", description="Отправьте 20.000 сообщений в пределах сервера", value = '11_achiev'),
                disnake.SelectOption(label="Голосовой первопроходец", description="Просидите 15 минут в голосовых каналах сервера", value = '12_achiev'),
                disnake.SelectOption(label="Любитель пообщаться", description="Просидите 1 час в голосовых каналах сервера", value = '13_achiev'),
                disnake.SelectOption(label="Начинающий подпивасник", description="Просидите 8 час в голосовых каналах сервера", value = '14_achiev'),
                disnake.SelectOption(label="Активный голосовой пользователь", description="Просидите 24 часа в голосовых каналах сервера", value = '15_achiev'),
            ],
        )

class Achievements2Dropdown(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Выберите достижение",
            options = [
                disnake.SelectOption(label="Голоса в голове", description="Просидите 5 дней в голосовых каналах сервера", value = '16_achiev'),
                disnake.SelectOption(label="Дед инсайд", description="Просидите 15 дней в голосовых каналах сервера", value = '17_achiev'),
                disnake.SelectOption(label="Начинайющий транжира", description="Потратьте 1.000 монет", value = '18_achiev'),
                disnake.SelectOption(label="Опытный транжира", description="Потратьте 5.000 монет", value = '19_achiev'),
                disnake.SelectOption(label="Отличный шоппинг", description="Потратьте 15.000 монет", value = '20_achiev'),
                disnake.SelectOption(label="Выдающийся шоппинг", description="Потратьте 25.000 монет", value = '21_achiev'),
                disnake.SelectOption(label="Закупаемся на последние деньги", description="Потратьте 50.000 монет", value = '22_achiev'),
                disnake.SelectOption(label="Чеканная монета", description="Передайте 500 монет", value = '23_achiev'),
                disnake.SelectOption(label="Делим добычу!", description="Передайте 1500 монет", value = '24_achiev'),
                disnake.SelectOption(label="Щедрый на монеты", description="Передайте 5000 монет", value = '25_achiev'),
                disnake.SelectOption(label="Богатый", description="Передайте 15000 монет", value = '26_achiev'),
                disnake.SelectOption(label="Мажор", description="Передайте 50000 монет", value = '27_achiev'),
            ],
        )
class Achievements3Dropdown(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Выберите достижение",
            options = [
                disnake.SelectOption(label="Клановый союзник", description="Вступить в клан", value = '32_achiev'),
                disnake.SelectOption(label="Узы вечной любви", description="Создать брак", value = '33_achiev'),
                disnake.SelectOption(label="Мастер инклюзивности", description="Создать личную роль", value = '34_achiev'),
                disnake.SelectOption(label="Личное пространство", description="Создать личную комнату", value = '35_achiev'),
                disnake.SelectOption(label="Любопытный путник", description="Пригласить 1 участника на сервер", value = '36_achiev'),
                disnake.SelectOption(label="Дружный приглашатель", description="Пригласить 3 участника на сервер", value = '37_achiev'),
                disnake.SelectOption(label="Ведущий группы", description="Пригласить 5 участников на сервер", value = '38_achiev'),
                disnake.SelectOption(label="Лидер десятки", description="Пригласить 10 участников на сервер", value = '39_achiev'),
                disnake.SelectOption(label="Платиновый спонсор", description="Стать спонсором", value = '40_achiev'),
                disnake.SelectOption(label="Сотрудник в рядах", description="Быть в стаффе сервера", value = '41_achiev'),
                disnake.SelectOption(label="Дебютная победа", description="Выиграть 1 дуэль", value = '42_achiev'),
                disnake.SelectOption(label="Мастер дуэльной арены", description="Выиграть 5 дуэлей", value = '43_achiev'),
                disnake.SelectOption(label="Покоритель дуэлей", description="Выиграть 15 дуэлей", value = '44_achiev'),
                disnake.SelectOption(label="Чемпион дуэлей", description="Выиграть 30 дуэлей", value = '45_achiev'),
                disnake.SelectOption(label="Олд сервера", description='Иметь роль "олд сервера', value = '46_achiev'),
            ],
        )

class Achievements2(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Achievements2Dropdown())
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label = 'Предыдущая', custom_id = 'achievements_next_1', emoji=f'{files.find_one({"_id": "left"})["emoji_take"]}'))
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label = 'Следующая', custom_id = 'achievements_next_3', emoji=f'{files.find_one({"_id": "right"})["emoji_take"]}'))
        self.add_item(disnake.ui.Button(style = ButtonStyle.red, label = 'Выход', custom_id = 'exit_profile', emoji=f'{files.find_one({"_id": "basket"})["emoji_take"]}'))

class Achievements3(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Achievements3Dropdown())
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label = 'Предыдущая', custom_id = 'achievements_next_2', emoji=f'{files.find_one({"_id": "left"})["emoji_take"]}'))
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label = 'Следующая', custom_id = 'achievements_next_4', emoji=f'{files.find_one({"_id": "right"})["emoji_take"]}', disabled = True))
        self.add_item(disnake.ui.Button(style = ButtonStyle.red, label = 'Выход', custom_id = 'exit_profile', emoji=f'{files.find_one({"_id": "basket"})["emoji_take"]}'))

class Achievements1(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Achievements1Dropdown())
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label = 'Предыдущая', custom_id = 'achievements_previous_zero', emoji=f'{files.find_one({"_id": "left"})["emoji_take"]}', disabled = True))
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label = 'Следующая', custom_id = 'achievements_next_2', emoji=f'{files.find_one({"_id": "right"})["emoji_take"]}'))
        self.add_item(disnake.ui.Button(style = ButtonStyle.red, label = 'Выход', custom_id = 'exit_profile', emoji=f'{files.find_one({"_id": "basket"})["emoji_take"]}'))

class ProfileView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label = 'Достижения', custom_id = 'achievements_main', emoji=f'{files.find_one({"_id": "achievements"})["emoji_take"]}'))
        self.add_item(disnake.ui.Button(style = ButtonStyle.red, label = 'Выход', custom_id = 'exit_profile', emoji=f'{files.find_one({"_id": "basket"})["emoji_take"]}'))

class LoveProfileView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label = 'Развод', custom_id = 'divorce', emoji=f'{files.find_one({"_id": "heart_broken"})["emoji_take"]}'))
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label = 'Пополнить', custom_id = 'givebalancelprofile', emoji=f'{files.find_one({"_id": "plus"})["emoji_take"]}'))
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label = 'Название', custom_id = 'editnamelprofile', emoji=f'{files.find_one({"_id": "edit"})["emoji_take"]}'))
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label = 'Выход', custom_id = 'exit_profile', emoji=f'{files.find_one({"_id": "basket"})["emoji_take"]}'))

class LoveBack(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = ButtonStyle.secondary, label = 'Назад', custom_id = 'backloveprofile', emoji=f'{files.find_one({"_id": "duel"})["emoji_take"]}'))
        self.add_item(disnake.ui.Button(style = ButtonStyle.red, label = 'Выход', custom_id = 'exit_profile', emoji=f'{files.find_one({"_id": "basket"})["emoji_take"]}'))
    
class profilecog(commands.Cog):
    def __init__(self, bot: commands.Bot(intents=disnake.Intents.all())):
        self.bot = bot

    @commands.slash_command(description = 'Профиль')
    async def profile(self, inter, тип: str = commands.Param(choices=[Localized("Обычный", key="CHOICE_A"), Localized("Любовный", key="CHOICE_O")]), пользователь: disnake.Member = None):
        if пользователь == inter.author or пользователь == None:
            пользователь = inter.author
        
        profile_user[inter.author.id] = пользователь.id

        if тип == 'Обычный':
            if database.economy.count_documents({"_id": str(пользователь.id)}) == 0:
                database.economy.insert_one({"_id": str(пользователь.id), "balance": 0})
            if database.donate.count_documents({"_id": str(пользователь.id)}) == 0:
                database.donate.insert_one({"_id": str(пользователь.id), "donate_balance": 0})
            if database.marry.count_documents({"_id": str(пользователь.id)}) == 0:
                database.marry.insert_one({"_id": str(пользователь.id), "love": 'Отсутствует'})
            if database.online.count_documents({"_id": str(пользователь.id)}) == 0:
                database.online.insert_one({"_id": str(пользователь.id), "online": 0})
            if database.reputation.count_documents({"_id": str(пользователь.id)}) == 0:
                database.reputation.insert_one({"_id": str(пользователь.id), "rep": 0})
            if database.message.count_documents({"_id": str(пользователь.id)}) == 0:
                database.message.insert_one({"_id": str(пользователь.id), "message_count": 0})

            im = Image.open('profile_sweetness.png')
            
            pipeline = [
                {"$sort": {"online": -1}},
                {"$group": {"_id": None, "users": {"$push": "$_id"}}},
                {"$unwind": {"path": "$users", "includeArrayIndex": "rank"}},
                {"$match": {"users": str(пользователь.id)}}
            ]

            results = list(database.online.aggregate(pipeline))

            if results:
                voice_top = results[0]["rank"] + 1
            else:
                voice_top = 0

            await inter.response.defer()

            ImageDraw.Draw(im).text((540, 57), str(voice_top), font=ImageFont.truetype("Gordita_bold.ttf", size=32), fill=(255, 255, 255))

            if database.lvl.count_documents({"_id": str(пользователь.id)}) == 0:
                database.lvl.insert_one({"_id": str(пользователь.id), "lvl": 1, "exp": 0, "message_count": 0})

            result = database.lvl.find_one({'_id': str(пользователь.id)})
            lvl = result['lvl']
            if lvl > 10:
                ImageDraw.Draw(im).text((930, 861), str(lvl), font = ImageFont.truetype('Gordita_bold.ttf', encoding='UTF-8', size = 48), fill = (255, 255, 255))
            else:
                ImageDraw.Draw(im).text((948, 861), str(lvl), font = ImageFont.truetype('Gordita_bold.ttf', encoding='UTF-8', size = 48), fill = (255, 255, 255))

            online = database.online.find_one({"_id": str(пользователь.id)})["online"]
            balance = database.economy.find_one({'_id': str(пользователь.id)})['balance']
            donate = database.donate.find_one({'_id': str(пользователь.id)})['donate_balance']
            message = database.message.find_one({'_id': str(пользователь.id)})['message_count']

            online_text = f"{online // 86400}д. {((online // 3600)) % 24}ч."

            ImageDraw.Draw(im).text((392, 931), "0", font = ImageFont.truetype('Gordita_bold.ttf', encoding='UTF-8', size = 40), fill = (255, 255, 255))
            

            ImageDraw.Draw(im).text((340, 605), str(online_text), font = ImageFont.truetype('Gordita_bold.ttf', encoding='UTF-8', size = 40), fill = (255, 255, 255))
            ImageDraw.Draw(im).text((300, 401), str(balance), font = ImageFont.truetype('Gordita_bold.ttf', encoding='UTF-8', size = 64), fill = (255, 255, 255))
            ImageDraw.Draw(im).text((1517, 403), str(donate), font = ImageFont.truetype('Gordita_bold.ttf', encoding='UTF-8', size = 64), fill = (255, 255, 255))
            ImageDraw.Draw(im).text((382, 714), str(message), font = ImageFont.truetype('Gordita_bold.ttf', encoding='UTF-8', size = 40), fill = (255, 255, 255))

            if not database.marry.find_one({'_id': str(пользователь.id)})['love'] == 'Отсутствует':
                try:
                    user = disnake.utils.get(inter.guild.members, id = int(database.marry.find_one({'_id': str(пользователь.id)})['love']))

                    ImageDraw.Draw(im).text((1495, 665), f"{user.name[:6]}..#{user.discriminator}" if len(user.name) > 8 else f"{user.name}#{user.discriminator}", font = ImageFont.truetype("Gordita_bold.ttf", size=36), fill = (255, 255, 255))
                    Image.open(requests.get(user.display_avatar.url, stream = True).raw).resize((103, 100)).save(f'avatars/avatar_profile_{user.name}.png')
                    mask_im = Image.new("L", Image.open(f"avatars/avatar_profile_{user.name}.png").size)
                    ImageDraw.Draw(mask_im).ellipse((0, 0, 103, 100), fill = 255)
                    im.paste(Image.open(f'avatars/avatar_profile_{user.name}.png'), (1356, 618), mask_im)
                except:
                    database.marry.delete_one({'_id': str(inter.author.id)})
            else:
                ImageDraw.Draw(im).text((1495, 665), f"Отсутствует", font = ImageFont.truetype("Gordita_bold.ttf", size=36), fill = (255, 255, 255))
            
            ImageDraw.Draw(im).text((697, 623), f"{пользователь.name[:6]}..#{пользователь.discriminator}" if len(пользователь.name) > 8 else f"{пользователь.name}#{пользователь.discriminator}", font = ImageFont.truetype('Gordita_bold.ttf', encoding='UTF-8', size =96), fill = (255, 255, 255))

            Image.open(requests.get(пользователь.display_avatar.url, stream = True).raw).resize((301, 301)).save('avatars/avatar_profile_sweetnes.png')
            mask_im = Image.new("L", Image.open("avatars/avatar_profile_sweetnes.png").size)
            ImageDraw.Draw(mask_im).ellipse((0, 0, 301, 301), fill = 255)
            im.paste(Image.open('avatars/avatar_profile_sweetnes.png'), (809, 141), mask_im)

            symbols = f"{пользователь.activity}"
            pattern = r'<:[^>]+>|<a:[^>]+>'
            new_string, n = re.subn(pattern, '', symbols)

            if symbols == 'None':
                ImageDraw.Draw(im).text((744, 746), str('Статус не установлен.'), font=ImageFont.truetype('Gordita_regular.ttf', encoding='UTF-8', size=36), fill = (255, 255, 255))
            else: 
                ImageDraw.Draw(im).text((726, 746), str(new_string[:25]), font=ImageFont.truetype('Gordita_regular.ttf', encoding='UTF-8', size=36), fill = (255, 255, 255))

            im.save('profiles/out_profile_sweetnes.png')
            await inter.send(inter.author.mention, file = disnake.File('profiles/out_profile_sweetnes.png'), view = ProfileView())

        if тип == 'Любовный':
            im = Image.open('lprofile_sweetness.png')
            database_marry = cluster.sweetness.marry
            if пользователь == inter.author or пользователь == None: 
                пользователь = inter.author
            if database_marry.count_documents({"_id": str(пользователь.id)}) == 0:
                database_marry.insert_one({"_id": str(пользователь.id), "love": 'Отсутствует'})

            if database.economy.count_documents({"_id": str(пользователь.id)}) == 0: 
                database.economy.insert_one({"_id": str(пользователь.id), "balance": 0})
            if database_marry.find_one({'_id': str(пользователь.id)})['love'] == 'Отсутствует':
                embed = disnake.Embed(title = "Любовный профиль", color = 3092790, description = f'У {пользователь.mention} **отсутствует пара**!')
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            user = disnake.utils.get(inter.guild.members, id = int(database_marry.find_one({"_id": str(пользователь.id)})["love"]))

            if database.love_online.count_documents({"_id": str(пользователь.id)}) == 0:
                database.love_online.insert_one({"_id": str(пользователь.id), "Love_online": 0})
            if database.love_online.count_documents({"_id": str(user.id)}) == 0:
                database.love_online.insert_one({"_id": str(user.id), "Love_online": 0})

            balance = database_marry.find_one({'_id': str(пользователь.id)})['balance']
            time = database_marry.find_one({'_id': str(пользователь.id)})['Time']
            N = int(database.love_online.find_one({"_id": str(пользователь.id)})["Love_online"]) + int(database.love_online.find_one({"_id": str(user.id)})["Love_online"])
            love_online = f'{((N // 3600)) % 24}ч. {((N // 60)) %60}м.'

            await inter.response.defer()

            ImageDraw.Draw(im).text((1198, 648), f"{balance}", font = ImageFont.truetype('Montserrat-Bold.ttf', encoding='UTF-8', size = 24), fill = (255, 255, 255))
            ImageDraw.Draw(im).text((740, 648), love_online, font = ImageFont.truetype('Montserrat-Bold.ttf', encoding='UTF-8', size = 24), fill = (255, 255, 255))
            ImageDraw.Draw(im).text((963, 97), time, font = ImageFont.truetype('Montserrat-Bold.ttf', encoding='UTF-8', size = 24), fill = (255, 255, 255))
            
            ImageDraw.Draw(im).text((143, 489), f"{пользователь.name[:6]}..#{пользователь.discriminator}" if len(пользователь.name) > 8 else f"{пользователь.name}#{пользователь.discriminator}", font = ImageFont.truetype('Gordita_bold.ttf', encoding='UTF-8', size = 64), fill = (255, 255, 255))
            ImageDraw.Draw(im).text((1406, 489), f"{user.name[:6]}..#{user.discriminator}" if len(user.name) > 8 else f"{user.name}#{user.discriminator}", font = ImageFont.truetype('Gordita_bold.ttf', encoding='UTF-8', size = 64), fill = (255, 255, 255))
            
            Image.open(requests.get(пользователь.display_avatar.url, stream = True).raw).resize((235, 235)).save(f"user_ava_lprofile_sweetness.png", quality = 90)
            mask_im = Image.new("L", Image.open(f"user_ava_lprofile_sweetness.png").size)
            ImageDraw.Draw(mask_im).ellipse((0, 0, 235, 235), fill = 255)
            im.paste(Image.open(f"user_ava_lprofile_sweetness.png"), (209, 229), mask_im)
            
            Image.open(requests.get(user.display_avatar.url, stream = True).raw).resize((235, 235)).save(f"user_ava_lprofile_sweetness2.png", quality = 90)
            mask_im = Image.new("L", Image.open(f"user_ava_lprofile_sweetness2.png").size)
            ImageDraw.Draw(mask_im).ellipse((0, 0, 235, 235), fill = 255)
            im.paste(Image.open(f"user_ava_lprofile_sweetness2.png"), (1473, 229), mask_im)
            im.save('out_loveprofile_sweetnes.png')
            
            await inter.send(inter.author.mention, file = disnake.File('out_loveprofile_sweetnes.png'), view = LoveProfileView())

    @commands.Cog.listener()
    async def on_dropdown(self, inter):
        custom_id = inter.values[0]

        if custom_id[-6:] == 'achiev':
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(title = f'Достижения', color = 3092790)
                embed.description = f"{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**"
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            
            пользователь = inter.author

            embed = disnake.Embed(description = "", color = 3092790)
            embed.set_author(name = f"Достижения — {inter.author} | {inter.guild.name}", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = пользователь.display_avatar.url)

            expenses = database.history.find_one({'_id': str(inter.author.id)})

            casino = expenses['casino']
            items = expenses['items']
            roles = expenses['roles']
            transfer = expenses['pay']
            loverooms = expenses['loverooms']
            clan = expenses['clan']
            general = int(casino) + int(items) + int(roles) + int(roles) + int(transfer) + int(loverooms) + int(clan)
            history_case = database.history_case.find_one({"_id": str(пользователь.id)})

            invited_count = 0

            for invite in filter(lambda i: i.inviter and i.inviter.id == пользователь.id, await inter.guild.invites()):
                invited_count += invite.uses

            if custom_id == "1_achiev":
                embed.description += "Напишите **30 сообщений** или просидите **5 минут в войсе**"
                embed.add_field(name = f"\n<:progress:1136957793480474664> Прогресс", value = f"```• [{database.message.find_one({'_id': str(пользователь.id)})['message_count']}/30] сообщений. [{database.online.find_one({'_id': str(пользователь.id)})['online']}/300]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```50 💰```")
            
            if custom_id == "2_achiev":
                embed.description += "**Поддержите** наш проект впервые с **помощью буста**"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{'1' if disnake.utils.get(inter.guild.roles, id=890469731285483541) in пользователь.roles else '0'}/1]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```1000 💰```")

            if custom_id == "3_achiev":
                embed.description += "**Заберите** ежедневные **награды 5 раз** (/timely)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{database.count.find_one({'_id': str(пользователь.id)})['daily']}/5]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```150 💰```")

            if custom_id == "4_achiev":
                embed.description += "**Заберите** ежедневные **награды 15 раз** (/timely)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{database.count.find_one({'_id': str(пользователь.id)})['daily']}/15]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```250 💰```")

            if custom_id == "5_achiev":
                embed.description += "**Заберите** ежедневные **награды 30 раз** (/timely)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{database.count.find_one({'_id': str(пользователь.id)})['daily']}/30]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```1000 💰```")

            if custom_id == "6_achiev":
                embed.description += "**Отправьте 100 сообщений** в пределах сервера"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{database.message.find_one({'_id': str(пользователь.id)})['message_count']}/100]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```100 💰```")

            if custom_id == "7_achiev":
                embed.description += "**Отправьте 500 сообщений** в пределах сервера"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{database.message.find_one({'_id': str(пользователь.id)})['message_count']}/500]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```200 💰```")

            if custom_id == "8_achiev":
                embed.description += "**Отправьте 1000 сообщений** в пределах сервера"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{database.message.find_one({'_id': str(пользователь.id)})['message_count']}/1000]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```300 💰```")

            if custom_id == "9_achiev":
                embed.description += "**Отправьте 5000 сообщений** в пределах сервера"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{database.message.find_one({'_id': str(пользователь.id)})['message_count']}/5000]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```400 💰```")

            if custom_id == "10_achiev":
                embed.description += "**Отправьте 10.000 сообщений** в пределах сервера"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{database.message.find_one({'_id': str(пользователь.id)})['message_count']}/10000]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```1000 💰```")

            if custom_id == "11_achiev":
                embed.description += "**Отправьте 20.000 сообщений** в пределах сервера"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{database.message.find_one({'_id': str(пользователь.id)})['message_count']}/20000]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```2000 💰```")

            if custom_id == "12_achiev":
                embed.description += "**Просидите 15 минут** в голосовых каналах сервера"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{database.online.find_one({'_id': str(пользователь.id)})['online']}/900]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```100 💰```")

            if custom_id == "13_achiev":
                embed.description += "**Просидите 1 час** в голосовых каналах сервера"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{database.online.find_one({'_id': str(пользователь.id)})['online']}/3600]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```200 💰```")

            if custom_id == "14_achiev":
                embed.description += "**Просидите 8 часов** в голосовых каналах сервера"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{database.online.find_one({'_id': str(пользователь.id)})['online']}/28800]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```300 💰```")

            if custom_id == "15_achiev":
                embed.description += "**Просидите 24 часа** в голосовых каналах сервера"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{database.online.find_one({'_id': str(пользователь.id)})['online']}/86400]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```400 💰```")

            if custom_id == "16_achiev":
                embed.description += "**Просидите 5 дней** в голосовых каналах сервера"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{database.online.find_one({'_id': str(пользователь.id)})['online']}/432000]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```500 💰```")

            if custom_id == "17_achiev":
                embed.description += "**Просидите 15 дней** в голосовых каналах сервера"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{database.online.find_one({'_id': str(пользователь.id)})['online']}/1296000]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```600 💰```")

            if custom_id == "18_achiev":
                embed.description += "**Потратьте 1.000 монет**"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{general}/1000]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```50 💰```")

            if custom_id == "19_achiev":
                embed.description += "**Потратьте 5.000 монет**"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{general}/5000]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```100 💰```")

            if custom_id == "20_achiev":
                embed.description += "**Потратьте 15.000 монет**"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{general}/15000]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```150 💰```")

            if custom_id == "21_achiev":
                embed.description += "**Потратьте 25.000 монет**"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{general}/25000]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```200 💰```")

            if custom_id == "22_achiev":
                embed.description += "**Потратьте 50.000 монет**"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{general}/50000]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```300 💰```")

            if custom_id == "23_achiev":
                embed.description += "**Передайте 500 монет** (/give)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{transfer}/500]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```50 💰```")

            if custom_id == "24_achiev":
                embed.description += "**Передайте 1500 монет** (/give)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{transfer}/1500]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```100 💰```")

            if custom_id == "25_achiev":
                embed.description += "**Передайте 5000 монет** (/give)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{transfer}/5000]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```150 💰```")

            if custom_id == "26_achiev":
                embed.description += "**Передайте 15000 монет** (/give)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{transfer}/15000]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```200 💰```")

            if custom_id == "27_achiev":
                embed.description += "**Передайте 50000 монет** (/give)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{transfer}/50000]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```300 💰```")

            if custom_id == "32_achiev":
                embed.description += "**Вступить в клан** (<#1114621290129661993>)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{'1' if disnake.utils.get(inter.guild.roles, id=1135115663686504538) in пользователь.roles else '0'}/1]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```300 💰```")

            if custom_id == "33_achiev":
                embed.description += "**Создать брак** (/marry)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{'1' if disnake.utils.get(inter.guild.roles, id=1009210754198679592) in пользователь.roles else '0'}/1]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```500 💰```")

            if custom_id == "34_achiev":
                embed.description += "**Создать личную роль** (/role_create)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [0/1]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```500 💰```")

            if custom_id == "35_achiev":
                embed.description += "**Создать личную комнату** (Вся информация: <#1077549078738636880>)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [0/1]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```500 💰```")

            if custom_id == "36_achiev":
                embed.description += "**Пригласить 1 участника** на сервер (сделать ссылку приглашения и скинуть другу)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [0/1]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```50 💰```")

            if custom_id == "37_achiev":
                embed.description += "**Пригласить 3 участника** на сервер (сделать ссылку приглашения и скинуть другу)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```•  [{invited_count}/3]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```100 💰```")

            if custom_id == "38_achiev":
                embed.description += "**Пригласить 5 участников** на сервер (сделать ссылку приглашения и скинуть другу)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```•  [{invited_count}/5]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```150 💰```")

            if custom_id == "39_achiev":
                embed.description += "**Пригласить 10 участников** на сервер (сделать ссылку приглашения и скинуть другу)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```•  [{invited_count}/10]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```200 💰```")

            if custom_id == "40_achiev":
                embed.description += "**Стать спонсором** (вся информация: <#1106619047715545148>)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{'1' if disnake.utils.get(inter.guild.roles, id=1030783838600830976) in пользователь.roles else '0'}/1]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```1000 💰```")

            if custom_id == "41_achiev":
                embed.description += "**Быть** в **стаффе** сервера"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{'1' if disnake.utils.get(inter.guild.roles, id=1135115879298891786) in пользователь.roles else '0'}/1]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```750 💰```")

            if custom_id == "42_achiev":
                embed.description += "**Выиграть 1 дуэль** (/duel)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{database.duel.find_one({'_id': str(пользователь.id)})['count']}/1] ```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```50 💰```")

            if custom_id == "43_achiev":
                embed.description += "**Выиграть 5 дуэлей** (/duel)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{database.duel.find_one({'_id': str(пользователь.id)})['count']}/5] ```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```100 💰```")

            if custom_id == "44_achiev":
                embed.description += "**Выиграть 15 дуэлей** (/duel)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```•  [{database.duel.find_one({'_id': str(пользователь.id)})['count']}/15]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```200 💰```")

            if custom_id == "45_achiev":
                embed.description += "**Выиграть 30 дуэлей** (/duel)"
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value = f"```• [{database.duel.find_one({'_id': str(пользователь.id)})['count']}/30]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```350 💰```")

            if custom_id == "46_achiv":

                embed.description += '**Иметь** роль **"олд сервера"**'
                embed.add_field(name = f"\n<:progress:1136957793480474664> прогресс", value=f"```• [{'1' if disnake.utils.get(inter.guild.roles, id=939009901416562718) in пользователь.roles else '0'}/1]```")
                embed.add_field(name = f"\n<:gift:1136967445530284073> Награда", value = f"```500 💰```")

            value_match = re.search(r'\d+', custom_id)
            id = int(value_match.group()) if value_match else 0
            achievement[str(inter.author.id)] = id
            
            value_match = re.search(r'\d+', embed.fields[1].value)
            reward_amount = int(value_match.group()) if value_match else 0
            achievement_reward[str(inter.author.id)] = reward_amount

            embed.set_footer(text = f"Запросил(а) {inter.author}", icon_url = inter.guild.icon.url)
            try:
                asfasf = database.achievements.find_one({'_id': str(inter.author.id)})[f"{str(id)}"]
                await inter.response.edit_message(embed = embed, view = BackAchievements(пользователь, id))
            except:
                database.achievements.update_one({'_id': str(inter.author.id)}, {'$set': {f"{str(id)}": "NO"}}, upsert = True)
                await inter.response.edit_message(embed = embed, view = BackAchievements(пользователь, id))

    @commands.Cog.listener()
    async def on_button_click(self, inter):

        custom_id = inter.component.custom_id

        if custom_id == "achievements_take_reward":
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description=f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color=3092790)
                embed.set_author(name = "Забрать награду", icon_url=inter.guild.icon.url)
                embed.set_thumbnail(url=inter.author.display_avatar.url)
                return await inter.send(ephemeral=True, embed=embed)
            
            achievements_reward = achievement_reward[str(inter.author.id)]
            achievements = achievement[str(inter.author.id)]

            database.economy.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": +int(achievements_reward)}})

            embed = disnake.Embed(description=f'{inter.author.mention}, **Вы** успешно **получили награду** за достижение в размере **{achievements_reward}** <:amitobal:1158567849707716708>', color=3092790)
            embed.set_author(name = "Получить награду за достижение", icon_url=inter.guild.icon.url)
            embed.set_thumbnail(url=inter.author.display_avatar.url)
            await inter.response.edit_message(embed = embed, components = [])

            database.achievements.update_one({'_id': str(inter.author.id)}, {'$set': {f'{str(achievements)}': "YES"}}, upsert = True)

        if custom_id == 'back_profile':
            if database.economy.count_documents({"_id": str(пользователь.id)}) == 0:
                database.economy.insert_one({"_id": str(пользователь.id), "balance": 0})
            if database.marry.count_documents({"_id": str(пользователь.id)}) == 0:
                database.marry.insert_one({"_id": str(пользователь.id), "love": 'Отсутствует'})
            if database.online.count_documents({"_id": str(пользователь.id)}) == 0:
                database.online.insert_one({"_id": str(пользователь.id), "online": 0})
            if database.reputation.count_documents({"_id": str(пользователь.id)}) == 0:
                database.reputation.insert_one({"_id": str(пользователь.id), "rep": 0})
            if database.message.count_documents({"_id": str(пользователь.id)}) == 0:
                database.message.insert_one({"_id": str(пользователь.id), "message_count": 0})

            im = Image.open('profile_sweetnes.png')
            
            pipeline = [
                {"$sort": {"online": -1}},
                {"$group": {"_id": None, "users": {"$push": "$_id"}}},
                {"$unwind": {"path": "$users", "includeArrayIndex": "rank"}},
                {"$match": {"users": str(пользователь.id)}}
            ]

            results = list(database.online.aggregate(pipeline))

            if results:
                voice_top = results[0]["rank"] + 1
            else:
                voice_top = 0

            ImageDraw.Draw(im).text((246.64, 441), str(voice_top), font=ImageFont.truetype("Gordita_bold.ttf", size=17), fill=(255, 255, 255))

            if database.lvl.count_documents({"_id": str(пользователь.id)}) == 0:
                database.lvl.insert_one({"_id": str(пользователь.id), "lvl": 1, "exp": 0, "message_count": 0})

            result = database.lvl.find_one({'_id': str(пользователь.id)})
            lvl = result['lvl']
            if lvl > 10:
                ImageDraw.Draw(im).text((456, 417), str(lvl), font = ImageFont.truetype('Gordita_bold.ttf', encoding='UTF-8', size = 75), fill = (255, 255, 255))
            else:
                ImageDraw.Draw(im).text((456, 417), str(lvl), font = ImageFont.truetype('Gordita_bold.ttf', encoding='UTF-8', size = 75), fill = (255, 255, 255))

            online = database.online.find_one({"_id": str(пользователь.id)})["online"]
            balance = database.economy.find_one({'_id': str(пользователь.id)})['balance']
            reputation = database.reputation.find_one({'_id': str(пользователь.id)})['rep']
            message = database.message.find_one({'_id': str(пользователь.id)})['message_count']

            online_text = f"{online // 86400}д. {((online // 3600)) % 24}ч."

            ImageDraw.Draw(im).text((208, 353), str(online_text), font = ImageFont.truetype('Gordita_bold.ttf', encoding='UTF-8', size = 17), fill = (255, 255, 255))
            ImageDraw.Draw(im).text((448, 342), str(balance), font = ImageFont.truetype('Gordita_bold.ttf', encoding='UTF-8', size = 30), fill = (255, 255, 255))
            ImageDraw.Draw(im).text((233, 395), str(message), font = ImageFont.truetype('Gordita_bold.ttf', encoding='UTF-8', size = 17), fill = (255, 255, 255))
            await inter.response.defer()
            if not database.marry.find_one({'_id': str(пользователь.id)})['love'] == 'Отсутствует':
                try:
                    user = disnake.utils.get(inter.guild.members, id = int(database.marry.find_one({'_id': str(пользователь.id)})['love']))

                    ImageDraw.Draw(im).text((721, 414), f"{user.name[:6]}..#{user.discriminator}" if len(user.name) > 8 else f"{user.name}#{user.discriminator}", font = ImageFont.truetype("Gordita_bold.ttf", size=24), fill = (255, 255, 255))
                    Image.open(requests.get(user.display_avatar.url, stream = True).raw).resize((133, 133)).save(f'avatars/avatar_profile_{user.name}.png')
                    mask_im = Image.new("L", Image.open(f"avatars/avatar_profile_{user.name}.png").size)
                    ImageDraw.Draw(mask_im).ellipse((0, 0, 133, 133), fill = 255)
                    im.paste(Image.open(f'avatars/avatar_profile_{user.name}.png'), (738, 269), mask_im)
                except:
                    database.marry.delete_one({'_id': str(inter.author.id)})
            
            ImageDraw.Draw(im).text((347, 286), f"{пользователь.name[:6]}..#{пользователь.discriminator}" if len(пользователь.name) > 8 else f"{пользователь.name}#{пользователь.discriminator}", font = ImageFont.truetype('Gordita_bold.ttf', encoding='UTF-8', size = 38), fill = (255, 255, 255))

            Image.open(requests.get(пользователь.display_avatar.url, stream = True).raw).resize((170, 170)).save('avatars/avatar_profile_sweetnes.png')
            mask_im = Image.new("L", Image.open("avatars/avatar_profile_sweetnes.png").size)
            ImageDraw.Draw(mask_im).ellipse((0, 0, 170, 170), fill = 255)
            im.paste(Image.open('avatars/avatar_profile_sweetnes.png'), (395, 60), mask_im)

            symbols = f"{пользователь.activity}"
            pattern = r'<:[^>]+>|<a:[^>]+>'
            new_string, n = re.subn(pattern, '', symbols)

            if symbols == 'None':
                ImageDraw.Draw(im).text((687, 660), str('Статус не установлен.'), font=ImageFont.truetype('Gordita_regular.ttf', encoding='UTF-8', size=51), fill = (255, 255, 255))
            else: 
                ImageDraw.Draw(im).text((687, 660), str(new_string[:22]), font=ImageFont.truetype('Gordita_regular.ttf', encoding='UTF-8', size=51), fill = (255, 255, 255))

            im.save('profiles/out_profile_sweetnes.png')
            
            await inter.message.edit(inter.author.mention, file = disnake.File('profiles/out_profile_sweetnes.png'), view = ProfileView())

        if inter.component.custom_id == 'backloveprofile':
            im = Image.open('lprofile_sweetnes.png')

            if пользователь == inter.author or пользователь == None: 
                пользователь = inter.author

            if database.marry.count_documents({"_id": str(пользователь.id)}) == 0: 
                database.marry.insert_one({"_id": str(пользователь.id), "love": "Отсутствует"})

            if database.economy.count_documents({"_id": str(пользователь.id)}) == 0: 
                database.economy.insert_one({"_id": str(пользователь.id), "balance": 0})
                
            if database.marry.find_one({'_id': str(пользователь.id)})['love'] == 'Отсутствует':
                embed = disnake.Embed(title = "Любовный профиль", color = 3092790, description = f'У {пользователь.mention} **отсутствует пара**!')
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)

            user = disnake.utils.get(inter.guild.members, id = int(database.marry.find_one({"_id": str(пользователь.id)})["love"]))

            if database.love_online.count_documents({"_id": str(пользователь.id)}) == 0:
                database.love_online.insert_one({"_id": str(пользователь.id), "Love_online": 0})
            if database.love_online.count_documents({"_id": str(user.id)}) == 0:
                database.love_online.insert_one({"_id": str(user.id), "Love_online": 0})

            font = ImageFont.truetype('Montserrat-Bold.ttf', encoding='UTF-8', size = 23)
            balance = database.marry.find_one({'_id': str(пользователь.id)})['balance']
            time = database.marry.find_one({'_id': str(пользователь.id)})['Time']
            N = int(database.love_online.find_one({"_id": str(пользователь.id)})["Love_online"]) + int(database.love_online.find_one({"_id": str(user.id)})["Love_online"])
            love_online = f'{((N // 3600)) % 24}ч. {((N // 60)) %60}м.'

            ImageDraw.Draw(im).text((840, 271), f"{balance}", font = ImageFont.truetype('Montserrat-Bold.ttf', encoding='UTF-8', size = 23), fill = (255, 255, 255))
            ImageDraw.Draw(im).text((125, 136), love_online, font = ImageFont.truetype('Montserrat-Bold.ttf', encoding='UTF-8', size = 27), fill = (255, 255, 255))
            ImageDraw.Draw(im).text((108, 194), time, font = ImageFont.truetype('Montserrat-Bold.ttf', encoding='UTF-8', size = 20), fill = (255, 255, 255))
            
            ImageDraw.Draw(im).text((247, 43), f"{пользователь.name[:6]}..#{пользователь.discriminator}" if len(пользователь.name) > 8 else f"{пользователь.name}#{пользователь.discriminator}", font = ImageFont.truetype('Gordita_bold.ttf', encoding='UTF-8', size = 27), fill = (255, 255, 255))
            ImageDraw.Draw(im).text((524, 324), f"{user.name[:6]}..#{user.discriminator}" if len(user.name) > 8 else f"{user.name}#{user.discriminator}", font = ImageFont.truetype('Gordita_bold.ttf', encoding='UTF-8', size = 27), fill = (255, 255, 255))
            
            Image.open(requests.get(пользователь.display_avatar.url, stream = True).raw).resize((170, 170)).save(f"user_ava_lprofile_sweetness.png", quality = 90)
            mask_im = Image.new("L", Image.open(f"user_ava_lprofile_sweetness.png").size)
            ImageDraw.Draw(mask_im).ellipse((0, 0, 170, 170), fill = 255)
            im.paste(Image.open(f"user_ava_lprofile_sweetness.png"), (281, 107), mask_im)
            
            Image.open(requests.get(user.display_avatar.url, stream = True).raw).resize((170, 170)).save(f"user_ava_lprofile_sweetness2.png", quality = 90)
            mask_im = Image.new("L", Image.open(f"user_ava_lprofile_sweetness2.png").size)
            ImageDraw.Draw(mask_im).ellipse((0, 0, 170, 170), fill = 255)
            im.paste(Image.open(f"user_ava_lprofile_sweetness2.png"), (508, 107), mask_im)
            im.save('out_loveprofile_sweetnes.png')
            
            await inter.response.edit_message(file = disnake.File('out_loveprofile_sweetnes.png'), view = LoveProfileView())

        if inter.component.custom_id == 'edit_status_lprofile':
            if not inter.message.content == inter.author.mention:
                return await inter.send(ephemeral = True, embed = disnake.Embed(title = 'Изменить статус', description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790).set_thumbnail(url = inter.author.display_avatar.url))
            await inter.response.send_modal(title=f"Изменить статус", custom_id = "status_edit_lprofile",components=[disnake.ui.TextInput(label="Текст", placeholder = "Введите текст",custom_id = "Текст", style = disnake.TextInputStyle.short, max_length = 150)])
        
        if inter.component.custom_id == 'givebalancelprofile':
            if not inter.message.content == inter.author.mention:
                return await inter.send(ephemeral = True, embed = disnake.Embed(title = 'Пополнить баланс лав румы', description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790).set_thumbnail(url = inter.author.display_avatar.url))
            await inter.response.send_modal(title=f"Пополнить баланс", custom_id = "popolnit",components=[disnake.ui.TextInput(label="Сумма", placeholder = "Введите сумму",custom_id = "Сумма", style = disnake.TextInputStyle.short, max_length = 6)])
        
        if inter.component.custom_id == 'editnamelprofile':
            if not inter.message.content == inter.author.mention:
                return await inter.send(ephemeral = True, embed = disnake.Embed(title = 'Название лав румы', description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790).set_thumbnail(url = inter.author.display_avatar.url))
            await inter.response.send_modal(title=f"Стоимость 500", custom_id = "edit_name_lprofile",components=[disnake.ui.TextInput(label="Стоимость 500", placeholder = "Введите название",custom_id = "Название", style = disnake.TextInputStyle.short, max_length = 30)])
        
        if inter.component.custom_id == 'divorce':
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790).set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_author(name = "Любовная комната", icon_url = inter.guild.icon.url)
                return await inter.send(ephemeral = True, embed = embed)

            if database.marry.find_one({'_id': str(inter.author.id)})['love'] == 'Отсутствует':
                disnake.Embed(description = '**Вы** не можете развестись, **не поженившись!**', color = 3092790)
                embed.set_author(name = "Любовная комната", icon_url = inter.guild.icon.url)
                return await inter.response.edit_message(embed = embed)
            
            embed =  disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно развелись!', color = 3092790)
            embed.set_author(name = "Любовная комната", icon_url = inter.guild.icon.url)
            embed.set_footer(text = inter.author,icon_url = inter.author.display_avatar.url)
            await inter.response.edit_message(attachments=None, embed = embed, files = [], components = [])
            
            user = disnake.utils.get(inter.guild.members, id = int(database.marry.find_one({'_id': str(inter.author.id)})['love']))
            
            database.marry.delete_one({'_id': str(inter.author.id)})
            database.marry.delete_one({'_id': str(user.id)})

            try:
                if user.voice.channel.category_id == 1150510070564651128: 
                    await user.move_to(None)
            except: 
                pass
            try:
                if inter.author.voice.channel.category_id == 1150510070564651128: 
                    await inter.author.move_to(None)
            except:
                pass

            await inter.author.remove_roles(disnake.utils.get(inter.guild.roles, id = 1153853219357864007))
            await user.remove_roles(disnake.utils.get(inter.guild.roles, id = 1153853219357864007))

        if inter.component.custom_id == 'exit_profile':
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(title = 'Выход', description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            await inter.message.delete()

        if custom_id[-4:] == 'main':
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(title = f'Профиль', color = 3092790)
                embed.description = f"{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**"
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)

            if custom_id == 'marry_main':
                await inter.response.send_modal(title=f"Пожениться", custom_id = "marry_main", components=[
                    disnake.ui.TextInput(label="Айди пользователя", placeholder="Например: 849353684249083914",custom_id = "Айди пользователя", style=disnake.TextInputStyle.short, max_length=35)],
                    )

        if custom_id[:12] == 'achievements':
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(title = f'Достижения', color = 3092790)
                embed.description = f"{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**"
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            
            пользователь = inter.author

            if database.online.count_documents({"_id": str(пользователь.id)}) == 0: 
                database.online.insert_one({"_id": str(пользователь.id),"online": 0})
            
            if database.history.count_documents({"_id": str(пользователь.id)}) == 0: 
                database.history.insert_one({"_id": str(пользователь.id), "casino": 0, "items": 0, "roles": 0, "pay": 0, "loverooms": 0, "clan": 0})

            if database.message.count_documents({"_id": str(пользователь.id)}) == 0: 
                database.message.insert_one({"_id": str(пользователь.id),"message_count": 0})

            if database.history_case.count_documents({"_id": str(пользователь.id)}) == 0: 
                database.history_case.insert_one({"_id": str(пользователь.id), "data": [], "prize": []})

            description = ""
            online = database.online.find_one({'_id': str(пользователь.id)})
            achievements_count = 0

            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = f"Достижения — {пользователь} | {inter.guild.name}", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = пользователь.display_avatar.url)

            if database.count.count_documents({"_id": str(пользователь.id)}) == 0:
                database.count.insert_one({"_id": str(пользователь.id), "daily": 0})

            if custom_id == 'achievements_next_1' or custom_id == "achievements_main":
                await inter.response.defer()

                if database.message.find_one({'_id': str(пользователь.id)})['message_count'] > 30 or online['online'] > 300:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'1': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Первые шаги\n'
                else:
                    description += '<:deny:1158567118921547826> Первые шаги\n'
    
                if disnake.utils.get(inter.guild.roles, id = 890469731285483541) in пользователь.roles:
                    achievements_count += 1
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'2': "YES"}}, upsert = True)
                    description += '<:accepts:1158567121840787606> Кто то сказал БУСТЕР?\n'
                else:
                    description += '<:deny:1158567118921547826> Кто то сказал БУСТЕР?\n'

                if database.count.find_one({'_id': str(пользователь.id)})['daily'] > 5:
                    achievements_count += 1
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'3': "YES"}}, upsert = True)
                    description += '<:accepts:1158567121840787606> Бесплатно?!\n'
                else:
                    description += '<:deny:1158567118921547826> Бесплатно?!\n'

                if database.count.find_one({'_id': str(пользователь.id)})['daily'] > 15:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'4': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> День сурка\n'
                else:
                    description += '<:deny:1158567118921547826> День сурка\n'

                if database.count.find_one({'_id': str(пользователь.id)})['daily'] > 30:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'5': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Ежедневный трудяга\n'
                else:
                    description += '<:deny:1158567118921547826> Ежедневный трудяга?!\n'

                if database.message.find_one({'_id': str(пользователь.id)})['message_count'] > 100:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'6': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Свой среди своих\n'
                else:
                    description += '<:deny:1158567118921547826> Свой среди своих\n'

                if database.message.find_one({'_id': str(пользователь.id)})['message_count'] > 500:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'7': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Произошла адаптация\n'
                else:
                    description += '<:deny:1158567118921547826> Произошла адаптация\n'

                if database.message.find_one({'_id': str(пользователь.id)})['message_count'] > 1000:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'8': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Тысяча чертей! Тысяча сообщений!\n'
                else:
                    description += '<:deny:1158567118921547826> Тысяча чертей! Тысяча сообщений!\n'

                if database.message.find_one({'_id': str(пользователь.id)})['message_count'] > 5000:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'9': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Буквенный абьюзер\n'
                else:
                    description += '<:deny:1158567118921547826> Буквенный абьюзер\n'

                if database.message.find_one({'_id': str(пользователь.id)})['message_count'] > 10000:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'10': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Клавиатурный чемпион\n'
                else:
                    description += '<:deny:1158567118921547826> Клавиатурный чемпион\n'

                if database.message.find_one({'_id': str(пользователь.id)})['message_count'] > 20000:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'11': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Клавиатурный червь\n'
                else:
                    description += '<:deny:1158567118921547826> Клавиатурный червь\n'

                if online['online'] > 900:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'12': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Голосовой первопроходец\n'
                else:
                    description += '<:deny:1158567118921547826> Голосовой первопроходец\n'

                if online['online'] > 3600:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'13': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Любитель пообщаться\n'
                else:
                    description += '<:deny:1158567118921547826> Любитель пообщаться\n'

                if online['online'] > 28800:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'14': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Начинающий подпивасник\n'
                else:
                    description += '<:deny:1158567118921547826> Начинающий подпивасник\n'
                    
                if online['online'] > 86400:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'15': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Активный голосовой пользователь\n'
                else:
                    description += '<:deny:1158567118921547826> Активный голосовой пользователь\n'

                embed.description = f"Количество **выполненных достижений** на этой странице: **{achievements_count}**\n\n"
                embed.description += description
                embed.set_footer(text = "Страница 1 из 3")
                await inter.message.edit(attachments=None, embed = embed, view = Achievements1())

            if custom_id == 'achievements_next_2':

                await inter.response.defer()

                expenses = database.history.find_one({'_id': str(пользователь.id)})
                history_case = database.history_case.find_one({"_id": str(пользователь.id)})

                casino = expenses['casino']
                items = expenses['items']
                roles = expenses['roles']
                transfer = expenses['pay']
                loverooms = expenses['loverooms']
                clan = expenses['clan']
                general = int(casino) + int(items) + int(roles) + int(roles) + int(transfer) + int(loverooms) + int(clan)

                if online['online'] > 432000:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'16': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Голоса в голове\n'
                else:
                    description += '<:deny:1158567118921547826> Голоса в голове\n'

                if online['online'] > 1296000:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'17': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Дед инсайд\n'
                else:
                    description += '<:deny:1158567118921547826> Дед инсайд\n'

                if general > 1000:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'18': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Начинайющий транжира\n'
                else:
                    description += '<:deny:1158567118921547826> Начинайющий транжира\n'

                if general > 5000:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'19': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Опытный транжира\n'
                else:
                    description += '<:deny:1158567118921547826> Опытный транжира\n'

                if general > 15000:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'20': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Отличный шоппинг\n'
                else:
                    description += '<:deny:1158567118921547826> Отличный шоппинг\n'

                if general > 25000:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'21': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Выдающийся шоппинг\n'
                else:
                    description += '<:deny:1158567118921547826> Волшебный шоппинг\n'

                if general > 50000:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'22': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Закупаемся на последние деньги\n'
                else:
                    description += '<:deny:1158567118921547826> Закупаемся на последние деньги\n'

                if transfer > 500:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'23': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Чеканная монета\n'
                else:
                    description += '<:deny:1158567118921547826> Чеканная монета\n'

                if transfer > 1500:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'24': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Делим добычу!\n'
                else:
                    description += '<:deny:1158567118921547826> Делим добычу!\n'

                if transfer > 5000:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'25': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Щедрый на монеты\n'
                else:
                    description += '<:deny:1158567118921547826> Щедрый на монеты\n'

                if transfer > 15000:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'26': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Богатый\n'
                else:
                    description += '<:deny:1158567118921547826> Богатый\n'

                if transfer > 50000:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'27': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Мажор\n'
                else:
                    description += '<:deny:1158567118921547826> Мажор\n'

                if len(history_case['prize']) >= 1:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'28': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Первый шажок в неизведанные сокровища\n'
                else:
                    description += '<:deny:1158567118921547826> Первый шажок в неизведанные сокровища\n'

                if len(history_case['prize']) >= 5:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'29': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Пятерка сюрпризов\n'
                else:
                    description += '<:deny:1158567118921547826> Пятерка сюрпризов\n'
                    
                embed.description = f"Количество **выполненных достижений** на этой странице: **{achievements_count}**\n\n"
                embed.description += description
                embed.set_footer(text = "Страница 2 из 3")
                await inter.message.edit(embed = embed, view = Achievements2())

            if custom_id == 'achievements_next_3':

                await inter.response.defer()

                if database.roomcheck.count_documents({"_id": str(inter.author.id)}) == 0:
                    database.roomcheck.insert_one({"_id": str(inter.author.id), "room": []})

                if database.role.count_documents({"_id": str(inter.author.id)}) == 0:
                    database.role.insert_one({"_id": str(inter.author.id), "rolemember": [], "role_time": {}})

                if database.duel.count_documents({"_id": str(пользователь.id)}) == 0:
                    database.duel.insert_one({"_id": str(пользователь.id), "count": 0})

                invited_count = 0

                for invite in filter(lambda i: i.inviter and i.inviter.id == пользователь.id, await inter.guild.invites()):
                    invited_count += invite.uses

                if not database.clan.count_documents({"_id": str(пользователь.id)}) == 0:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'32': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Клановый союзник\n'
                else:
                    description += '<:deny:1158567118921547826> Клановый союзник\n'

                if not database.love_online.count_documents({"_id": str(пользователь.id)}) == 0:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'33': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Узы вечной любви\n'
                else:
                    description += '<:deny:1158567118921547826> Узы вечной любви\n'

                if not database.role.find_one({'_id': str(пользователь.id)})['rolemember'] == []:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'34': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Мастер инклюзивности\n'
                else:
                    description += '<:deny:1158567118921547826> Мастер инклюзивности\n'

                if not database.roomcheck.find_one({'_id': str(пользователь.id)})['room'] == []:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'35': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Личное пространство\n'
                else:
                    description += '<:deny:1158567118921547826> Личное пространство\n'
                    
                if int(invited_count) >= 1:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'36': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Любопытный путник\n'
                else:
                    description += '<:deny:1158567118921547826> Любопытный путник\n'

                if int(invited_count) >= 3:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'37': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Дружный приглашатель\n'
                else:
                    description += '<:deny:1158567118921547826> Дружный приглашатель\n'
                    
                if int(invited_count) >= 5:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'38': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Ведущий группы\n'
                else:
                    description += '<:deny:1158567118921547826> Ведущий группы\n'

                if int(invited_count) >= 10:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'39': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Лидер десятки\n'
                else:
                    description += '<:deny:1158567118921547826> Лидер десятки\n'

                if disnake.utils.get(inter.guild.roles, id = 1030783838600830976) in пользователь.roles:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'40': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Платиновый спонсор\n'
                else:
                    description += '<:deny:1158567118921547826> Платиновый спонсор\n'

                if disnake.utils.get(inter.guild.roles, id = 1135115879298891786) in пользователь.roles:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'41': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Сотрудник в рядах\n'
                else:
                    description += '<:deny:1158567118921547826> Сотрудник в рядах\n'
                    
                if database.duel.find_one({'_id': str(пользователь.id)})['count'] >= 1:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'42': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Дебютная победа\n'
                else:
                    description += '<:deny:1158567118921547826> Дебютная победа\n'
                    
                if database.duel.find_one({'_id': str(пользователь.id)})['count'] >= 5:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'43': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Мастер дуэлей\n'
                else:
                    description += '<:deny:1158567118921547826> Мастер дуэлей\n'

                if database.duel.find_one({'_id': str(пользователь.id)})['count'] >= 15:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'44': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Покоритель дуэлей\n'
                else:
                    description += '<:deny:1158567118921547826> Покоритель дуэлей\n'

                if database.duel.find_one({'_id': str(пользователь.id)})['count'] >= 30:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'45': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Чемпион дуэлей\n'
                else:
                    description += '<:deny:1158567118921547826> Чемпион дуэлей\n'

                if disnake.utils.get(inter.guild.roles, id = 939009901416562718) in пользователь.roles:
                    database.achievements_count.update_one({'_id': str(пользователь.id)}, {'$set': {'46': "YES"}}, upsert = True)
                    achievements_count += 1
                    description += '<:accepts:1158567121840787606> Олд сервера\n'
                else:
                    description += '<:deny:1158567118921547826> Олд сервера\n'

                embed.description = f"Количество **выполненных достижений** на этой странице: **{achievements_count}**\n\n"
                embed.description += description
                embed.set_footer(text = "Страница 3 из 3")
                await inter.message.edit(embed = embed, view = Achievements3())

    @commands.Cog.listener()
    async def on_modal_submit(self, inter):

        if inter.custom_id == 'marry_main':
            for key, value in inter.text_values.items():
                id_member = value

            пользователь = disnake.utils.get(inter.guild.members, id = int(id_member))

            if database.economy.count_documents({"_id": str(inter.author.id)}) == 0: 
                database.economy.insert_one({"_id": str(inter.author.id), "balance": 0})
            if database.economy.count_documents({"_id": str(пользователь.id)}) == 0: 
                database.economy.insert_one({"_id": str(пользователь.id), "balance": 0})

            if database.marry.count_documents({"_id": str(inter.author.id)}) == 0: 
                database.marry.insert_one({"_id": str(inter.author.id), "love": "Отсутствует"})
            if database.marry.count_documents({"_id": str(пользователь.id)}) == 0: 
                database.marry.insert_one({"_id": str(пользователь.id), "love": "Отсутствует"})

            if пользователь == inter.author:
                embed = disnake.Embed(description = f'{inter.author.mention}, **Нельзя** жениться на **себе**!', color = 3092790)
                embed.set_author(name = "Брак", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(embed = embed)

            if database.economy.find_one({"_id": str(inter.author.id)})["balance"] < 1500:
                balance = database.economy.find_one({"_id": str(inter.author.id)})["balance"]
                embed = disnake.Embed(description = f'{inter.author.mention}, У **Вас** на балансе **недостаточно средств**!\nНехватает: **{1500 - balance}** :cookie:', color = 3092790)
                embed.set_author(name = "Брак", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(embed = embed)

            if пользователь != inter.author:
                if database.marry.find_one({'_id': str(inter.author.id)})['love'] == 'Отсутствует':
                    if database.marry.find_one({'_id': str(пользователь.id)})['love'] == 'Отсутствует':
                        embed = disnake.Embed(description = f'**Всё**, что мне когда-либо **требовалось в женщине**, я **нашел в тебе**.. и не могу **позволить**, чтобы другой человек, не я, когда-нибудь **заботился о тебе**. Ты станешь **моей женой?**\n\n{inter.author.mention} сделал **предложение руки и сердца** {пользователь.mention}, мы в **предвкушении..!!**', color=3092790)
                        embed.set_author(name = "Брак", icon_url = inter.guild.icon.url)
                        embed.set_image(url = 'https://i.ytimg.com/vi/wSU81YVVOq0/hqdefault.jpg')
                        msg = await inter.send(content = пользователь.mention, embed = embed, view = MarryYes())
                        intermessage_id[пользователь.id] = inter.author.id

                    else: 
                        embed = disnake.Embed(description = f'{inter.author.mention}, **Этот** пользователь **уже состоит** в браке!', color = 3092790)
                        embed.set_author(name = "Брак", icon_url = inter.guild.icon.url)
                        embed.set_thumbnail(url = inter.author.display_avatar.url)
                        return await inter.send(embed = embed)
                else:
                    embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** уже состоите в **браке**!', color = 3092790)
                    embed.set_author(name = "Брак", icon_url = inter.guild.icon.url)
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    return await inter.send(embed = embed)

        if inter.custom_id == 'popolnit':
            for key, value in inter.text_values.items():
                count = value

            if int(count) > int(database.economy.find_one({'_id': str(inter.author.id)})['balance']):
                embed = disnake.Embed(color = 3092790, description = f'{inter.author.mention}, У **Вас** на балансе **недостаточно средств**')
                embed.set_author(name = "Любовная комната", icon_url = inter.guild.icon.url)
                return await inter.message.edit(embed = embed)

            if database.balance.count_documents({"_id": str(inter.author.id)}) == 0: 
                database.balance.insert_one({"_id": str(inter.author.id), "balance": 0})

            user = disnake.utils.get(inter.guild.members, id = int(database.marry.find_one({'_id': str(inter.author.id)})['love']))
            
            database.economy.update_one({"_id": str(inter.author.id)},{"$inc": {"balance": -int(count)}})
            database.balance.update_one({"_id": str(inter.author.id)},{"$inc": {"balance": +int(count)}})

            database.marry.update_one({"_id": str(inter.author.id)},{"$inc": {"balance": +int(count)}})
            database.marry.update_one({"_id": str(user.id)},{"$inc": {"balance": +int(count)}})

            embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно **внесли** в брак **{count}** <:amitobal:1158567849707716708> ', color = 3092790)
            embed.set_author(name = "Любовная комната", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            return await inter.send(ephemeral = True, embed = embed)

        if inter.custom_id == 'edit_name_lprofile':
            for key, value in inter.text_values.items():
                new_name = value
            user = disnake.utils.get(inter.guild.members, id = int(database.marry.find_one({'_id': str(inter.author.id)})['love']))
            if 500 > int(database.marry.find_one({'_id': str(inter.author.id)})['balance']):
                embed = disnake.Embed(description = f'{inter.author.mention}, На **балансе** лав румы **недостаточно средств**!', color = 3092790)
                embed.set_author(name = "Любовная комната", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            try:
                if inter.author.voice.channel.category.id == 1142583140330782820:
                    await inter.author.voice.channel.edit(name = new_name)
                if user.voice.channel.category.id == 1142583140330782820:
                    await inter.author.voice.channel.edit(name = new_name)
            except:
                pass
            database.marry.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": -500}})
            database.marry.update_one({"_id": str(user.id)},{"$inc": {"balance": -500}})
            database.marry.update_one({'_id': str(inter.author.id)}, {'$set': {'name': new_name}}, upsert = True)
            database.marry.update_one({'_id': str(user.id)}, {'$set': {'name': new_name}}, upsert = True)

            embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно **изменили название** любовной комнаты на **{new_name}**', color = 3092790)
            embed.set_author(name = "Любовная комната", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            embed.set_footer(text = 'С баланса лав румы было снято 500 звезд', icon_url = 'https://cdn.discordapp.com/emojis/1007741833037754479.gif?size=40&quality=lossless')
            return await inter.send(ephemeral = True, embed = embed)
        
def setup(bot): 
    bot.add_cog(profilecog(bot))