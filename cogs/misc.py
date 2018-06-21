import random
import traceback
import sys

import discord
from discord.ext import commands


class General:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='8ball', description="Answers a yes/no question.", brief="Answers from the beyond.", pass_context=True)
	async def answer_machine(self, context):
		responses = [
			'That is a resounding no',
			'It is not looking likely',
			'Too hard to tell',
			'It is quite possible',
			'Definitely',
		]
		await self.bot.say(random.choice(responses) + ", " + context.message.author.mention)

	@commands.command(name='reload', hidden=True)
	async def _reload(self, module):
		"""Reloads a module."""
		try:
			self.bot.unload_extension(module)
			self.bot.load_extension(module)
		except Exception as e:
			await self.bot.say(f'```py\n{traceback.format_exc()}\n```')
		else:
			await self.bot.say('\N{OK HAND SIGN}')

	@commands.command(name='unload', hidden=True)
	async def _unload(self, module):
		"""Unloads a module."""
		try:
			self.bot.unload_extension(module)
		except Exception as e:
			await self.bot.say(f'```py\n{traceback.format_exc()}\n```')
		else:
			await self.bot.say('\N{OK HAND SIGN}')

	@commands.command(name='load', hidden=True)
	async def _load(self, module):
		"""Loads a module."""
		try:
			self.bot.load_extension(module)
		except Exception as e:
			await self.bot.say(f'```py\n{traceback.format_exc()}\n```')
		else:
			await self.bot.say("It's loaded. \N{OK HAND SIGN}")

	@commands.command(name='shutdown', hidden=True)
	async def _shutdown(self):
		"""Exits the bot."""
		try:
			await self.bot.say("Executed, bye.")
			sys.exit(0)
		except Exception as e:
			await self.bot.say(f'```py\n{traceback.format_exc()}\n```')


def setup(bot):
	bot.add_cog(General(bot))
