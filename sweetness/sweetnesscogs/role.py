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

rolebutton = {}
role_shop = {}
hour = 60 * 60
roleyes = {}
idmessage = {}

class RoleAccept(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'accept_icon_role', emoji = '<:accept:1138812685039968337>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Меню', custom_id = 'menu_role', emoji = '<:menu11:1111709626438783036>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Информация о роли', custom_id = 'info_role', emoji = '<:information1:1111712238886191154>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Выход', custom_id = 'exit_profile', emoji = '<:exit_1:1111689838568165437>'))

class RoleYesNo(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'yes_role', emoji = '<:accept:1138812685039968337>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'no_role', emoji = '<:minus:1111704763860529182>'))

class RoleDropdown(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            options = [
                disnake.SelectOption(label="Выдать роль", value = 'vidat_role', emoji = '<:plus:1111704771288645642>'),
                disnake.SelectOption(label="Снять роль", value = 'snyat_role', emoji = '<:minus:1111704763860529182>'),
                disnake.SelectOption(label="Переименовать", value = 'editname_role', emoji = '<:edit:1111701664865464440>'),
                disnake.SelectOption(label="Выставить на продажу", value = 'sell_role', emoji = '<:cart11:1111712234402488360>'),
                disnake.SelectOption(label="Снять с продажи", value = 'buy123_role', emoji = '<:cart11:1111712234402488360>'),
                disnake.SelectOption(label="Изменить цену", value = 'editmoney_role', emoji = '<:edit:1111701664865464440>'),
                disnake.SelectOption(label="Изменить цвет", value = 'editcolor_role', emoji = '<:edit:1111701664865464440>'),
                disnake.SelectOption(label="Иконка", value = 'icon_role', emoji = '<:edit:1111701664865464440>'),
                disnake.SelectOption(label="Продлить", value = 'prodlit_role', emoji = '<:date1:1111712236042457188>'),
                disnake.SelectOption(label="Удалить роль", value = 'delete_role', emoji = '<:mysorka11:1111712241838997574>'),
                disnake.SelectOption(label="Информация о роли", value = 'info_role', emoji = '<:information1:1111712238886191154>'),
                disnake.SelectOption(label="Добавить в чёрный список", value = 'add_black_list_role', emoji = '<:privates3:1109823486907658330>'),
                disnake.SelectOption(label="Удалить из чёрного списка", value = 'remove_black_list_role', emoji = '<:privates4:1109823489508122666>'),
                disnake.SelectOption(label="Передать права", value = 'role_give_owner_role', emoji = '<:privates10:1109823504636985414>'),
                disnake.SelectOption(label="Вернуться к выбору роли", value = 'back_role', emoji = '<:back1:1111712230363373700>'),
                disnake.SelectOption(label="Выход", value = 'exit_role', emoji = '<:exit_1:1111689838568165437>'),
            ],
        )

class RoleManage(disnake.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(RoleDropdown())

class RoleManageBack(disnake.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Вернуться к выбору роли', custom_id = 'back_role', emoji = '<:back1:1111712230363373700>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Меню', custom_id = 'menu_role', emoji = '<:menu11:1111709626438783036>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Информация о роли', custom_id = 'info_role', emoji = '<:information1:1111712238886191154>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Выход', custom_id = 'exit_profile', emoji = '<:exit_1:1111689838568165437>'))

class RoleManageBack1(disnake.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Вернуться к выбору роли', custom_id = 'back_role', emoji = '<:back1:1111712230363373700>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Меню', custom_id = 'menu_role', emoji = '<:menu11:1111709626438783036>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = 'Выход', custom_id = 'exit_profile', emoji = '<:exit_1:1111689838568165437>'))

class RoleManageMenu(disnake.ui.View):

    def __init__(self, guild, id_author):
        super().__init__()
        idd = 1
        self.author_id = id_author
        for role in cluster.sweetness.role.find_one({'_id': str(self.author_id)})['rolemember']:
            try:
                label_role = disnake.utils.get(guild.roles, id = int(role)).name
                idd += 1
                self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = label_role, emoji = '<:dev:1089660500800974919>'))
            except:
                pass

def hex_to_rgb(value):
    value = value.lstrip('#')
    RGB = list(tuple(int(value[i:i + len(value) // 3], 16) for i in range(0, len(value), len(value) // 3)))
    return (RGB[0]<<16) + (RGB[1]<<8) + RGB[2]

class rolecog(commands.Cog):
    def __init__(self, bot: commands.Bot(intents = disnake.Intents.all(), command_prefix = '!')):
        self.bot = bot

    @commands.slash_command(description = 'Создать роль')
    async def role_create(inter, цвет, *, название):
        balance = cluster.sweetness.economy.find_one({"_id": str(inter.author.id)})["balance"]

        for role in inter.guild.roles:
            if role.name == название:
                embed = disnake.Embed(color = 3092790)
                embed.set_author(name = f"Создание личной роли", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.description = f'{inter.author.mention}, Выберите другое **название** для роли, так как роль с таким **названием** уже **есть** на сервере!'
                return await inter.send(embed = embed)

        if cluster.sweetness.role.count_documents({"_id": str(inter.author.id)}) == 0:
            cluster.sweetness.role.insert_one({"_id": str(inter.author.id), "rolemember": []})

        if cluster.sweetness.economy.count_documents({"_id": str(inter.author.id)}) == 0:
            cluster.sweetness.economy.insert_one({"_id": str(inter.author.id), "balance": 0})

        if len(cluster.sweetness.role.find_one({'_id': str(inter.author.id)})['rolemember']) > 4:
            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = f"Создание личной роли", icon_url = inter.guild.icon.url)
            embed.description = f'{inter.author.mention}, Больше **чётырех ролей** нельзя **создать**!'
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            return await inter.send(embed = embed)

        if int(balance) < 10000:
            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = f"Создание личной роли", icon_url = inter.guild.icon.url)
            embed.set_author(name = inter.author, icon_url = inter.author.display_avatar.url)
            embed.description = f'{inter.author.mention}, У **Вас** на балансе **недостаточно средств!**\nНехватает: **{10000 - int(balance)}** <:amitobal:1158567849707716708> '
            return await inter.send(embed = embed)

        try:
            new_role = await inter.guild.create_role(name = название, color = disnake.Color(hex_to_rgb(цвет)), mentionable=True)
        except:
            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = f"Создание личной роли", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            embed.description = '**Ошибка!** Введите цвет роли в **формате: #bbb3f3**'
            return await inter.send(embed = embed)

        role_category = disnake.utils.get(inter.guild.roles, id = 1150608025325949140)
        channelxd = role_category.position

        await new_role.edit(position = int(channelxd) - 1)

        embed = disnake.Embed(color = 3092790)
        embed.set_author(name = f"Создание личной роли", icon_url = inter.guild.icon.url)
        embed.set_thumbnail(url = inter.author.display_avatar.url)
        embed.description = f'{inter.author.mention}, **Вы** успешно **создали роль** под названием **{название}**'
        await inter.send(embed = embed)

        await inter.author.add_roles(new_role)

        cluster.sweetness.economy.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": -int(10000)}})
        cluster.sweetness.history.update_one({"_id": str(inter.author.id)}, {"$inc": {"roles": +int(10000)}})
        cluster.sweetness.role.update_one({'_id': str(inter.author.id)}, {'$push': {'rolemember': new_role.id}}, upsert = True)
        cluster.sweetness.role.update_one({'_id': str(new_role.id)}, {'$set': {'author': inter.author.id}}, upsert = True)
        cluster.sweetness.role.update_one({"_id": str(new_role.id)}, {"$set": {"blacklist": []}})
        cluster.sweetness.role_plata.update_one({'_id': str(new_role.id)}, {'$set': {'time': 2592000}}, upsert = True)
        
        new_date = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(days=30)

        cluster.sweetness.role_plata.update_one({'_id': str(new_role.id)}, {'$set': {'time': new_date}}, upsert = True)
        cluster.sweetness.role_plata.update_one({'_id': str(new_role.id)}, {'$set': {'notification': "No"}}, upsert = True)

    @commands.slash_command(description = 'Управление ролями')
    async def role_manage(inter):
        if cluster.sweetness.role.count_documents({"_id": str(inter.author.id)}) == 0: 
            cluster.sweetness.role.insert_one({"_id": str(inter.author.id), "rolemember": [], "role_time": {}})

        if cluster.sweetness.role.find_one({'_id': str(inter.author.id)})['rolemember'] == []:
            embed = disnake.Embed(description = 'У **Вас** нет личных ролей, которыми **Вы** можете управлять', color = 3092790)
            embed.set_author(name = f'Выберите роль для управления - {inter.author}', icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url=inter.author.display_avatar.url)
            return await inter.send(inter.author.mention, embed = embed)
        
        guild = inter.guild
        id_author = inter.author.id
        embed = disnake.Embed(color = 3092790)
        embed.set_thumbnail(url = inter.author.display_avatar.url)
        embed.set_footer(text = f'Запросил(а) {inter.author}')
        embed.set_author(name = f'Выберите роль для управления - {inter.author}', icon_url = inter.guild.icon.url)
        await inter.send(inter.author.mention, embed = embed, view = RoleManageMenu(guild, id_author))
    
    @commands.Cog.listener()
    async def on_modal_submit(self, inter):
        custom_id = inter.custom_id

        if custom_id == "role_give_owner_role":
            for key, value in inter.text_values.items():
                member = disnake.utils.get(inter.guild.members, id = int(value))

            id_role = rolebutton[inter.author.id]

            cluster.sweetness.role.update_one({'_id': str(member.id)}, {'$push': {'rolemember': id_role}}, upsert = True)
            cluster.sweetness.role.update_one({'_id': str(inter.author.id)}, {'$pull': {'rolemember': id_role}}, upsert = True)

            embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно передали права на роль**{member.mention}**', color = 3092790)
            embed.set_author(name = "Управление личной ролью", icon_url = inter.guild.icon.url)
            await inter.response.edit_message(embed = embed, components = [])

        if custom_id[-10:] == 'rolecreate':
            for key, value in inter.text_values.items():
                value = value

            if inter.custom_id == "edit_color_rolecreate":
                await disnake.utils.get(inter.guild.roles, id = int(rolebutton[inter.author.id])).edit(color = disnake.Color(hex_to_rgb(value)))
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно изменили **цвет роли!**', color = 3092790)
                embed.set_author(name = "Управление личной ролью", icon_url = inter.guild.icon.url)
                return await inter.response.edit_message(embed = embed, view = RoleManageBack())
            
            if inter.custom_id == "edit_name_rolecreate":
                await disnake.utils.get(inter.guild.roles, id = int(rolebutton[inter.author.id])).edit(name = value)
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно изменили **название роли!**', color = 3092790)
                embed.set_author(name = "Управление личной ролью", icon_url = inter.guild.icon.url)
                return await inter.response.edit_message(embed = embed, view = RoleManageBack())
            
            if inter.custom_id == "edit_count_rolecreate":
                cluster.sweetness.role.update_one({'_id': str(rolebutton[inter.author.id])}, {'$set': {'cost': value}}, upsert = True)
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно изменили **цену роли!**', color = 3092790)
                embed.set_author(name = "Управление личной ролью", icon_url = inter.guild.icon.url)
                return await inter.response.edit_message(embed = embed, view = RoleManageBack())
        
        if custom_id[-10:] == 'roletarget':
            for key, value in inter.text_values.items():
                member = disnake.utils.get(inter.guild.members, id = int(value))

            if inter.custom_id == "add_black_list_roletarget":
                cluster.sweetness.role.update_one({'_id': str(rolebutton[inter.author.id])}, {'$push': {'blacklist': int(member.id)}}, upsert = True)
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно добавили **{member.mention}** в **чёрный список**', color = 3092790)
                embed.set_author(name = "Управление личной ролью", icon_url = inter.guild.icon.url)
                await inter.response.edit_message(embed = embed, view = RoleManageBack())
            
            if inter.custom_id == "remove_black_list_roletarget":
                cluster.sweetness.role.update_one({'_id': str(rolebutton[inter.author.id])}, {'$pull': {'blacklist': int(member.id)}}, upsert = True)
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно удалили **{member.mention}** из **чёрного списка**', color = 3092790)
                embed.set_author(name = "Управление личной ролью", icon_url = inter.guild.icon.url)
                await inter.response.edit_message(embed = embed, view = RoleManageBack())
            
            if inter.custom_id == "vidat_role_roletarget":
                idmessage[inter.message.id] = inter.author.id
                rolebutton[member.id] = rolebutton[inter.author.id]
                embed = disnake.Embed(description = f'{inter.author.mention} хочет **Вам** выдать роль <@&{rolebutton[inter.author.id]}>, для согласия, воспользуйтесь кнопками ниже', color = 3092790)
                embed.set_author(name = "Управление личной ролью", icon_url = inter.guild.icon.url)
                await inter.response.edit_message(content = f'{member.mention}', embed = embed, view = RoleYesNo())
            
            if inter.custom_id == "snyat_role_roletarget":
                await member.remove_roles(disnake.utils.get(inter.guild.roles, id = int(rolebutton[inter.author.id])))
                embed = disnake.Embed(color = 3092790, description = f'{inter.author.mention}, **Вы** успешно **сняли роль** <@&{rolebutton[inter.author.id]}> пользователю {member.mention}')
                embed.set_author(name = f"Снять роль", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.avatar.url)
                await inter.response.edit_message(embed = embed, view = RoleManageBack())
    
    @commands.Cog.listener()
    async def on_dropdown(self, inter):

        custom_id = inter.values[0]

        if custom_id[-4:] == 'role':
            
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description = f"{inter.author.mention}, **Вы** не можете управлять **чужими кнопками!**", color = 3092790)
                embed.set_author(name = "Управление личною ролью", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            role = disnake.utils.get(inter.guild.roles, id = int(rolebutton[inter.author.id]))
            if custom_id[-9:] == 'icon_role':
                
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы уверены**, что Вы хотите **Добавить/Изменить иконку** за **5000** <:amitobal:1158567849707716708>? \
                                      \nДля **согласия** нажмите на <:accept:1138812685039968337>, для **отказа** на <:back1:1111712230363373700>', color = 3092790)
                embed.set_author(name = f"Добавить/Изменить иконку", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.response.edit_message(embed = embed, view = RoleAccept())

            if custom_id == "exit_role":
                await inter.message.delete()

            if custom_id == 'role_give_owner_role':
                await inter.response.send_modal(title=f"Передать права", custom_id = "role_give_owner_role",components=[disnake.ui.TextInput(label="Айди участника",
                                                placeholder="Например: 849353684249083914",custom_id = "Айди участника",style=disnake.TextInputStyle.short, max_length=20)])

            if custom_id == 'back_role':
                if cluster.sweetness.role.count_documents({"_id": str(inter.author.id)}) == 0: 
                    cluster.sweetness.role.insert_one({"_id": str(inter.author.id), "rolemember": [], "role_time": {}})

                if cluster.sweetness.role.find_one({'_id': str(inter.author.id)})['rolemember'] == []:
                    embed = disnake.Embed(description = 'У **Вас** нет личных ролей, которыми **Вы** можете управлять', color = 3092790)
                    embed.set_author(name = "Выберите роль для управления", icon_url = inter.guild.icon.url)
                    embed.set_thumbnail(url=inter.author.display_avatar.url)
                    return await inter.send(inter.author.mention, embed = embed)

                guild = inter.guild
                id_author = inter.author.id

                embed = disnake.Embed(color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_footer(text = f'Запросил(а) {inter.author}')
                embed.set_author(name = "Выберите роль для управления", icon_url = inter.guild.icon.url)
                return await inter.response.edit_message(embed = embed, view = RoleManageMenu(guild, id_author))

            if custom_id == 'sell_role':
                if role.id in cluster.sweetness.role.find_one({'_id': 1230})['roleshop']:
                    embed = disnake.Embed(description = f'{inter.author.mention}, у **Вас** роль и так выставлена на продажу.', color = 3092790)
                    embed.set_author(name = f'Управление личной ролью - {inter.author}', icon_url = inter.guild.icon.url)
                    return await inter.response.edit_message(embed = embed, view=RoleManageBack())
                
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно выставили роль <@&{role.id}> на **аукцион**, её стоимость **500** <:amitobal:1158567849707716708> , **если** Вы хотите **изменить цену**, воспользуйтесь кнопкой "**изменить цену**"', color = 3092790)
                embed.set_author(name = f'Управление личной ролью - {inter.author}', icon_url = inter.guild.icon.url)
                await inter.response.edit_message(embed = embed, view=RoleManageBack())

                cluster.sweetness.role.update_one({'_id': 1230}, {'$push': {'roleshop': int(role.id)}}, upsert = True)
                cluster.sweetness.role.update_one({'_id': str(role.id)}, {'$set': {'cost': 500}}, upsert = True)
                cluster.sweetness.role.update_one({'_id': str(role.id)}, {'$set': {'buy': 0}}, upsert = True)

            if custom_id == 'prodlit_role':

                if cluster.sweetness.economy.find_one({'_id': str(inter.author.id)})['balance'] < 1500:
                    embed = disnake.Embed(description = f'{inter.author.mention}, У **Вас** на балансе **недостаточно средств**', color = 3092790)
                    embed.set_author(name = "Продлить роль", icon_url = inter.guild.icon.url)
                    embed.set_thumbnail(url = inter.author.avatar.url)
                    return await inter.send(embed = embed, view = RoleManageBack())

                role = rolebutton[inter.author.id]
                new_date = cluster.sweetness.role_plata.find_one({'_id': str(role)})['time'] + datetime.timedelta(days=30)

                cluster.sweetness.economy.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": -int(1500)}})

                cluster.sweetness.role_plata.update_one({'_id': str(role)}, {'$set': {'time': new_date}}, upsert = True)
                cluster.sweetness.role_plata.update_one({'_id': str(role)}, {'$set': {'notification': "No"}}, upsert = True)

                embed = disnake.Embed(description = f'> {inter.author.mention}, **Вы** успешно продлили роль **<@&{role}>**', color = 3092790)
                embed.set_thumbnail(url = inter.author.avatar.url)
                embed.set_author(name = "Продлить роль", icon_url = inter.guild.icon.url)
                await inter.response.edit_message(embed = embed, view = RoleManageBack())
                
            if custom_id == 'add_black_list_role':
                await inter.response.send_modal(title=f"Добавить в ЧС", custom_id = "add_black_list_roletarget",components=[disnake.ui.TextInput(label="Айди участника",
                placeholder="Например: 849353684249083914",custom_id = "Айди участника",style=disnake.TextInputStyle.short, max_length=20)])
            
            if custom_id == 'remove_black_list_role':
                await inter.response.send_modal(title=f"Удалить из ЧС", custom_id = "remove_black_list_roletarget",components=[disnake.ui.TextInput(label="Айди участника",
                placeholder="Например: 849353684249083914",custom_id = "Айди участника",style=disnake.TextInputStyle.short, max_length=20)])

            if custom_id == 'buy123_role':

                cluster.sweetness.role.removeIdDemo.find({},{'_id': str(rolebutton[inter.author.id])})
                cluster.sweetness.role.update_one({'_id': 1230}, {'$pull': {'roleshop': rolebutton[inter.author.id]}}, upsert = True)

                embed = disnake.Embed(color = 3092790)
                embed.set_author(name = "Управление личной ролью", icon_url = inter.guild.icon.url)
                embed.description = f'{inter.author.mention}, **Вы** успешно сняли с продажи роль <@&{rolebutton[inter.author.id]}>'
                await inter.response.edit_message(embed = embed, view = RoleManageBack())

            if custom_id == 'editcolor_role':
                await inter.response.send_modal(title=f"Изменить цвет", custom_id = "edit_color_rolecreate", components=[
                    disnake.ui.TextInput(label="Цвет",placeholder="Например: #00000",custom_id = "Цвет",style=disnake.TextInputStyle.short, max_length=20)])
                
            if custom_id == 'editname_role':
                await inter.response.send_modal(title=f"Переименовать роль", custom_id = "edit_name_rolecreate", components=[
                    disnake.ui.TextInput(label="Название",placeholder="Например: zxc zxc",custom_id = "Название",style=disnake.TextInputStyle.short, max_length=45)])
                
            if custom_id == 'snyat_role':
                await inter.response.send_modal(title=f"Снять роль", custom_id = "snyat_role_roletarget", components=[
                    disnake.ui.TextInput(label="Айди участника",placeholder="Например: 849353684249083914",custom_id = "Айди участника",style=disnake.TextInputStyle.short, max_length=20)])
                
            if custom_id == 'vidat_role':
                await inter.response.send_modal(title=f"Выдать роль", custom_id = "vidat_role_roletarget", components=[
                    disnake.ui.TextInput(label="Айди участника",placeholder="Например: 849353684249083914",custom_id = "Айди участника",style=disnake.TextInputStyle.short, max_length=20)])
                
            if custom_id == 'editmoney_role':
                await inter.response.send_modal(title=f"Новая цена", custom_id = "edit_count_rolecreate", components=[
                    disnake.ui.TextInput(label="Цена",placeholder="Например: 1000",custom_id = "Цена",style=disnake.TextInputStyle.short, max_length=6)])
                
            if custom_id == 'delete_role':
                try:
                    cluster.sweetness.role.delete_one({'_id': str(role.id)})
                    cluster.sweetness.role.update_one({'_id': 1230}, {'$pull': {'roleshop': role.id}}, upsert = True)
                except: 
                    pass

                cluster.sweetness.role.update_one({'_id': str(inter.author.id)}, {'$pull': {'rolemember': role.id}}, upsert = True)
                await disnake.utils.get(inter.guild.roles, id = int(rolebutton[inter.author.id])).delete()

                embed = disnake.Embed(description = '**Вы** успешно удалили роль!', color = 3092790)
                embed.set_author(name = "Управление личной ролью", icon_url = inter.guild.icon.url)
                embed.set_footer(text = inter.author,icon_url = inter.author.display_avatar.url)
                return await inter.response.edit_message(embed = embed, components = [])

            if custom_id == 'info_role':
                count = 0
                owner = f'{inter.author.mention}'
                role_time = cluster.sweetness.role_plata.find_one({'_id': str(role.id)})['time']
                
                for member in role.members:
                    count += 1
                
                description = f'<:to4ka:1090923466435346454> **Роль**: <@&{role.id}>\n<:to4ka:1090923466435346454> **Владелец:** {owner}\n<:to4ka:1090923466435346454> **Носителей:** {count}\n\n<:to4ka:1090923466435346454> **ID роли:** {role.id}\n<:to4ka:1090923466435346454> **Заканчивается:** `через {role_time // 86400} дней {(role_time // 3600) % 24} часов {(role_time - (role_time // hour * hour)) // 60} минут`'
                
                if role.id in cluster.sweetness.role.find_one({'_id': 1230})['roleshop']:
                    buy = 'Да'
                    role_buy = cluster.sweetness.role.find_one({'_id': str(role.id)})['buy']
                    role_cost = cluster.sweetness.role.find_one({'_id': str(role.id)})['cost']
                    description += f'\n<:to4ka:1090923466435346454> **Цена роли:** {role_cost}'
                    description += f'\n<:to4ka:1090923466435346454> **Продана раз:** {role_buy}'
                    description += f'\n<:to4ka:1090923466435346454> **Продается:** {buy}'
                else:
                    buy = 'Нет'
                    description += f'\n<:to4ka:1090923466435346454> **Продается:** {buy}'
                embed = disnake.Embed(description = description, color = 3092790)
                embed.set_author(name = "<:information1:1111712238886191154> Посмотреть информацию о роли", icon_url = inter.guild.icon.url)
                if len(cluster.sweetness.role.find_one({'_id': str(role.id)})['blacklist']) == 0:
                    embed.add_field(name = '> Чёрный список', value = f'Пусто')
                else:
                    members = ' '.join([inter.guild.get_member(i).mention for i in cluster.sweetness.role.find_one({'_id': str(role.id)})['blacklist']])
                    embed.add_field(name = '> Чёрный список', value = f'{members}')
                return await inter.response.edit_message(embed = embed, view = RoleManageBack1())

    @commands.Cog.listener()
    async def on_button_click(self, inter):

        custom_id = inter.component.custom_id
        if custom_id[-4:] == 'role':
            
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description = f"{inter.author.mention}, **Вы** не можете управлять **чужими кнопками!**", color = 3092790)
                embed.set_author(name = "Управление личной ролью", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)

            role = disnake.utils.get(inter.guild.roles, id = int(rolebutton[inter.author.id]))
            
            if custom_id[-9:] == 'icon_role':
                if custom_id == "accept_icon_role":

                    if int(5000) > int(cluster.sweetness.economy.find_one({"_id": str(inter.author.id)})["balance"]):
                        embed = disnake.Embed(description = f'{inter.author.mention}, На вашем балансе **недостаточно средств**!', color = disnake.Color.red())
                        embed.set_author(name = f"Купить товар | {inter.guild.name}", icon_url = inter.guild.icon.url)
                        embed.set_thumbnail(url = inter.author.display_avatar.url)
                        return await inter.response.edit_message(embed = embed)

                    embed = disnake.Embed(description = f'{inter.author.mention}, **Скиньте** фотографию в чат, для того чтобы **поставить/изменить** иконку на роли!', color=3092790)
                    embed.set_author(name = f"Добавить/Изменить иконку", icon_url = inter.guild.icon.url)
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    await inter.response.edit_message(embed = embed, components = [])

                    def check(m):
                        return m.author.id == inter.author.id
                    try: 
                        image = await self.bot.wait_for("message", check = check)
                    except TimeoutError:
                        return

                    for attach in image.attachments:
                        await attach.save(f"icon_role.png")

                    with open(f'icon_role.png', "rb") as image:
                        img_byte = image.read()

                    emoji = await inter.guild.create_custom_emoji(name = 'xdd', image = img_byte)
                    try:
                        await role.edit(icon = emoji)
                    except:
                        embed = disnake.Embed(description = f"{inter.author.mention}, **На сервере недостаточно бустов** для того чтобы добавить иконку на роль!", color = 3092790)
                        embed.set_thumbnail(url = inter.author.display_avatar.url)
                        embed.set_author(name = f"Добавить/Изменить иконку", icon_url = inter.guild.icon.url)
                        return await inter.message.edit(embed = embed)

                    await emoji.delete()

                    cluster.sweetness.economy.update_one({"_id": str(inter.author.id)}, {"$inc": {"balance": -int(5000)}})
                    embed = disnake.Embed(description = f"{inter.author.mention}, **Вы** успешно добавили/изменили иконку **личной комнаты!**", color = 3092790)
                    embed.set_author(name = f"Добавить/Изменить иконку", icon_url = inter.guild.icon.url)
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    return await inter.message.edit(embed = embed)

            if custom_id == 'yes_role':
                if not inter.message.content == inter.author.mention:
                    embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
                    embed.set_author(name = "Управление личной ролью", icon_url = inter.guild.icon.url)
                    embed.set_thumbnail(url = inter.author.display_avatar.url)
                    return await inter.send(ephemeral = True, embed = embed)

                else:
                    member = inter.author
                    await member.add_roles(role)
                    embed = disnake.Embed(description = f'{member.mention}, **Вы** успешно согласились и **Вам** была выдана роль <@&{rolebutton[inter.author.id]}>', color = 3092790)
                    embed.set_author(name = "Управление личной ролью", icon_url = inter.guild.icon.url)
                    return await inter.response.edit_message(embed = embed, components=[])

            if custom_id == 'no_role':
                member = disnake.utils.get(inter.guild.members, id = int(idmessage[inter.message.id]))
                embed = disnake.Embed(description = f'{member.mention}, **Вы** успешно отказались от роли **<@&{rolebutton[inter.author.id]}>**', color = 3092790)
                embed.set_author(name = "Управление личной ролью", icon_url = inter.guild.icon.url)
                await inter.response.edit_message(embed = embed, components=[])

            if custom_id == 'menu_role':

                role = disnake.utils.get(inter.guild.roles, id = int(rolebutton[inter.author.id]))

                embed = disnake.Embed(description = f'{inter.author.mention}, выберите **операцию** для взаимодействия с ролью <@&{role.id}>', color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_author(name = 'Управление личной ролью', icon_url = inter.guild.icon.url)
                embed.set_footer(text = f'Запросил(а) {inter.author}')
                await inter.response.edit_message(embed = embed, view = RoleManage())
        try:

            await asyncio.sleep(1)

            rolebutton[inter.author.id] = disnake.utils.get(inter.guild.roles, name = inter.component.label).id

            role = disnake.utils.get(inter.guild.roles, name = inter.component.label)

            if not inter.message.content == inter.author.mention:
                return await inter.send(f"{inter.author.mention}, **Вы** не можете использовать **чужие кнопки**!", ephemeral=True)

            embed = disnake.Embed(description = f'{inter.author.mention}, выберите **операцию** для взаимодействия с ролью <@&{disnake.utils.get(inter.guild.roles, name = inter.component.label).id}>', color = 3092790)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            embed.set_author(name = 'Управление личной ролью', icon_url = inter.guild.icon.url)
            embed.set_footer(text = f'Запросил(а) {inter.author}')
            await inter.response.edit_message(embed = embed, view = RoleManage())

        except: 
            pass
def setup(bot):
    bot.add_cog(rolecog(bot))