# This is borrowed code from: https://github.com/Rapptz/RoboDanny/blob/async/cogs/meta.py

from discord.ext import commands
from .utils import config, checks, formats
from collections import Counter

import discord
import os
import datetime
import re
import asyncio


class TimeParser:
	def __init__(self, argument):
		compiled = re.compile(r"(?:(?P<hours>\d+)h)?(?:(?P<minutes>\d+)m)?(?:(?P<seconds>\d+)s)?")
		self.original = argument
		try:
			self.seconds = int(argument)
		except ValueError as e:
			match = compiled.match(argument)
			if match is None or not match.group(0):
				raise commands.BadArgument('Failed to parse time.') from e

			self.seconds = 0
			hours = match.group('hours')
			if hours is not None:
				self.seconds += int(hours) * 3600
			minutes = match.group('minutes')
			if minutes is not None:
				self.seconds += int(minutes) * 60
			seconds = match.group('seconds')
			if seconds is not None:
				self.seconds += int(seconds)


class Meta:
	"""Commands for utilities related to Discord or the Bot itself."""

	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def timer(self, ctx, time: TimeParser, *, message=''):
		"""Reminds you of something after a certain amount of time.
		The time can optionally be specified with units such as 'h'
		for hours, 'm' for minutes and 's' for seconds. If no unit
		is given then it is assumed to be seconds. You can also combine
		multiple units together, e.g. 2h4m10s.
		"""

		author = ctx.message.author
		reminder = None
		completed = None

		if not message:
			reminder = 'Okay {0.mention}, I\'ll remind you in {1.seconds} seconds.'
			completed = 'Time is up {0.mention}! You asked to be reminded about something.'
		else:
			reminder = 'Okay {0.mention}, I\'ll remind you about "{2}" in {1.seconds} seconds.'
			completed = 'Time is up {0.mention}! You asked to be reminded about "{1}".'

		await self.bot.say(reminder.format(author, time, message))
		await asyncio.sleep(time.seconds)
		await self.bot.say(completed.format(author, message))

	@commands.command(name='quit', hidden=True)
	@checks.is_owner()
	async def _quit(self):
		"""Quits the bot."""
		await self.bot.logout()

	@commands.command(pass_context=True)
	async def info(self, ctx, *, member: discord.Member = None):
		"""Shows info about a member.
		This cannot be used in private messages. If you don't specify
		a member then the info returned will be yours.
		"""
		channel = ctx.message.channel
		if channel.is_private:
			await self.bot.say('You cannot use this in PMs.')
			return

		if member is None:
			member = ctx.message.author

		roles = [role.name.replace('@', '@\u200b') for role in member.roles]
		shared = sum(1 for m in self.bot.get_all_members() if m.id == member.id)
		voice = member.voice_channel
		if voice is not None:
			voice = '{} with {} people'.format(voice, len(voice.voice_members))
		else:
			voice = 'Not connected.'

		entries = [
			('Name', member.name),
			('User ID', member.id),
			('Joined', member.joined_at),
			('Roles', ', '.join(roles)),
			('Servers', '{} shared'.format(shared)),
			('Channel', channel.name),
			('Voice Channel', voice),
			('Channel ID', channel.id),
			('Avatar', member.avatar_url),
		]

		await formats.entry_to_code(self.bot, entries)

	async def say_permissions(self, member, channel):
		permissions = channel.permissions_for(member)
		entries = []
		for attr in dir(permissions):
			is_property = isinstance(getattr(type(permissions), attr), property)
			if is_property:
				entries.append((attr.replace('_', ' ').title(), getattr(permissions, attr)))

		await formats.entry_to_code(self.bot, entries)

	def get_bot_uptime(self):
		now = datetime.datetime.utcnow()
		delta = now - self.bot.uptime
		hours, remainder = divmod(int(delta.total_seconds()), 3600)
		minutes, seconds = divmod(remainder, 60)
		days, hours = divmod(hours, 24)
		if days:
			fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'
		else:
			fmt = '{h} hours, {m} minutes, and {s} seconds'
		return fmt.format(d=days, h=hours, m=minutes, s=seconds)

	@commands.command()
	async def uptime(self):
		"""Tells you how long the bot has been up for."""
		await self.bot.say('Uptime: **{}**'.format(self.get_bot_uptime()))

	@commands.command(name="about")
	async def about_me(self):
		"""Tells you information about the bot itself."""
		result = ['**About Me:**']
		result.append('- Author: samip537 (Discord ID: 157970669261422592, Github: samip5)')
		result.append('- Bot ID: {} (Discord ID: {})'.format(self.bot.user.name, self.bot.user.id))
		result.append('- Created on May 1st, 2018')
		result.append('- Library: discord.py (Python)')
		changes = os.popen(r'git show -s HEAD~3..HEAD --format="[%h](https://github.com/samip5/Discord-Bots/commit/%H) %s (%cr)"').read().strip()
		result.append('- Changes: {}'.format(changes))
		result.append('- Uptime: {}'.format(self.get_bot_uptime()))
		result.append('- Servers: {}'.format(len(self.bot.servers)))
		# stats
		total_members = sum(len(s.members) for s in self.bot.servers)
		total_online = sum(1 for m in self.bot.get_all_members() if m.status != discord.Status.offline)
		unique_members = set(self.bot.get_all_members())
		unique_online = sum(1 for m in unique_members if m.status != discord.Status.offline)
		channel_types = Counter(c.type for c in self.bot.get_all_channels())
		voice = channel_types[discord.ChannelType.voice]
		text = channel_types[discord.ChannelType.text]
		result.append('- Total Members: {} ({} online)'.format(total_members, total_online))
		result.append('- Unique Members: {} ({} online)'.format(len(unique_members), unique_online))
		result.append('- {} text channels, {} voice channels'.format(text, voice))
		await self.bot.say('\n'.join(result))


def setup(bot):
	bot.add_cog(Meta(bot))
