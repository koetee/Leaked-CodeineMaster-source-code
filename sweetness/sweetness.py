import disnake
import asyncio
import json
import os
from disnake.ext import commands

bot = commands.Bot(command_prefix = commands.when_mentioned_or('day!'), intents = disnake.Intents.all(), test_guilds = [1143903608946045048], sync_commands = True)

@bot.event
async def on_ready():
    print("Bot Ready")
    await bot.change_presence(status=disnake.Status.online, activity=disnake.Activity(type=disnake.ActivityType.watching, name=f"за {bot.get_guild(1143903608946045048).name}"))

@bot.command(name='load')
async def load(inter, extension):
    if not inter.author.id == 1150439981110788247: 
        return
    try:
        await inter.message.delete()
        bot.load_extension(f'sweetnesscogs.{extension}')
    except:
        pass

@bot.command(name='unload')
async def unload(inter, extension):
    if not inter.author.id == 1150439981110788247: 
        return
    try: 
        await inter.message.delete()
        bot.unload_extension(f'sweetnesscogs.{extension}')
    except:
        pass

@bot.command(name='reload')
async def reload(inter, extension):
    if not inter.author.id == 1150439981110788247: 
        return
    try: 
        await inter.message.delete()
        bot.unload_extension(f'sweetnesscogs.{extension}')
        await asyncio.sleep(4)
        bot.load_extension(f'sweetnesscogs.{extension}')
    except: 
        pass

if __name__ == '__main__':
    for filename in os.listdir("./sweetnesscogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"sweetnesscogs.{filename[:-3]}")
            
bot.run("MTE1MDQzOTk4MTExMDc4ODI0Nw.G5VTHr.e-Oh6Pw6YxIC6GwV6P6jsgFzYd6dPJr7nS8Rko")