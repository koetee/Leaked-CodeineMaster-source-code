import pymongo
import disnake
import asyncio
import json
from disnake.ext import commands
from disnake.utils import get
from disnake.enums import ButtonStyle, TextInputStyle

cluster = pymongo.MongoClient(f"mongodb://3ZJPyQEil5INOym:i7NhCqUFG4lQFcsE1YMZkwFRLP4IKU@5.42.77.117:59152")

files = cluster.sweetness.files

class PrivatesButton(disnake.ui.View):
    def __init__(self): 
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'btn1_privates', emoji = '<:privates1:1138812755521056938>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'btn2_privates', emoji = '<:privates2:1138812681437065277>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'btn3_privates', emoji = '<:privates3:1138812696142299227>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'btn4_privates', emoji = '<:privates4:1138812806884495381>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'btn5_privates', emoji = '<:privates5:1138812686617018368>'))

        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'btn6_privates', emoji = '<:privates6:1138812798592372826>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'btn7_privates', emoji = '<:privates7:1138812769395802173>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'btn8_privates', emoji = '<:privates8:1138812800966336622>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'btn9_privates', emoji = '<:privates9:1138812802363043891>'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = 'btn10_privates', emoji = '<:privates10:1138812698692427819>'))


async def vignat(inter, member):
    await inter.author.voice.channel.set_permissions(member, connect=False)
    await member.move_to(None)

class privatecog(commands.Cog):
    def __init__(self, bot: commands.Bot(intents = disnake.Intents.all(), command_prefix = 'privates!')):
        self.bot = bot

    @commands.command()
    async def privates(self, inter):

        await inter.message.delete()
        to4ka = "<:to4kaa:947909744985800804>"

        embed = disnake.Embed(description='> Жми следующие кнопки, чтобы настроить свою комнату\n\n', color=3092790)
        embed.add_field(name = '⠀', value = f'{to4ka} <:privates1:1138812755521056938> - Изменить название комнаты\n{to4ka} <:privates2:1138812681437065277> - Установить лимит\n{to4ka} <:privates3:1138812696142299227> - Закрыть комнату для всех\n{to4ka} <:privates4:1138812806884495381> - Открыть комнату для всех\n{to4ka} <:privates5:1138812686617018368> - Выгнать пользователя из комнаты\n', inline = True)
        embed.add_field(name = '⠀', value = f'{to4ka} <:privates6:1138812798592372826> - Забрать доступ\n{to4ka} <:privates7:1138812769395802173> - Выдать доступ\n{to4ka} <:privates8:1138812800966336622> - Забрать право\n{to4ka} <:privates9:1138812802363043891> - Выдать право\n{to4ka} <:privates10:1138812698692427819> - Назначить нового владельца канала', inline = True)
        embed.set_author(name = f"Управление приватным каналом {inter.guild.name}", icon_url = inter.guild.icon.url)
        embed.set_footer(text = 'Использовать их можно только когда у тебя есть приватный канал')
        await inter.send(embed = embed, view=PrivatesButton())

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: 
            return

        if message.channel.id == 1142555772648173728:
            try: 
                await message.delete()
            except: 
                pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if after.channel is not None:
            if int(after.channel.id) == 1142555774334283870:
                channel5 = await member.guild.create_voice_channel(name = f"Канал {member.name}", category = disnake.utils.get(member.guild.categories, id = 1142555772648173728))
                await member.move_to(channel5)
                await channel5.set_permissions(member, manage_channels=True, connect = True, view_channel = True)
                cluster.sweetness.priv.update_one({'_id': str(member.id)}, {'$set': {'author': channel5.id}}, upsert = True)

        if before.channel:
            if before.channel.category_id == 1142555772648173728:
                if len(before.channel.members) == 0:
                    try:
                        if not before.channel.id == 1142555774334283870:
                            await before.channel.delete()
                    except:
                        pass

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        custom_id = inter.component.custom_id

        if custom_id[-8:] == "privates":
            embed = disnake.Embed(color = 3092790).set_thumbnail(url = inter.author.display_avatar.url)
            embed.set_author(name = "Управление приватной комнатой", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)

            if not int(inter.author.voice.channel.category.id) == 1142555772648173728 or int(inter.author.voice.channel.id) == 1142555774334283870:
                embed.description = f'{inter.author.mention}, **Для** управления комнатой **зайдите** в голосовой канал категории "приватные комнаты".'
                return await inter.send(ephemeral = True, embed = embed)

            if not inter.author.voice and inter.author.voice.channel:
                embed.description = f'{inter.author.mention}, **Для** управления комнатой **зайдите** в голосовой канал.'
                return await inter.send(ephemeral = True, embed = embed)
            
            if inter.component.custom_id == 'btn1_privates':
                await inter.response.send_modal(title=f"Изменить название", custom_id = "btn1_privates",components=[
                    disnake.ui.TextInput(label="Название", placeholder = "Введите текст", custom_id = "Название", style = disnake.TextInputStyle.short, max_length = 150)])
                
            if inter.component.custom_id == 'btn2_privates':
                await inter.response.send_modal(title=f"Изменить лимит", custom_id = "btn2_privates",components=[
                    disnake.ui.TextInput(label="Лимит", placeholder = "Введите текст", custom_id = "Лимит", style = disnake.TextInputStyle.short, max_length = 2)])
                
            if inter.component.custom_id == 'btn3_privates':
                await inter.author.voice.channel.set_permissions(inter.guild.default_role, connect=False)

                embed.description = f"{inter.author.mention}, **Вы** успешно **закрыли комнату** для всех"
                return await inter.send(embed = embed, ephemeral = True)
            if inter.component.custom_id == 'btn4_privates':
                await inter.author.voice.channel.set_permissions(inter.guild.default_role, connect=True)

                embed.description = f"{inter.author.mention}, **Вы** успешно **открыли комнату** для всех"
                return await inter.send(embed = embed, ephemeral = True)
            
            if inter.component.custom_id == 'btn5_privates':
                await inter.response.send_modal(title=f"Выгнать из комнаты", custom_id = "btn5_privates",components=[
                    disnake.ui.TextInput(label="Айди пользователя", placeholder = "Введите айди", custom_id = "Айди пользователя", style = disnake.TextInputStyle.short, max_length = 25)])
                
            if inter.component.custom_id == 'btn6_privates':
                await inter.response.send_modal(title=f"Забрать доступ", custom_id = "btn6_privates",components=[
                    disnake.ui.TextInput(label="Айди пользователя", placeholder = "Введите айди",custom_id = "Айди пользователя", style = disnake.TextInputStyle.short, max_length = 25)])
                
            if inter.component.custom_id == 'btn7_privates':
                await inter.response.send_modal(title=f"Выдать доступ", custom_id = "btn7_privates",components=[
                    disnake.ui.TextInput(label="Айди пользователя", placeholder = "Введите айди",custom_id = "Айди пользователя", style = disnake.TextInputStyle.short, max_length = 25)])
                
            if inter.component.custom_id == 'btn8_privates':
                await inter.response.send_modal(title=f"Забрать право говорить", custom_id = "btn8_privates",components=[
                    disnake.ui.TextInput(label="Айди пользователя", placeholder = "Введите айди",custom_id = "Айди пользователя", style = disnake.TextInputStyle.short, max_length = 25)])
                
            if inter.component.custom_id == 'btn9_privates':
                await inter.response.send_modal(title=f"Выдать право говорить", custom_id = "btn9_privates",components=[
                    disnake.ui.TextInput(label="Айди пользователя", placeholder = "Введите айди",custom_id = "Айди пользователя", style = disnake.TextInputStyle.short, max_length = 25)])
                
            if inter.component.custom_id == 'btn10_privates':
                await inter.response.send_modal(title=f"Назначить нового владельца", custom_id = "btn10_privates",components=[
                    disnake.ui.TextInput(label="Айди пользователя", placeholder = "Введите айди",custom_id = "Айди пользователя", style = disnake.TextInputStyle.short, max_length = 25)])

    @commands.Cog.listener()
    async def on_modal_submit(self, inter):

        custom_id = inter.custom_id

        if custom_id[-8:] == 'privates':

            for key, value in inter.text_values.items():
                value = value

            embed = disnake.Embed(color = 3092790).set_thumbnail(url = inter.author.display_avatar.url)
            embed.set_author(name = "Управление приватной комнатой", icon_url = inter.guild.icon.url)

            if not int(inter.author.voice.channel.category.id) == 1142555772648173728 or int(inter.author.voice.channel.id) == 1142555774334283870:
                embed.description = f'{inter.author.mention}, **Для** управления комнатой **зайдите** в голосовой канал категории "приватные комнаты".'
                return await inter.send(ephemeral = True, embed = embed)

            try:
                asd = cluster.sweetness.priv.find_one({"_id": str(inter.author.id)})["author"]
            except:
                embed.description = f"{inter.author.mention}, **Вы** не являетесь **владельцем** этой комнаты"
                return await inter.send(embed = embed, ephemeral = True)

            if not inter.author.voice and inter.author.voice.channel:
                embed.description = f'{inter.author.mention}, **Для** управления комнатой **зайдите** в голосовой канал.'
                return await inter.send(ephemeral = True, embed = embed)

            if custom_id == "btn1_privates":
               embed.description = f'{inter.author.mention}, **Вы** успешно **изменили** название на **{value}**'
               await inter.author.voice.channel.edit(name = f'Комната {value}')
            
            if custom_id == "btn2_privates":
                embed.description = f'{inter.author.mention}, **Вы** успешно **изменили** лимит на **{value}**'
                await inter.author.voice.channel.edit(user_limit = value)

            if custom_id == "btn5_privates":
                member = get(self.bot.get_all_members(), id = int(value))
                if member.voice.channel.id == inter.author.voice.channel.id:
                    try:
                        await member.move_to(None)
                    except:
                        pass
                    
                    await inter.author.voice.channel.set_permissions(member, connect=False)
    
                    embed.description = f"{inter.author.mention}, **Вы** успешно **выгнали** из приватной комнаты <@{value}>"
                else:
                    embed.description = f"{inter.author.mention}, **Вы** не можете **выгнать** <@{value}>, так как вы не находитесь в одном **голосовом канале с ним.**"
            if custom_id == "btn6_privates":
                member = get(self.bot.get_all_members(), id = int(value))
                if member.voice.channel.id == inter.author.voice.channel.id:
                    embed.description = f'{inter.author.mention}, **Вы** успешно **выгнали** <@{value}>'
                    await asyncio.create_task(vignat(inter, member))
                else:
                    embed.description = f"{inter.author.mention}, **Вы** не можете **выгнать** <@{value}>, так как вы не находитесь в одном **голосовом канале с ним.**"
            if custom_id == "btn7_privates":
                embed.description = f"{inter.author.mention}, **Вы** успешно **добавили** в приватную комнату <@{value}>"
                member = disnake.utils.get(inter.guild.members, id = int(value))
                await inter.author.voice.channel.set_permissions(member, connect = True)

            if custom_id == "btn8_privates":
                member = get(self.bot.get_all_members(), id = int(value))
                if member.voice.channel.id == inter.author.voice.channel.id:
                    embed.description = f"{inter.author.mention}, **Вы** успешно **забрали** право говорить <@{value}>"
                    await inter.author.voice.channel.set_permissions(member, speak=False)
                    await member.move_to(inter.author.voice.channel)
                else:
                    embed.description = f"{inter.author.mention}, **Вы** не можете забрать право говорить, так как вы не находитесь в одном канале с пользователем"
            if custom_id == "btn9_privates":
                member = get(self.bot.get_all_members(), id=int(value))
                if member.voice.channel.id == inter.author.voice.channel.id:
                    embed.description = f"{inter.author.mention}, **Вы** успешно **выдали** право говорить <@{value}>"
                else:
                    embed.description = f"{inter.author.mention}, **Вы** не можете выдать право говорить, так как вы не находитесь в одном канале с пользователем"
                await inter.author.voice.channel.set_permissions(member, speak=True)
                await member.move_to(inter.author.voice.channel)

            if custom_id == "btn10_privates":
                member = get(self.bot.get_all_members(), id=int(value))
                if member.voice.channel.id == inter.author.voice.channel.id:
                    embed.description = f"{inter.author.mention}, **Вы** успешно **назначили** нового владельца <@{value}>"
                else:
                    embed.description = f"{inter.author.mention},** Вы не можете назначить** <@{value}> владельцем комнаты, так как вы не находитесь в **одной комнате с ним.**"
                await inter.author.voice.channel.set_permissions(inter.author, manage_channels=False)
                await inter.author.voice.channel.set_permissions(member, manage_channels=True, speak=True)
            
            return await inter.send(ephemeral = True, embed = embed)
        
def setup(bot):
    bot.add_cog(privatecog(bot))