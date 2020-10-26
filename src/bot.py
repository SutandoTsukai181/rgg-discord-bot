import os

from discord import Intents
from discord.ext import commands

from commands import COGS

# DISCORD_TOKEN: Bot token (str)
TOKEN = os.environ.get('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.', intents=Intents.all())


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

for cog in COGS:
    bot.add_cog(cog(bot))

bot.run(TOKEN)
