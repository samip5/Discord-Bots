# NOTICE: Develoment Bot, may or may not work
# Author: samip5


import sys
import traceback

import discord
from discord import Game
from discord.ext import commands


def get_prefix(bot, message):
	prefixes = ['!!']
	return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = ['cogs.misc']

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


# bot.run(token, bot=True, reconnect=True)
