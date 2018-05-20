import time
import giphy_client
import json
import aiohttp
import random

import discord
from discord.ext import commands
from discord.ext.commands import cooldown

from giphy_client.rest import ApiException
from pprint import pprint

class Misc:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='8ball',
		description="Answers a yes/no question.",
		brief="Answers from the beyond.",
		pass_context=True)
	async def answer_machine(self, context):
		responses = [
		'That is a resounding no',
		'It is not looking likely',
		'Too hard to tell',
		'It is quite possible',
		'Definitely',]
		await self.bot.say(random.choice(responses) + ", " + context.message.author.mention)

	@commands.command(name='giphy',
		description="Giphy API integration (WIP)",
		brief="Giphy API (WIP)")
	async def giphy(self, input):
		api_instance = giphy_client.DefaultApi()
		api_key = '<not-included>'
		#q = ''
		try:
			raise NotImplementedError("This is not implemented.")
		except Exception as e:
			fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
			await self.bot.say(fmt.format(type(e).__name__, e))

	@commands.command(name='facepalmed', brief="Command says everything needed.",pass_context=True)
	async def facepalm(self):
		urls = ['https://media1.giphy.com/media/AjYsTtVxEEBPO/giphy.gif',
				'https://media2.giphy.com/media/3og0INyCmHlNylks9O/giphy.gif',
				'https://media2.giphy.com/media/ADr35Z4TvATIc/giphy.gif',
				'https://media3.giphy.com/media/6yRVg0HWzgS88/giphy.gif']

		thumb_url = random.choice(urls)
		f = discord.Embed(color=random.randint(1, 255**3-1))
		f.set_image(url=thumb_url)
		f.set_footer(text="Powered by Giphy.")
		await self.bot.say(embed=f)

	@commands.command(name='cat',
		description="Gives you a random cat picture",
		brief="Returns random image of a cat",
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
