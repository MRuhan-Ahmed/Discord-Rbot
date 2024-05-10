'''
level.py is the cog that encapsulates all the algorithms the bot uses
to maintain a database of users info (user id, guild id, level and experience).
The events are: on_message
The commands are: level

Band A:
/1. Dynamic generation of objects based on complex user-defined use of OOP model
/2. Server-side scripting using request and response objects;
/3. Server-side extensions for a complex client-server model;
/4. Calling parameterised Web service APIs;
/5. Cross-table parameterised SQL

Band B:
/1. Simple user defined algorithms;
/2. Generation of objects based on simple OOP model

Band C:
/1. Simple mathematical calculations
/2. Single table database

Key:
Band A.1 = an example of: Dynamic generation of objects...
'''

import discord
from discord.ext import commands

class Level(commands.Cog):
    '''Encapsulates all algorithms & commands in the Levels class (Band A.1)'''
    def __init__(self, bot):
        self.bot = bot

    async def lvl_up(self, user):
        '''The algorithm that updates the user's level (Band B.1)'''
        current_xp = user['xp']
        current_lvl = user['level']

        if current_xp >= round((4 * (current_lvl ** 3)) / 5):
        # Computes the next current xp (Band C.1)
            await self.bot.pg_con.execute(
                """
                UPDATE users
                SET level = $1
                WHERE user_id = $2 AND guild_id = $3
                """,
                current_lvl + 1, user['user_id'], user['guild_id']
            )   # Updates the user's record in the database (Band C.2)
            # Dollar sign used as placeholder for variable names not defined in SQL (Band A.5)
            return True
        return False

    @commands.Cog.listener()
    # (Band A.2)
    async def on_message(self, ctx):
        '''Event is called on every message recieved by the bot and levels up the user'''
        if ctx.author == self.bot.user: # Doesn't level up the bot itself
            return

        user = await self.bot.pg_con.fetchrow(
            """
            SELECT *
            FROM users
            WHERE user_id = $1 AND guild_id = $2
            """,
            ctx.author.id, ctx.guild.id
        )   # (Band A.5; C.2)

        if not user: # Creates a new user if user is returned false
            user = await self.bot.pg_con.fetchrow(
                """
                INSERT INTO users (user_id, guild_id)
                VALUES ($1, $2)
                RETURNING *
                """,
                ctx.author.id, ctx.guild.id
            )   # (Band A.5; C.2)

        await self.bot.pg_con.execute(
            """
            UPDATE users
            SET xp = $1
            WHERE user_id = $2 AND guild_id = $3
            """,
            user['xp'] + 1, ctx.author.id, ctx.guild.id
        )   # Finds the user and gives them +1 xp (Band A.5; C.1; C.2) 

        if await self.lvl_up(user): # Sends a mention to the user that they have levelled up
            await ctx.channel.send(f"{ctx.author.mention} is now level {user['level'] + 1}")

    @commands.command(aliases=['lvl'])
    async def level(self, ctx, member: discord.Member = None):
        '''Shows the level of members in the current guild'''
        if member == self.bot.user:
            return

        member = ctx.author if not member else member
        # If no member argument is given, then the member is the user who typed the message

        user = await self.bot.pg_con.fetchrow(
            """
            SELECT *
            FROM users
            WHERE user_id = $1 AND guild_id = $2
            """,
            member.id, member.guild.id
        )   # (Band A.5)

        if not user:
            user = await self.bot.pg_con.fetchrow(
                """
                INSERT INTO users (user_id, guild_id)
                VALUES ($1, $2)
                RETURNING *
                """,
                member.id, member.guild.id
            )   # Creates a new user if user is returned as false (Band A.5; C.2)

        await self.bot.pg_con.execute(
            """
            UPDATE users
            SET xp = $1
            WHERE user_id = $2 AND guild_id = $3
            """,
            user['xp'], member.id, member.guild.id
        )   # Updates the user's record to match their current data (Band A.5; C.2)

        embed = discord.Embed(
            color=member.color,
            timestamp=ctx.message.created_at
        )   # Creates a Discord integrated embed (a sort of g.u.i for images)

        embed.set_author(name=f"Level - {member}", icon_url=member.avatar_url)
        embed.add_field(name='Level', value=user['level'])
        embed.add_field(name='Experience', value=user['xp'])
        # Fields created to enter in the user's data (Band C.2)

        await ctx.send(embed=embed)
        print(user['user_id'])

def setup(bot):
    '''Entry point to the "r_bot.py" file (Band B.1)'''
    bot.add_cog(Level(bot))
    # Registers the "lvent.py" cog to the bot
