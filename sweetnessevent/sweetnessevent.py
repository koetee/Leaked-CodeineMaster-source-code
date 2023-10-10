import disnake
import asyncio
import json
import os
from disnake.ext import commands

bot = commands.Bot(command_prefix = commands.when_mentioned_or('clans!'), intents = disnake.Intents.all(), test_guilds = [890304318643785769], sync_commands = True)

@bot.event
async def on_ready():
    print("Bot Ready")
    await bot.change_presence(status=disnake.Status.online, activity=disnake.Activity(type=disnake.ActivityType.watching, name=f"за {bot.get_guild(890304318643785769).name}"))

@bot.command(name='load')
async def load(inter, extension):
    if not inter.author.id == 849353684249083914: 
        return
    try:
        await inter.message.delete()
        bot.load_extension(f'sweetnesseventcogs.{extension}')
    except:
        pass

@bot.command(name='unload')
async def unload(inter, extension):
    if not inter.author.id == 849353684249083914: 
        return
    try: 
        await inter.message.delete()
        bot.unload_extension(f'sweetnesseventcogs.{extension}')
    except:
        pass

@bot.command(name='reload')
async def reload(inter, extension):
    if not inter.author.id == 849353684249083914: 
        return
    try: 
        await inter.message.delete()
        bot.unload_extension(f'sweetnesseventcogs.{extension}')
        await asyncio.sleep(4)
        bot.load_extension(f'sweetnesseventcogs.{extension}')
    except: 
        pass

if __name__ == '__main__':
    for filename in os.listdir("./sweetnesseventcogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"sweetnesseventcogs.{filename[:-3]}")
            
bot.run("MTAwOTUwNTM0NTU3NzY5NzM1Mg.GKSjEn.6EJ_mPBWuFsfqeqkSTr5bLtD58CTKD6hXbscKo")