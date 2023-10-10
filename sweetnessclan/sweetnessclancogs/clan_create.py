import pymongo
import disnake
import datetime
import json
from disnake.ext import commands, tasks
from disnake.enums import ButtonStyle, TextInputStyle

cluster = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/test?retryWrites=true&w=majority")

files = cluster.sweetness.files
database = cluster.sweetness

clanjoin_message = {}

class ClanJoin(disnake.ui.View):
    def __init__(self):
        super().__init__()
    @disnake.ui.button(style = ButtonStyle.green, emoji = '<:galochka:949261066163064844>', custom_id = 'yesjoin')
    async def first_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction): pass
    @disnake.ui.button(style = ButtonStyle.red, emoji = '<:krestik:949261056226779177>', custom_id = 'nojoin')
    async def second_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction): pass

def hex_to_rgb(value):
    value = value.lstrip('#')
    RGB = list(tuple(int(value[i:i + len(value) // 3], 16) for i in range(0, len(value), len(value) // 3)))
    return (RGB[0]<<16) + (RGB[1]<<8) + RGB[2]

class clan_cog(commands.Cog):
    def __init__(self, bot: commands.Bot(intents = disnake.Intents.all(), command_prefix = 'clan!')):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        with open('clan_sweetness.json','r', encoding='utf-8') as f: 
            clan = json.load(f)

        if not str(member.guild.id) in clan:
            clan[str(member.guild.id)] = {}
            with open('clan_sweetness.json','w') as f: 
                json.dump(clan,f)
        if after.channel is not None:

            if not str(member.id) in clan[str(960579506425446472)]:
                return
            if clan[str(960579506425446472)][str(member.id)] == 'Отсутствует':
                return
            
            id_role = clan[str(960579506425446472)][str(clan[str(960579506425446472)][str(member.id)])]['Role']

            role = disnake.utils.get(member.guild.roles, id = int(id_role))

            category_id = disnake.utils.get(member.guild.categories, id = database.clan.find_one({'_id': str(id_role)})['category'])
            channel_5 = database.clan.find_one({'_id': str(id_role)})['channel_5']

            if int(after.channel.id) == int(channel_5):
                channel5 = await member.guild.create_voice_channel(name = f"{role.name}・{member.name}", category = category_id)
                await member.move_to(channel5)
                await channel5.set_permissions(role, view_channel = True, connect = True)
                await channel5.set_permissions(member.guild.default_role, view_channel = True, connect = False)
                for admin in clan[str(member.guild.id)][str(clan[str(member.guild.id)][str(member.id)])]['Admin']:
                    await channel5.set_permissions(disnake.utils.get(member.guild.members, id = int(admin)), manage_channels = True)
                clan_leader = clan[str(member.guild.id)][str(clan[str(member.guild.id)][str(member.id)])]['Owner']
                await channel5.set_permissions(disnake.utils.get(member.guild.members, id = int(clan_leader)), manage_channels = True)
                await channel5.set_permissions(member, manage_channels = True)
                await channel5.set_permissions(disnake.utils.get(member.guild.roles, id = 1045677896976584806), move_members = True, deafen_members = True, mute_members = True, view_channel = True, connect = True) # клан стафф

        if before.channel:

            if not str(member.id) in clan[str(960579506425446472)]:
                return
            if clan[str(960579506425446472)][str(member.id)] == 'Отсутствует':
                return
            
            id_role = clan[str(960579506425446472)][str(clan[str(960579506425446472)][str(member.id)])]['Role']

            role = disnake.utils.get(member.guild.roles, id = int(id_role))

            category_id = disnake.utils.get(member.guild.categories, id = database.clan.find_one({'_id': str(id_role)})['category'])
            try:
                voice_channels = database.clan.find_one({'_id': str(id_role)})['voice_channels']
                channel_5 = database.clan.find_one({'_id': str(id_role)})['channel_5']
                if int(before.channel.category.id) == int(category_id.id):
                    if not int(before.channel.id) == int(channel_5):
                        if not int(before.channel.id) in voice_channels:
                            if len(before.channel.members) == 0:
                                await before.channel.delete()
            except:
                channel_5 = database.clan.find_one({'_id': str(id_role)})['channel_5']
                if int(before.channel.category.id) == int(category_id.id):
                    if not int(before.channel.id) == int(channel_5):
                        if len(before.channel.members) == 0:
                            await before.channel.delete()

    @commands.slash_command(description = 'Выдать клан')
    @commands.has_any_role(960579506467373114, 960579506467373112)
    async def clan_give(self, inter, цвет:str, *, название, пользователь: disnake.Member):
        with open('clan_sweetness.json','r', encoding='utf-8') as f: 
            clan = json.load(f)

        if not str(inter.guild.id) in clan:
            clan[str(inter.guild.id)] = {}
            with open('clan_sweetness.json','w') as f: 
                json.dump(clan,f)

        if not str(пользователь.id) in clan[str(inter.guild.id)]:
            clan[str(inter.guild.id)][str(пользователь.id)] = "Отсутствует"
            with open('clan_sweetness.json','w') as f: 
                json.dump(clan,f)

        await inter.response.defer()
        try:
            role = await inter.guild.create_role(name = название, color = disnake.Color(hex_to_rgb(str(цвет))), mentionable = True)
        except:
            embed = disnake.Embed(color = 3092790, title = f'Создание клана {название}', description = 'Ошибка! Укажите правильно цвет для роли')
            embed.set_author(name = 'Ошибка!', icon_url = 'https://cdn.disnakeapp.com/emojis/975801324811747329.webp?size=96&quality=lossless')
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            return await inter.send(embed = embed)

        embed = disnake.Embed(description = f'{inter.author.mention}, **Вы** успешно **создали клан** {пользователь.mention}!', color = 3092790)
        embed.set_author(name=f"Создание клана | {inter.guild.name}",icon_url = inter.author.display_avatar.url)
        embed.set_footer(text = "Управление кланом /clan_profile", icon_url = "https://cdn.discordapp.com/emojis/1137278045930127381.gif?size=96&quality=lossless")
        embed.set_author(name=inter.author,icon_url = inter.author.display_avatar.url)
        embed.set_thumbnail(url = inter.guild.icon.url)
        await inter.send(embed = embed)

        MainCategory = await inter.guild.create_category(f"[ {название} ]")

        channel_1 = await inter.guild.create_text_channel(name = "📜・требования", category = MainCategory)
        channel_2 = await inter.guild.create_text_channel(name = "🔔・заявки", category = MainCategory)
        channel_3 = await inter.guild.create_text_channel(name = "📃・новости", category = MainCategory)
        channel_4 = await inter.guild.create_text_channel(name = "💬・клан-чат", category = MainCategory)
        channel_5 = await inter.guild.create_voice_channel(name = "🏠・Создать канал", category = MainCategory)

        database.clan.insert_one({"_id": str(role.id), "category": MainCategory.id, "channel_1": channel_1.id, "channel_2": channel_2.id, "channel_3": channel_3.id, "channel_5": channel_5.id})
        
        if database.clan.count_documents({"_id": str(inter.guild.id)}) == 0:
            database.clan.insert_one({"_id": str(inter.guild.id), "categories": []})
            
        database.clan.update_one({"_id": str(inter.guild.id)}, {"$push": {"categories": MainCategory.id}})
        
        privat = disnake.utils.get(inter.guild.categories, id = 1142757576992366603)
        channelxd = privat.position

        role_category = disnake.utils.get(inter.guild.roles, id = 1142757719783264366)
        role_xd = role_category.position

        await role.edit(position = int(role_xd) - 1)

        await MainCategory.edit(position = int(channelxd) - 1)
        await MainCategory.set_permissions(disnake.utils.get(inter.guild.roles, id = 1102597291203895326), view_channel = False) #local ban
        await MainCategory.set_permissions(inter.guild.default_role, view_channel = False)

        await channel_4.set_permissions(disnake.utils.get(inter.guild.roles, id = 1045677896976584806), view_channel = True, send_messages = True, manage_messages = True) # Clan Staff
        await channel_4.set_permissions(inter.guild.default_role, send_messages = False, use_external_emojis = True, add_reactions = True)
        await channel_4.set_permissions(inter.guild.default_role, send_messages = False, use_external_emojis = True, add_reactions = True)
        await channel_4.set_permissions(inter.guild.default_role, send_messages = False, use_external_emojis = True, add_reactions = True)

        role1 = disnake.utils.get(inter.guild.roles, id = 961296301901885531)
        await пользователь.add_roles(role1)

        await пользователь.add_roles(role)

        clan[str(inter.guild.id)][role.id] = {}
        clan[str(inter.guild.id)][role.id]['Time'] = datetime.datetime.now().strftime("%d.%m.%Y")
        with open('clan_sweetness.json','w') as f:
            json.dump(clan,f)

        input = datetime.datetime.now()
        data = int(input.timestamp())
        cluster.sweetness.clan.update_one({'_id': str(пользователь.id)}, {'$set': {'tip_data': f'<t:{data}:F>'}}, upsert = True)
        cluster.sweetness.clan.update_one({'_id': str(пользователь.id)}, {'$set': {'rank': f'Лидер'}}, upsert = True)

        clan[str(inter.guild.id)][str(пользователь.id)] = str(role.id)
        clan[str(inter.guild.id)][role.id]['TextChannel'] = channel_4.id
        clan[str(inter.guild.id)][role.id]['Role'] = role.id
        clan[str(inter.guild.id)][role.id]['Deposit'] = {}
        clan[str(inter.guild.id)][role.id]['EmbedDescription'] = 'Отсутствует'
        clan[str(inter.guild.id)][role.id]['BanList'] = []
        clan[str(inter.guild.id)][role.id]['Thumbnail'] = 'Отсутствует'
        clan[str(inter.guild.id)][role.id]['Limit'] = 15
        clan[str(inter.guild.id)][role.id]['Points'] = 0
        clan[str(inter.guild.id)][role.id]['Level'] = 1
        clan[str(inter.guild.id)][role.id]['ClanMembers'] = 1
        clan[str(inter.guild.id)][role.id]['Balance'] = 1000
        clan[str(inter.guild.id)][role.id]['Owner'] = пользователь.id
        clan[str(inter.guild.id)][role.id]['Description'] = 'Отсутствует'
        clan[str(inter.guild.id)][role.id]['Admin'] = []

        with open('clan_sweetness.json','w') as f:
            json.dump(clan,f)

        await channel_4.set_permissions(пользователь, manage_messages=True)

        embed = disnake.Embed(description = f'{inter.author.mention}, **Выдал** вам клан {role.name}!', color = 3092790)
        embed.set_footer(text = "Управление кланом /clan_profile", icon_url = "https://cdn.discordapp.com/emojis/1137278045930127381.gif?size=96&quality=lossless")
        embed.set_author(name=f"Создание клана | {inter.guild.name}",icon_url = inter.author.display_avatar.url)
        embed.set_thumbnail(url = inter.guild.icon.url)
        await пользователь.send(embed = embed)

        await channel_1.set_permissions(inter.guild.default_role, send_messages=False)
        await channel_2.set_permissions(inter.guild.default_role, send_messages=False, view_channel = False)
        await channel_3.set_permissions(inter.guild.default_role, send_messages = False, view_channel = False)
        await channel_4.set_permissions(inter.guild.default_role, send_messages = False, view_channel = False)
        await channel_5.set_permissions(inter.guild.default_role, connect = False, view_channel = False)

        await channel_2.set_permissions(role, send_messages=True, view_channel = True)
        await channel_3.set_permissions(role, send_messages=False, view_channel = True)
        await channel_3.set_permissions(disnake.utils.get(inter.guild.roles, id = 961296301901885531), send_messages = True) # leader
        await channel_3.set_permissions(disnake.utils.get(inter.guild.roles, id = 961299056968237127), send_messages = True) # zam


        await channel_4.set_permissions(role, send_messages=True, view_channel = True)
        await channel_5.set_permissions(role, connect=True, view_channel = True)
        return await self.bot.get_channel(1026239319624667236).set_permissions(пользователь, view_channel=True, send_messages=True)
            
    @clan_give.error
    async def clan_give_error(self, inter, error):
        if isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed(title = "Выдать клан", description = f'{inter.author.mention}, У **Вас** нет на это **разрешения**!', timestamp = datetime.datetime.utcnow(), color = disnake.Color.red())
            embed.set_author(name = f"Выдать клан {inter.guild.name}", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            await inter.send(embed = embed)
        else: 
            print(error)

def setup(bot):
    bot.add_cog(clan_cog(bot))