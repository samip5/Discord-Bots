import random

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


def setup(bot):
	bot.add_cog(General(bot))