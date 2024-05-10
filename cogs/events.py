'''
events.py is the cog that encapsulates the listeners a bot uses
in the Discord guilds (servers) it has been invited to (running in).
The events are: on_ready, on_message, on_message_join, on_reaction_add
    on_reaction_remove, on_command_error

Band A:
/1. Dynamic generation of objects based on complex user-defined use of OOP model;
/2. Server-side scripting using request and response objects;
/3. Server-side extensions for a complex client-server model;
/4. Calling parameterised Web service APIs

Band B:
/1. Simple user defined algorithms;
/2. Generation of objects based on simple OOP model

Key:
Band A.1 = an example of: Dynamic generation of objects...
'''

import time
import discord
from discord.ext import commands
# (Band A.3)

class Events(commands.Cog):
    '''Encapsulates all event listeners in the Events class (Band A.1)'''
    # This event class is instantiated with decoratored attributes, as with all cogs (Band A.1)

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    # All listeners are essentially request and response objects (Band A.2)
    async def on_ready(self):
        '''
        Event is called every time bot connects / reconnects
        Due to how the listener works, this must be named "on_ready"
        like reserved methods such as "__init__" (defined community standard)
        '''

        print(
            f"""
            {time.strftime('%X')}: {self.bot.user} Logged in
            Discord Version: {discord.__version__}\n
            """
        )
        # Prints when the bot connected to the guild, in the shell

    @commands.Cog.listener()
    # (Band A.2)
    async def on_message(self, message):
        '''Event is called on every message recieved by the bot'''

        if message.author == self.bot.user:
        # Makes sure the bot doesn't reply to itself
            return

        print(
            f"{time.strftime('%X')}: {message.channel}: {message.author}: {message.content}"
        )
        # Prints each message members post in the guild

        if message.content.startswith('hi there'):
            await message.channel.send(f'Hi {message.author.name}! :smiley:')
        elif message.content.startswith('good bot'):
            await message.channel.send(f'Thank you! :smile:')
        # Bot finds string message without a prefix and responds
        # E.g. if a user starts a message with "hi there" -
        # - the bot will respond with "Hi <user who typed the message>"
        # followed by a smiley face (integrated within the Discord app.)

    @commands.Cog.listener()
    # (Band A.2)
    async def on_member_join(self, member):
        '''Event is called when a member joins the guild'''

        role = discord.utils.get(member.guild.roles, name='Newcomer')
        await member.add_roles(role)
        # Autoroles the member to the newcomer role

        print(f"{member.author} has joined the guild")

    @commands.Cog.listener()
    # (Band A.2)
    async def on_reaction_add(self, reaction, user):
        '''Event is called when a reaction is added to any message'''

        await reaction.message.channel.send(
            f"""
            {time.strftime('%X')}:
            {user.name} has added {reaction.emoji} to the message:
            `{reaction.message.content}`
            in the {reaction.message.channel} channel
            """
            )

    @commands.Cog.listener()
    # (Band A.2)
    async def on_reaction_remove(self, reaction, user):
        '''Event is called when a reaction is removed from any message'''

        await reaction.message.channel.send(
            f"""
            {time.strftime('%X')}:
            {user.name} has removed {reaction.emoji} from the message:
            `{reaction.message.content}`
            in the {reaction.message.channel} channel
            """
            )

    @commands.Cog.listener()
    # (Band A.2)
    async def on_command_error(self, ctx, error):
        '''Listens for command errors and prints them'''

        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to do that!")
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("I don't have permission to do that!")
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Err0r 404: Command not found!")

        raise error

def setup(bot):
    '''Entry point to the "r_bot.py" file (Band B.1)'''
    bot.add_cog(Events(bot))
    # Registers the "event.py" cog to the bot
