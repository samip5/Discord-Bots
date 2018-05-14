import time
import math
import json
import aiohttp
import random

import discord
from discord.ext import commands
from discord.ext.commands import cooldown


class Misc:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='ping',
		brief="Ping pong")
	async def ping(self):
		await self.bot.say("Pong!")

	@commands.command(name='cat',
		description="Gives you a random cat picture",
		brief="Cats",
		pass_context=True)
	#@commands.cooldown(4, 30, BucketType)
	async def randomcat(self,context):
		async with aiohttp.ClientSession() as ses:
			async with ses.get('https://aws.random.cat/meow') as response:
				ret = await response.json()
		e = discord.Embed(color=random.randint(1, 255**3-1))
		e.set_image(url=ret['file'])
		e.set_author(name="Random.cat", url='https://random.cat/')
		e.set_footer(text="Powered by random.cat")
		await self.bot.say(embed=e)

def setup(bot):
	bot.add_cog(Misc(bot))
