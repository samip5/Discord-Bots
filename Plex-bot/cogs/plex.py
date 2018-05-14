import random
import json
import aiohttp
import requests
import discord

from plexapi.server import PlexServer
from plexapi.library import Library
from discord.ext import commands


plexToken = ""
plexSRV = ""
plexURL = ""

TAUTULLI_API_KEY = ""
TAUTULLI_BASE_URL = "https://"

class Plex:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='streams',
                description="Returns currently playing streams on Plex.",
                brief="Display current streams")
	#@commands.guild_only()
	async def query_plex_streams(self):
				sess = requests.Session()
				sess.verify = False
				plex = PlexServer(baseurl=plexSRV,token=plexToken,session=sess)
				session_check = plex.sessions() == []
				session_check_not_empty = plex.sessions() != []
				#print (session_check)
				#print (plex.sessions())
				#if session_check_not_empty:
				for session in plex.sessions():
					state = session.players[0].state
					duration = session.duration
					duration_millis = session.duration
					duration_seconds=(duration_millis/1000)%60
					duration_seconds = int(duration_seconds)
					duration_minutes=(duration_millis/(1000*60))%60
					duration_minutes = int(duration_minutes)
					duration_hours = hours=(duration_millis/(1000*60*60))%24
					if(duration_hours == 0):
						total_duration = ("%d Minutes" % (duration_minutes))
					if(duration_hours != 0):
						total_duration = ("%d Hours and %d Minutes" % (duration_hours, duration_minutes))
					view_offset = session.viewOffset
					view_offset_millis = session.viewOffset
					view_offset_seconds=(view_offset_millis/1000)%60
					view_offset_seconds = int(view_offset_seconds)
					view_offset_minutes=(view_offset_millis/(1000*60))%60
					view_offset_minutes = int(view_offset_minutes)
					view_offset_hours = hours=round((view_offset_millis/(1000*60*60)))%24
					if(view_offset_hours == 0):
						offset = ("%d Minutes" % (view_offset_minutes))
					if(view_offset_hours != 0):
						offset = ("%d Hours and %d Minutes" % (view_offset_hours, view_offset_minutes))
					#print(view_offset)
					#print(view_offset_hours)
					percentage = round(view_offset / duration * 100)
					username = session.usernames[0]
					title = (session.grandparentTitle + ' - ' if session.type == 'episode' else '') + session.title
					state = session.players[0].state
					embed = discord.Embed(title="Currently streaming", description="", color=0x00ff00)
					embed.add_field(name="Username", value="{}".format(username))
					embed.add_field(name="Title", value="".join(title), inline=False)
					embed.add_field(name="State", value="".join(state), inline=False)
					embed.add_field(name="Watched Duration", value="{watched} ({procent} %)".format(watched=offset, procent=percentage),inline=False)
					embed.add_field(name="Total Duration", value="".join(total_duration), inline=False)
					embed.set_footer(text="Powered by plexapi.")
					await self.bot.say(embed=embed)
				if session_check:
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
						#print (generated_url)
						tv_embed = discord.Embed(title="Search results for TV", description="", color=0x00ff00)
						tv_embed.set_thumbnail(url=tv_generated_url)
						#print (title)
						#print (year)
						#print (desc)
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
	print ("Plex extension is loaded.")
