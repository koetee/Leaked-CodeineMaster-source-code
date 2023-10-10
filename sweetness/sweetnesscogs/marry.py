import pymongo
import disnake
import datetime
import json
import random
from disnake import utils, Embed
from disnake.ext import commands
from disnake.enums import ButtonStyle, TextInputStyle

love_role = 1149818927770238996
intermessage_id = {}
cluster = pymongo.MongoClient(f"mongodb://127.0.0.1/myFirstDatabase?retryWrites=true&w=majority")

files = cluster.sweetness.files
database = cluster.sweetness

class MarryYes(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, emoji=f'{files.find_one({"_id": "accept"})["emoji_take"]}', custom_id = 'yesmarry'))
        self.add_item(disnake.ui.Button(style = disnake.ButtonStyle.secondary, emoji=f'{files.find_one({"_id": "decline"})["emoji_take"]}', custom_id = 'nomarry'))

class marry_cog(commands.Cog):
    def __init__(self, bot: commands.Bot(intents = disnake.Intents.all(), command_prefix = 'marry!')):
        self.bot = bot
    @commands.slash_command(description='Пожениться')
    async def marry(self, inter, пользователь: disnake.Member):
        economy_collection = database.economy
        marry_collection = database.marry
        history_marry_collection = database.history_marry

        author_id = str(inter.author.id)
        user_id = str(пользователь.id)

        if economy_collection.count_documents({"_id": author_id}) == 0:
            economy_collection.insert_one({"_id": author_id, "balance": 0})
        if economy_collection.count_documents({"_id": user_id}) == 0:
            economy_collection.insert_one({"_id": user_id, "balance": 0})

        if marry_collection.count_documents({"_id": author_id}) == 0:
            marry_collection.insert_one({"_id": author_id, "love": "Отсутствует"})
        if marry_collection.count_documents({"_id": user_id}) == 0:
            marry_collection.insert_one({"_id": user_id, "love": "Отсутствует"})

        if пользователь == inter.author:
            embed = Embed(description=f'{inter.author.mention}, **Нельзя** жениться на **себе**!', color=3092790)
            embed.set_author(name = "Брак", icon_url=inter.guild.icon.url)
            embed.set_thumbnail(url=inter.author.display_avatar.url)
            return await inter.send(embed=embed)

        author_balance = economy_collection.find_one({"_id": author_id})["balance"]
        if author_balance < 1500:
            needed_balance = 1500 - author_balance
            embed = Embed(description=f'{inter.author.mention}, У **Вас** на балансе **недостаточно средств**!\nНехватает: **{needed_balance}** <:amitobal:1158567849707716708>', color=3092790)
            embed.set_author(name = "Брак", icon_url=inter.guild.icon.url)
            embed.set_thumbnail(url=inter.author.display_avatar.url)
            return await inter.send(embed=embed)

        if пользователь != inter.author:
            if marry_collection.find_one({'_id': author_id})['love'] == "Отсутствует":
                if marry_collection.find_one({'_id': user_id})['love'] == "Отсутствует":
                    embed = Embed(description=f'**Всё**, что мне когда-либо **требовалось в женщине**, я **нашел в тебе**.. и не могу **позволить**, чтобы другой человек, не я, когда-нибудь **заботился о тебе**. \
                                  Ты станешь **моей женой?**\n\n{inter.author.mention} сделал **предложение руки и сердца** {пользователь.mention}, мы в **предвкушении..!!**', color=3092790)
                    embed.set_author(name = "Брак", icon_url=inter.guild.icon.url)
                    embed.set_image(url='https://i.ytimg.com/vi/wSU81YVVOq0/hqdefault.jpg')
                    await inter.send(content=пользователь.mention, embed=embed, view=MarryYes())
                    intermessage_id[str(пользователь.id)] = inter.author.id
                else:
                    embed = Embed(description=f'{inter.author.mention}, **Этот** пользователь **уже состоит** в браке!', color=3092790)
                    embed.set_author(name = "Брак", icon_url=inter.guild.icon.url)
                    embed.set_thumbnail(url=inter.author.display_avatar.url)
                    return await inter.send(embed=embed)
            else:
                embed = Embed(description=f'{inter.author.mention}, **Вы** уже состоите в **браке**!', color=3092790)
                embed.set_author(name = "Брак", icon_url=inter.guild.icon.url)
                embed.set_thumbnail(url=inter.author.display_avatar.url)
                return await inter.send(embed=embed)

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        custom_id = inter.component.custom_id
        if custom_id.endswith("marry"):
            history_marry_collection = database.history_marry
            marry_collection = database.marry
            author_id = str(inter.author.id)
            author = inter.author
            пользователь = utils.get(inter.guild.members, id=int(intermessage_id[str(inter.author.id)]))
            user_id = str(пользователь.id)

            await inter.response.defer()

            if not inter.message.content == inter.author.mention:
                embed = Embed(description=f'{inter.author.mention}, **Вы** не можете использовать **чужие кнопки!**', color=3092790)
                embed.set_author(name = "Брак", icon_url=inter.guild.icon.url)
                embed.set_thumbnail(url=inter.author.display_avatar.url)
                return await inter.send(ephemeral=True, embed=embed)

            if custom_id == 'yesmarry':
                embed = Embed(color=3092790)
                embed.set_author(name = "Брак", icon_url=inter.guild.icon.url)
                embed.add_field(name='АПЛОДИРУЕМ, ВЕДЬ', value=f'{inter.author.mention} **и** {пользователь.mention} __**новая пара нашего сервера!**__')
                embed.set_footer(text='Стоимость брака: 1500')
                embed.set_image(url=random.choice([
                    "https://i.pinimg.com/originals/6f/3c/3c/6f3c3c46d748327e47a431b125943f7b.gif",
                    "https://i.pinimg.com/originals/91/6b/e6/916be6f230ccebe3faeade6b94f9eecc.gif",
                    "https://i.pinimg.com/originals/16/8b/da/168bda7633d3bf55215a8807690cbab3.gif",
                    "https://i.pinimg.com/originals/cf/26/86/cf2686f3951799742f0f279c4c7ca966.gif",
                    "https://i.pinimg.com/originals/62/4a/ef/624aef5526dff41cea125e0648938078.gif",
                    "https://i.pinimg.com/originals/18/c7/53/18c753a9afe7b9456f8cdbbfe75c7253.gif",
                    "https://i.pinimg.com/originals/5d/9d/94/5d9d942d786dfd13b68fa0b7a862e7ba.gif",
                    "https://i.pinimg.com/originals/67/31/e4/6731e4386531bbc0d4c26d7d56e14b30.gif"
                ]))
                await inter.message.edit(embed=embed, components=[])

                if history_marry_collection.count_documents({"_id": author_id}) == 0:
                    history_marry_collection.insert_one({"_id": author_id, "tip_data": [], "user": [], "brakov": 0})

                if history_marry_collection.count_documents({"_id": user_id}) == 0:
                    history_marry_collection.insert_one({"_id": user_id, "tip_data": [], "user": [], "brakov": 0})

                history_marry_collection.update_one({"_id": author_id},{"$push": {"tip_data": f"Заключил(а) | `{datetime.datetime.now().strftime('%d.%m.%Y')}`"}})
                history_marry_collection.update_one({"_id": author_id}, {"$push": {"user": int(user_id)}})

                history_marry_collection.update_one({"_id": user_id},{"$push": {"tip_data": f"Заключил(а) | `{datetime.datetime.now().strftime('%d.%m.%Y')}`"}})
                history_marry_collection.update_one({"_id": user_id}, {"$push": {"user": int(author_id)}})

                history_marry_collection.update_one({"_id": user_id}, {"$inc": {"brakov": +1}})
                history_marry_collection.update_one({"_id": author_id}, {"$inc": {"brakov": +1}})

                marry_collection.update_one({'_id': author_id}, {'$set': {'love': str(user_id)}}, upsert=True)
                marry_collection.update_one({'_id': user_id}, {'$set': {'love': str(author_id)}}, upsert=True)
                marry_collection.update_one({'_id': author_id}, {'$set': {'Time': datetime.datetime.now().strftime("%d.%m.%Y")}}, upsert=True)
                marry_collection.update_one({'_id': user_id}, {'$set': {'Time': datetime.datetime.now().strftime("%d.%m.%Y")}}, upsert=True)
                marry_collection.update_one({'_id': author_id}, {'$set': {'Online': 'Offline'}}, upsert=True)
                marry_collection.update_one({'_id': user_id}, {'$set': {'Online': 'Offline'}}, upsert=True)
                marry_collection.update_one({'_id': author_id}, {'$set': {'balance': 0}}, upsert=True)
                marry_collection.update_one({'_id': user_id}, {'$set': {'balance': 0}}, upsert=True)
                database.love_online.update_one({'_id': author_id}, {'$set': {'Love_online': 0}}, upsert=True)
                database.love_online.update_one({'_id': user_id}, {'$set': {'Love_online': 0}}, upsert=True)

                new_date = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(days=30)

                cluster.sweetness.love_plata.update_one({'_id': str(author_id)}, {'$set': {'time': new_date}}, upsert = True)
                cluster.sweetness.love_plata.update_one({'_id': str(user_id)}, {'$set': {'time': new_date}}, upsert = True)

                cluster.sweetness.love_plata.update_one({'_id': str(author_id)}, {'$set': {'notification': "No"}}, upsert = True)
                cluster.sweetness.love_plata.update_one({'_id': str(user_id)}, {'$set': {'notification': "No"}}, upsert = True)

                database.economy.update_one({"_id": str(user_id)}, {"$inc": {"balance": -1500}})
                database.history.update_one({"_id": str(user_id)}, {"$inc": {"loverooms": +1500}})

                await author.add_roles(utils.get(inter.guild.roles, id=love_role))
                return await пользователь.add_roles(utils.get(inter.guild.roles, id=love_role))

            if custom_id == 'nomarry':
                del intermessage_id[author_id]
                embed = disnake.Embed(description=f'{author.mention} **Отказался(ась)** вступать в **брак** с {пользователь.mention}!', color=3092790)
                embed.set_author(name = "Брак", icon_url=inter.guild.icon.url)
                embed.set_thumbnail(url=inter.author.display_avatar.url)
                await inter.message.edit(embed=embed, components=[])

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel and after.channel != before.channel:
            if int(after.channel.id) == 1156694167947317289:
                if database.marry.count_documents({"_id": str(member.id)}) == 0: 
                    database.marry.insert_one({"_id": str(member.id), "love": "Отсутствует"})
                if database.marry.find_one({'_id': str(member.id)})['love'] == "Отсутствует":
                    try:
                        embed = disnake.Embed(description = f'{member.author.mention}, У **Вас** нету **пары**!', color = 3092790)
                        embed.set_author(name = "Любовные комнаты", icon_url=member.guild.icon.url)
                        embed.set_thumbnail(url = member.display_avatar.url)
                        await member.send(embed = embed)
                    except: 
                        pass
                    return await member.move_to(None)
                user = disnake.utils.get(member.guild.members, id = int(database.marry.find_one({'_id': str(member.id)})['love']))
                try: 
                    if user.voice.channel.category_id == 1149340569722695840: 
                        return await member.move_to(user.voice.channel)
                except: 
                    pass

                try: 
                    channel5 = await member.guild.create_voice_channel(name = database.marry.find_one({'_id': str(member.id)})['name'], category = disnake.utils.get(member.guild.categories, id=1142583140330782820))
                except: 
                    channel5 = await member.guild.create_voice_channel(name = f'{user.name} {random.choice(["💙", "💚", "💛", "💜", "💞", "💕", "❤️"])} {member.name}', category = disnake.utils.get(member.guild.categories, id=1142583140330782820))
                await member.move_to(channel5)
                await channel5.set_permissions(member.guild.default_role, connect=False, view_channel=True)
                await channel5.set_permissions(member, connect = True, view_channel = True)
                await channel5.set_permissions(user, connect = True, view_channel = True)
        if before.channel:
            if before.channel.category_id == 1149340569722695840:
                if len(before.channel.members) == 0: 
                    try:
                        if not before.channel.id == 1156694167947317289: 
                            await before.channel.delete()
                    except: 
                        pass
def setup(bot): 
    bot.add_cog(marry_cog(bot))