import pymongo
import disnake
import json
from disnake.ext import commands
from disnake import Localized, utils, Embed
from disnake.enums import ButtonStyle, TextInputStyle

cluster = pymongo.MongoClient(f"mongodb://3ZJPyQEil5INOym:i7NhCqUFG4lQFcsE1YMZkwFRLP4IKU@5.42.77.117:59152")

files = cluster.sweetness.files

min = 60
hour = 60 * 60
day = 60 * 60 * 24
profile_user = {}
currentHistoryPage = {}
items_per_page = 5

class ButtonsHistory(disnake.ui.View):
    def __init__(self, author: int):
        super().__init__()
        if not str(author) in currentHistoryPage or currentHistoryPage[str(author)] == 0:
            self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = "history_first_page", emoji = f"{files.find_one({'_id': 'double_left'})['emoji_take']}", disabled = True))
            self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = "history_prev_page", emoji = f"{files.find_one({'_id': 'left'})['emoji_take']}", disabled = True))
        else:
            self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = "history_first_page", emoji = f"{files.find_one({'_id': 'double_left'})['emoji_take']}"))
            self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = "history_prev_page", emoji=f"{files.find_one({'_id': 'left'})['emoji_take']}"))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = "history_exit", emoji=f"{files.find_one({'_id': 'basket'})['emoji_take']}"))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = "history_right_page", emoji=f"{files.find_one({'_id': 'right'})['emoji_take']}"))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, custom_id = "history_last_page", emoji = f"{files.find_one({'_id': 'double_right'})['emoji_take']}"))

class History_cog(commands.Cog):
    def __init__(self, bot: commands.Bot(intents = disnake.Intents.all(), command_prefix = "test!")):
        self.bot = bot

    @commands.slash_command(description="История")
    async def history(self, inter, тип: str = commands.Param(choices=[Localized("Браки", key="A"), Localized("Переводы", key="B"), Localized("Наказания", key="C")]), пользователь: disnake.Member = None):
        if пользователь is None:
            пользователь = inter.author

        profile_user[inter.author.id] = пользователь.id
        embed = Embed(color=3092790).set_thumbnail(url=пользователь.display_avatar.url)
        embed.set_author(name=f"История {пользователь} {тип} | {inter.guild}", icon_url=inter.guild.icon.url)

        if тип == "Браки":
            collection = cluster.sweetness.history_marry
            history_marry = collection.find_one({"_id": str(пользователь.id)})

            if not history_marry:
                collection.insert_one({"_id": str(пользователь.id), "tip_data": [], "user": [], "brakov": 0})

            if collection.find_one({"_id": str(пользователь.id)})["tip_data"] == []:
                embed.description = f"{inter.author.mention}, у пользователя {пользователь.mention} нет истории переводов"
                return await inter.send(embed = embed)
            all_brak = history_marry.get("brakov", 0)
            embed.description = f"За все время **{all_brak}**"

            tip_data = history_marry.get("tip_data", ["-"])
            ispolnitel = history_marry.get("user", ["-"])

        if тип == "Переводы":
            if cluster.sweetness.history_transactions.count_documents({"_id": str(пользователь.id)}) == 0: 
                cluster.sweetness.history_transactions.insert_one({"_id": str(пользователь.id), "tip_data": [], "punishment": [], "moderator": [], "perevodov": 0, "pereveli": 0})
            if cluster.sweetness.history_transactions.find_one({"_id": str(пользователь.id)})["tip_data"] == []:
                embed.description = f"{inter.author.mention}, у пользователя {пользователь.mention} нет истории переводов"
                return await inter.send(embed = embed)
            result = cluster.sweetness.history_transactions.find_one({"_id": str(пользователь.id)})

            perevodov = result.get("perevodov", 0)
            pereveli = result.get("pereveli", 0)

            embed.description = f"За все время **{perevodov}** переводов **{pereveli}** перевели"

            tip_data = result.get("tip_data", ["-"])
            reason = result.get("msg_sum", ["-"])
            ispolnitel = result.get("moderator", ["-"])

        if тип == "Наказания":
            with open("time_day.json", "r") as f:
                moder = json.load(f)

            history_punishment = cluster.sweetness.history_punishment.find_one({"_id": str(пользователь.id)})
            history_add = cluster.sweetness.history_add.find_one({"_id": str(пользователь.id)})

            if not history_punishment:
                cluster.sweetness.history_punishment.insert_one({"_id": str(пользователь.id),"warns": 0,"mutes": 0,"bans": 0,"eventban": 0})

            if not history_add:
                cluster.sweetness.history_add.insert_one({"_id": str(пользователь.id), "tip_data": [], "punishment": [], "moderator": []})
                
            if cluster.sweetness.history_add.find_one({"_id": str(пользователь.id)})["tip_data"] == []:
                embed.description = f"{inter.author.mention}, у пользователя {пользователь.mention} нет нарушений"
                return await inter.send(embed = embed)
            
            all_bans = history_punishment.get("bans", 0)
            all_mute = history_punishment.get("mutes", 0)
            all_warns = history_punishment.get("warns", 0)
            active_warns = history_punishment.get("warns", 0)

            if str(пользователь.id) in moder[str(inter.guild.id)]["warn1"]:
                D = int(moder[str(inter.guild.id)]["warn1"][str(пользователь.id)])
                N = f"{D // hour}ч. {(D - (D // hour * hour)) // 60}м."
            else:
                N = "-"

            embed.description = f"За все время **{all_bans}** банов **{all_mute}** мутов **{all_warns}** варнов\nДо истечения последнего варна: {N}\nАктивных варнов: **{active_warns}**"

            tip_data = history_add.get("tip_data", ["-"])
            reason = history_add.get("punishment", ["-"])
            ispolnitel = history_add.get("moderator", ["-"])

        cluster.sweetness.history_target.update_one({"_id": str(inter.author.id)},{"$set": {"history": тип}}, upsert=True)

        items_per_page = 10
        current_history_page = currentHistoryPage.setdefault(str(inter.author.id), 0)

        pages = [tip_data[i:i + items_per_page] for i in range(0, len(tip_data), items_per_page)]
        pages2 = [ispolnitel[i:i + items_per_page] for i in range(0, len(ispolnitel), items_per_page)]

        description = "\n".join(f"**{tip}**" for tip in pages[current_history_page][:10])
        embed.add_field(name="  Тип/Дата  ", value=description)

        try:
            pages1 = [reason[i:i + items_per_page] for i in range(0, len(reason), items_per_page)]
            description1 = "\n".join(reasons for reasons in pages1[current_history_page][:10])
            embed.add_field(name="  Причина/Время  ", value=description1)
        except:
            pass

        description2 = "\n".join(f"<@{ispolnitel}>" for ispolnitel in pages2[current_history_page][:10] if ispolnitel != "-")
        embed.add_field(name="  Исполнитель  ", value=description2)

        embed.set_footer(text=f"Страница {current_history_page + 1} из {len(pages)}", icon_url="https://cdn.discordapp.com/attachments/1091732133111939135/1109845138764738653/menu.png")
        await inter.send(content=inter.author.mention, embed=embed, view=ButtonsHistory(inter.author.id))

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        custom_id = inter.component.custom_id
        if custom_id.startswith("history"):
            пользователь = utils.get(inter.guild.members, id=profile_user[inter.author.id])
    
            with open("time_day.json", "r") as f:
                moder = json.load(f)
    
            if "Браки" in custom_id:
                collection = cluster.sweetness.history_marry
                history_data = collection.find_one({"_id": str(пользователь.id)})
                tip_data = history_data.get("tip_data", ["-"])
                ispolnitel = history_data.get("user", ["-"])
                all_bans = 0
                all_mute = 0
                all_warns = 0
                active_warns = 0
                D = 0
            elif "Переводы" in custom_id:
                result = cluster.sweetness.history_transactions.find_one({"_id": str(пользователь.id)})
                tip_data = result.get("tip_data", ["-"])
                reason = result.get("msg_sum", ["-"])
                ispolnitel = result.get("moderator", ["-"])
                all_bans = 0
                all_mute = 0
                all_warns = 0
                active_warns = 0
                D = 0
            elif "Наказания" in custom_id:
                result = cluster.sweetness.history_punishment.find_one({"_id": str(пользователь.id)})
                history_add = cluster.sweetness.history_add.find_one({"_id": str(пользователь.id)})
                tip_data = history_add.get("tip_data", ["-"])
                reason = history_add.get("punishment", ["-"])
                ispolnitel = history_add.get("moderator", ["-"])
                all_bans = result.get("bans", 0)
                all_mute = result.get("mutes", 0)
                all_warns = result.get("warns", 0)
                active_warns = result.get("warns", 0)
                D = int(moder[str(inter.guild.id)]["warn1"].get(str(пользователь.id), 0))
    
            N = f"**{D // hour}ч. {(D % hour) // 60}м.**" if D else "-"
    
            embed = Embed(color=3092790)
            embed.set_thumbnail(url=пользователь.display_avatar.url)
            embed.description = f"За все время **{all_bans}** банов **{all_mute}** мутов **{all_warns}** варнов\nДо истечения последнего варна: {N}\nАктивных варнов: **{active_warns}**"
    
            items_per_page = 10

            if not str(inter.author.id) in currentHistoryPage:
                currentHistoryPage[str(inter.author.id)] = 0

            pages = [tip_data[i:i + items_per_page] for i in range(0, len(tip_data), items_per_page)]
    
            if custom_id == "history_first_page":
                currentHistoryPage[str(inter.author.id)] = 0
            elif custom_id == "history_prev_page" and currentHistoryPage[str(inter.author.id)] > 0:
                currentHistoryPage[str(inter.author.id)] -= 1
            elif custom_id == "history_exit":
                return await inter.message.delete()
            elif custom_id == "history_right_page":
                if currentHistoryPage[str(inter.author.id)] < len(pages) - 1:
                    currentHistoryPage[str(inter.author.id)] += 1
            elif custom_id == "history_last_page":
                currentHistoryPage[str(inter.author.id)] = len(pages) - 1
    
            description = "\n".join(f"**{tip}**" for tip in tip_data[currentHistoryPage[str(inter.author.id)] * items_per_page: (currentHistoryPage[str(inter.author.id)] + 1) * items_per_page])
            embed.add_field(name="`  Тип/Дата  `", value=description)
    
            if "Наказания" in custom_id:
                pages1 = [reason[i:i + items_per_page] for i in range(0, len(reason), items_per_page)]
                description1 = "\n".join(reasons for reasons in pages1[currentHistoryPage[str(inter.author.id)]][:10])
                embed.add_field(name="`  Причина/Время  `", value=description1)
    
            description2 = "\n".join(f"<@{ispolnitel}>" for ispolnitel in ispolnitel[currentHistoryPage[str(inter.author.id)] * items_per_page: (currentHistoryPage[str(inter.author.id)] + 1) * items_per_page] if ispolnitel != "-")
            embed.add_field(name="`  Исполнитель  `", value=description2)
    
            embed.set_footer(text=f"Страница {currentHistoryPage[str(inter.author.id)] + 1} из {len(pages)}",
                                icon_url="https://cdn.discordapp.com/attachments/1091732133111939135/1109845138764738653/menu.png")
            embed.set_author(name=f"История {пользователь} | {inter.guild}", icon_url=inter.guild.icon.url)
            await inter.response.edit_message(embed=embed, view=ButtonsHistory(inter.author.id))

def setup(bot): 
    bot.add_cog(History_cog(bot))