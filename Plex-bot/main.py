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
import datetime


from discord import Game
from discord.ext import commands
from cogs.utils import checks

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


initial_extensions = ['cogs.general', 'cogs.plex', 'cogs.ombi', 'cogs.misc', 'cogs.meta', 'cogs.mod']

help_attrs = dict(hidden=True)
bot = commands.Bot(command_prefix=get_prefix, help_attrs=help_attrs)


# @bot.event
# async def on_command_error(error, ctx):
#    if isinstance(error, commands.NoPrivateMessage):
#        await bot.send_message(ctx.message.author, 'This command cannot be used in private messages.')
#    elif isinstance(error, commands.DisabledCommand):
#        await bot.send_message(ctx.message.author, 'Sorry. This command is disabled and cannot be used.')


@bot.event
async def on_ready():
    bot.uptime = datetime.datetime.utcnow()
    print (f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nAPI Version: {discord.__version__}\n')
    await bot.change_presence(game=Game(name="with code"))
    print (f'Successfully connected.')


@bot.event
async def on_message(message):
    mod = bot.get_cog('Mod')

    if mod is not None and not checks.is_owner_check(message):
        # check if the user is bot banned
        if message.author.id in mod.config.get('plonks', []):
            return

        # check if the channel is ignored
        # but first, resolve their permissions

        perms = message.channel.permissions_for(message.author)
        bypass_ignore = perms.manage_roles

        # if we don't have manage roles then we should
        # check if it's the owner of the bot or they have Bot Admin role.

        if not bypass_ignore:
            if not message.channel.is_private:
                bypass_ignore = discord.utils.get(message.author.roles, name='Bot Admin') is not None

        # now we can finally realise if we can actually bypass the ignore.

        if not bypass_ignore:
            if message.channel.id in mod.config.get('ignored', []):
                return

    # if someone private messages us with something that looks like a URL then
    # we should try to see if it's an invite to a discord server and join it if so.
    if message.channel.is_private and message.content.startswith('http'):
        try:
            invite = await bot.get_invite(message.content)
            await bot.accept_invite(invite)
            await bot.send_message(message.channel, 'Joined the server.')
        except:
            # if an error occurs at this point then ignore it and move on.
            pass
        finally:
            return
    await bot.process_commands(message)

if __name__ == '__main__':
    if any('debug' in arg.lower() for arg in sys.argv):
        bot.command_prefix = '$'
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()
bot.run(TOKEN, bot=True, reconnect=True)
