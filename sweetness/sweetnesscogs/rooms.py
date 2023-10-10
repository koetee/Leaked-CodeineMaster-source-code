import pymongo
import disnake
import json
import asyncio
import datetime
from disnake.ext import commands
from disnake.utils import get
from disnake.enums import ButtonStyle, TextInputStyle

cluster = pymongo.MongoClient(f"mongodb://127.0.0.1/myFirstDatabase?retryWrites=true&w=majority")

files = cluster.sweetness.files

roleasd = {}
roombutton = {}
idmessage = {}
roomshop = {}
currentRoomMembersPage = {}

min = 60
hour = 60 * 60
day = 60 * 60 * 24

def hex_to_rgb(value):
    value = value.lstrip('#')
    RGB = list(tuple(int(value[i:i + len(value) // 3], 16) for i in range(0, len(value), len(value) // 3)))
    return (RGB[0]<<16) + (RGB[1]<<8) + RGB[2]

class RoomShop(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = '1', custom_id = '1room', emoji = '<:1_:1091732820768075860>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = '2', custom_id = '2room', emoji = '<:2_:1091732822449987654>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = '3', custom_id = '3room', emoji = '<:3_:1091732824823959583>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = '4', custom_id = '4room', emoji = '<:4_:1091732828028411944>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Вернуться к выбору комнаты', custom_id = 'back_room', emoji = '<:back1:1111712230363373700>', row = 1))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Меню', custom_id = 'menu_room_manage', emoji = '<:menu11:1111709626438783036>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Выход', custom_id = 'exit_profile', emoji = '<:cancel:1111701613942415380>', row = 1))

class RoomMembers(disnake.ui.View):

    def __init__(self, author: int):
        super().__init__()

        if not str(author) in currentRoomMembersPage or currentRoomMembersPage[str(author)] == 0:
            self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'room_members_first_page', emoji = '<:back:1008774480778252539>', disabled = True))
            self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'room_members_prev_page', emoji = '<:zxc5:1009168367342587915>', disabled = True))
        else:
            self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'room_members_first_page', emoji = '<:back:1008774480778252539>'))
            self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'room_members_prev_page', emoji = '<:zxc5:1009168367342587915>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.red, custom_id = 'exit_profile', emoji = '<:delete:1135560294190563349>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'room_members_right_page', emoji = '<:zxc4:1009168369112600728>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'room_members_last_page', emoji = '<:zxc7:1009168365627125861>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.blurple, label = 'Меню', custom_id = 'menu_room_manage', emoji = '<:menu11:1111709626438783036>'))

class VidatDostyp(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Меню', custom_id = 'menu_room_manage', emoji = '<:menu11:1111709626438783036>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Вернуться к выбору комнаты', custom_id = 'back_room', emoji = '<:back1:1111712230363373700>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'С ролью', custom_id = 'vidat_1', emoji = '<:plus:1111704771288645642>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Без роли', custom_id = 'vidat_2', emoji = '<:minus:1092011714557521990>'))

class RoomYesDelete(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'room_delete_yes', emoji = '<:yes1:1092007373733900348>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Вернуться к выбору комнаты', custom_id = 'back_room', emoji = '<:back1:1111712230363373700>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Меню', custom_id = 'menu_room_manage', emoji = '<:menu11:1111709626438783036>'))

class RoomYesNo(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'yes_room', emoji = '<:yes1:1092007373733900348>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Вернуться к выбору комнаты', custom_id = 'back_room', emoji = '<:back1:1111712230363373700>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Меню', custom_id = 'menu_room_manage', emoji = '<:menu11:1111709626438783036>'))

class RoomYesNo1(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'yes_room1', emoji = '<:yes1:1092007373733900348>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Вернуться к выбору комнаты', custom_id = 'back_room', emoji = '<:back1:1111712230363373700>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Меню', custom_id = 'menu_room_manage', emoji = '<:menu11:1111709626438783036>'))

class RoomYesOrNo(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'yesroomshop', emoji = '<:yes1:1092007373733900348>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Вернуться к выбору комнаты', custom_id = 'back_room', emoji = '<:back1:1111712230363373700>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Меню', custom_id = 'menu_room_manage', emoji = '<:menu11:1111709626438783036>'))

class TopListRoomsDropdown(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Выберите категорию",
            custom_id = 'top_rooms',
            options = [
                disnake.SelectOption(label="Баланс", value = 'leaderboard_balance_rooms', description="Топ по балансу", emoji = '<:balancetop1:1066435313389547580>'),
                disnake.SelectOption(label="Войс", value = 'leaderboard_voice_rooms',description="Топ по войсу", emoji = '<:time:1064457661480980540>'),
            ],
        )

class TopListRooms(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(TopListRoomsDropdown())
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Меню', custom_id = 'back_room', emoji = '<:menu11:1111709626438783036>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Выход', custom_id = 'exit_profile', emoji = '<:cancel:1111701613942415380>'))

class TopListRoomsView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(TopListRoomsDropdown())
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'За все время', custom_id = 'top_voice_rooms'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'За неделю', custom_id = 'top_voice_rooms_week', emoji = '📅'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Меню', custom_id = 'back_room', emoji = '<:menu11:1111709626438783036>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Выход', custom_id = 'exit_profile', emoji = '<:cancel:1111701613942415380>'))

class RoomManageBack(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Вернуться к выбору комнаты', custom_id = 'back_room', emoji = '<:back1:1111712230363373700>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Меню', custom_id = 'menu_room_manage', emoji = '<:menu11:1111709626438783036>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Выход', custom_id = 'room_manage_exit_3', emoji = '<:cancel:1111701613942415380>'))
    

class RoomDropdown(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            options = [
                disnake.SelectOption(label='Магазин', value = 'room_shop', emoji = '<:shop_1:1111689899452674129>'),
                disnake.SelectOption(label='Участники комнаты', value = 'room_members', emoji = '<:staff:1111701618346434581>'),
                disnake.SelectOption(label='Основная информация', value = 'room_info', emoji = '<:information1:1111712238886191154>'),
                disnake.SelectOption(label='Пополнить баланс', value = 'room_pay', emoji = '<:plus:1111704771288645642>'),
                disnake.SelectOption(label='Выдать доступ', value = 'room_give', emoji = '<:privates4:1109823489508122666>'),
                disnake.SelectOption(label='Выгнать из комнаты', value = 'room_del', emoji = '<:privates3:1109823486907658330>'),
                disnake.SelectOption(label='Выдать совладельца', value = 'room_owner', emoji = '<:plus_man_1:1111689903907012679>'),
                disnake.SelectOption(label='Забрать совладельца', value = 'room_delowner', emoji = '<:minus_man_1:1111689901281394739>'),
                disnake.SelectOption(label='Передать права', value = 'room_give_owner', emoji = '<:privates10:1109823504636985414>'),
                disnake.SelectOption(label='Топы', value = 'room_top', emoji = '<:trophy:1111701669428875284>'),
                disnake.SelectOption(label='Удалить', value = 'room_delete', emoji = '<:mysorka11:1111712241838997574>'),
                disnake.SelectOption(label='Вернуться к выбору комнаты', value = 'back_room', emoji = '<:back1:1111712230363373700>'),
                disnake.SelectOption(label='Выход', value = 'room_otmena', emoji = '<:cancel:1111701613942415380>'),
            ],
        )

class RoomManageMain(disnake.ui.View):

    def __init__(self):
        super().__init__()
        self.add_item(RoomDropdown())

class room1(disnake.ui.Button):
    def __init__(self, xd1):
        super().__init__(style = disnake.ButtonStyle.secondary, label = f'{xd1}')
class room2(disnake.ui.Button):
    def __init__(self, xd2):
        super().__init__(style = disnake.ButtonStyle.secondary, label = f'{xd2}')
class room3(disnake.ui.Button):
    def __init__(self, xd3):
        super().__init__(style = disnake.ButtonStyle.secondary, label = f'{xd3}')
class room4(disnake.ui.Button):
    def __init__(self, xd4):
        super().__init__(style = disnake.ButtonStyle.secondary, label = f'{xd4}')
class room5(disnake.ui.Button):
    def __init__(self, xd5):
        super().__init__(style = disnake.ButtonStyle.secondary, label = f'{xd5}')

class RoomManage(disnake.ui.View):
    def __init__(self, xd1, xd2, xd3, xd4, xd5):
        super().__init__()
        if not xd1 == 'Пусто':
            self.add_item(room1(xd1))
        if not xd2 == 'Пусто':
            self.add_item(room2(xd2))
        if not xd3 == 'Пусто':
            self.add_item(room3(xd3))
        if not xd4 == 'Пусто':
            self.add_item(room4(xd4))
        if not xd5 == 'Пусто':
            self.add_item(room5(xd5))
            
class room_cog(commands.Cog):
    def __init__(self, bot: commands.Bot(intents = disnake.Intents.all(), command_prefix = 'test!')):
        self.bot = bot

    @commands.slash_command(description = 'Создать комнату')
    @commands.has_permissions(administrator = True)
    async def room_give(self, inter, пользователь:disnake.Member, цвет:str, *, название):
        embed = disnake.Embed(title = 'Выдача комнаты', description = f'**Вы** успешно выдали комнату {пользователь.mention} под названием **{название}**', color = 3092790)
        embed.set_thumbnail(url = inter.author.display_avatar.url).set_author(name = inter.author, icon_url = inter.author.display_avatar.url)
        await inter.send(embed = embed)

        new_role = await inter.guild.create_role(name = название, color = disnake.Color(hex_to_rgb(цвет)), mentionable=True)
        channel123 = await inter.guild.create_voice_channel(name = f'・{название}', category = disnake.utils.get(inter.guild.categories, id = 1158537276800913461))
        cluster.sweetness.room.update_one({'_id': str(channel123.id)}, {'$set': {'Data': datetime.datetime.now().strftime("%d.%m.%Y")}}, upsert = True)
        cluster.sweetness.room.update_one({'_id': str(пользователь.id)}, {'$set': {'Plata': 2592000}}, upsert = True)
        cluster.sweetness.room.update_one({'_id': str(пользователь.id)}, {'$set': {'Room': channel123.id}}, upsert = True)
        cluster.sweetness.room.update_one({'_id': str(channel123.id)}, {'$set': {'textchannel': "Отсутствует"}}, upsert = True)
        cluster.sweetness.roomcheck.update_one({'_id': str(пользователь.id)}, {'$push': {'room': int(channel123.id)}}, upsert = True)
        cluster.sweetness.room.update_one({'_id': str(channel123.id)}, {'$set': {'owner': int(пользователь.id)}}, upsert = True)
        cluster.sweetness.room.update_one({'_id': str(channel123.id)}, {'$set': {'Role': new_role.id}}, upsert = True)
        cluster.sweetness.room.update_one({'_id': str(channel123.id)}, {'$set': {'balance': 0}}, upsert = True)
        cluster.sweetness.room.update_one({'_id': str(channel123.id)}, {'$set': {'roommembers': []}}, upsert = True)
        cluster.sweetness.room.update_one({'_id': str(channel123.id)}, {'$set': {'so_owner': []}}, upsert = True)
        cluster.sweetness.room.update_one({'_id': str(channel123.id)}, {'$push': {'roommembers': f'**1) {пользователь.mention} — Владелец**'}}, upsert = True)
        await channel123.set_permissions(new_role, connect = True, view_channel = True)
        await пользователь.add_roles(new_role)

    @room_give.error
    async def room_give_error(self, inter, error):
        if isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed(title = "Выдача комнаты", description = f'{inter.author.mention}, У **Вас** нет на это **разрешения**!', color = 3092790)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            embed.set_author(name = inter.author, icon_url = inter.author.avatar.url)
            await inter.send(embed = embed)
        else: 
            print(error)

    @commands.command()
    async def room(self, inter):
        embed = disnake.Embed(color = 3092790, description = "<:to4kaa:1013180857202258000> Имеешь **большую компанию**, либо просто всегда мечтал иметь свою **личную комнату?** \
                              Тогда у нас есть к тебе **специальное** предложение. \n\nБесплатная личная комната!\n\n\n<:to4kaa:1013180857202258000> Если ты хочешь перейти с друзьями на \
                               **наш сервер**, либо нашёл себе крутых друзей, мыможем создать вам собственную комнату со своей ролью **абсолютно бесплатно!**\n\n \
                              **Для этого тебе необходимо**\n<:to4kaa:1013180857202258000> Иметь 4-6 **активных** пользователей которые будут \
                              поднимать актив\n<:to4kaa:1013180857202258000> Связаться с <@&1123703969663942686>\n<:to4kaa:1013180857202258000> Либо же написать в ⁠🎫・поддержка\n\n \
                               Комната выдаётся на **неограниченное** кол-во дней,при условии актива в ней.")
        await inter.send(embed = embed)

    @commands.slash_command(description = 'Управление личной комнатой')
    async def room_manage(self, inter):
        if cluster.sweetness.roomcheck.count_documents({"_id": str(inter.author.id)}) == 0:
            cluster.sweetness.roomcheck.insert_one({"_id": str(inter.author.id), "room": []})

        if cluster.sweetness.roomcheck.find_one({'_id': str(inter.author.id)})['room'] == []:
            embed = disnake.Embed(description=f'{inter.author.mention}, У **Вас** нет личных комнат, которыми **Вы** можете управлять', color=3092790)
            embed.set_author(name="Выберите комнату для управления", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url=inter.author.display_avatar.url)
            return await inter.send(inter.author.mention, embed=embed)

        idd = 1
        for room in cluster.sweetness.roomcheck.find_one({'_id': str(inter.author.id)})['room']:
            try:
                roleasd[idd] = self.bot.get_channel(int(room)).name
                idd += 1
            except:
                cluster.sweetness.roomcheck.update_one({'_id': str(inter.author.id)}, {'$pull': {'room': int(room)}})

        xd1 = 'Пусто'
        xd2 = 'Пусто'
        xd3 = 'Пусто'
        xd4 = 'Пусто'
        xd5 = 'Пусто'
        room_count = len(cluster.sweetness.roomcheck.find_one({'_id': str(inter.author.id)})['room'])
        if room_count >= 1:
            xd1 = roleasd.get(1, 'Пусто')
        if room_count >= 2:
            xd2 = roleasd.get(2, 'Пусто')
        if room_count >= 3:
            xd3 = roleasd.get(3, 'Пусто')
        if room_count >= 4:
            xd4 = roleasd.get(4, 'Пусто')
        if room_count >= 5:
            xd5 = roleasd.get(5, 'Пусто')

        embed = disnake.Embed(color=3092790, description = f"{inter.author.mention}, **Выберите** комнату для дальнейшего управления.")
        embed.set_author(name="Управление личной комнатой", icon_url = inter.guild.icon.url)
        embed.set_thumbnail(url=inter.author.display_avatar.url)
        await inter.send(inter.author.mention, embed=embed, view=RoomManage(xd1, xd2, xd3, xd4, xd5))
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is not None:
            if after.channel.category_id == 1149816516838166719: 
                await after.channel.set_permissions(member.guild.default_role, view_channel = True, connect = False)

        if before.channel:
            if int(before.channel.category.id) == int(1149816516838166719):
                if len(before.channel.members) == 0:
                    await before.channel.set_permissions(member.guild.default_role, view_channel = False, connect = False)

    @commands.Cog.listener()
    async def on_dropdown(self, inter):
        custom_id = inter.values[0]
        if custom_id[:12] == 'room_members':

            await inter.response.defer()

            channel123 = roombutton[inter.author.id]
            role = disnake.utils.get(inter.guild.roles, id = int(cluster.sweetness.room.find_one({'_id': str(channel123)})['Role']))

            idd = 1
            description = f'### Всего участников в личной комнате: {len(role.members)}\n\n'
            membersID = []
            items_per_page = 10
            for member in role.members:
                membersID.append(member.id)
            pages = [membersID[i:i + items_per_page] for i in range(0, len(membersID), items_per_page)]

            if not str(inter.author.id) in currentRoomMembersPage:
                currentRoomMembersPage[str(inter.author.id)] = 0

            for member_id in pages[currentRoomMembersPage[str(inter.author.id)]]:
                if idd == 1: description += f"**<:11:1096126530247204966> — <@{member_id}>**\n\n"
                if idd == 2: description += f"**<:21:1096126528670138469> — <@{member_id}>**\n\n"
                if idd == 3: description += f"**<:31:1096126525683810465> — <@{member_id}>**\n\n"
                if idd == 4: description += f"**<:41:1096126532826697909> — <@{member_id}>**\n\n"
                if idd == 5: description += f"**<:51:1097534359675879515> — <@{member_id}>**\n\n"
                if idd == 6: description += f"**<:61:1107004738194653246> — <@{member_id}>*\n\n"
                if idd == 7: description += f"**<:71:1107004742326034593> — <@{member_id}>*\n\n"
                if idd == 8: description += f"**<:81:1107004743815008328> — <@{member_id}>*\n\n"
                if idd == 9: description += f"**<:91:1107004746822328350> — <@{member_id}>*\n\n"
                if idd == 10: description += f"**<:101:1107004740723802112> — <@{member_id}>**\n\n"
                idd += 1
                if idd > 10:
                    break

            embed = disnake.Embed(description = description, color = 3092790)
            embed.set_author(name = f"Участники комнаты {role.name}", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            embed.set_footer(text = f'Запросил(а) {inter.author}', icon_url = inter.author.display_avatar.url)
            return await inter.message.edit(content = inter.author.mention, embed = embed, view = RoomMembers(inter.author.id))

        if custom_id[:4] == 'room':

            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
                embed.set_author(name = "Управление личной комнатой", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            
            if custom_id == 'room_top':
                embed = disnake.Embed(title = 'Топы', description = f'{inter.author.mention}, Выберите топ, который вы хотите посмотреть ', color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                await inter.response.edit_message(embed = embed, view = TopListRooms())

            if custom_id == 'room_shop':
                embed = disnake.Embed(color = 3092790, title = 'Личные Комнаты Магазин')
                embed.add_field(name = '1) Добавить текстовый канал', value = '**Цена:** 2000 <:amitobal:1158567849707716708>', inline = False)
                embed.add_field(name = '2) Изменить цвет', value = '**Цена:** 2000 <:amitobal:1158567849707716708>', inline = False)
                embed.add_field(name = '3) Изменить название', value = '**Цена:** 2000 <:amitobal:1158567849707716708>', inline = False)
                embed.add_field(name = '4) Добавить/Изменить иконку', value = '**Цена:** 5000 <:amitobal:1158567849707716708>', inline = False)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_footer(text = f'Запросил(а) {inter.author}', icon_url = inter.author.display_avatar.url)
                return await inter.response.edit_message(embed = embed, view = RoomShop())
            
            if custom_id == 'room_delete':
                embed = disnake.Embed(title = 'Удалить комнату', description = f'{inter.author.mention}, **Вы уверены**, что Вы хотите **Удалить комнату**?', color = 3092790)
                return await inter.response.edit_message(embed = embed, view = RoomYesDelete())
            
            if custom_id == 'room_info':
                channel123 = roombutton[inter.author.id]
                if cluster.sweetness.roomweek.count_documents({"_id": str(channel123)}) == 0: 
                    cluster.sweetness.roomweek.insert_one({"_id": str(channel123), "day": 0})
                room_members = cluster.sweetness.room.find_one({'_id': str(channel123)})['roommembers']
                room_role = cluster.sweetness.room.find_one({'_id': str(channel123)})['Role']
                room = self.bot.get_channel(int(cluster.sweetness.room.find_one({"_id": str(inter.author.id)})["Room"]))
                N = cluster.sweetness.roomweek.find_one({"_id": str(channel123)})["day"]
                room_members = cluster.sweetness.room.find_one({'_id': str(channel123)})['roommembers']
                textchannel = cluster.sweetness.room.find_one({'_id': str(channel123)})['textchannel']
                if not textchannel == 'Отсутствует':
                    text_channel = f"<#{textchannel}>"
                else:
                    text_channel = f"Отсутствует"
                embed = disnake.Embed(color = 3092790, description = f"**> Владелец: <@{cluster.sweetness.room.find_one({'_id': str(channel123)})['owner']}>\n> Роль: <@&{room_role}>\n> Текстовый канал: {text_channel}**\n")
                embed.set_author(name = f"Профиль комнаты {room.name}", icon_url = inter.guild.icon.url)
                embed.set_footer(text = f"Запросил(а) {inter.author}", icon_url = inter.author.display_avatar.url)
                embed.add_field(name = '> <:to4ka:1080888733139746856> Общий онлайн', value = f'```{N // hour}ч. {(N - (N // hour * hour)) // 60}м. {N - ((N // hour * hour) + ((N - (N // hour * hour)) // 60 * min))}с.```')
                embed.add_field(name = '> <:to4ka:1080888733139746856> Создана', value = f'```{cluster.sweetness.room.find_one({"_id": str(channel123)})["Data"]}```')
                embed.add_field(name = '> <:to4ka:1080888733139746856> Участников', value = f'```{len(room_members)}```')
                embed.add_field(name = '> <:to4ka:1080888733139746856> Общий банк', value = f"```{cluster.sweetness.room.find_one({'_id': str(channel123)})['balance']}```")
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                if len(cluster.sweetness.room.find_one({'_id': str(channel123)})['so_owner']) == 0:
                    embed.add_field(name = '> <:to4ka:1080888733139746856>СоВладельцы', value = f'```Пусто```')
                else:
                    members = ' '.join([inter.guild.get_member(i).mention for i in cluster.sweetness.room.find_one({'_id': str(channel123)})['so_owner'] if inter.guild.get_member(i)])
                    embed.add_field(name = '> <:to4ka:1080888733139746856> СоВладельцы', value = f'{members}')            
                await inter.response.edit_message(embed = embed, view = RoomManageBack())

            if custom_id == 'back_room':
                
                if cluster.sweetness.roomcheck.count_documents({"_id": str(inter.author.id)}) == 0:
                    cluster.sweetness.roomcheck.insert_one({"_id": str(inter.author.id), "room": []})
        
                if cluster.sweetness.roomcheck.find_one({'_id': str(inter.author.id)})['room'] == []:
                    embed = disnake.Embed(description='У **Вас** нет личных комнат, которыми **Вы** можете управлять', color=3092790)
                    embed.set_author(name="Выберите комнату для управления", icon_url = inter.guild.icon.url)
                    embed.set_thumbnail(url=inter.author.display_avatar.url)
                    return await inter.response.edit_message(inter.author.mention, embed=embed)
        
                idd = 1
                for room in cluster.sweetness.roomcheck.find_one({'_id': str(inter.author.id)})['room']:
                    try:
                        roleasd[idd] = self.bot.get_channel(int(room)).name
                        idd += 1
                    except:
                        cluster.sweetness.roomcheck.update_one({'_id': str(inter.author.id)}, {'$pull': {'room': int(room)}})
                        
                xd1 = 'Пусто'
                xd2 = 'Пусто'
                xd3 = 'Пусто'
                xd4 = 'Пусто'
                xd5 = 'Пусто'
                room_count = len(cluster.sweetness.roomcheck.find_one({'_id': str(inter.author.id)})['room'])
                if room_count >= 1:
                    xd1 = roleasd.get(1, 'Пусто')
                if room_count >= 2:
                    xd2 = roleasd.get(2, 'Пусто')
                if room_count >= 3:
                    xd3 = roleasd.get(3, 'Пусто')
                if room_count >= 4:
                    xd4 = roleasd.get(4, 'Пусто')
                if room_count >= 5:
                    xd5 = roleasd.get(5, 'Пусто')
        
                embed = disnake.Embed(color=3092790)
                embed.set_author(name="Выберите комнату для управления", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url=inter.author.display_avatar.url)
                await inter.response.edit_message(embed=embed, view=RoomManage(xd1, xd2, xd3, xd4, xd5))

            if custom_id == 'room_del':
                await inter.response.send_modal(title=f"Снять доступ", custom_id = "snyat_room_permissions",components=[disnake.ui.TextInput(label="Айди участника",placeholder="Например: 849353684249083914",custom_id = "Айди участника",style=disnake.TextInputStyle.short, max_length=20)])
            if custom_id == 'room_owner':
                await inter.response.send_modal(title=f"Выдать совладельца", custom_id = "vidat_so_owner",components=[disnake.ui.TextInput(label="Айди участника",placeholder="Например: 849353684249083914",custom_id = "Айди участника",style=disnake.TextInputStyle.short, max_length=20)])
            if custom_id == 'room_delowner':
                await inter.response.send_modal(title=f"Забрать совладельца", custom_id = "zabrat_so_owner",components=[disnake.ui.TextInput(label="Айди участника",placeholder="Например: 849353684249083914",custom_id = "Айди участника",style=disnake.TextInputStyle.short, max_length=20)])
            if custom_id == 'room_give_owner':
                await inter.response.send_modal(title=f"Передать владельца", custom_id = "give_owner",components=[disnake.ui.TextInput(label="Айди участника",placeholder="Например: 849353684249083914",custom_id = "Айди участника",style=disnake.TextInputStyle.short, max_length=20)])
            if custom_id == 'room_otmena':
                await inter.message.delete()
            if custom_id == 'room_pay':
                await inter.response.send_modal(title=f"Пополнить комнату", custom_id = "pay_room",components=[disnake.ui.TextInput(label="Сумма",placeholder="Например: 1000",custom_id = "Сумма",style=disnake.TextInputStyle.short, max_length=25)])
            if custom_id == 'room_give':
                embed = disnake.Embed(title = 'Личная комната', description = f'{inter.author.mention}, **Выберите как вы хотите выдать доступ пользователю**', color = 3092790)
                await inter.response.edit_message(embed = embed, view = VidatDostyp())

        if custom_id[:11] == "leaderboard":

            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(title = f'Топ рум', description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            
            description = ""
            if custom_id == 'leaderboard_balance_rooms':
                with open('room_balance.json', 'r') as f:
                    time_room = json.load(f)

                top_users = {k: v for k, v in sorted(time_room[str(roombutton[inter.author.id])].items(), key=lambda item: item[1], reverse=True)}
                idd = 1
                for postion, user in enumerate(top_users):
                    if idd == 1: description += f"**<:1_:1091732820768075860> — <@{user}>** <:amitobal:1158567849707716708> **{time_room[str(roombutton[inter.author.id])][str(user)]}** \n\n"
                    if idd == 2: description += f"**<:2_:1091732822449987654> — <@{user}>** <:amitobal:1158567849707716708> **{time_room[str(roombutton[inter.author.id])][str(user)]}** \n\n"
                    if idd == 3: description += f"**<:3_:1091732824823959583> — <@{user}>** <:amitobal:1158567849707716708> **{time_room[str(roombutton[inter.author.id])][str(user)]}** \n\n"
                    if idd == 4: description += f"**<:4_:1091732828028411944> — <@{user}>** <:amitobal:1158567849707716708> **{time_room[str(roombutton[inter.author.id])][str(user)]}** \n\n"
                    if idd == 5: description += f"**<:5_:1091732829211214030> — <@{user}>** <:amitobal:1158567849707716708> **{time_room[str(roombutton[inter.author.id])][str(user)]}** \n\n"
                    if idd == 6: description += f"**<:6_:1091732831069282325> — <@{user}>** <:amitobal:1158567849707716708> **{time_room[str(roombutton[inter.author.id])][str(user)]}** \n\n"
                    if idd == 7: description += f"**<:7_:1091732832851857481> — <@{user}>** <:amitobal:1158567849707716708> **{time_room[str(roombutton[inter.author.id])][str(user)]}** \n\n"
                    if idd == 8: description += f"**<:8_:1091732834563141653> — <@{user}>** <:amitobal:1158567849707716708> **{time_room[str(roombutton[inter.author.id])][str(user)]}** \n\n"
                    if idd == 9: description += f"**<:9_:1091732835863363634> — <@{user}>** <:amitobal:1158567849707716708> **{time_room[str(roombutton[inter.author.id])][str(user)]}** \n\n"
                    if idd == 10:description += f"**<:10:1091732838023434241> — <@{user}>** <:amitobal:1158567849707716708> **{time_room[str(roombutton[inter.author.id])][str(user)]}** \n\n"
                    idd += 1
                    if idd > 10:
                        break
                    
                embed = disnake.Embed(description=description, color = 3092790)
                embed.set_author(name = "Топ по вносу баланса в Личной Комнате | За все время", icon_url = inter.guild.icon.url)
                embed.set_image(url = 'https://cdn.discordapp.com/attachments/877327839022710894/974414791504429086/222.png')
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                await inter.response.edit_message(embed = embed, view = TopListRooms())

            if custom_id == 'leaderboard_voice_rooms':
                with open('room_balance_online.json', 'r') as f:
                    time_room_online = json.load(f)

                if not str(roombutton[inter.author.id]) in time_room_online:
                    time_room_online[str(roombutton[inter.author.id])] = {}
                    with open('room_balance_online.json','w') as f: 
                        json.dump(time_room_online,f)

                top_users = {k: v for k, v in sorted(time_room_online[str(roombutton[inter.author.id])].items(), key=lambda item: item[1], reverse=True)}
                idd = 1
                for postion, user in enumerate(top_users):
                    N = time_room_online[str(roombutton[inter.author.id])][str(user)]
                    if idd == 1: description += f"**<:1_:1091732820768075860> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    if idd == 2: description += f"**<:2_:1091732822449987654> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    if idd == 3: description += f"**<:3_:1091732824823959583> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    if idd == 4: description += f"**<:4_:1091732828028411944> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    if idd == 5: description += f"**<:5_:1091732829211214030> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    if idd == 6: description += f"**<:6_:1091732831069282325> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    if idd == 7: description += f"**<:7_:1091732832851857481> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    if idd == 8: description += f"**<:8_:1091732834563141653> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    if idd == 9: description += f"**<:9_:1091732835863363634> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    if idd == 10:description += f"**<:10:1091732838023434241> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    idd += 1
                    if idd > 10:
                        break

                embed = disnake.Embed(description=description, color = 3092790)
                embed.set_author(name = "Топ по онлайну в Личной Комнате | За все время", icon_url = inter.guild.icon.url)
                embed.set_image(url = 'https://cdn.discordapp.com/attachments/877327839022710894/974414791504429086/222.png').set_thumbnail(url = inter.author.display_avatar.url)
                await inter.response.edit_message(embed = embed, view = TopListRoomsView())

    @commands.Cog.listener()
    async def on_button_click(self, inter):

        custom_id = inter.component.custom_id

        if custom_id[:12] == 'room_members':
            
            await inter.response.defer()

            channel123 = roombutton[inter.author.id]
            role = disnake.utils.get(inter.guild.roles, id = int(cluster.sweetness.room.find_one({'_id': str(channel123)})['Role']))

            idd = 1
            description = f'### Всего участников в личной комнате: {len(role.members)}\n\n'
            membersID = []
            items_per_page = 10

            for member in role.members:
                membersID.append(member.id)

            pages = [membersID[i:i + items_per_page] for i in range(0, len(membersID), items_per_page)]

            if not str(inter.author.id) in currentRoomMembersPage:
                currentRoomMembersPage[str(inter.author.id)] = 0

            if custom_id == 'room_members_first_page':
                currentRoomMembersPage[str(inter.author.id)] = 0
            if custom_id == 'room_members_prev_page':
                if currentRoomMembersPage[str(inter.author.id)] > 0:
                    currentRoomMembersPage[str(inter.author.id)] -= 1
            if custom_id == 'room_members_exit':
                return await inter.message.delete()
            if custom_id == 'room_members_right_page':
                if currentRoomMembersPage[str(inter.author.id)] < len(pages) - 1:
                    currentRoomMembersPage[str(inter.author.id)] += 1
            if custom_id == 'room_members_last_page':
                currentRoomMembersPage[str(inter.author.id)] = len(pages) - 1

            for member_id in pages[currentRoomMembersPage[str(inter.author.id)]]:
                if idd == 1: description += f"**<:11:1096126530247204966> — <@{member_id}>**\n\n"
                if idd == 2: description += f"**<:21:1096126528670138469> — <@{member_id}>**\n\n"
                if idd == 3: description += f"**<:31:1096126525683810465> — <@{member_id}>**\n\n"
                if idd == 4: description += f"**<:41:1096126532826697909> — <@{member_id}>**\n\n"
                if idd == 5: description += f"**<:51:1097534359675879515> — <@{member_id}>**\n\n"
                if idd == 6: description += f"**<:61:1107004738194653246> — <@{member_id}>*\n\n"
                if idd == 7: description += f"**<:71:1107004742326034593> — <@{member_id}>*\n\n"
                if idd == 8: description += f"**<:81:1107004743815008328> — <@{member_id}>*\n\n"
                if idd == 9: description += f"**<:91:1107004746822328350> — <@{member_id}>*\n\n"
                if idd == 10: description += f"**<:101:1107004740723802112> — <@{member_id}>**\n\n"
                idd += 1
                if idd > 10:
                    break

            embed = disnake.Embed(description = description, color = 3092790)
            embed.set_author(name = f"Участники комнаты {role.name}", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            embed.set_footer(text = f'Запросил(а) {inter.author}', icon_url = inter.author.display_avatar.url)
            return await inter.message.edit(content = inter.author.mention, embed = embed, view = RoomMembers(inter.author.id))

        if custom_id == 'back_room':
            if cluster.sweetness.roomcheck.find_one({'_id': str(inter.author.id)})['room'] == []:
                embed = disnake.Embed(title = 'Выберите комнату для управления', description = 'У **Вас** нет личных комнат, которыми **Вы** можете управлять', color = 3092790).set_thumbnail(url=inter.author.display_avatar.url)
                return await inter.response.edit_message(embed = embed)
            idd = 1
            for room in cluster.sweetness.roomcheck.find_one({'_id': str(inter.author.id)})['room']:
                roleasd[idd] = self.bot.get_channel(int(room)).name
                idd += 1
            xd1 = 'Пусто'
            xd2 = 'Пусто'
            xd3 = 'Пусто'
            xd4 = 'Пусто'
            xd5 = 'Пусто'

            if len(cluster.sweetness.roomcheck.find_one({'_id': str(inter.author.id)})['room']) == 1: 
                xd1 = roleasd[1]

            if len(cluster.sweetness.roomcheck.find_one({'_id': str(inter.author.id)})['room']) == 2: 
                xd1 = roleasd[1]
                xd2 = roleasd[2]

            if len(cluster.sweetness.roomcheck.find_one({'_id': str(inter.author.id)})['room']) == 3: 
                xd1 = roleasd[1]
                xd2 = roleasd[2]
                xd3 = roleasd[3]

            if len(cluster.sweetness.roomcheck.find_one({'_id': str(inter.author.id)})['room']) == 4:
                xd1 = roleasd[1]
                xd2 = roleasd[2]
                xd3 = roleasd[3]
                xd4 = roleasd[4]

            if len(cluster.sweetness.roomcheck.find_one({'_id': str(inter.author.id)})['room']) == 5: 
                xd1 = roleasd[1]
                xd2 = roleasd[2]
                xd3 = roleasd[3]
                xd4 = roleasd[4]
                xd5 = roleasd[5]

            embed = disnake.Embed( title = 'Выберите комнату для управления', color = 3092790).set_thumbnail(url = inter.author.display_avatar.url)
            await inter.response.edit_message(embed = embed, view = RoomManage(xd1, xd2, xd3, xd4, xd5))

        if custom_id == 'room_delete_yes':
            channel123 = roombutton[inter.author.id]

            room_role = cluster.sweetness.room.find_one({'_id': str(channel123)})['Role']
            await disnake.utils.get(inter.guild.roles, id = int(room_role)).delete()

            cluster.sweetness.roomcheck.update_one({'_id': str(inter.author.id)}, {'$pull': {'room': int(channel123)}})

            await self.bot.get_channel(int(channel123)).delete()

            cluster.sweetness.room.delete_one({'_id': str(inter.author.id)})
            cluster.sweetness.roomweek.delete_one({'_id': str(channel123)})

            embed = disnake.Embed(title = 'Удаление комнаты', description = '**Вы** успешно удалили комнату!', color = disnake.Color.green())
            embed.set_footer(text = inter.author,icon_url = inter.author.display_avatar.url)
            return await inter.response.edit_message(embed = embed, components = [])

        if custom_id == 'top_voice_rooms_week':
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(title = f'Топ рум', description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)

            with open('room_balance_online_week.json', 'r') as f:
                time_room_online = json.load(f)

            if not str(roombutton[inter.author.id]) in time_room_online:
                time_room_online[str(roombutton[inter.author.id])] = {}
                with open('room_balance_online_week.json','w') as f:
                    json.dump(time_room_online,f)

            top_users = {k: v for k, v in sorted(time_room_online[str(roombutton[inter.author.id])].items(), key=lambda item: item[1], reverse=True)}
            idd = 1
            description = ''
            for postion, user in enumerate(top_users):
                try:
                    N = time_room_online[str(roombutton[inter.author.id])][str(user)]
                    if idd == 1: description += f"**<:1_:1091732820768075860> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    if idd == 2: description += f"**<:2_:1091732822449987654> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    if idd == 3: description += f"**<:3_:1091732824823959583> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    if idd == 4: description += f"**<:4_:1091732828028411944> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    if idd == 5: description += f"**<:5_:1091732829211214030> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    if idd == 6: description += f"**<:6_:1091732831069282325> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    if idd == 7: description += f"**<:7_:1091732832851857481> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    if idd == 8: description += f"**<:8_:1091732834563141653> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    if idd == 9: description += f"**<:9_:1091732835863363634> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    if idd == 10 : description += f"**<:10:1091732838023434241> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    idd += 1
                    if idd > 10: 
                        embed = disnake.Embed(description = description, title="<:clock:1091777604941529089> Топ по онлайну в личной комнате | За неделю", color = 3092790).set_image(url = 'https://cdn.discordapp.com/attachments/877327839022710894/974414791504429086/222.png').set_thumbnail(url = inter.author.display_avatar.url)
                        return await inter.response.edit_message(embed = embed, view = TopListRoomsView())
                except:
                    pass
            embed = disnake.Embed(description = description, title="<:clock:1091777604941529089> Топ по онлайну в личной комнате | За неделю", color = 3092790).set_image(url = 'https://cdn.discordapp.com/attachments/877327839022710894/974414791504429086/222.png').set_thumbnail(url = inter.author.display_avatar.url)
            await inter.response.edit_message(embed = embed, view = TopListRoomsView())

        if custom_id == 'top_voice_rooms':
            if not inter.message.content == inter.author.mention:
                return await inter.send(ephemeral = True, embed = disnake.Embed(title = f'Топ рум', description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790).set_thumbnail(url = inter.author.display_avatar.url))
            

            with open('room_balance_online.json', 'r') as f:
                time_room_online = json.load(f)

            if not str(roombutton[inter.author.id]) in time_room_online:
                time_room_online[str(roombutton[inter.author.id])] = {}
                with open('room_balance_online.json','w') as f: 
                    json.dump(time_room_online,f)

            top_users = {k: v for k, v in sorted(time_room_online[str(roombutton[inter.author.id])].items(), key=lambda item: item[1], reverse=True)}
            idd = 1
            description = ''
            for postion, user in enumerate(top_users):
                N = time_room_online[str(roombutton[inter.author.id])][str(user)]
                if idd == 1: description += f"**<:1_:1091732820768075860> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                if idd == 2: description += f"**<:2_:1091732822449987654> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                if idd == 3: description += f"**<:3_:1091732824823959583> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                if idd == 4: description += f"**<:4_:1091732828028411944> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                if idd == 5: description += f"**<:5_:1091732829211214030> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                if idd == 6: description += f"**<:6_:1091732831069282325> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                if idd == 7: description += f"**<:7_:1091732832851857481> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                if idd == 8: description += f"**<:8_:1091732834563141653> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                if idd == 9: description += f"**<:9_:1091732835863363634> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                if idd == 10 : description += f"**<:10:1091732838023434241> — <@{user}>** <:clock:1091777604941529089> **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                idd += 1
                if idd > 10: 
                    embed = disnake.Embed(description = description, title="<:clock:1091777604941529089> Топ по онлайну в личной комнате | За все время", color = 3092790).set_image(url = 'https://cdn.discordapp.com/attachments/877327839022710894/974414791504429086/222.png').set_thumbnail(url = inter.author.display_avatar.url)
                    return await inter.response.edit_message(embed = embed, view = TopListRoomsView())
            embed = disnake.Embed(description = description, title="<:clock:1091777604941529089> Топ по онлайну в личной комнате | За все время", color = 3092790).set_image(url = 'https://cdn.discordapp.com/attachments/877327839022710894/974414791504429086/222.png').set_thumbnail(url = inter.author.display_avatar.url)
            await inter.response.edit_message(embed = embed, view = TopListRoomsView())

        if custom_id[:8] == 'yes_room':
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(title = f'Личные Комнаты', description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            member = inter.author
            channel123 = roombutton[inter.author.id]
            cluster.sweetness.room.update_one({'_id': str(channel123)}, {'$push': {'roommembers': f"\n**{len(cluster.sweetness.room.find_one({'_id': str(channel123)})['roommembers']) + 1})** <@{member.id}>"}}, upsert = True)
            if custom_id == 'yes_room':

                room_role = cluster.sweetness.room.find_one({'_id': str(channel123)})['Role']
                await member.add_roles(disnake.utils.get(inter.guild.roles, id = int(room_role)))

                embed = disnake.Embed(description = f'{inter.author.mention}, **Теперь** у **Вас** есть доступ в **комнату** <#{channel123}>', color = 3092790)
                embed.set_author(name = "Управление личной комнатой", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.response.edit_message(embed = embed, components = [])
            if custom_id == 'yes_room1':
                
                channel = disnake.utils.get(inter.guild.channels, id = int(channel123))
                await channel.set_permissions(member, connect = True, view_channel = True)
                try:
                    text_channel = self.bot.get_channel(cluster.sweetness.room.find_one({'_id': str(channel123)})['textchannel'])
                    await text_channel.set_permissions(member, connect = True, view_channel = True)
                except:
                    pass

                embed = disnake.Embed(description = f'{inter.author.mention}, **Теперь** у **Вас** есть доступ в **комнату** <#{channel123}>', color = 3092790)
                embed.set_author(name = "Управление личной комнатой", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.response.edit_message(embed = embed, components = [])
        
        if custom_id == '1room':
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(title = f'Магазин', description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790).set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            roomshop[inter.author.id] = '1'
            
            embed = disnake.Embed(title = 'Магазин', description = f'{inter.author.mention}, **Вы уверены**, что Вы хотите **Добавить текстовый канал** за **2000** <:amitobal:1158567849707716708>?\nДля **согласия** нажмите на <:yes1:1092007373733900348>, для **отказа** на <:back1:1111712230363373700>', color = 3092790)
            return await inter.response.edit_message(embed = embed, view = RoomYesOrNo())
        
        if custom_id == '2room':
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(title = f'Магазин', description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790).set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            roomshop[inter.author.id] = '2'
            
            embed = disnake.Embed(title = 'Магазин', description = f'{inter.author.mention}, **Вы уверены**, что Вы хотите **Изменить цвет** за **2000** <:amitobal:1158567849707716708>?\nДля **согласия** нажмите на <:yes1:1092007373733900348>, для **отказа** на <:back1:1111712230363373700>', color = 3092790)
            return await inter.response.edit_message(embed = embed, view = RoomYesOrNo())
        
        if custom_id == '3room':
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(title = f'Магазин', description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790).set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            roomshop[inter.author.id] = '3'
            
            embed = disnake.Embed(title = 'Магазин', description = f'{inter.author.mention}, **Вы уверены**, что Вы хотите **Изменить название** за **2000** <:amitobal:1158567849707716708>?\nДля **согласия** нажмите на <:yes1:1092007373733900348>, для **отказа** на <:back1:1111712230363373700>', color = 3092790)
            return await inter.response.edit_message(embed = embed, view = RoomYesOrNo())
        
        if custom_id == '4room':
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(title = f'Магазин', description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790).set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            roomshop[inter.author.id] = '4'
            
            embed = disnake.Embed(title = 'Магазин', description = f'{inter.author.mention}, **Вы уверены**, что Вы хотите **Добавить/Изменить иконку** за **5000** <:amitobal:1158567849707716708>?\nДля **согласия** нажмите на <:yes1:1092007373733900348>, для **отказа** на <:back1:1111712230363373700>', color = 3092790)
            return await inter.response.edit_message(embed = embed, view = RoomYesOrNo())
        
        if custom_id == 'yesroomshop':
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(title = f'Купить товар', description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790).set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            if roomshop[inter.author.id] == '1':
                channel123 = roombutton[inter.author.id]
                if int(2000) > int(cluster.sweetness.room.find_one({"_id": str(channel123)})["balance"]):
                    embed = disnake.Embed(title = 'Купить товар', description = f'{inter.author.mention}, На **балансе** комнаты **недостаточно средств**!', color = disnake.Color.red())
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    return await inter.response.edit_message(embed = embed)
                await inter.response.send_modal(title=f"Добавить канал", custom_id = "add_channel",components=[disnake.ui.TextInput(label="Название",placeholder="Например: zxc zxc", custom_id = "Название",style=disnake.TextInputStyle.short, max_length=25)])
            if roomshop[inter.author.id] == '2':
                channel123 = roombutton[inter.author.id]
                if int(2000) > int(cluster.sweetness.room.find_one({"_id": str(channel123)})["balance"]):
                    embed = disnake.Embed(title = 'Купить товар', description = f'{inter.author.mention}, На **балансе** комнаты **недостаточно средств**!', color = disnake.Color.red())
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    return await inter.response.edit_message(embed = embed)
                await inter.response.send_modal(title=f"Изменить цвет", custom_id = "edit_color_room",components=[disnake.ui.TextInput(label="Цвет",placeholder="Например: #00000",custom_id = "Цвет",style=disnake.TextInputStyle.short, max_length=25)])
            if roomshop[inter.author.id] == '3':
                channel123 = roombutton[inter.author.id]
                if int(2000) > int(cluster.sweetness.room.find_one({"_id": str(channel123)})["balance"]):
                    embed = disnake.Embed(title = 'Купить товар', description = f'{inter.author.mention}, На **балансе** комнаты **недостаточно средств**!', color = disnake.Color.red())
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    return await inter.response.edit_message(embed = embed)
                await inter.response.send_modal(title=f"Изменить название", custom_id = "edit_name",components=[disnake.ui.TextInput(label="Название",placeholder="Например: zxc zxc",custom_id = "Название",style=disnake.TextInputStyle.short, max_length=25)])
            if roomshop[inter.author.id] == '4':

                channel123 = roombutton[inter.author.id]
                if int(5000) > int(cluster.sweetness.room.find_one({"_id": str(channel123)})["balance"]):
                    embed = disnake.Embed(title = 'Купить товар', description = f'{inter.author.mention}, На **балансе** комнаты **недостаточно средств**!', color = disnake.Color.red())
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    return await inter.response.edit_message(embed = embed)
                
                embed = disnake.Embed(title = 'Добавить иконку', description = f'{inter.author.mention}, **Скиньте** фотографию в чат, для того чтобы **поставить/изменить** иконку на роли!', color=3092790)
                embed.set_author(name = inter.author, icon_url = inter.author.display_avatar.url)
                await inter.send(embed = embed)

                def check(m):
                    return m.author.id == inter.author.id
                try: 
                    image = await self.bot.wait_for("message", check = check)
                except TimeoutError:
                    return
                
                room_id = cluster.sweetness.room.find_one({'_id': str(channel123)})['Role']
                role = disnake.utils.get(inter.guild.roles, id = int(room_id))

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

                cluster.sweetness.room.update_one({"_id": str(channel123)}, {"$inc": {"balance": -int(5000)}})
                embed = disnake.Embed(title = f"Добавить/Изменить иконку", description = f"{inter.author.mention}, **Вы** успешно добавили/изменили иконку **личной комнаты!**", color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                await inter.send(embed = embed)
        
        
        if custom_id == 'menu_room_manage':

            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
                embed.set_author(name = "Управление личной комнатой", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            
            embed = disnake.Embed(description=f"{inter.author.mention}, **Выберите** что вы хотите настроить", color = 3092790)
            embed.set_author(name = "Управление личной комнатой", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            embed.set_image(url = "https://i.ibb.co/fkPw2Lf/bg23232.png")
            return await inter.response.edit_message(embed = embed, view = RoomManageMain())
        
        if custom_id == 'vidat_1':
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(title = 'Выдать доступ', description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            await inter.response.send_modal(title=f"Выдать доступ",custom_id = "vidat_room_permissions",components=[disnake.ui.TextInput(label="Айди участника",placeholder="Например: 849353684249083914",custom_id = "Айди участника",style=disnake.TextInputStyle.short, max_length=20)])
        if custom_id == 'vidat_2':
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(title = 'Выдать доступ', description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            await inter.response.send_modal(title=f"Выдать доступ",custom_id = "vidat_room_permissions1",components=[disnake.ui.TextInput(label="Айди участника",placeholder="Например: 849353684249083914",custom_id = "Айди участника",style=disnake.TextInputStyle.short, max_length=20)])

        try:
            channel = disnake.utils.get(inter.guild.channels, name = inter.component.label)
            roombutton[inter.author.id] = channel.id
            channel123 = roombutton[inter.author.id]
            room_role = cluster.sweetness.room.find_one({'_id': str(channel123)})['Role']

            with open('room_balance.json', 'r') as f:
                time_room = json.load(f)

            if not str(channel.id) in time_room:
                time_room[str(channel.id)] = {}
                with open('room_balance.json','w') as f: 
                    json.dump(time_room,f)

            embed = disnake.Embed(description=f"{inter.author.mention}, **Выберите** что вы хотите настроить", color = 3092790)
            embed.set_author(name = "Управление личной комнатой", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            embed.set_image(url = "https://i.ibb.co/fkPw2Lf/bg23232.png")
            return await inter.response.edit_message(embed = embed, view = RoomManageMain())
        except:
            pass

    @commands.Cog.listener()
    async def on_modal_submit(self, inter):

        custom_id = inter.custom_id

        if custom_id == 'add_channel':

            for key, value in inter.text_values.items():
                name = value

            channel123 = roombutton[inter.author.id]
            room_role = cluster.sweetness.room.find_one({'_id': str(channel123)})['Role']
            channel5 = await inter.guild.create_text_channel(name = name, category = disnake.utils.get(inter.guild.categories, id = 1124789725107077240))
            await channel5.set_permissions(disnake.utils.get(inter.guild.roles, id = int(room_role)), send_messages=True,view_channel=True)
            await channel5.set_permissions(inter.guild.default_role, send_messages=False, view_channel=False)
            cluster.sweetness.room.update_one({"_id": str(channel123)}, {"$inc": {"balance": -int(2000)}})
            cluster.sweetness.room.update_one({'_id': str(channel123)}, {'$set': {'textchannel': channel5.id}}, upsert = True)
            embed = disnake.Embed(title = 'Купить товар', description = f'{inter.author.mention}, **Вы** успешно **добавили канал** под названием {name}', color = 3092790)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            return await inter.response.edit_message(embed = embed, view = RoomManageBack())

        if custom_id == "edit_color_room":

            for key, value in inter.text_values.items():
                color = value

            channel123 = roombutton[inter.author.id]
            room_role = cluster.sweetness.room.find_one({'_id': str(roombutton[inter.author.id])})['Role']
            await disnake.utils.get(inter.guild.roles, id = int(room_role)).edit(color = disnake.Color(hex_to_rgb(color)))
            cluster.sweetness.room.update_one({"_id": str(channel123)}, {"$inc": {"balance": -int(2000)}})
            embed = disnake.Embed(title = 'Управление личной комнатой', description = f'{inter.author.mention}, **Вы** успешно изменили **цвет роли комнаты!** <#{roombutton[inter.author.id]}>', color = 3092790)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            await inter.response.edit_message(embed = embed, view = RoomManageBack())

        if custom_id == "edit_name":

            for key, value in inter.text_values.items():
                name = value

            await self.bot.get_channel(roombutton[inter.author.id]).edit(name = name)
            room_role = cluster.sweetness.room.find_one({'_id': str(roombutton[inter.author.id])})['Role']
            channel123 = roombutton[inter.author.id]
            cluster.sweetness.room.update_one({"_id": str(channel123)}, {"$inc": {"balance": -int(2000)}})
            await disnake.utils.get(inter.guild.roles, id = int(room_role)).edit(name = name)
            embed = disnake.Embed(title = 'Управление личной комнатой', description = f'{inter.author.mention}, **Вы** успешно изменили **название комнаты** <#{roombutton[inter.author.id]}>', color = 3092790)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            await inter.response.edit_message(embed = embed, view = RoomManageBack())
        if custom_id[:22] == 'vidat_room_permissions':

            for key, value in inter.text_values.items():
                member = disnake.utils.get(inter.guild.members, id = int(value))

            idmessage[inter.message.id] = inter.author.id
            roombutton[member.id] = roombutton[inter.author.id]
            if custom_id == "vidat_room_permissions":

                embed = disnake.Embed(title = 'Управление личной комнатой', color = 3092790, description = f'{inter.author.mention} хочет **Вам** выдать доступ в свою комнату <#{roombutton[inter.author.id]}>, для согласия, воспользуйтесь кнопками ниже')
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                await inter.response.edit_message(content = f'{member.mention}', embed = embed, view = RoomYesNo())

            if custom_id == 'vidat_room_permissions1':

                embed = disnake.Embed(title = 'Управление личной комнатой', color = 3092790, description = f'{inter.author.mention} хочет **Вам** выдать доступ в свою комнату <#{roombutton[inter.author.id]}>, для согласия, воспользуйтесь кнопками ниже')
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                await inter.response.edit_message(content = f'{member.mention}', embed = embed, view = RoomYesNo1())

        if custom_id == "snyat_room_permissions":

            for key, value in inter.text_values.items():
                member = disnake.utils.get(inter.guild.members, id = int(value))

            channel = disnake.utils.get(inter.guild.channels, id = int(roombutton[inter.author.id]))
            room_id = cluster.sweetness.room.find_one({'_id': str(roombutton[inter.author.id])})['Role']
            room_role = disnake.utils.get(inter.guild.roles, id = int(room_id))
            await member.remove_roles(room_role)
            await channel.set_permissions(member, connect = False)
            try:
                await member.move_to(None)
            except:
                pass
            embed = disnake.Embed(title = 'Забрать доступ', color = 3092790, description = f'{inter.author.mention}, **Вы** успешно забрали **доступ** <#{roombutton[inter.author.id]}> пользователю {member.mention}')
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            await inter.response.edit_message(content = f'{member.mention}', embed = embed, view = RoomManageBack())

        if custom_id == "pay_room":
            
            for key, value in inter.text_values.items():
                count = value

            with open('room_balance.json', 'r') as f:
                time_room = json.load(f)
                
            if int(cluster.sweetness.economy.find_one({"_id": str(inter.author.id)})["balance"]) < int(count): 
                embed = disnake.Embed(title = 'Пополнить комнату', description = f'{inter.author.mention}, у **Вас** на балансе недостаточно <:amitobal:1158567849707716708>', color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.response.edit_message(embed = embed, view = RoomManageBack())

            channel123 = roombutton[inter.author.id]
            if not str(inter.author.id) in time_room[str(channel123)]:
                time_room[str(channel123)][str(inter.author.id)] = 0
                with open('room_balance.json','w') as f:
                    json.dump(time_room,f)

            cluster.sweetness.room.update_one({"_id": str(channel123)}, {"$inc": {"balance": +int(count)}})
            cluster.sweetness.room_balance_history.update_one({"_id": str(channel123)}, {"$inc": {"balance": +int(count)}})
            cluster.sweetness.economy.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": -int(count)}})
            time_room[str(channel123)][str(inter.author.id)] += int(count)
            with open('room_balance.json','w') as f: 
                json.dump(time_room,f)

            embed = disnake.Embed(title = 'Управление личной комнатой', description = f'{inter.author.mention}, **Вы** успешно **внесли** {count} <:amitobal:1158567849707716708> на счёт **личной комнаты**', color = 3092790)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            return await inter.response.edit_message(embed = embed, view = RoomManageBack())

        if custom_id == 'vidat_so_owner':

            for key, value in inter.text_values.items():
                member = disnake.utils.get(inter.guild.members, id = int(value))
            embed = disnake.Embed(title = 'Управление личной комнатой', description = f'{inter.author.mention}, **Вы** успешно **выдали совладельца** <@{member.id}>', color = 3092790)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            await inter.response.edit_message(embed = embed, view = RoomManageBack())
            channel123 = self.bot.get_channel(roombutton[inter.author.id])
            idd = len(cluster.sweetness.room.find_one({'_id': str(roombutton[inter.author.id])})['roommembers'])
            cluster.sweetness.room.update_one({'_id': str(member.id)}, {'$set': {'Room': channel123.id}}, upsert = True)
            cluster.sweetness.roomcheck.update_one({'_id': str(member.id)}, {'$push': {'room': int(channel123.id)}}, upsert = True)
            cluster.sweetness.room.update_one({'_id': str(channel123.id)}, {'$push': {'so_owner': int(member.id)}}, upsert = True)
            cluster.sweetness.room.update_one({'_id': str(channel123.id)}, {'$push': {'roommembers': f'\n**{idd + 1}) {member.mention} — СоВладелец**'}}, upsert = True)

        if custom_id == 'zabrat_so_owner':

            for key, value in inter.text_values.items():
                member = disnake.utils.get(inter.guild.members, id = int(value))

            embed = disnake.Embed(title = 'Управление личной комнатой', description = f'{inter.author.mention}, **Вы** успешно **забрали совладельца** у <@{member.id}>', color = 3092790)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            await inter.response.edit_message(embed = embed, view = RoomManageBack())

            channel123 = self.bot.get_channel(roombutton[inter.author.id])
            idd = len(cluster.sweetness.room.find_one({'_id': str(roombutton[inter.author.id])})['roommembers'])
            cluster.sweetness.room.delete_one({'_id': str(member.id)})
            cluster.sweetness.roomcheck.update_one({'_id': str(member.id)}, {'$pull': {'room': int(channel123.id)}}, upsert = True)
            cluster.sweetness.room.update_one({'_id': str(channel123.id)}, {'$pull': {'so_owner': int(member.id)}}, upsert = True)
            cluster.sweetness.room.update_one({'_id': str(channel123.id)}, {'$pull': {'roommembers': f'\n**{idd - 1}) {member.mention} — СоВладелец**'}}, upsert = True)

        if custom_id == "give_owner":

            for key, value in inter.text_values.items():
                member = disnake.utils.get(inter.guild.members, id = int(value))

            embed = disnake.Embed(title = 'Управление личной комнатой', description = f'{inter.author.mention}, **Вы** успешно **передали владельца** <@{member.id}>', color = 3092790)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            await inter.response.edit_message(embed = embed, components = [])

            channel123 = self.bot.get_channel(roombutton[inter.author.id])
            room_role = cluster.sweetness.room.find_one({'_id': str(roombutton[inter.author.id])})['Role']
        
            cluster.sweetness.room.update_one({'_id': str(inter.author.id)}, {'$pull': {'roommembers': f'**1) {inter.author.mention} — Владелец**'}}, upsert = True)

            cluster.sweetness.room.update_one({'_id': str(member.id)}, {'$set': {'Room': channel123.id}}, upsert = True)
            cluster.sweetness.roomcheck.update_one({'_id': str(member.id)}, {'$push': {'room': int(channel123.id)}}, upsert = True)
            cluster.sweetness.room.update_one({'_id': str(channel123.id)}, {'$set': {'owner': int(member.id)}}, upsert = True)
            cluster.sweetness.room.update_one({'_id': str(channel123.id)}, {'$push': {'roommembers': f'\n**1) {member.mention} — Владелец**'}}, upsert = True)
            cluster.sweetness.roomcheck.update_one({'_id': str(inter.author.id)}, {'$pull': {'room': channel123.id}}, upsert = True)
            cluster.sweetness.room.delete_one({'_id': str(inter.author.id)})

def setup(bot):
    bot.add_cog(room_cog(bot))