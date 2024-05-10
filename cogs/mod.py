'''
mod.py is the cog that encapsulates all the commands a Moderator user
of a given Discord guild (server) would use (to moderate other players).
The current commands are: kick, ban, clear

Band A:
/1. Dynamic generation of objects based on complex user-defined use of OOP model;
/2. Server-side scripting using request and response objects;
/3. Server-side extensions for a complex client-server model;
/4. Calling parameterised Web service APIs;
/5. Cross-table parameterised SQL

Band B:
/1. Simple user defined algorithms;
/2. Generation of objects based on simple OOP model

Key:
Band A.1 = an example of: Dynamic generation of objects...
'''

import discord
from discord.ext import commands
# (Band A.4)

class Mod(commands.Cog):
    '''Encapsulates all moderation commands in the Mod class (Band A.1)'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['k'])
    @commands.has_permissions(kick_members=True)
    #  The user must have permission to kick the other member (Band A.2)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        '''Kicks a member'''

##  if member.author.id == ctx.author.id: - Need to test this
##      raise Exception

        await member.kick(reason='No reason' if not reason else reason)
        # If no reason is given, the reason argument will be "no reason"
        await ctx.send(
            f'{member.mention} was kicked by {ctx.author.mention} for: `[{reason}]`'
        )   # Kicks the user from a guild with a reason (Band B.1)


    @commands.command(aliases=['b'])
    @commands.has_permissions(ban_members=True)
    # The user must have permission to kick the other member (Band A.2)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        '''Bans a member'''

        reason = 'No reason' if not reason else reason
        await member.ban(reason=reason)
        await ctx.send(
            f'{member.mention} was banned by {ctx.author.mention} for: `[{reason}]`'
        )   # (Band B.1)

    @commands.command(aliases=['c'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        '''Clears the past messages'''

        await ctx.channel.purge(limit=amount + 1, check=lambda msg: not msg.pinned)
        # Checks if the message is pinned; if not -
        # - it deletes the amount given by user plus the command message itself (Band B.1)
        await ctx.send(f'{amount} messages were deleted')

    @kick.error
    @ban.error
    @clear.error
    async def _error(self, ctx, error):
        '''Runs when the prefix error is raised'''
        # Underscore implies this is not a user command to be used

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing a required argument')
            # Runs if an essential argument is missing from the user's command
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Give an appropriate argument')
            # Runs if the user gives an invald argument from the user's command
        else:
            await ctx.send("You can't do that")

        raise error
    # (Band B.1)

def setup(bot):
    '''Entry point to the "r_bot.py" file (Band B.1)'''
    bot.add_cog(Mod(bot))
    # Registers the "mod.py" cog to the bot
