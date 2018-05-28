## Author: samip5
################### Warning #######################
# PLexapi uses requests lib, which is not optimal.#
###################################################

import random
import time
import json
import aiohttp
import requests
import discord

from plexapi.server import PlexServer
from plexapi.library import Library
from discord.ext import commands


PLEX_TOKEN = ""
PLEX_SRV = "https://
PLEX_URL = "https://"

TAUTULLI_API_KEY = "
TAUTULLI_BASE_URL = "https://"

class Plex:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='streams',
                description="Returns currently playing streams on Plex.",
                brief="Display current streams")
	async def query_plex_streams_though_tautulli(self):
		tautulli_url = "{tautulli_base_url}api/v2?apikey={api_key}&cmd=get_activity".format(tautulli_base_url=TAUTULLI_BASE_URL,api_key=TAUTULLI_API_KEY)
		#tautulli_query = "{string}"
		#print (f'Plex Extension: Tautulli API called with query string of' tautulli_query)
		async with aiohttp.ClientSession() as ses:
			async with ses.get(tautulli_url) as resp:
				a = await resp.json()
				session_check = a['response']['data']['sessions'] == []
				for entry in a['response']['data']['sessions']:
					username = entry['user']
					platform = entry['platform']
					state = entry['state']
					full_title = entry['full_title']
					desc = entry['summary']
					duration_millis = entry['duration']
					duration_millis=int(duration_millis)
					#print(duration_millis)
					duration_seconds=(duration_millis/1000)%60
					duration_seconds = int(duration_seconds)
					duration_minutes=(duration_millis/(1000*60))%60
					duration_minutes = int(duration_minutes)
					duration_hours = hours=(duration_millis/(1000*60*60))%24
					if(duration_hours >=1):
						total_duration = ("%d Hours and %d Minutes" % (duration_hours, duration_minutes))
					else:
						total_duration = ("%d Minutes" % (duration_minutes))
					view_offset_millis = entry['view_offset']
					view_offset_millis=int(view_offset_millis)
					print(view_offset_millis)
					view_offset_seconds=(view_offset_millis/1000)%60
					view_offset_seconds = int(view_offset_seconds)
					view_offset_minutes=(view_offset_millis/(1000*60))%60
					view_offset_minutes = int(view_offset_minutes)
					view_offset_hours = hours=((view_offset_millis/(1000*60*60)))%24
					if(view_offset_hours >=1):
						offset = ("%d Hours and %d Minutes" % (view_offset_hours, view_offset_minutes))
					else:
						offset = ("%d Minutes" % (view_offset_minutes))
					if(entry['media_type'] == 'episode'):
						episode_number = int(entry['media_index'])
						season = int(entry['parent_media_index'])
						season_and_ep_formatted = ("(s%d:e%d)" % (season, episode_number))
						current_tv_token = '?checkFiles=1&X-Plex-Token=' + PLEX_TOKEN
						tv_thumb = PLEX_URL + entry['grandparent_thumb'] + current_tv_token
						#print(tv_thumb)
						title = entry['grandparent_title'] + ' - ' + entry['title'] + ' ' + season_and_ep_formatted
					if(entry['media_type'] == 'movie'):
						int_year = int(entry['year'])
						year = ("(%d)" % (int_year))
						current_movie_token = '?checkFiles=1&X-Plex-Token=' + PLEX_TOKEN
						movie_thumb = PLEX_URL + entry['thumb'] + current_movie_token
						#print(movie_thumb)
						title = entry['title'] + ' ' + year
					procent = entry['progress_percent']
					embed = discord.Embed(title="Currently streaming", description="", color=0x00ff00)
					if(entry['media_type'] == 'episode'):
						embed.set_thumbnail(url=tv_thumb)
					if(entry['media_type'] == 'movie'):
						embed.set_thumbnail(url=movie_thumb)
					embed.add_field(name="Username", value="{}".format(username))
					embed.add_field(name="Player", value="".join(platform), inline=False)
					embed.add_field(name="Title", value="".join(title), inline=False)
					embed.add_field(name="Summary", value="".join(desc), inline=False)
					embed.add_field(name="State", value="".join(state), inline=False)
					embed.add_field(name="Watched Duration", value="{watched} ({procent} %)".format(watched=offset, procent=procent),inline=False)
					embed.add_field(name="Total Duration", value="".join(total_duration), inline=False)
					embed.set_footer(text="Powered by Tautulli.")
					await self.bot.say(embed=embed)
				if(session_check):
					await self.bot.say("Nothing is currently streaming.")


	@commands.command(name='plex-search',
        	        description="Search from PLex",
                	brief="Search Plex")
	#@commands.guild_only()
	async def search_plex_though_tautulli(self, input):
		tautulli_url = "{tautulli_base_url}api/v2?apikey={api_key}&cmd=search&query={string}".format(tautulli_base_url=TAUTULLI_BASE_URL,api_key=TAUTULLI_API_KEY,string=input)
		#tautulli_query = "{string}"
		#print (f'Plex Extension: Tautulli API called with query string of' tautulli_query)
		async with aiohttp.ClientSession() as ses:
			async with ses.get(tautulli_url) as resp:
				a = await resp.json()
				for entry in range(a['response']['data']['results_count']):
					a = await resp.json()
					b = await resp.json()
					is_TvShow = (a['response']['data']['results_list']['show'])
					is_movie = (b['response']['data']['results_list']['movie'])
					if is_TvShow:
						c = await resp.json()
						d = await resp.json()
						e = await resp.json()
						f = await resp.json()
						title = (c['response']['data']['results_list']['show'][entry]['title'])
						year = (d['response']['data']['results_list']['show'][entry]['year'])
						desc = (e['response']['data']['results_list']['show'][entry]['summary'])
						thumbail_not_full = (f['response']['data']['results_list']['show'][entry]['thumb'])
						tv_plex_token = '?checkFiles=1&X-Plex-Token=' + PLEX_TOKEN
						tv_generated_url = PLEX_URL + thumbail_not_full + tv_plex_token
						tv_embed = discord.Embed(title="Search results for TV", description="", color=0x00ff00)
						tv_embed.set_thumbnail(url=tv_generated_url)
						tv_embed.add_field(name="Title", value=title)
						tv_embed.add_field(name="Year", value=year)
						tv_embed.add_field(name="Summary", value=desc)
						await self.bot.say(embed=tv_embed)
					elif is_movie:
						h = await resp.json()
						i = await resp.json()
						j = await resp.json()
						k = await resp.json()
						l = await resp.json()
						movie_title = (h['response']['data']['results_list']['movie'][entry]['title'])
						movie_genre = (i['response']['data']['results_list']['movie'][entry]['genres'])
						movie_year = (j['response']['data']['results_list']['movie'][entry]['year'])
						movie_desc = (k['response']['data']['results_list']['movie'][entry]['summary'])
						movie_thumb_not_full = (l['response']['data']['results_list']['movie'][entry]['thumb'])
						movie_plex_token = '?checkFiles=1&X-Plex-Token=' + PLEX_TOKEN
						movie_generated_url = PLEX_URL + movie_thumb_not_full + movie_plex_token
						movie_embed = discord.Embed(title="Search results for Movies", description="", color=0x00ff00)
						movie_embed.set_thumbnail(url=movie_generated_url)
						movie_embed.add_field(name="Title", value=movie_title)
						movie_embed.add_field(name="Genre", value=" ,\n".join(movie_genre))
						movie_embed.add_field(name="Year", value=movie_year)
						movie_embed.add_field(name="Summary", value=movie_desc)
						await self.bot.say(embed=movie_embed)
					else:
						await self.bot.say("Unable to find anything.")
						break
def setup(bot):
	bot.add_cog(Plex(bot))
	print ("Plex extension has been loaded.")
