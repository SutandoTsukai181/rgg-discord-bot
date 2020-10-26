import os

from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

from commands import COGS

load_dotenv()

# DISCORD_TOKEN: Bot token (str)
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.', intents=Intents.all())


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

for cog in COGS:
    bot.add_cog(cog(bot))

bot.run(TOKEN)
