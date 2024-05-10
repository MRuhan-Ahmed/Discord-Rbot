'''
voice.py is the cog that encapsulates all the commands a standard user
of a given Discord guild voice channel would use.
The commands are: join, play, yt, stream, volume, pause, resume, stop

NB: This script is from: https://github.com/Rapptz/discord.py/blob/rewrite/examples/basic_voice.py
    and I modified is appropriately to work with my bot specifically
    e.g. add the setup function, change some line syntax etc.

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

import asyncio
import discord
from discord.ext import commands
import youtube_dl

# ------------------------- Voice channel -------------------------

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
    # Makes all connections via IPv4
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# ------------------------- Voice cog -------------------------

class YTDLSource(discord.PCMVolumeTransformer):
    '''Gets the youtube source from the url'''

    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Voice(commands.Cog):
    '''Encapsulates all the voice commands in the Voice cog'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):
        """Joins a voice channel
        If no channel is given, the bot joins the author's current voice channel"""

        channel = channel or ctx.author.voice.channel

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(destination)

        await destination.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send(f'Now playing: {query}')

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume, in the range [0, 100]"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    # I created the pause and resume commands
    # which were not included in the basic_voice.py I modified
    @commands.command()
    async def pause(self, ctx):
        """Pauses the player."""

        if ctx.voice_client:
            ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        """Resumes the player."""

        if ctx.voice_client:
            ctx.voice_client.resume()

    @commands.command()
    async def stop(self, ctx):
        """Stops the song playing and disconnects the bot from the channel"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

def setup(bot): # basic_voice.py was modified to create this setup procedure
    '''Entry point to the "r_bot.py" file'''
    bot.add_cog(Voice(bot))
