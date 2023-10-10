import pymongo
import disnake
import datetime
import json
from disnake.utils import get
from disnake.ext import commands
from disnake.enums import ButtonStyle, TextInputStyle
from disnake import Localized

cluster = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/test?retryWrites=true&w=majority")

files = cluster.sweetness.files
database = cluster.sweetness

currentTopPage = {}
selectTop = {}

min = 60
hour = 60 * 60
day = 60 * 60 * 24

async def send_top_page(self, inter, author, page_number):
    idd = 1
    items_per_page = 10
    выбери = selectTop.get(str(author.id))

    if выбери is None:
        return

    top_options = {
        "Онлайн": ("clan_online", "clan_online", "<:online:1109846973378470050>"),
        "Онлайн участников": ("clanonline", "online", "<:online:1109846973378470050>"),
        "Рейтинг": ("clan_rating", "rating", "<:top:1096087524985810964>"),
        "Боевая мощь": ("clan_online", "clan_online", "<:attack:1139675138334412880>")
    }

    if выбери not in top_options:
        return

    collection_name, output, emoji = top_options[выбери]
    collection = database[collection_name]
    membersID = await get_member_ids(collection_name, output)

    pages = [membersID[i:i + items_per_page] for i in range(0, len(membersID), items_per_page)]

    emoji_numbers = [
        "<:11:1138468003026059325>", "<:21:1138800607931674744>",
        "<:31:1096126525683810465>", "<:41:1096126532826697909>",
        "<:51:1097534359675879515>", "<:61:1107004738194653246>",
        "<:71:1107004742326034593>", "<:81:1107004743815008328>",
        "<:91:1107004746822328350>", "<:101:1107004740723802112>"
    ]

    description = ""
    for member_id in pages[page_number]:
        N = collection.find_one({"_id": str(member_id)})[output]
        emoji_number = emoji_numbers[idd - 1] if 0 <= idd <= len(emoji_numbers) else ""
        if выбери in ["Онлайн участников"]:
            description += f"**{emoji_number} — <@{member_id}>** {emoji} **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
        else:
            description += f"**{emoji_number} — <@&{member_id}>** {emoji} {N}\n\n"
        idd += 1
    

    embed = disnake.Embed(description=description, color=3092790)
    embed.set_author(name=f"📋 Топ кланов по {выбери}", icon_url=author.display_avatar.url)
    embed.set_thumbnail(url=author.display_avatar.url)
    embed.set_footer(text=f"Запросил(а) {author}", icon_url=author.display_avatar.url)
    await inter.response.edit_message(embed = embed, view=TopList(author.id))


class TopList(disnake.ui.View):
    def __init__(self, author: int):
        super().__init__()
        if not str(author) in currentTopPage or currentTopPage[str(author)] == 0:
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="top_first_page", emoji=f"<:back:1008774480778252539>", disabled = True))
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="top_prev_page", emoji=f"<:zxc5:1009168367342587915>", disabled = True))
        else:
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="top_first_page", emoji=f"<:back:1008774480778252539>"))
            self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="top_prev_page", emoji=f"<:zxc5:1009168367342587915>"))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.red, custom_id="top_exit", emoji=f"<:basket:1138812689502699680>"))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="top_right_page", emoji=f"<:zxc4:1009168369112600728>"))
        self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="top_last_page", emoji=f"<:zxc7:1009168365627125861>"))

async def get_member_ids(collection_name, key):
    membersID = []
    collection = database[collection_name]
    cursor = collection.find().sort(key, -1)
    for document in cursor:
        membersID.append(document["_id"])
    return membersID

class clan_top(commands.Cog):
    def __init__(self, bot: commands.Bot(intents = disnake.Intents.all(), command_prefix = 'clan_top!')):
        self.bot = bot

    @commands.slash_command(description="Выберите топ, который вы хотите посмотреть")
    async def clan_top(inter, выбери: str = commands.Param(choices=[
        Localized("Онлайн", key="A"),
        Localized("Онлайн участников", key="A"),
        Localized("Рейтинг", key="A"),
        Localized("Боевая мощь", key="A"),
        Localized("Количество участников", key="A"),
    ])):
        idd = 1
        description = ""
        items_per_page = 10
        selectTop[str(inter.author.id)] = выбери
    
        if str(inter.author.id) not in currentTopPage:
            currentTopPage[str(inter.author.id)] = 0
    
        match str(выбери):
            case "Онлайн":
                collection_name = "clan_online"
                output = "clan_online"
                emoji = "<:online:1109846973378470050>"
                membersID = await get_member_ids("clan_online", "clan_online")

            case "Онлайн участников":
                collection_name = "clanonline"
                output = "online"
                emoji = "<:online:1109846973378470050>"
                membersID = await get_member_ids("clanonline", "online")

            case "Рейтинг":
                collection_name = "clan_rating"
                output = "rating"
                emoji = "<:top:1096087524985810964>"
                membersID = await get_member_ids("clan_rating", "rating")

            case "Боевая мощь":
                emoji = "<:attack:1139675138334412880>"

            case "Количество участников":
                emoji = "<:staff:1096087520023945417>"
        try:
            pages = [membersID[i:i + items_per_page] for i in range(0, len(membersID), items_per_page)]
            collection = cluster.sweetness[collection_name]
        except:
            pass

        emoji_numbers = [
            "<:11:1138468003026059325>", "<:21:1138800607931674744>",
            "<:31:1096126525683810465>", "<:41:1096126532826697909>",
            "<:51:1097534359675879515>", "<:61:1107004738194653246>",
            "<:71:1107004742326034593>", "<:81:1107004743815008328>",
            "<:91:1107004746822328350>", "<:101:1107004740723802112>"
        ]
        await inter.response.defer()

        match str(выбери):
            case "Онлайн":
                for clanxd in pages[0]:
                    N = collection.find_one({"_id": str(clanxd)})[output]
                    emoji_number = emoji_numbers[idd - 1] if 0 <= idd <= len(emoji_numbers) else ""
                    description += f"**{emoji_number} — <@&{clanxd}>** {emoji} **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    idd += 1

            case "Онлайн участников":
                for member_id in pages[0]:
                    N = collection.find_one({"_id": str(member_id)})[output]
                    emoji_number = emoji_numbers[idd - 1] if 0 <= idd <= len(emoji_numbers) else ""
                    description += f"**{emoji_number} — <@{member_id}>** {emoji} **{N // hour}**ч. **{(N - (N // hour * hour)) // 60}**м.\n\n"
                    idd += 1
  
            case "Количество участников":
                clans = []
                membersID = []

                for clan_data in database.clan_online.find():
                    clanxd = clan_data["_id"]
                    role_take = disnake.utils.get(inter.guild.roles, id=int(clanxd))
                    members = len(role_take.members)
                    clans.append({"clanxd": clanxd, "members": int(members)})

                filtered_clans = [clan_data for clan_data in clans if "members" in clan_data and isinstance(clan_data["members"], int)]
                sorted_clans = sorted(filtered_clans, key=lambda x: x["members"], reverse=True)

                for clan_data in sorted_clans:
                    membersID.append(clan_data["clanxd"])
                pages = [membersID[i:i + items_per_page] for i in range(0, len(membersID), items_per_page)]
                for clanxd in pages[0]:
                    for clan_data in clans:
                        if str(clan_data["clanxd"]) == str(clanxd):
                            members = clan_data.get("members")
                            break
                    emoji_number = emoji_numbers[idd - 1] if 0 <= idd <= len(emoji_numbers) else ""
                    description += f"**{emoji_number} — <@&{clanxd}>** {emoji} {members}\n\n"
                    idd += 1

            case "Боевая мощь":
                clans = []
                powers = []
                membersID = []

                for clan_data in database.clan_online.find():
                    clanxd = clan_data["_id"]
                    clan_heroes = len(cluster.sweetness.clan_heroes.find_one({'_id': str(clanxd)})['heroes'])
                    voice_members = 1
                    role_take = disnake.utils.get(inter.guild.roles, id=int(clanxd))
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

                    clans.append({"clanxd": clanxd, "power": int(power)})

                filtered_clans = [clan_data for clan_data in clans if "power" in clan_data and isinstance(clan_data["power"], int)]

                sorted_clans = sorted(filtered_clans, key=lambda x: x["power"], reverse=True)

                for clan_data in sorted_clans:
                    membersID.append(clan_data["clanxd"])
                pages = [membersID[i:i + items_per_page] for i in range(0, len(membersID), items_per_page)]
                for clanxd in pages[0]:
                    for clan_data in clans:
                        if str(clan_data["clanxd"]) == str(clanxd):
                            power = clan_data.get("power")
                            break
                    emoji_number = emoji_numbers[idd - 1] if 0 <= idd <= len(emoji_numbers) else ""
                    description += f"**{emoji_number} — <@&{clanxd}>** {emoji} {power}\n\n"
                    idd += 1

        embed = disnake.Embed(description=description, color=3092790)
        embed.set_author(name = f"📋 Топ кланов по {выбери}", icon_url = inter.guild.icon.url)
        embed.set_thumbnail(url=inter.author.display_avatar.url)
        embed.set_footer(text=f"Запросил(а) {inter.author}", icon_url=inter.author.display_avatar.url)
        return await inter.send(content=inter.author.mention, embed=embed, view=TopList(inter.author.id))

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        custom_id = inter.component.custom_id

        with open('clan_sweetness.json','r', encoding='utf-8') as f:
            clan = json.load(f)

        if custom_id.startswith("top"):
            if not inter.message.content == inter.author.mention:
                embed = disnake.Embed(description=f"{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**", color=3092790)
                embed.set_author(name = "Топы", icon_url = inter.guild.icon.url)
                embed.set_thumbnail(url=inter.author.display_avatar.url)
                return await inter.send(ephemeral=True, embed=embed)

            idd = 1
            items_per_page = 10
            выбери = selectTop.get(str(inter.author.id))

            if выбери is None:
                return

            top_options = {
                "Онлайн": ("clan_online", "clan_online", "<:online:1109846973378470050>"),
                "Онлайн участников": ("clanonline", "online", "<:online:1109846973378470050>"),
                "Рейтинг": ("clan_rating", "rating", "<:top:1096087524985810964>"),
                "Боевая мощь": ("clan_online", "clan_online", "<:attack:1139675138334412880>")
            }

            if выбери not in top_options:
                return

            collection_name, output, emoji = top_options[выбери]
            collection = database[collection_name]
            membersID = await get_member_ids(collection_name, output)

            pages = [membersID[i:i + items_per_page] for i in range(0, len(membersID), items_per_page)]

            match custom_id:
                case 'top_first_page':
                    currentTopPage[str(inter.author.id)] = 0
                case 'top_prev_page' if currentTopPage[str(inter.author.id)] > 0:
                    currentTopPage[str(inter.author.id)] -= 1
                case 'top_exit':
                    await inter.message.delete()
                case 'top_right_page' if currentTopPage[str(inter.author.id)] < len(pages) - 1:
                    currentTopPage[str(inter.author.id)] += 1
                case 'top_last_page':
                    currentTopPage[str(inter.author.id)] = len(pages) - 1
            page_number = int(currentTopPage[str(inter.author.id)])
            await send_top_page(self, inter, inter.author, page_number)

def setup(bot):
    bot.add_cog(clan_top(bot))