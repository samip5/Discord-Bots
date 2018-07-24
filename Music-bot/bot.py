import datetime
import traceback
import sys
import discord
from discord.ext import commands
from discord import Game


def get_prefix(bot, message):
    prefixes = ['!']
    return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = ['cogs.meta', 'cogs.music']

bot_description = """
    This is a simple music bot
"""

help_attrs = dict(hidden=True)
bot = commands.Bot(command_prefix=get_prefix, help_attrs=help_attrs, description=bot_description)


@bot.event
async def on_ready():
    bot.uptime = datetime.datetime.utcnow()
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nAPI Version: {discord.__version__}\n')
    await bot.change_presence(game=Game(name="with music"))
    print(f'Successfully connected.')


if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()
    bot.run("")
