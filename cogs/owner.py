'''
owner.py is the cog that encapsulates all the commands the owner
of a given Discord guild (server) would use
The commands are: prefix, reload

Band A:
/1. Dynamic generation of objects based on complex user-defined use of OOP model;
/2. Server-side scripting using request and response objects;
/3. Server-side extensions for a complex client-server model;
/4. Calling parameterised Web service APIs;
/5. Cross-table parameterised SQL

Band B:
/1. Simple user defined algorithms;
/2. Generation of objects based on simple OOP model;
/3. Writing and reading from files

Key:
Band A.1 = an example of: Dynamic generation of objects...
'''

import json
import os
from discord.ext import commands
# (Band A.4)

async def is_guild_owner(ctx):
    '''Checks if the user is the guild owner'''
    return ctx.author.id == ctx.guild.owner.id

class Owner(commands.Cog):
    '''Encapsulates all moderation commands in the Owner class (Band A.1)'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['pref'], hidden=True)
    @commands.check(is_guild_owner)
    # Checks the user's identity as the guild owner - 
    # - and hides the command from the list of commands (Band B.1)
    async def prefix(self, ctx, *, pre):
        '''Changes the bot's prefix within a guild'''

        file_path = os.path.dirname(__file__)
        prefix_file = os.path.join(file_path + "\\..\\data\\prefixes.json")
        with open(prefix_file, 'r') as _f:
            prefixes = json.load(_f)
        # Loads the prefixes json file, for the bot to assign the guild to (Band )

        pre = prefixes[(ctx.guild.id)]  # Checks the prefix assigned to the guild
        msg = await ctx.send(f'Guild prefix is `{pre}`')
        await msg.pin() # Pins the message to the channel

        with open(prefix_file, 'w') as _f:
            json.dump(prefixes, _f, indent=4)

    @commands.command(aliases=['r'])
    @commands.check(is_guild_owner)
    async def reload(self, ctx, cog):
        '''Reloads a given cog within discord'''

        try:
            self.bot.unload_extension(f'cogs.{cog}') 
            self.bot.load_extension(f'cogs.{cog}')
            await ctx.send(f'```{cog} was reloaded```')
        except Exception as _e:
            await ctx.send(f'```{cog} cannot be loaded```')
            raise _e

    @prefix.error
    async def _prefix_error(self, ctx, error):
        '''Runs when the prefix error is raised'''
        # Underscore implies this is not a user command to be used

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Specify a prefix')
        if isinstance(error, commands.BadArgument):
            await ctx.send('Set an appropriate prefix')

def setup(bot):
    '''Entry point to the "r_bot.py" file (Band B.1)'''
    bot.add_cog(Owner(bot))
    # Registers the "owner.py" cog to the bot
