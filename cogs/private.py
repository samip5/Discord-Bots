import discord
from discord.ext import commands


class Private:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test")
    async def private_msg(self, input):
        the_gamergirl = await self.bot.get_user_info(351003696097918979)
        owner = await self.bot.get_user_info(157970669261422592)
        try:
            await self.bot.send_message(the_gamergirl, input)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.say(fmt.format(type(e).__name__, e))
        # await self.bot.send_message(owner, input)
        await self.bot.send_message(owner, "The message was sent successfully.")


def setup(bot):
    bot.add_cog(Private(bot))
    print("Not public extension is loaded.")
