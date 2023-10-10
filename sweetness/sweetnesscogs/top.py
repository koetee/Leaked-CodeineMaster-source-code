import pymongo
import disnake
import json
from disnake.ext import commands
from disnake import Localized
from disnake.enums import ButtonStyle, TextInputStyle

cluster = pymongo.MongoClient(f"mongodb://127.0.0.1/myFirstDatabase?retryWrites=true&w=majority")

files = cluster.sweetness.files

currentTopPage = {}
selectTop = {}

min = 60
hour = 60 * 60
day = 60 * 60 * 24

class TopList(disnake.ui.View):
    def __init__(self, author: int):
        super().__init__()
        if not str(author) in currentTopPage or currentTopPage[str(author)] == 0:
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="top_first_page", emoji=f"{files.find_one({'_id': 'double_left'})['emoji_take']}", disabled = True))
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="top_prev_page", emoji=f"{files.find_one({'_id': 'left'})['emoji_take']}", disabled = True))
        else:
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="top_first_page", emoji=f"{files.find_one({'_id': 'double_left'})['emoji_take']}"))
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="top_prev_page", emoji=f"{files.find_one({'_id': 'left'})['emoji_take']}"))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="top_exit", emoji=f"{files.find_one({'_id': 'basket'})['emoji_take']}"))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="top_right_page", emoji=f"{files.find_one({'_id': 'right'})['emoji_take']}"))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="top_last_page", emoji=f"{files.find_one({'_id': 'double_right'})['emoji_take']}"))

class ActionListDropdown(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Выберите категорию топа",
            options = [
                disnake.SelectOption(label="Баланс", value = "top_balance_main", description="Топ по балансу", emoji=f"<:amitobal:1158567849707716708>"),
                disnake.SelectOption(label="Сообщения", value = "top_message_main", description="Топ по сообщениям", emoji=f"<:smsonline:1153488350821503058>"),
                disnake.SelectOption(label="Онлайн", value = "top_online_main", description="Топ по онлайну", emoji=f"<:clock11:1111709651109695560>"),
                disnake.SelectOption(label="Лав румы", value = "top_love_main", description="Топ по лав румам", emoji=f"<:clock11:1111709651109695560>"),
                disnake.SelectOption(label="Репутация", value = "top_rep_main", description="Топ по репутации", emoji=f"<:clock11:1111709651109695560>"),
            ],
        )

class TopListRoomViewBalance(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ActionListDropdown())
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="Выход", custom_id="exit_profile", emoji=f"{files.find_one({'_id': 'basket'})['emoji_take']}"))

async def get_member_ids(collection_name, key):
    membersID = []
    collection = cluster.sweetness[collection_name]
    cursor = collection.find().sort(key, -1)
    for document in cursor:
        membersID.append(document["_id"])
    return membersID

class topcog(commands.Cog):
    def __init__(self, bot: commands.Bot(intents = disnake.Intents.all(), command_prefix = "!")):
        self.bot = bot

    @commands.slash_command(description="Выберите топ, который вы хотите посмотреть")
    async def top(inter, выбери: str = commands.Param(choices=[
        Localized("Баланс", key="A"),
        Localized("Сообщения", key="B"),
        Localized("Онлайн", key="C"),
        Localized("Лав румы", key="D"),
        Localized("Репутация", key="F"),
    ])):
        await inter.response.defer()
        idd = 1
        description = ""
        items_per_page = 10
        selectTop[str(inter.author.id)] = выбери
    
        if str(inter.author.id) not in currentTopPage:
            currentTopPage[str(inter.author.id)] = 0
    
        if выбери == "Баланс":
            collection_name = "economy"
            output = "balance"
            emoji=f"<:amitobal:1158567849707716708> "
            membersID = await get_member_ids("economy", "balance")
        elif выбери == "Сообщения":
            collection_name = "message"
            output = "message_count"
            emoji=f"<:smsonline:1153488350821503058>"
            membersID = await get_member_ids("message", "message_count")
        elif выбери == "Онлайн":
            collection_name = "online"
            output = "online"
            emoji=f"<:clock:1096090255402221658>"
            membersID = await get_member_ids("online", "online")
        elif выбери == "Лав румы":
            collection_name = "love_online"
            output = "Love_online"
            emoji=f"<:clock:1096090255402221658>"
            membersID = await get_member_ids("love_online", "Love_online")
        elif выбери == "Репутация":
            collection_name = "reputation"
            output = "rep"
            emoji=f"<:clock:1096090255402221658>"
            membersID = await get_member_ids("reputation", "rep")
    
        pages = [membersID[i:i + items_per_page] for i in range(0, len(membersID), items_per_page)]

        emoji_numbers = [
            "<:11:1138468003026059325>", "<:21:1138800607931674744>",
            "<:31:1138467999012110367>", "<:four:1151556783207366706>",
            "<:five:1151556781550612541>", "<:six:1151556790367035502>",
            "<:seven:1151556787741409480>", "<:eight:1151556778983690342>",
            "<:nine:1151556784675360920>", "<:ten:1151556792430624839>"
        ]


        if выбери in ["Онлайн", "Лав румы"]:
            for member_id in pages[0]:
                collection = cluster.sweetness[collection_name]
                N = collection.find_one({"_id": str(member_id)})[output]
                emoji_number = emoji_numbers[idd - 1] if 0 <= idd <= len(emoji_numbers) else ""
                description += f"**{emoji_number} — <@{member_id}>** {emoji} **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                idd += 1
        else:
            for member_id in pages[0]:
                collection = cluster.sweetness[collection_name]
                N = collection.find_one({"_id": str(member_id)})[output]
                emoji_number = emoji_numbers[idd - 1] if 0 <= idd <= len(emoji_numbers) else ""
                description += f"**{emoji_number} — <@{member_id}>** {emoji} {N}\n\n"
                idd += 1

        embed = disnake.Embed(description=description, color=3092790)
        embed.set_author(name = f"📋 Топ по {выбери}", icon_url = inter.guild.icon.url)
        embed.set_thumbnail(url=inter.author.display_avatar.url)
        embed.set_footer(text=f"Запросил(а) {inter.author}", icon_url=inter.author.display_avatar.url)
        return await inter.send(content=inter.author.mention, embed=embed, view=TopList(inter.author.id))
    
    @commands.Cog.listener()
    async def on_button_click(self, inter):
        custom_id = inter.component.custom_id
        if custom_id[:3] == "top":
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description=f"{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**", color=3092790)
                embed.set_author(name = "Топы", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url=inter.author.display_avatar.url)
                return await inter.send(ephemeral=True, embed=embed)

            idd = 1
            items_per_page = 10
            выбери = selectTop[str(inter.author.id)]

            if str(inter.author.id) not in currentTopPage:
                currentTopPage[str(inter.author.id)] = 0

            top_options = {
                "Баланс": ("economy", "balance", "<:amitobal:1158567849707716708> "),
                "Сообщения": ("message", "message_count", "<:smsonline:1153488350821503058>"),
                "Онлайн": ("online", "online", "<:clock:1096090255402221658>"),
                "Личные Комнаты": ("room_online", "day", "<:clock:1096090255402221658>"),
                "Репутация": ("reputation", "rep", "<:clock:1096090255402221658>"),
                "Лав румы": ("love_online", "Love_online", "<:clock:1096090255402221658>")
            }

            if выбери in top_options:
                collection_name, output, emoji = top_options[выбери]
                membersID = await get_member_ids(collection_name, output)
            else:
                # Handle invalid выбери value here
                return

            pages = [membersID[i:i + items_per_page] for i in range(0, len(membersID), items_per_page)]

            embed = disnake.Embed(description = "", color=3092790)

            if not str(inter.author.id) in currentTopPage:
                currentTopPage[str(inter.author.id)] = 0
            if custom_id == "top_first_page":
                currentTopPage[str(inter.author.id)] = 0
            if custom_id == "top_prev_page":
                if currentTopPage[str(inter.author.id)] > 0:
                    currentTopPage[str(inter.author.id)] -= 1
            if custom_id == "top_exit":
                return await inter.message.delete()
            if custom_id == "top_right_page":
                if currentTopPage[str(inter.author.id)] < len(pages) - 1:
                    currentTopPage[str(inter.author.id)] += 1
            if custom_id == "top_last_page":
                currentTopPage[str(inter.author.id)] = len(pages) - 1

            emoji_numbers = [
                "<:11:1138468003026059325>", "<:21:1138800607931674744>",
                "<:31:1138467999012110367>", "<:four:1151556783207366706>",
                "<:five:1151556781550612541>", "<:six:1151556790367035502>",
                "<:seven:1151556787741409480>", "<:eight:1151556778983690342>",
                "<:nine:1151556784675360920>", "<:ten:1151556792430624839>"
            ]

            if выбери in ["Онлайн", "Лав румы"]:
                for member_id in pages[currentTopPage[str(inter.author.id)]]:
                    if currentTopPage[str(inter.author.id)] > 0:
                        emoji_number = idd + (currentTopPage[str(inter.author.id)] * items_per_page)
                    else:
                        emoji_number = emoji_numbers[idd - 1] if 0 <= idd <= len(emoji_numbers) else ""
                    collection = cluster.sweetness[collection_name]
                    N = collection.find_one({"_id": str(member_id)})[output]
                    embed.description += f"**{emoji_number} — <@{member_id}>** {emoji} **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    idd += 1
            else:
                for member_id in pages[currentTopPage[str(inter.author.id)]]:
                    if currentTopPage[str(inter.author.id)] > 0:
                        emoji_number = idd + (currentTopPage[str(inter.author.id)] * items_per_page)
                    else:
                        emoji_number = emoji_numbers[idd - 1] if 0 <= idd <= len(emoji_numbers) else ""
                    collection = cluster.sweetness[collection_name]
                    N = collection.find_one({"_id": str(member_id)})[output]
                    embed.description += f"**{emoji_number} — <@{member_id}>** {emoji} {N}\n\n"
                    idd += 1
                    
            embed.set_author(name = f"📋 Топ по {выбери}", icon_url = inter.guild.icon.url)
            embed.set_thumbnail(url=inter.author.display_avatar.url)
            embed.set_footer(text=f"Запросил(а) {inter.author}", icon_url=inter.author.display_avatar.url)
            return await inter.response.edit_message(content=inter.author.mention, embed=embed, view=TopList(inter.author.id))
    
def setup(bot): 
    bot.add_cog(topcog(bot))