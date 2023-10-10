import pymongo
import disnake
import json
import os
from disnake.ext import commands
from PIL import Image
from disnake.enums import ButtonStyle, TextInputStyle

cluster = pymongo.MongoClient(f"mongodb://127.0.0.1/myFirstDatabase?retryWrites=true&w=majority")

def change_image_color(input_image_path, output_image_path, new_color_hex):
    try:
        original_image = Image.open(input_image_path).convert("RGBA")
        width, height = original_image.size

        new_color_rgb = tuple(int(new_color_hex[i:i+2], 16) for i in (1, 3, 5))

        new_image_data = []
        for pixel in original_image.getdata():
            if pixel[:3] == (0, 0, 0):
                new_image_data.append((0, 0, 0, 0))  # Пропускаем прозрачные пиксели
            else:
                new_image_data.append(new_color_rgb + (pixel[3],))

        new_image = Image.new("RGBA", (width, height))
        new_image.putdata(new_image_data)

        new_image.save(output_image_path)
    except Exception as e:
        print(e)

def batch_change_color(input_folder, output_folder, new_color_hex):
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for filename in os.listdir(input_folder):
            if filename.endswith((".png", ".jpg", ".jpeg")):
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, filename)
                change_image_color(input_path, output_path, new_color_hex)
    except Exception as e:
        print(e)

class award(commands.Cog):
    def __init__(self, bot: commands.Bot(intents = disnake.Intents.all(), command_prefix="!")):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def update(self, inter, new_color):
        await inter.message.delete()

        embed = disnake.Embed(color = 3092790)
        embed.set_author(name = "Перекрашивание эмоджи", icon_url = inter.guild.icon.url)
        embed.set_thumbnail(url = inter.author.display_avatar.url)
        embed.description = f'### <a:waiting:1143927212291129374> Перекрашиваю эмоджи в цвет {new_color}'
        await inter.response.edit_message(embed = embed, components = [])

        input_folder = "images_sweetness/economy"
        output_folder = "images_sweetness/economy"
        batch_change_color(input_folder, output_folder, new_color)

        await inter.message.edit(embed = embed)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def update(self, inter):
        await inter.message.delete()

        embed = disnake.Embed(
            color=3092790,
            description=(
                "**Дорогие участники нашего проекта**, у нас для вас есть пара **хороших новостей**!\n\n"
                "**Сегодня** на сервере было выпущено обновление, связанное с **экономикой**. В **частности**, мы добавили **кейсы**, **подарки** и **достижения**.\n"
                "Теперь у вас есть возможность получить около **30 новых достижений** и получать за них **заслуженные награды**.\n\n"
                "Что касается **кейсов**, в честь выпуска обновления мы предоставляем вам **промокод** на получение одного из таких **кейсов**: "
                "**</case:1144293319174799460> > Активировать промо > UPDATE**.\n"
                "К тому же, рады представить вам **новую команду**: **</gift:1142921845977395350>**.\n\n"
                "Все доступные команды можно **протестировать** в чате <#945028622744444948>.\n\n"
                "Обратите внимание, что активно проводится **набор на все ветки** в канале <#1141707844480139424>.\n"
                "Также, рекомендуем приобрести **спонсорские пакеты** в канале <#1126043232288120863>, так как у спонсоров теперь доступны новые интересные возможности и привилегии\n\n"
                "Будьте в курсе всех дальнейших обновлений, подписавшись на наш **телеграм-канал**!"
            )
        )
        embed.set_author(name = f"Новости | {inter.guild.name}", icon_url = inter.guild.icon.url)
        await inter.send(content = "@everyone", embed = embed)

    @commands.slash_command(description = "Выдать валюту")
    async def award(self, inter, пользователь: disnake.Member, number: int):
        if inter.author.id in [674002588605349949, 284010976313868288, 849353684249083914, 274874981169758209]:
            if cluster.sweetness.economy.count_documents({"_id": str(пользователь.id)}) == 0:
                cluster.sweetness.economy.insert_one({"_id": str(пользователь.id),"balance": 0})

            cluster.sweetness.economy.update_one({"_id": str(пользователь.id)}, {"$inc": {"balance": +int(number)}})

            embed = disnake.Embed(color = 3092790)
            embed.set_author(name = f"Выдать валюту | {inter.guild.name}", icon_url = inter.guild.icon.url)
            embed.description = f"**Вы** успешно **выдали** валюту в размере **{number}** {пользователь.mention} <:amitobal:1158567849707716708>"
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            await inter.send(embed = embed)

            embed.description = f"{пользователь.mention}, **Вам** было выдано валюты в размере **{number}** <:amitobal:1158567849707716708>"
            await пользователь.send(embed = embed)
        else:
            embed = disnake.Embed(description=f"{inter.author.mention}, У **Вас** недостаточно прав на **выполнение этой команды**", color=3092790)
            embed.set_author(name = f"Недостаточно прав", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            await inter.send(embed = embed, ephemeral=True)
        
    @commands.slash_command(description = "Снять валюту")
    @commands.has_any_role(1106929858833039591, 1153738679475507232, 1142875756209381496, 1131539393207865354)
    async def unaward(self, inter, пользователь: disnake.Member, number: int):
        if cluster.sweetness.economy.count_documents({"_id": str(пользователь.id)}) == 0:
            cluster.sweetness.economy.insert_one({"_id": str(пользователь.id),"balance": 0})

        cluster.sweetness.economy.update_one({"_id": str(пользователь.id)}, {"$inc": {"balance": -int(number)}})

        embed = disnake.Embed(color = 3092790)
        embed.set_author(name = f"Снять валюту | {inter.guild.name}", icon_url = inter.guild.icon.url)
        embed.description = f"**Вы** успешно **сняли** валюту в размере **{number}** {пользователь.mention} <:amitobal:1158567849707716708> "
        embed.set_thumbnail(url = inter.author.display_avatar.url)
        await inter.send(embed = embed)

        embed.description = f"{пользователь.mention}, у **Вас** сняли валюту в размере **{number}** <:amitobal:1158567849707716708> "
        await пользователь.send(embed = embed)
            
    @unaward.error
    async def unaward_error(self, inter, error):
        if isinstance(error, commands.MissingAnyRole):
            embed = disnake.Embed(description=f"{inter.author.mention}, У **Вас** недостаточно прав на **выполнение этой команды**", color=3092790)
            embed.set_author(name = f"Недостаточно прав", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url = inter.author.display_avatar.url)
            await inter.send(embed = embed, ephemeral=True)
        else: 
            raise error

    @commands.Cog.listener()
    async def on_button_click(self, inter):

        custom_id = inter.component.custom_id

        if custom_id == "asd":
            await inter.response.send_modal(title = "Требования", custom_id="fsad", components = [
                disnake.ui.TextInput(label="Название:", custom_id="Название:",style=disnake.TextInputStyle.short, max_length=100),
                ])

def setup(bot): 
    bot.add_cog(award(bot))