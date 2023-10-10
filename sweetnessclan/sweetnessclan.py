import disnake
import asyncio
import json
import os
from disnake.ext import commands

bot = commands.Bot(command_prefix = commands.when_mentioned_or('clans!'), intents = disnake.Intents.all(), test_guilds = [960579506425446472], sync_commands = True)

@bot.event
async def on_ready():
    print("Bot Ready")
    await bot.change_presence(status=disnake.Status.online, activity=disnake.Activity(type=disnake.ActivityType.watching, name=f"за {bot.get_guild(960579506425446472).name}"))

@bot.command(name='load')
async def load(inter, extension):
    if not inter.author.id == 284010976313868288: 
        return
    try:
        await inter.message.delete()
        bot.load_extension(f'sweetnessclancogs.{extension}')
    except:
        pass

@bot.command(name='unload')
async def unload(inter, extension):
    if not inter.author.id == 284010976313868288: 
        return
    try: 
        await inter.message.delete()
        bot.unload_extension(f'sweetnessclancogs.{extension}')
    except:
        pass

@bot.command(name='reload')
async def reload(inter, extension):
    if not inter.author.id == 284010976313868288: 
        return
    try: 
        await inter.message.delete()
        bot.unload_extension(f'sweetnessclancogs.{extension}')
        await asyncio.sleep(4)
        bot.load_extension(f'sweetnessclancogs.{extension}')
    except: 
        pass

if __name__ == '__main__':
    for filename in os.listdir("./sweetnessclancogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"sweetnessclancogs.{filename[:-3]}")
            
bot.run("MTExMDIwMzE0Mzg0MjcwNTQ1MA.GMRlWL.nl71QUjRBUE_n0sL_atFPXtdNvQ5neh_mmaJew")