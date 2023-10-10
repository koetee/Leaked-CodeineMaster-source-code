import pymongo
import disnake
import datetime
import json
import requests
from random import randint
from disnake.ext import commands, tasks
from disnake.enums import ButtonStyle, TextInputStyle
from PIL import Image, ImageDraw, ImageFont

cluster = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/test?retryWrites=true&w=majority")

files = cluster.sweetness.files
database = cluster.sweetness

def hex_to_rgb(value):
    value = value.lstrip('#')
    RGB = list(tuple(int(value[i:i + len(value) // 3], 16) for i in range(0, len(value), len(value) // 3)))
    return (RGB[0]<<16) + (RGB[1]<<8) + RGB[2]

class giveonlcog(commands.Cog):
    def __init__(self, bot: commands.Bot(intents = disnake.Intents.all(), command_prefix = 'tasks!')):
        self.bot = bot
        if not self.giveonline1.is_running(): self.giveonline1.start()
        if not self.clan_war.is_running(): self.clan_war.start()
        if not self.clan_war_zombie.is_running(): self.clan_war_zombie.start()
        if not self.clan_shield.is_running(): self.clan_shield.start()
        
    @tasks.loop(seconds = 500)
    async def clan_shield(self):
        for x in cluster.sweetness.clan_shield.find():
            try:
                activate = cluster.sweetness.clan_shield.find_one({'_id': str(x['_id'])})['activate']
                if activate == "YES":
                    data_delete = cluster.sweetness.clan_shield.find_one({'_id': str(x['_id'])})['time']

                    remaining_minutes = (data_delete - datetime.datetime.now()).total_seconds() // 60
                    if remaining_minutes < 1:
                        cluster.sweetness.clan_shield.delete_one({'_id': str(x['_id'])})
            except:
                pass

    @tasks.loop(seconds = 60)
    async def giveonline1(self):
        try:
            guild_get = self.bot.get_guild(960579506425446472)
            for category_id in cluster.sweetness.clan.find_one({'_id': str(960579506425446472)})['categories']:
                try: 
                    category_get = disnake.utils.get(guild_get.categories, id = int(category_id))
                    for channel in category_get.voice_channels:
                        for member in channel.members:
                            if not member.bot == True:
                                with open('clan_sweetness.json','r', encoding='utf-8') as f:
                                    clan = json.load(f)
                                if not clan[str(member.guild.id)][str(member.id)] == 'Отсутствует':
                                    clanxd = clan[str(member.guild.id)][str(member.id)]
                                    if cluster.sweetness.clan_online.count_documents({"_id": str(clanxd)}) == 0:
                                        cluster.sweetness.clan_online.insert_one({"_id": str(clanxd), "clan_online": 0})
                                    if cluster.sweetness.clanonline.count_documents({"_id": str(member.id)}) == 0:
                                        cluster.sweetness.clanonline.insert_one({"_id": str(member.id), "online": 0})
                                    cluster.sweetness.clan_online.update_one({"_id": str(clanxd)}, {"$inc": {"clan_online": +60}})
                                    cluster.sweetness.clanonline.update_one({"_id": str(member.id)}, {"$inc": {"online": +60}})
                                    
                except:
                    pass
        except:
            pass

    @tasks.loop(seconds = 50)
    async def clan_war(self):
        try:
            for x in cluster.sweetness.clan_war.find():

                data_attack = cluster.sweetness.clan_war.find_one({'_id': str(x['_id'])})['time']
                remaining_minutes = (data_attack - datetime.datetime.now()).total_seconds() // 60
                if remaining_minutes < 1:

                    with open('clan_sweetness.json', 'r') as f:
                        clan = json.load(f)

                    clan_defender = cluster.sweetness.clan_war.find_one({'_id': str(x['_id'])})['target']
                    guild = self.bot.get_guild(960579506425446472)

                    role_take = disnake.utils.get(guild.roles, id = int(x['_id']))
                    clan_heroes = len(cluster.sweetness.clan_heroes.find_one({'_id': str(x['_id'])})['heroes'])
                    voice_members = 1
                    if int(clan_heroes) == 0:
                        power_attacker = len(role_take.members) * 50 * voice_members
                    else:
                        for member in role_take.members:
                            try:
                                channel = member.voice.channel.id
                                voice_members += 1
                            except:
                                pass
                        power_heroes = len(cluster.sweetness.clan_heroes.find_one({'_id': str(x['_id'])})['heroes']) * 100
                        power_attacker = len(role_take.members) * 50 * voice_members * int(power_heroes)
                    role_take = disnake.utils.get(guild.roles, id = int(clan_defender))
                    clan_heroes = len(cluster.sweetness.clan_heroes.find_one({'_id': str(clan_defender)})['heroes'])
                    voice_members = 1
                    if int(clan_heroes) == 0:
                        power_defender = len(role_take.members) * 50 * voice_members
                    else:
                        for member in role_take.members:
                            try:
                                channel = member.voice.channel.id
                                voice_members += 1
                            except:
                                pass
                        power_heroes = len(cluster.sweetness.clan_heroes.find_one({'_id': str(clan_defender)})['heroes']) * 100
                        power_defender = len(role_take.members) * 50 * voice_members * int(power_heroes)
                    if database.clan_lose.count_documents({"_id": str(x['_id'])}) == 0:
                        database.clan_lose.insert_one({"_id": str(x['_id']), "lose": 0})
                    if database.clan_win.count_documents({"_id": str(x['_id'])}) == 0:
                        database.clan_win.insert_one({"_id": str(x['_id']), "win": 0})

                    if database.clan_lose.count_documents({"_id": str(clan_defender)}) == 0:
                        database.clan_lose.insert_one({"_id": str(clan_defender), "lose": 0})
                    if database.clan_win.count_documents({"_id": str(clan_defender)}) == 0:
                        database.clan_win.insert_one({"_id": str(clan_defender), "win": 0})

                    if int(power_attacker) > int(power_defender):
                        embed = disnake.Embed(description=f"Клан <@&{x['_id']}> **Победил** с огромным преимуществом, **разбив** <@&{clan_defender}> одним ударом.", color=disnake.Color(hex_to_rgb(str("#2c40f6"))))
                        embed.add_field(name = f"<:gift:1136967445530284073> Награда", value = f"```Баланс: {int(power_defender) // 100} 💰\nРейтинг: 30 🏆```")
                        embed.set_thumbnail("https://cdn.discordapp.com/attachments/1147505417417670726/1147515271934906408/battle_1_1.png")
                        embed.set_author(name = f"Клановые Войны | {guild.name}", icon_url = guild.icon.url)
                        database.clan_win.update_one({"_id": str(x['_id'])}, {"$inc": {"win": +int(1)}})
                        database.clan_lose.update_one({"_id": str(clan_defender)}, {"$inc": {"lose": +int(1)}})

                        database.clan_rating.update_one({"_id": str(x['_id'])}, {"$inc": {"rating": +int(30)}})

                        clan_take = clan[str(guild.id)][x['_id']]
                        clan_take['Balance'] += int(power_defender) // 100
                        with open('clan_sweetness.json','w') as f:
                            json.dump(clan,f)

                        clan_take = clan[str(guild.id)][clan_defender]
                        clan_take['Balance'] -= int(power_defender) // 100
                        with open('clan_sweetness.json','w') as f:
                            json.dump(clan,f)
                    else:
                        embed = disnake.Embed(description=f"Клан <@&{clan_defender}> **Победил** с преимуществом, **защищаясь** от <@&{x['_id']}>", color=disnake.Color(hex_to_rgb(str("#2c40f6"))))
                        embed.add_field(name = f"<:gift:1136967445530284073> Награда", value = f"```Баланс: {int(power_defender) // 100} 💰\nРейтинг: 30 🏆```")
                        embed.set_thumbnail("https://cdn.discordapp.com/attachments/1147505417417670726/1147515271934906408/battle_1_1.png")
                        embed.set_author(name = f"Клановые Войны | {guild.name}", icon_url = guild.icon.url)
                        database.clan_win.update_one({"_id": str(clan_defender)}, {"$inc": {"win": +int(1)}})
                        database.clan_lose.update_one({"_id": str(x['_id'])}, {"$inc": {"lose": +int(1)}})

                        database.clan_rating.update_one({"_id": str(clan_defender)}, {"$inc": {"rating": +int(30)}})

                        clan_take = clan[str(guild.id)][x['_id']]
                        clan_take['Balance'] -= int(power_defender) // 100
                        with open('clan_sweetness.json','w') as f:
                            json.dump(clan,f)

                        clan_take = clan[str(guild.id)][clan_defender]
                        clan_take['Balance'] += int(power_defender) // 100
                        with open('clan_sweetness.json','w') as f:
                            json.dump(clan,f)

                    await self.bot.get_channel(1156342323450478592).send(embed = embed)

                    cluster.sweetness.clan_war.delete_one({'_id': str(x['_id'])})
                    cluster.sweetness.clan_defender.delete_one({'_id': str(clan_defender)})
        except:
            pass

    @tasks.loop(seconds = 50)
    async def clan_war_zombie(self):
        try:
            for x in cluster.sweetness.clan_zombie.find():
                data_attack = cluster.sweetness.clan_zombie.find_one({'_id': str(x['_id'])})['time']
                remaining_minutes = (data_attack - datetime.datetime.now()).total_seconds() // 60
                if remaining_minutes < 1:
                    with open('clan_sweetness.json', 'r') as f:
                        clan = json.load(f)

                    guild = self.bot.get_guild(960579506425446472)

                    lvl = cluster.sweetness.clan_zombie.find_one({'_id': str(x['_id'])})['target']
                    role_take = disnake.utils.get(guild.roles, id = int(x['_id']))
                    clan_heroes = len(cluster.sweetness.clan_heroes.find_one({'_id': str(x['_id'])})['heroes'])
                    
                    voice_members = 1
                    if int(clan_heroes) == 0:
                        power_attacker = len(role_take.members) * 50 * voice_members
                    else:
                        for member in role_take.members:
                            try:
                                channel = member.voice.channel.id
                                voice_members += 1
                            except:
                                pass
                        power_heroes = len(cluster.sweetness.clan_heroes.find_one({'_id': str(x['_id'])})['heroes']) * 100
                        power_attacker = len(role_take.members) * 50 * voice_members * int(power_heroes)

                    if int(lvl) == 1:
                        power_zombie = 20000
                        prize = 500
                    if int(lvl) == 2:
                        power_zombie = 100000
                        prize = 2000
                    if int(lvl) == 3:
                        power_zombie = 1000000
                        prize = 3500
                    if int(lvl) == 4:
                        power_zombie = 10000000
                        prize = 5000
                    if int(lvl) == 5:
                        power_zombie = 45000000
                        prize = 7500
                    if int(lvl) == 6:
                        power_zombie = 100000000
                        prize = 10000
                    if int(lvl) == 7:
                        power_zombie = 1000000000
                        prize = 50000

                    if int(power_attacker) > int(power_zombie):
                        embed = disnake.Embed(description=f"Клан <@&{x['_id']}> **Победил** с огромным преимуществом, **над** зомби {lvl}-ого уровня одним ударом.", color=disnake.Color.green())
                        embed.add_field(name = f"<:gift:1136967445530284073> Награда", value = f"```Баланс: {prize} 💰```")
                        embed.set_thumbnail("https://cdn.discordapp.com/attachments/1147505417417670726/1147515271934906408/battle_1_1.png")
                        embed.set_author(name = f"Клановые Войны | {guild.name}", icon_url = guild.icon.url)

                        clan_take = clan[str(guild.id)][x['_id']]
                        clan_take['Balance'] += int(prize)
                        with open('clan_sweetness.json','w') as f:
                            json.dump(clan,f)
                    else:
                        embed = disnake.Embed(description=f"Клан <@&{x['_id']}> **Проиграл**, **атакуя** зомби {lvl}-ого уровня", color=disnake.Color.red())
                        embed.set_thumbnail("https://cdn.discordapp.com/attachments/1147505417417670726/1147515271934906408/battle_1_1.png")
                        embed.set_author(name = f"Клановые Войны | {guild.name}", icon_url = guild.icon.url)

                    await self.bot.get_channel(1156342323450478592).send(embed = embed)

                    cluster.sweetness.clan_zombie.delete_one({'_id': str(x['_id'])})
        except:
            pass

def setup(bot):
    bot.add_cog(giveonlcog(bot))