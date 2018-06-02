import random
import os, sys

import discord
from discord.ext import commands
from discord import __version__


class General:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="ping",brief="Ping pong")
	async def ping(self):
		await self.bot.say("Pong!")

	@commands.command(name="about", brief="About me")
	async def about_me(self):
		changes = os.popen(r'git show -s HEAD~3..HEAD --format="[%h](https://github.com/samip5/Discord-Bots/commit/%H) %s (%cr)"').read().strip()
		embed = discord.Embed(title = "About Me")
		embed.set_author(name = "Samip's Bot (Discord ID: {})".format(self.bot.user.id))
		if changes:
			embed.add_field(name = "Latest Changes: ", value = changes, inline = False)
		embed.add_field(name="Created on:", value="May 1st, 2018")
		embed.add_field(name = "Library", value = "[discord.py](https://github.com/Rapptz/discord.py) v{0}\n([Python](https://www.python.org/) v{1.major}.{1.minor}.{1.micro})".format(discord.__version__, sys.version_info))
		await self.bot.reply("You requested it", embed=embed)

	@commands.group(name="faq", brief="Frequently Asked Questions", pass_context=True)
	async def Frequently_Asked_Questions(self, context):
		if context.invoked_subcommand is None:
			embed = discord.Embed(title="Frequently Asked Questions")
			embed.add_field(name="Want to know about the requests system?", value="Just execute this command with with `requests` after it.", inline=False)
			await self.bot.say(embed=embed)
		pass

	@Frequently_Asked_Questions.command()
	async def requests(self):
		embed=discord.Embed(title="Plex Media Request System FAQ", color=0xdc1111)
		embed.add_field(name="1. Where can I find it?", value="It's located at: https://home.samip.fi/pmrs/", inline=False)
		embed.add_field(name="2. How do I log-on?", value="You login with your plex.tv credentials.\nThe admin wont see it as it's securely checked against plex.tv API.", inline=False)
		embed.set_footer(text="Generated by samip5's code.")
		await self.bot.say(embed=embed)


def setup(bot):
	bot.add_cog(General(bot))
