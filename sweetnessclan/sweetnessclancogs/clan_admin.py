import pymongo
import disnake
import datetime
import json
from disnake.ext import commands
from disnake.enums import ButtonStyle, TextInputStyle

cluster = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/test?retryWrites=true&w=majority")

files = cluster.sweetness.files
database = cluster.sweetness

role_clan = {}
clan_invite = {}
min = 60

hour = 60 * 60
day = 60 * 60 * 24

class ClanAdmin(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Добавить участника в клан", custom_id = 'adm_invite', emoji = '<:plus_man1:1096087509781450772>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Удалить участника из клана", custom_id = 'adm_kick', emoji = '<:minus_man1:1096087502210744331>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Изменить слоты", custom_id = 'adm_limit', emoji = '<:privates2:1109822758642270248>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Выдать монеты", custom_id = 'adm_deposit', emoji = '<:transfer:1096087526785163354>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Снять монеты", custom_id = 'adm_remove_deposit', emoji = '<:take:1096087521978486894>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Выдать онлайн", custom_id = 'adm_add_lvl', emoji = '<:plus1:1096093185282945074>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Снять онлайн", custom_id = 'adm_remove_lvl', emoji = '<:minus1:1096093188013441184>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Изменить владельца", custom_id = 'adm_owner', emoji = '<:edit1:1096092966570971218>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Добавить заместителя", custom_id = 'adm_zam', emoji = '<:plus_man1:1096087509781450772>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Убрать заместителя", custom_id = 'adm_remove_zam', emoji = '<:minus_man1:1096087502210744331>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, label = "Удалить клан", custom_id = 'adm_delete', emoji = '<a:LogoWarningChillfr:996459723249422408>'))

class AdmLevelGive(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = ButtonStyle.green, emoji = '<:zxc3:1009168371213926452>', custom_id = 'adm_add_lvl_accept', row = 0))
        self.add_item(disnake.ui.Button(style = ButtonStyle.green, emoji = '<:zxc2:1009168373936050206>', custom_id = 'adm_add_lvl_decline', row = 0))

class AdmLevelTake(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = ButtonStyle.green, emoji = '<:zxc3:1009168371213926452>', custom_id = 'adm_remove_lvl_accept', row = 0))
        self.add_item(disnake.ui.Button(style = ButtonStyle.green, emoji = '<:zxc2:1009168373936050206>', custom_id = 'adm_remove_lvl_decline', row = 0))

class ClanDeleteAdmin(disnake.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'adm_delete_yes', emoji = '<:yes1:1092007373733900348>'))

class clan_adm(commands.Cog):
    def __init__(self, bot: commands.Bot(intents = disnake.Intents.all(), command_prefix = 'test!')):
        self.bot = bot

    @commands.slash_command(description = 'Управление кланами')
    async def clan_admin(self, inter, role: disnake.Role):
        if inter.author.id in [ 284010976313868288]:
            with open('clan_sweetness.json', 'r', encoding='utf-8') as f:
                clan = json.load(f)
            clan_take = clan[str(inter.guild.id)][str(role.id)]
            if database.clan_online.count_documents({"_id": str(role.id)}) == 0:
                database.clan_online.insert_one({"_id": str(role.id), "clan_online": 0})
            clan_online = database.clan_online.find_one({'_id': str(role.id)})['clan_online']
            clan_points = clan_online // 3600
            clan_level = clan_points // 20 + 1
            clan_take['Points'] = int(clan_points)
            clan_take['Level'] = int(clan_level)
            with open('clan_sweetness.json', 'w') as f:
                json.dump(clan, f)

            clan_owner = f"<@{clan_take['Owner']}>"
            clan_date = f"{clan_take['Time']}"
            clan_points = f"{clan_take['Points']}"
            clan_level = f"{clan_take['Level']}"
            clan_limit = f"{clan_take['Limit']}"
            clan_balance = f"{clan_take['Balance']}"

            role_clan[inter.author.id] = role.id

            embed = disnake.Embed(color = 3092790, description = f"{inter.author.mention}, выберите **действие** над кланом **{role.mention}**\n> Участников: **{len(role.members)}/{clan_limit}**\n> Овнер: {clan_owner}\n> \
                                  Дата создания: **{clan_date}**\n> Баланс: **{clan_balance}**\n> Уровень: **{clan_level}**\n> Голосовой онлайн: **{clan_online // hour}ч. {(clan_online - (clan_online // hour * hour)) // 60}м.**")
            embed.set_author(name = f"Управление кланами {inter.guild.name}", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            await inter.send(inter.author.mention, embed = embed, view = ClanAdmin())
        else:
            embed = disnake.Embed(description = f'{inter.author.mention}, У **Вас** нет на это **разрешения**!', color = disnake.Color.red())
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            embed.set_author(name = f"Управление кланами {inter.guild.name}", icon_url = inter.guild.icon.url)
            await inter.send(embed = embed)

    @commands.Cog.listener()
    async def on_button_click(self, inter):

        custom_id = inter.component.custom_id
        if custom_id[:3] == 'adm':
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color = 3092790)
                embed.set_author(name = f"Управление кланами {inter.guild.name}", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                return await inter.send(ephemeral = True, embed = embed)
            
            with open('clan_sweetness.json','r', encoding='utf-8') as f: 
                clan = json.load(f)

            clanxd = role_clan[inter.author.id]

            if custom_id == "adm_invite":
                components = [disnake.ui.TextInput(label="Айди пользователя",placeholder="Например: 849353684249083914",custom_id = "Айди пользователя",style=disnake.TextInputStyle.paragraph, max_length=25)]
                await inter.response.send_modal(title=f"Добавить участника в клан",custom_id = "adm_invite", components=components)
            if custom_id == "adm_kick":
                components = [disnake.ui.TextInput(label="Айди пользователя",placeholder="Например: 849353684249083914",custom_id = "Айди пользователя",style=disnake.TextInputStyle.paragraph, max_length=25)]
                await inter.response.send_modal(title=f"Выгнать участника из клана",custom_id = "adm_kick", components=components)
            if custom_id == 'adm_limit':
                await inter.response.send_modal(title="Лимит",custom_id = "adm_limit",components=[
                    disnake.ui.TextInput(label="Лимит", placeholder="Например: 10", custom_id = "Лимит",style=disnake.TextInputStyle.short,max_length=50)])
            if custom_id == 'adm_deposit':
                await inter.response.send_modal(title="Депозит",custom_id = "adm_deposit",components=[
                    disnake.ui.TextInput(label="Количество", placeholder="Например: 10", custom_id = "Количество",style=disnake.TextInputStyle.short,max_length=50)])
            if custom_id == 'adm_add_lvl':
                embed = disnake.Embed(color = 3092790, description = f"{inter.author.mention}, **Вы** уверены что хотите выдать онлайн часы у клана (добавится уровень, так как онлайн зависит от уровня.)")
                embed.set_author(name = f"Управление кланами {inter.guild.name}", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                await inter.response.edit_message(embed = embed, view = AdmLevelGive())
            if custom_id == "adm_add_lvl_accept":
                await inter.response.send_modal(title="Добавить онлайн",custom_id = "adm_add_lvl",components=[
                    disnake.ui.TextInput(label="Секунды", placeholder="10", custom_id = "Секунды",style=disnake.TextInputStyle.short,max_length=5)])
            if custom_id == "adm_add_lvl_decline":
                return await inter.message.delete()
            
            if custom_id == "adm_remove_lvl_accept":
                await inter.response.send_modal(title="Убрать онлайн",custom_id = "adm_remove_lvl",components=[
                    disnake.ui.TextInput(label="Секунды", placeholder="10", custom_id = "Секунды",style=disnake.TextInputStyle.short,max_length=5)])
                
            if custom_id == "adm_remove_lvl_decline":
                return await inter.message.delete()

            if custom_id == 'adm_remove_lvl':
                embed = disnake.Embed(color = 3092790, description = f"{inter.author.mention}, **Вы** уверены что хотите забрать онлайн часы у клана (добавится уровень, так как онлайн зависит от уровня.)")
                embed.set_author(name = f"Управление кланами {inter.guild.name}", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                await inter.response.edit_message(embed = embed, view = AdmLevelTake())
                
            if custom_id == 'adm_delete':
                embed = disnake.Embed(color = 3092790, description = f"{inter.author.mention}, **Вы** точно хотите удалить клан <@&{clanxd}>?!")
                embed.set_author(name = f"Управление кланами {inter.guild.name}", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                await inter.response.edit_message(embed = embed, view = ClanDeleteAdmin())
            if custom_id == 'adm_delete_yes':

                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно удалили клан!', color = 3092790)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_author(name = f"Управление кланами {inter.guild.name}", icon_url = inter.guild.icon.url)
                await inter.response.edit_message(embed = embed, components = [])

                category_id = cluster.sweetness.clan.find_one({'_id': str(clanxd)})['category']
                category = disnake.utils.get(inter.guild.categories, id = int(category_id))

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

                await disnake.utils.get(inter.guild.roles, id = int(clanxd)).delete()

                for channel in category.voice_channels:
                    await channel.delete()

                for channel in category.text_channels:
                    await channel.delete()

                await category.delete()
                
                cluster.sweetness.clan.delete_one({'_id': str(clanxd)})
                del clan[str(inter.guild.id)][str(clanxd)]
                with open('clan_sweetness.json','w') as f:
                    json.dump(clan,f)

            if custom_id == "adm_owner":
                components = [disnake.ui.TextInput(label="Айди пользователя",placeholder="Например: 849353684249083914",custom_id = "Айди пользователя",style=disnake.TextInputStyle.paragraph, max_length=25)]
                await inter.response.send_modal(title=f"Передать владельца клана",custom_id = "adm_clan_owner", components=components)

            if custom_id == "adm_zam":
                pass
            if custom_id == "adm_remove_zam":
                pass

    @commands.Cog.listener()
    async def on_modal_submit(self, inter):
        custom_id = inter.custom_id
        if custom_id[:3] == 'adm':
            for key, value in inter.text_values.items():
                value = int(value)

            with open('clan_sweetness.json','r', encoding='utf-8') as f: 
                clan = json.load(f)

            clanxd = role_clan[inter.author.id]
            if custom_id == "adm_add_lvl":
                embed = disnake.Embed(color = 3092790)
                embed.set_author(name = "Добавить онлайн", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)

                cluster.sweetness.clan_online.update_one({"_id": str(clanxd)}, {"$inc": {"clan_online": +value}})

                embed.description = f'{inter.author.mention}, **Вы** успешно добавили **{value}** онлайна секунд клану <@{clanxd}>'
                await inter.response.edit_message(embed = embed, components = [])
            if custom_id == "adm_remove_lvl":
                embed = disnake.Embed(color = 3092790)
                embed.set_author(name = "Убрать онлайн", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)

                cluster.sweetness.clan_online.update_one({"_id": str(clanxd)}, {"$inc": {"clan_online": -value}})

                embed.description = f'{inter.author.mention}, **Вы** успешно убрали **{value}** онлайна секунд клану <@{clanxd}>'
                await inter.response.edit_message(embed = embed, components = [])

            if custom_id == "adm_kick":
                member = disnake.utils.get(inter.guild.members, id = int(value))

                embed = disnake.Embed(color = 3092790)
                embed.set_author(name = "Выгнать из клана", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)

                clan[str(inter.guild.id)][str(member.id)] = 'Отсутствует'
                with open('clan_sweetness.json','w') as f:
                    json.dump(clan,f)

                embed.description = f'{inter.author.mention}, **Вы** успешно выгнали <@{value}> из клана <@&{clanxd}>'
                await inter.response.edit_message(embed = embed, components = [])

                if member.id in clan[str(inter.guild.id)][clanxd]['Admin']:
                    await member.remove_roles(disnake.utils.get(inter.guild.roles, id = 961299056968237127))
                    clan[str(inter.guild.id)][clanxd]['Admin'].remove(member.id)
                    with open('clan_sweetness.json','w') as f:
                        json.dump(clan,f)

                clan[str(inter.guild.id)][str(member.id)] = 'Отсутствует'
                
                role = disnake.utils.get(inter.guild.roles, id = int(clanxd))
                await member.remove_roles(role)

                return await member.remove_roles(disnake.utils.get(inter.guild.roles, id = 961529522082185226))

            if custom_id == "adm_invite":
                role_id = int(clan[str(960579506425446472)][str(clanxd)]['Role'])
                
                member = disnake.utils.get(inter.guild.members, id = int(value))
                clan_invite[str(value)] = int(role_id)

                role = disnake.utils.get(inter.guild.roles, id = int(role_id))
                await member.add_roles(role)

                cluster.sweetness.clan.update_one({'_id': str(value)}, {'$set': {'rank': f'Участник'}}, upsert = True)

                embed = disnake.Embed(description = f'### > {inter.author.mention} теперь ты в клане **<@&{role_id}>**!', color = 3092790)
                embed.set_author(name = f"Кланы | {self.bot.get_guild(960579506425446472).name}", icon_url = self.bot.get_guild(960579506425446472).icon.url)
                embed.set_footer(text = f"Добавил в клан: {inter.author.mention}", icon_url = inter.author.display_avatar.url)
                embed.set_image(url = "https://cdn.discordapp.com/attachments/1138543077548625930/1138550082606735571/6b5a50a2860dfb67a8cd4014a019e31e.jpg")
                await member.send(embed = embed, components = [])

                embed = disnake.Embed(description = f'### > Добро пожаловать в клан <@&{role_id}>', color = 3092790)
                embed.set_author(name = f"Кланы | {self.bot.get_guild(960579506425446472).name}", icon_url = self.bot.get_guild(960579506425446472).icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.set_footer(text = f"Добавил в клан: {inter.author.mention}", icon_url = inter.author.display_avatar.url)
                await self.bot.get_channel(int(clan[str(960579506425446472)][str(clanxd)]['TextChannel'])).send(f"<@{value}>", embed = embed)

                embed = disnake.Embed(color = 3092790)
                embed.set_author(name = f"Кланы | {self.bot.get_guild(960579506425446472).name}", icon_url = self.bot.get_guild(960579506425446472).icon.url)
                embed.set_thumbnail(url = inter.author.display_avatar.url)
                embed.description = f'{inter.author.mention}, **Вы** успешно добавили в клан <@&{clanxd}> уч. <@{value}>'
                await inter.response.edit_message(embed = embed, components = [])

                input = datetime.datetime.now()
                data = int(input.timestamp())
                cluster.sweetness.clan.update_one({'_id': str(value)}, {'$set': {'tip_data': f'<t:{data}:F>'}}, upsert = True)

                clan[str(960579506425446472)][str(clanxd)]['ClanMembers'] += 1
                clan[str(960579506425446472)][str(value)] = clanxd
                with open('clan_sweetness.json','w') as f:
                    json.dump(clan,f)
                
            if custom_id == 'adm_limit':
                clan[str(inter.guild.id)][str(clanxd)]['Limit'] += int(value)
                with open('clan_sweetness.json','w') as f: 
                    json.dump(clan,f)

                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно выдали лимит **{value}** клану <@&{clanxd}>', color = disnake.Color.red())
                embed.set_author(name = f"Управление кланами {inter.guild.name}", icon_url = inter.guild.icon.url)
                embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
                return await inter.send(embed = embed, ephemeral = True)
            if custom_id == 'adm_deposit':
                clan[str(inter.guild.id)][str(clanxd)]['Balance'] += int(value)
                with open('clan_sweetness.json','w') as f: 
                    json.dump(clan,f)

                embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно выдали депозит **{value}** клану <@&{clanxd}>', color = disnake.Color.red())
                embed.set_author(name = f"Управление кланами {inter.guild.name}", icon_url = inter.guild.icon.url)
                embed.set_footer(text = inter.author, icon_url = inter.author.display_avatar.url)
            
                return await inter.send(embed = embed, ephemeral = True)
        
        if custom_id == 'adm_clan_owner':
            for key, value in inter.text_values.items():
                member = disnake.utils.get(inter.guild.members, id = int(value))

            embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно передали **владельца клана** {member.mention}!', color = 3092790)
            embed.set_footer(text = f"Выполнил(а) {inter.author}",icon_url = inter.author.display_avatar.url)
            embed.set_author(name = "Передать владельца клана", icon_url = inter.guild.icon.url)
            await inter.response.edit_message(embed = embed, components = [])

            try:
                clan_leader_id = clan[str(inter.guild.id)][str(clanxd)]['Owner']
                clan_leader = disnake.utils.get(inter.guild.members, id = int(clan_leader_id))

                await clan_leader.remove_roles(disnake.utils.get(inter.guild.roles, id = 961296301901885531))
            except:
                pass

            clan[str(inter.guild.id)][str(clanxd)]['Owner'] = member.id
            await member.add_roles(disnake.utils.get(inter.guild.roles, id = 961296301901885531))
            await member.add_roles(disnake.utils.get(inter.guild.roles, id = 961529522082185226))
            await member.add_roles(disnake.utils.get(inter.guild.roles, id = int(clanxd)))
            with open('clan_sweetness.json','w') as f: 
                json.dump(clan,f)

def setup(bot):
    bot.add_cog(clan_adm(bot))