import os

from discord.ext import commands
from dotenv import load_dotenv

from commands import FUNCTIONS

load_dotenv()

# DISCORD_TOKEN: Bot token (str)
# DISCORD_GUILD: Guild name (str)
# DISCORD_CHANNELS: Channel names (List[str])
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNELS = os.getenv('DISCORD_CHANNELS')

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

for func in FUNCTIONS:
    bot.add_command(func)

bot.run(TOKEN)