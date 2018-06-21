# NOTICE: Develoment Bot, may or may not work
# Author: samip5


import configparser as parser
import sys
import traceback

import discord
from discord import Game
from discord.ext import commands

config = parser.ConfigParser()

config.read('./config.ini')

dev_token = config['secrets']['BOT-DEVELOMENT-TOKEN']
token = config['secrets']['BOT-TOKEN']


def get_prefix(bot, message):
	prefixes = ['!!']
	return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = ['cogs.private', 'cogs.misc']

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
	print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nAPI Version: {discord.__version__}\n')
	await bot.change_presence(game=Game(name="with code"))
	print(f'Successfully connected.')


@bot.event
async def on_message(message):
	await bot.process_commands(message)


@bot.event
async def on_error(event, *args, **kwargs):
	message = args[0]
	await bot.say(message.channel, "You caused an error.")


bot.run(token, bot=True, reconnect=True)
