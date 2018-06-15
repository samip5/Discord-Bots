########################################################
## Discord bot which integrates with Ombi and Plex.   ##
##                                                    ##
## Author: samip5 				      ##
## Version: 0.4 				      ##
########################################################

import configparser as parser
import discord
import logging
import sys
import traceback

from discord import Game
from discord.ext import commands

config = parser.ConfigParser()

config.read('./config.ini')

TOKEN = config['secrets']['BOT-DEVELOMENT-TOKEN']

logger_info = logging.getLogger('discord')
# logger_debug = logging.getLogger('discord')
logger_info.setLevel(logging.INFO)
# logger_debug.setLevel(logging.DEBUG)
logFile_info_handler = logging.FileHandler(filename='discord_info.log', encoding='utf-8', mode='w')
# logFile_debug_handler = logging.FileHandler(filename='discord_debug.log', encoding='utf-8', mode='w')
logFile_info_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logFile_debug_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger_info.addHandler(logFile_info_handler)
# logger_debug.addHandler(logFile_debug_handler)


def get_prefix(bot, message):
    prefixes = ['!']
    return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = ['cogs.general', 'cogs.plex', 'cogs.ombi', 'cogs.misc', 'cogs.music']

bot = commands.Bot(command_prefix=get_prefix)
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_ready():
    print (f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nAPI Version: {discord.__version__}\n')
    await bot.change_presence(game=Game(name="with code"))
    print (f'Successfully connected.')


bot.run(TOKEN, bot=True, reconnect=True)
