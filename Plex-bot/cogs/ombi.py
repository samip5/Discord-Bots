# Author: samip5

import configparser as parser
import datetime

import aiohttp
import discord
from discord.ext import commands


class Pmrs:
	def __init__(self, bot):
		self.bot = bot

	@commands.group(name='pmrs-search', description="Search from Plex Media Request System", brief="Search pmrs", pass_context=True)
	async def search_ombi(self, context):
		if context.invoked_subcommand is None:
			embed = discord.Embed(title="Plex Media System - Search", color=0xdc1112)
			embed.add_field(name="How to use search with it?", value="If you wish to search for movies, you have to specify it after this command `movie <replaceme-with-title>`.\nIf you wish to search for tv shows, you have to specify it after this command `tv <replaceme-with-series>`.", inline=False)
			embed.add_field(name="How to lookup most popular content?", value="If you wish to lookup popular movies, execute `popularmovie` after this command.\nIf you wish to lookup popular TV Shows, execute `populartv` after this command.", inline=False)
			await self.bot.say(embed=embed)

	@search_ombi.command()
	async def movie(self, input):
		config = parser.ConfigParser()
		config.read('./config.ini')
		pmrs_url = config.get('urls', 'PMRS_BASE_URL')
		pmrs_api_base = config.get('api-urls', 'ombi_api_base')
		pmrs_api_token = config.get('secrets', 'PMRS_API_KEY')
		pmrs_endpoint = config.get('api-urls', 'search_movie')
		pmrs_full_endpoint = pmrs_url + pmrs_api_base + pmrs_endpoint + input
		tvdb_image_not_full = config.get('urls', 'TVMD_IMAGE_URL')
		request_headers = {'apiKey': pmrs_api_token, 'content-type': 'application/json'}
		async with aiohttp.ClientSession() as ses:
			async with ses.get(pmrs_full_endpoint, headers=request_headers) as response:
				a = await response.json()
				for entry in a:
					title = entry['title']
					released_at = entry['releaseDate']
					poster_path = entry['posterPath']
					released_from_string = datetime.datetime.strptime(released_at, '%Y-%m-%dT%H:%M:%S')
					formatted_released = released_from_string.strftime('%B %d, %Y')
					desc = entry['overview']
					generated_url_for_thumb = tvdb_image_not_full + poster_path
					embed = discord.Embed(title="PMRS - Search Results for Movie", description="", color=0x00ff00)
					embed.add_field(name="Title", value="".join(title), inline=False)
					embed.add_field(name="Release Date", value="".join(formatted_released), inline=False)
					embed.add_field(name="Description", value="".join(desc), inline=False)
					embed.set_thumbnail(url=generated_url_for_thumb)
					embed.set_footer(text="This data is gathered from PMRS's API.")
					await self.bot.say(embed=embed)

	@search_ombi.command()
	async def tv(self, input):
		config = parser.ConfigParser()
		config.read('./config.ini')
		pmrs_url = config.get('urls', 'PMRS_BASE_URL')
		pmrs_api_base = config.get('api-urls', 'ombi_api_base')
		pmrs_api_token = config.get('secrets', 'PMRS_API_KEY')
		pmrs_endpoint = config.get('api-urls', 'search_tv')
		pmrs_full_endpoint = pmrs_url + pmrs_api_base + pmrs_endpoint + input
		request_headers = {'apiKey': pmrs_api_token, 'content-type': 'application/json'}
		async with aiohttp.ClientSession() as ses:
			async with ses.get(pmrs_full_endpoint, headers=request_headers) as response:
				a = await response.json()
				for entry in a:
					title = entry['title']
					banner = entry['banner']
					first_aired = entry['firstAired']
					aired_from_string = datetime.datetime.strptime(first_aired, '%Y-%m-%d')
					formatted_aired = aired_from_string.strftime('%B %d, %Y')
					network = entry['network']
					desc = entry['overview']
					embed = discord.Embed(title="PMRS - Search Results for TV", description="", color=0x00ff00)
					embed.add_field(name="Title", value="".join(title), inline=False)
					embed.add_field(name="Airing Network", value="".join(network), inline=False)
					embed.add_field(name="First Aired", value="".join(formatted_aired), inline=False)
					embed.add_field(name="Description", value="".join(desc), inline=False)
					embed.set_thumbnail(url=banner)
					embed.set_footer(text="This data is gathered from PMRS's API.")
					await self.bot.say(embed=embed)

	@search_ombi.command()
	async def populartv(self):
		config = parser.ConfigParser()
		config.read('./config.ini')
		pmrs_url = config.get('urls', 'PMRS_BASE_URL')
		pmrs_api_base = config.get('api-urls', 'ombi_api_base')
		pmrs_api_token = config.get('secrets', 'PMRS_API_KEY')
		pmrs_endpoint = config.get('api-urls', 'search_populartv')
		imdb_url_base = config.get('urls', 'IMDB_URL')
		pmrs_full_endpoint = pmrs_url + pmrs_api_base + pmrs_endpoint
		request_headers = {'apiKey': pmrs_api_token, 'content-type': 'application/json'}
		async with aiohttp.ClientSession() as ses:
			async with ses.get(pmrs_full_endpoint, headers=request_headers) as response:
				a = await response.json()
				for entry in a:
					title = entry['title']
					first_aired = entry['firstAired']
					aired_from_string = datetime.datetime.strptime(first_aired, '%Y-%m-%dT%H:%M:%S')
					formatted_aired = aired_from_string.strftime('%B %d, %Y')
					desc = entry['overview']
					imdbId = entry['imdbId']
					imdb_url_full = imdb_url_base + imdbId
					embed = discord.Embed(title="Currently popular TV shows", description="", color=0x00ff00)
					embed.add_field(name="Title", value="".join(title), inline=False)
					embed.add_field(name="First Aired", value="".join(formatted_aired), inline=False)
					embed.add_field(name="IMDb", value="".join(imdb_url_full), inline=False)
					embed.add_field(name="Description", value="".join(desc), inline=False)
					embed.set_footer(text="This data is gathered from PMRS's API.")
					await self.bot.say(embed=embed)

	@search_ombi.command()
	async def popularmovie(self):
		config = parser.ConfigParser()
		config.read('./config.ini')
		pmrs_url = config.get('urls', 'PMRS_BASE_URL')
		pmrs_api_base = config.get('api-urls', 'ombi_api_base')
		pmrs_api_token = config.get('secrets', 'PMRS_API_KEY')
		pmrs_endpoint = config.get('api-urls', 'search_popularmovie')
		pmrs_full_endpoint = pmrs_url + pmrs_api_base + pmrs_endpoint
		tmdb_image_not_full = config.get('urls', 'TVMD_IMAGE_URL')
		tmdb_base_url = config.get('urls', 'TMDB_URL')
		request_headers = {'apiKey': pmrs_api_token, 'content-type': 'application/json'}
		async with aiohttp.ClientSession() as ses:
			async with ses.get(pmrs_full_endpoint, headers=request_headers) as response:
				a = await response.json()
				for entry in a:
					title = entry['title']
					releaseDate = entry['releaseDate']
					released_from_string = datetime.datetime.strptime(releaseDate, '%Y-%m-%dT%H:%M:%S')
					formatted_released = released_from_string.strftime('%B %d, %Y')
					desc = entry['overview']
					picture_url = entry['posterPath']
					moviedbID = entry['theMovieDbId']
					generated_picture_url = tmdb_image_not_full + picture_url
					generated_tmdb_url = tmdb_base_url + moviedbID
					embed = discord.Embed(title="Currently popular movies", description="", color=0x00ff00)
					embed.add_field(name="Title", value="".join(title), inline=False)
					embed.add_field(name="Release date", value="".join(formatted_released), inline=False)
					embed.add_field(name="TMDB", value="".join(generated_tmdb_url), inline=False)
					embed.add_field(name="Description", value="".join(desc), inline=False)
					embed.set_thumbnail(url=generated_picture_url)
					embed.set_footer(text="This data is gathered from PMRS's API.")
					await self.bot.say(embed=embed)


def setup(bot):
	bot.add_cog(Pmrs(bot))
	print("Ombi extension has been loaded.")
