# NOTICE: Develoment Bot, may or may not work
# Author: samip5


import sys
import os
import traceback

import http.server
import socketserver

import discord
from discord import *
from discord.ext import commands

token = os.environ['TOKEN']

Handler = http.server.SimpleHTTPRequestHandler

PORT = 8000

httpd = socketserver.TCPServer(("", PORT), Handler)


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
	await bot.change_presence(game=Game(name="with code on Heroku"))
	print(f'Successfully connected.')
	for Server in bot.servers:
		ch = bot.get_channel(Server.id)
		print(ch)
		if ch:
			await bot.send_message(ch, "Hello from Heroku!")


# bot.run(token, bot=True, reconnect=True)
bot.run(token, bot=True, reconnect=True)
httpd.serve_forever()