########################################################
## Discord bot which integrates with Ombi and Plex.   ##
##                                                    ##
## Author: samip5 				                      ##
## Version: 0.2 				                      ##
########################################################

import configparser as parser
import discord
import sys, traceback

from discord import __version__
from discord import Game
from discord.ext import commands

config = parser.ConfigParser()

config.read('./config.ini')

token = config['secrets']['BOT-TOKEN']
devToken = config['secrets']['BOT-DEVELOMENT-TOKEN']

def get_prefix(bot, message):
  prefixes = ['!']
  return commands.when_mentioned_or(*prefixes)(bot, message)

initial_extensions = ['cogs.general',
			'cogs.error_handler',
            'cogs.plex',
			'cogs.ombi',
			'cogs.misc',
			'cogs.music']

bot = commands.Bot(command_prefix=get_prefix, description="Samip's Advanced Bot")
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
        await bot.change_presence(game=Game(name="with humans"))
        print (f'Successfully connected.')

@bot.event
async def on_error(event, *args, **kwargs):
	message = args[0]
	await bot.say(message.channel, "You caused an error.")



#bot.run(TOKEN, bot=True, reconnect=True)
bot.run(devToken, bot=True, reconnect=True)
