'''
text.py is the cog that encapsulates all the commands a standard user
of a given Discord guild (server) would use.
The commands are: ping, echo, help, display_embed, userinfo

Band A:
Dynamic generation of objects based on complex user-defined use of OOP model;
Server-side scripting using request and response objects;
Server-side extensions for a complex client-server model;
Calling parameterised Web service APIs;
Cross-table parameterised SQL

Band B:
Simple user defined algorithms;
Generation of objects based on simple OOP model
'''

import discord
from discord.ext import commands

class Text(commands.Cog):
    '''Encapsulates all text commands in the Text class'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['p'])
    # Aliases are shortcuts to the commands e.g. "r-ping" ≡ "r-p"
    # Youtube tutorial in v0.16.0 shows problematic error
    # Add this correction to NEA (with context)
    async def ping(self, ctx):
        '''Sends "pong" and the latency between the client and bot'''
        # Commands docstrings are in the "r-help" list (default on all bots)

        await ctx.send(f'Pong! The time latency was: {self.bot.latency}')
        # E.g. bot.say() ==> ctx.send(), say this in design

    @commands.command(aliases=['e'])
    async def echo(self, ctx, *, message: commands.clean_content):
        '''
        Echoes messages without commands triggering
        i.e. "r-echo @here" will print out the string "@here"
        but won't trigger the Discord command "@here"
        '''

        await ctx.send(message)

    @commands.command(aliases=['h'])
    async def help(self, ctx):
        '''Sends an embedded PM to the user of a list of commands'''

        embed = discord.Embed(
            title='Help commands:',
            colour=ctx.author.color,
            timestamp=ctx.message.created_at
        )

        embed.set_author(name='Help', icon_url=ctx.author.avatar_url)

        for cmds in self.bot.commands: # Creates a field for each command
            embed.add_field(name=cmds, value=f'{cmds.aliases}: {cmds.help}', inline=False)
        await ctx.author.send(embed=embed)

    @commands.command(aliases=['de'])
    async def display_embed(self, ctx):
        '''Displays a default embedded media on discord'''

        embed = discord.Embed(
            title='Google',
            description='Description',
            colour=discord.Colour.blue(),
            url='https://www.google.co.uk',
        )

        embed.set_footer(text='footer')
        embed.set_image(url='https://discordpy.readthedocs.io/en/rewrite/_images/snake.png')
        embed.set_thumbnail(url='https://www.python.org/static/img/python-logo.png')
        embed.set_author(name='Author name', icon_url='https://bit.ly/2wGaL05')
        embed.add_field(name='Field name', value='Field value', inline=False)

        await ctx.send(embed=embed) # Bot posts the embed

    @commands.command(aliases=['ui'])
    async def userinfo(self, ctx, member: discord.Member = None):
        '''Displays the user's account information'''

        member = ctx.author if not member else member
        # Makes member argument the user if it isn't given
        roles = [role for role in member.roles]
        # Makes a list of member roles a user has

        user = await self.bot.pg_con.fetchrow(
            """
            SELECT *
            FROM users
            WHERE user_id = $1 AND guild_id = $2
            """,
            member.id, member.guild.id
        )
        # Get's the user's record

        if not user: # Creates a new user if user is returned false
            user = await self.bot.pg_con.fetchrow(
                """
                INSERT INTO users (user_id, guild_id)
                VALUES ($1, $2)
                RETURNING *
                """,
                member.id, member.guild.id
            )

        await self.bot.pg_con.execute(
            """
            UPDATE users
            SET xp = $1
            WHERE user_id = $2 AND guild_id = $3
            """,
            user['xp'], member.id, member.guild.id
        )

        embed = discord.Embed(
            colour=member.colour,
            timestamp=ctx.message.created_at)

        embed.set_author(name=f'User Info - {member}')
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

        embed.add_field(name='ID:', value=member.id)
        embed.add_field(name='Guild name:',
                        value=member.display_name)
        embed.add_field(name='Created at:',
                        value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p GMT'))
        embed.add_field(name='Joined at:',
                        value=member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p GMT'))
        embed.add_field(name=f'No. of Roles: {len(roles)}',
                        value=' '.join([role.mention for role in roles]))
        embed.add_field(name='Top role:',
                        value=member.top_role.mention)
        embed.add_field(name='Level',
                        value=user['level'])
        embed.add_field(name='Experience',
                        value=user['xp'])
        embed.add_field(name='Bot?',
                        value='Human.' if not member.bot else 'B33p b00p, True')

        await ctx.send(embed=embed)

def setup(bot):
    '''Entry point to the "r_bot.py" file'''
    bot.add_cog(Text(bot))
