from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pymongo
import random
import os
import datetime
import disnake
import requests
from disnake.ext import commands, tasks
import time
import re
import json
from PIL import Image, ImageDraw, ImageFont

cluster = pymongo.MongoClient(f"mongodb://127.0.0.1/myFirstDatabase?retryWrites=true&w=majority")

files = cluster.sweetness.files

db = cluster["sweetness"]
collection = db["files"]

class EmojiHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        emoji_name = os.path.splitext(os.path.basename(event.src_path))[0]

        db.query.update_one({'_id': str(emoji_name)}, {'$set': {"event_type": "modified"}}, upsert=True)
        db.query.update_one({'_id': str(emoji_name)}, {'$set': {"src_path": event.src_path}}, upsert=True)

    def on_modified(self, event):
        if event.is_directory:
            return

        emoji_name = os.path.splitext(os.path.basename(event.src_path))[0]

        db.query.update_one({'_id': str(emoji_name)}, {'$set': {"event_type": "modified"}}, upsert=True)
        db.query.update_one({'_id': str(emoji_name)}, {'$set': {"src_path": event.src_path}}, upsert=True)

class giveonlcog(commands.Cog):
    def __init__(self, bot: commands.Bot(intents = disnake.Intents.all(), command_prefix = 'tasks!')):
        self.bot = bot

        event_handler = EmojiHandler()
        bserver = Observer()
        bserver.schedule(event_handler, path="images_sweetness/economy")
        bserver.start()

        if not self.files.is_running():
            self.files.start()

        if not self.minysrole.is_running(): self.minysrole.start()
        if not self.giveonline.is_running(): self.giveonline.start()
        #if not self.banner.is_running(): self.banner.start()
        if not self.minyslove.is_running(): self.minyslove.start()
        #if not self.action.is_running(): self.action.start()

    @tasks.loop(seconds=35)
    async def files(self):
        for x in db.query.find():
            try:
                emoji_name = x['_id']

                src_path = db.query.find_one({'_id': str(x['_id'])})['src_path']
                if not collection.count_documents({"_id": str(x['_id'])}) == 0:
                    try:
                        existing_emoji = disnake.utils.get(self.bot.emojis, id = collection.find_one({'_id': str(x['_id'])})['emoji_id'])
                        await existing_emoji.delete(reason="Обновление эмоджи")
                    except:
                        pass
                    guilds = []

                    for guild in self.bot.guilds:
                        if int(guild.owner.id) == 1124362810739146863:
                            if not len(guild.emojis) >= 50:
                                guilds.append(guild.id)
                    if guilds == []:
                        for i in range(10):
                            guild = await self.bot.create_guild(name = "Emoji Creative")
                    else:
                        guild = self.bot.get_guild(random.choice(guilds))
                    with open(src_path, "rb") as emoji_image:
                        new_emoji = await guild.create_custom_emoji(name=emoji_name, image=emoji_image.read(), reason="Добавление нового эмоджи")
                        collection.update_one({'_id': str(emoji_name)}, {'$set': {"emoji_take": f"<:{emoji_name}:{new_emoji.id}>"}}, upsert = True)
                        collection.update_one({'_id': str(emoji_name)}, {'$set': {"emoji_id": f"{new_emoji.id}"}}, upsert = True)
                else:
                    guilds = []
                    for guild in self.bot.guilds:
                        if int(guild.owner.id) == 1124362810739146863:
                            if not len(guild.emojis) >= 50:
                                guilds.append(guild.id)
                    if guilds == []:
                        for i in range(10):
                            guild = await self.bot.create_guild(name = "Emoji Creative")
                    else:
                        guild = self.bot.get_guild(random.choice(guilds))

                    with open(src_path, "rb") as emoji_image:
                        new_emoji = await guild.create_custom_emoji(name=emoji_name, image=emoji_image.read(), reason="Добавление нового эмоджи")
                        collection.update_one({'_id': str(emoji_name)}, {'$set': {"emoji_take": f"<:{emoji_name}:{new_emoji.id}>"}}, upsert = True)
                        collection.update_one({'_id': str(emoji_name)}, {'$set': {"emoji_id": f"{new_emoji.id}"}}, upsert = True)
                db.query.delete_one({'_id': str(emoji_name)})
            except Exception as e:
                try:
                    await self.bot.get_channel(1154463674346508390).send(e)
                except:
                    pass

    @tasks.loop(seconds = 60)
    async def banner(self):
        try:
            im = Image.open('sweetness_banner.png')
            voice_member_online = 0

            guild = self.bot.get_guild(1143903608946045048)

            for member in guild.members:
                try:
                    channel = member.voice.channel.id
                    voice_member_online += 1
                except:
                    pass

            if voice_member_online > 9:
                ImageDraw.Draw(im).text((920, 452), str(voice_member_online), font=ImageFont.truetype('Gordita_bold.ttf', size=50), fill = (255, 255, 255))
            else:
                ImageDraw.Draw(im).text((935, 452), str(voice_member_online), font=ImageFont.truetype('Gordita_bold.ttf', size=50), fill = (255, 255, 255))

            member = disnake.utils.get(guild.members, id = int(cluster.sweetness.channels.find_one({'_id': 1000})['banner']))
            try:
                ImageDraw.Draw(im).text((315, 334), f"{member.name[:11]}..." if len(member.name) > 11 else f"{member.name}", font=ImageFont.truetype('Gordita_bold.ttf', encoding='UTF-8', size = 50), fill = (255, 255, 255))
            except KeyError as e:
                print(e)
 
            symbols = f"{member.activity}"
            pattern = r'<:[^>]+>|<a:[^>]+>'
            new_string, n = re.subn(pattern, '', symbols)
            member_status1 = ''
            member_status2 = ''
            ix = 0

            if symbols == 'None':
                ImageDraw.Draw(im).text((315, 396), str('Статус не установлен.'), font=ImageFont.truetype('Gordita_regular.ttf', encoding='UTF-8', size=25), fill = (255, 255, 255))
            else: 
                if len(str(new_string)) > 27:
                    for s in new_string:
                        if ix > 45:
                            break
                        if ix > 27:
                            member_status2 += s
                        if ix < 27:
                            member_status1 += s
                        ix += 1
                    ImageDraw.Draw(im).text((315, 396), f'{str(member_status1)}', font=ImageFont.truetype('Gordita_regular.ttf', encoding='UTF-8', size=25), fill = (255, 255, 255))
                    ImageDraw.Draw(im).text((315, 420), f'{str(member_status2)}', font=ImageFont.truetype('Gordita_regular.ttf', encoding='UTF-8', size=25), fill = (255, 255, 255))
                else:
                    ImageDraw.Draw(im).text((315, 396), str(new_string), font=ImageFont.truetype('Gordita_regular.ttf', encoding='UTF-8', size=25), fill = (255, 255, 255))

            Image.open(requests.get(member.display_avatar.url, stream=True).raw).resize((162, 165)).save('sweetnes_ava.png')
            mask_im = Image.new("L", Image.open(f"sweetnes_ava.png").size)
            ImageDraw.Draw(mask_im).ellipse((0, 0, 162, 165), fill=255)
            im.paste(Image.open('sweetnes_ava.png'), (128, 334), mask_im)

            im.save('out_banner_sweetnes.png')

            with open('out_banner_sweetnes.png', 'rb') as f:
                await guild.edit(banner=f.read())
        except:
            pass

    @tasks.loop(seconds = 60)
    async def giveonline(self):
        try:
            channels = self.bot.get_guild(1143903608946045048).voice_channels
            for channel in channels:
                for member in channel.members:
                    if not member.bot == True:
                        if cluster.sweetness.online.count_documents({"_id": str(member.id)}) == 0:
                            cluster.sweetness.online.insert_one({"_id": str(member.id), "online": 0})

                        if cluster.sweetness.day.count_documents({"_id": str(member.id)}) == 0:
                            cluster.sweetness.day.insert_one({"_id": str(member.id), "day": 0})

                        cluster.sweetness.online.update_one({"_id": str(member.id)}, {"$inc": {"online": +60}})
                        cluster.sweetness.day.update_one({"_id": str(member.id)}, {"$inc": {"day": +60}})

                        if cluster.sweetness.economy.count_documents({"_id": str(member.id)}) == 0:
                            cluster.sweetness.economy.insert_one({"_id": str(member.id), "balance": 0})
                        cluster.sweetness.economy.update_one({"_id": str(member.id)}, {"$inc": {"balance": +1}})

                        if cluster.sweetness.history_win.count_documents({"_id": str(member.id)}) == 0:
                            cluster.sweetness.history_win.insert_one({"_id": str(member.id), "active": 0,"giveaway": 0,"roles": 0,"promocode": 0,"clan": 0,"gifts": 0,"casino": 0,"transfer": 0,"events": 0})

                        cluster.sweetness.history_win.update_one({"_id": str(member.id)}, {"$inc": {"active": +1}})

                        for role in member.roles:
                            if role.id in [1000834852444192884]:
                                if cluster.sweetness.online_staff.count_documents({"_id": str(member.id)}) == 0:
                                    cluster.sweetness.online_staff.insert_one({"_id": str(member.id), "mod": 0})
                                cluster.sweetness.online_staff.update_one({"_id": str(member.id)}, {"$inc": {"mod": +60}})

                                if cluster.sweetness.online_staff_week.count_documents({"_id": str(member.id)}) == 0:
                                    cluster.sweetness.online_staff_week.insert_one({"_id": str(member.id), "mod": 0})
                                cluster.sweetness.online_staff_week.update_one({"_id": str(member.id)}, {"$inc": {"mod": +60}})

                        try:
                            if int(member.voice.channel.category.id) == int(1149340569722695840):
                                user = disnake.utils.get(member.guild.members, id = int(cluster.sweetness.marry.find_one({'_id': str(member.id)})['love']))
                                if int(user.voice.channel.category.id) == int(1149340569722695840):
                                    cluster.sweetness.love_online.update_one({"_id": str(member.id)}, {"$inc": {"Love_online": +60}})
                        except:
                            pass

                        try:
                            if int(member.voice.channel.category.id) == int(1143903611777187841):
                                if cluster.sweetness.room_online.count_documents({"_id": str(member.voice.channel.id)}) == 0: 
                                    cluster.sweetness.room_online.insert_one({"_id": str(member.voice.channel.id), "day": 0})
                                cluster.sweetness.room_online.update_one({"_id": str(member.voice.channel.id)}, {"$inc": {"day": +60}})

                                if cluster.sweetness.roomweek.count_documents({"_id": str(member.voice.channel.id)}) == 0: 
                                    cluster.sweetness.roomweek.insert_one({"_id": str(member.voice.channel.id), "day": 0})
                                cluster.sweetness.roomweek.update_one({"_id": str(member.voice.channel.id)}, {"$inc": {"day": +60}})
                        except:
                            pass

        except:
            pass

    @tasks.loop(seconds = 10000)
    async def minysrole(self):
        try:
            for x in cluster.sweetness.role.find():
                for role_id in cluster.sweetness.role.find_one({'_id': str(x['_id'])})['rolemember']:
                    data_delete = cluster.sweetness.role_plata.find_one({'_id': str(role_id)})['time']

                    remaining_days = (data_delete - datetime.datetime.now()).sweetness

                    if remaining_days < 6:

                        notification = cluster.sweetness.role_plata.find_one({'_id': str(role_id)})['notification']
                        guild = self.bot.get_guild(1143903608946045048)
                        member = disnake.utils.get(guild.members, id = int(x['_id']))

                        if notification == "No":
                            embed = disnake.Embed(description=f"<@{x['_id']}>, **Ваша** роль будет удалена через **5 дней**, если вы не её **оплатите.**", color=3092790)
                            embed.set_author(name = f"Оповещение о плате за личную роль | {guild.name}", icon_url = guild.icon.url)
                            embed.set_thumbnail(url = member.display_avatar.url)
                            await member.send(embed = embed)
                            cluster.sweetness.role_plata.update_one({'_id': str(role_id)}, {'$set': {'notification': "Yes"}}, upsert = True)
                        else:
                            if remaining_days < 2:
                                embed = disnake.Embed(description=f"<@{x['_id']}>, **Ваша** роль **была** удалена за **неоплату**.", color=3092790)
                                embed.set_author(name = f"Удаление личной роли | {guild.name}", icon_url = guild.icon.url)
                                embed.set_thumbnail(url = member.display_avatar.url)
                                await member.send(embed = embed)
                                cluster.sweetness.role.delete_one({'_id': str(member.id)})
        except:
            pass

    @tasks.loop(seconds = 10000)
    async def minyslove(self):
        try:
            for x in cluster.sweetness.love_plata.find():

                data_delete_room = cluster.sweetness.love_plata.find_one({'_id': str(x['_id'])})['time']

                remaining_days = (data_delete_room - datetime.datetime.now()).sweetness

                if remaining_days < 6:

                    notification = cluster.sweetness.love_plata.find_one({'_id': str(x['_id'])})['notification']
                    guild = self.bot.get_guild(1143903608946045048)
                    member = disnake.utils.get(guild.members, id = int(x['_id']))

                    if notification == "No":
                        embed = disnake.Embed(description=f"<@{x['_id']}>, **Ваша** любовная комната будет удалена через **5 дней**, если вы не её **оплатите.**", color=3092790)
                        embed.set_author(name = f"Оповещение о плате за любовную комнату | {guild.name}", icon_url = guild.icon.url)
                        embed.set_thumbnail(url = member.display_avatar.url)
                        await member.send(embed = embed)
                        cluster.sweetness.love_plata.update_one({'_id': str(x['_id'])}, {'$set': {'notification': "yes"}}, upsert = True)
                    else:
                        if remaining_days < 2:
                            embed = disnake.Embed(description=f"<@{x['_id']}>, **Ваша** любовная комната **была** удалена за **неоплату**.", color=3092790)
                            embed.set_author(name = f"Удаление любовный комнаты | {guild.name}", icon_url = guild.icon.url)
                            embed.set_thumbnail(url = member.display_avatar.url)
                            await member.send(embed = embed)
                            cluster.sweetness.marry.delete_one({'_id': str(member.id)})
                            cluster.sweetness.love_plata.delete_one({'_id': str(member.id)})
        except:
            pass

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.bot.process_commands(message)

        if cluster.sweetness.message.count_documents({"_id": str(message.author.id)}) == 0: 
            cluster.sweetness.message.insert_one({"_id": str(message.author.id), "message_count": 0})
        cluster.sweetness.message.update_one({"_id": str(message.author.id)}, {"$inc": {"message_count": +1}})

        if message.author.bot:
            return

        if cluster.sweetness.messageandvoice.count_documents({"_id": str(message.author.id)}) == 0: 
            cluster.sweetness.messageandvoice.insert_one({"_id": str(message.author.id), "message_count": 0})
        cluster.sweetness.messageandvoice.update_one({"_id": str(message.author.id)}, {"$inc": {"message_count": +1}})

    @tasks.loop(seconds = 60)
    async def action(self):
        try:
            guild = self.bot.get_guild(1143903608946045048)
            embed = disnake.Embed(color = 3092790)
            embed.set_thumbnail(url = guild.icon.url)
            for x in cluster.sweetness.action.find():
                data_delete = cluster.sweetness.action.find_one({'_id': str(x['_id'])})['time']
                role_id = cluster.sweetness.action.find_one({'_id': str(x['_id'])})['role']
                type = cluster.sweetness.action.find_one({'_id': str(x['_id'])})['type']

                remaining_minutes = (data_delete - datetime.datetime.now()).total_seconds()
                if remaining_minutes < 1:
                    user = disnake.utils.get(guild.members, id = int(x['_id']))
                    rolemute = disnake.utils.get(guild.roles, id = int(role_id))
                    try:
                        await user.remove_roles(rolemute)
                    except: 
                        pass
                        
                    if type == "Текстовый мут":
                        embed.description=f'Привет <@{x["_id"]}>, **Ваш** текстовый мут был закончен!'
                        embed.set_author(name = f'Размут | {guild.name}', icon_url = guild.icon.url)
                    if type == "Голосовой мут":
                        embed.description=f'Привет <@{x["_id"]}>, **Ваш** голосовой мут был закончен!'
                        embed.set_author(name = f'Размут | {guild.name}', icon_url = guild.icon.url)
                    if type == "Бан":
                        embed.description=f'Привет <@{x["_id"]}>, **Ваш** бан был закончен!', 
                        embed.set_author(name = f'Разбан | {guild.name}', icon_url = guild.icon.url)
 
                    try:
                        await user.send(embed=embed) 
                    except: 
                        pass
                    try:
                        await user.move_to(user.voice.channel)
                    except: 
                        pass

                cluster.sweetness.action.delete_one({'_id': str(x['_id'])})
        except Exception as e:
            try:
                await self.bot.get_channel(1133377571778727947).send(e)
            except: 
                pass

def setup(bot):
    bot.add_cog(giveonlcog(bot))