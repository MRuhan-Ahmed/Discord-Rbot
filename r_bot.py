'''
r_bot is the main python script that initiliases the bot client
and runs all the cogs together asynchronously.
All the commands/events from the youtube tutorial are used throughout this file and the cogs,
since they are required in every bot; a defined community standard -
- from the community which created the discord.py -
but everything else (e.g. the code syntax, the os algorithms, the database) is my own

Band A:
/1. Server-side extensions for a complex client-server model;
/2. Calling parameterised Web service APIs;
/3. Parsing JSON/XML to service a complex client-server model
/4. Files organised for direct access

Band B:
/1. Writing and reading from files;

Band C:
/1. Single table database

Key:
Band A.1 = an example of: Server-side extensions...
'''

# bot ID:519932173969522698
# perm integer:8
# https://discordapp.com/oauth2/authorize?bot_id=519932173969522698&scope=bot&permissions=8
# Use CMD instead of IDLE, E.g. echo command won't work properly with idle

from itertools import cycle
import json
import os
import asyncio
import asyncpg
import discord
from discord.ext import commands
# Every python script that involves the bot's events/commands
# will call parameterised web server API's - the discord modules (Band A.2)

# ------------------------- Constants -------------------------

FILE_PATH = os.path.dirname(__file__)
# Sets current directory to R-bot's directory
TOKEN_FILE = os.path.join(FILE_PATH + "\\data\\token.txt")
TOKEN = open(TOKEN_FILE, 'r').read()
# Reads the token found in the text file

def get_prefix(rbot, message):
    '''
    Changes the command prefix depending on what guild the user typed the command.
    I use a Band A technique here, where I parse a json file, storing prefixes,
    to service my bot which effectively runs on a client-server model
    '''

    if not message.guild:
        return commands.when_mentioned_or('r-')(rbot, message)

    # These operating system algorithms aren't in Band A,
    # but they are an example of complex code
    file_path = os.path.dirname(__file__)
    prefix_file = os.path.join(file_path + "\\data\\prefixes.json")
    with open(prefix_file, 'r') as _f:
        prefixes = json.load(_f)
        # The prefixes are loaded into the json file and parsed to the bot (Band A.2)

    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or('r-')(rbot, message)
        # If the current guild doesn't have a custom prefix, the default prefix will be 'r-'

    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix)(rbot, message)

DESCRIPTION = "A bot made for helping out human users"
BOT = commands.Bot(command_prefix=get_prefix, description=DESCRIPTION)
# Initiates bot with keyword from json file and the bot's description

BOT.remove_command('help')
# Removes default help command so I can make my own

# ------------------------- Background tasks -------------------------

async def change_status():
    '''aynchronous function without threading'''
    await BOT.wait_until_ready()    # Will not run until ready() is True
    status = ['Eating cake', 'Debugging errors', 'Testing']
    msgs = cycle(status)    # Cycles through the list of pre-given messages

    while not BOT.is_closed():
        current_status = next(msgs)
        await BOT.change_presence(activity=discord.Game(current_status))
        # shows what activity the bot is doing (in reality, any string I choose)
        await asyncio.sleep(5)
        # Cycles this specific function every 3 seconds instead of using -
        # - time.sleep(3), which pauses entire program for 3 seconds

# This procedure creates the database into asyncpg (Band C.1)
async def create_db_pool():
    '''Connects to the database using asyncpg.'''
    BOT.pg_con = await asyncpg.create_pool(
        database='levelDB',
        user='postgres',
        password='password')
    

# ------------------------- Main loop -------------------------

# Loads each cog in the "cogs" directory (Band A.4)
for cog in os.listdir('.\\cogs'):
    if cog.endswith('.py'):
        # Looks for the python cogs in the current directory
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            BOT.load_extension(cog)
            print(f'{cog} loaded')
            # Loads each file as cog.{filename} and prints them
        except Exception as _e:
            print(f'{cog} cannot be loaded')
            raise _e

BOT.loop.run_until_complete(create_db_pool())
BOT.loop.create_task(change_status())   # Starts the status' cycle
BOT.run(TOKEN)  # Runs the bot using it's unique token
