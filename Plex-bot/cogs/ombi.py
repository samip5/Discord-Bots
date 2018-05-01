import random
import json
import aiohttp
import requests
import discord

from discord.ext import commands

class PlexPmrs:
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(name='pmrs-search',
                        description="Search from Plex Media Request System",
                        brief="Search pmrs")
        #@commands.guild_only()
	async def search_ombi(self, input):
			try:
				raise NotImplementedError("This is WIP, and as such not usable yet.")
			except Exception as e:
            			fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            			await self.bot.say(fmt.format(type(e).__name__, e))
		
def setup(bot):
	bot.add_cog(PlexPmrs(bot))
