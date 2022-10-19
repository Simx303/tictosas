import discord, API
import pafy, urllib
from urllib.parse import quote as qurl
import re, time
import requests
from discord.voice_client import VoiceClient
from discord.ext import commands
import os
from io import BytesIO
from io import BufferedIOBase
from pedalboard import (
    Pedalboard,
    Convolution,
    Compressor,
    Chorus,
    Gain,
    Reverb,
    Limiter,
    LadderFilter,
    Phaser,
)
# board = Pedalboard([
#     Compressor(threshold_db=-50, ratio=25),
#     Gain(gain_db=30),
#     Chorus(),
#     LadderFilter(mode=LadderFilter.Mode.HPF12, cutoff_hz=900),
#     Phaser(),
#     Reverb(room_size=0.25),
#     ])
bot = commands.Bot(command_prefix='.',help_command=None)
FFMPEG_OPTIONS = {
    # 'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
'options': '-vn'}
volf = 0.75
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
def mod_ch():
    def predicate(ctx):
        return ctx.author.id == 477480560651141131
    return commands.check(predicate)
def bot_ch(ctx):
    def predicate(ctx):
        return ctx.author.bot == False
    return commands.check(predicate)
@bot.command()
async def clean(ctx, arg):
    await ctx.channel.purge(limit=int(arg))
    await ctx.send("**{0}** žinučiu ištrinta :white_check_mark:".format(str(arg)),delete_after=5)
@bot.command()
async def recomend(ctx):
    await ctx.send(API.get_video())
@bot.command()
async def bars(ctx):
    await ctx.send(API.get_lyrics(),tts=True)
@bot.command()
async def join(ctx):
    await ctx.author.voice.channel.connect()
@bot.command(alias=['p'])
async def play(ctx, *sh: str):
    if not ctx.voice_client:
        time.sleep(2)
        await ctx.send(API.response("prijunk"))
        return
    if not re.search(r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$', sh[0]):
        search = ' '.join(sh)
        search = search.replace(" ", "+")
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + qurl(search))
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        sh = ["https://www.youtube.com/watch?v="+video_ids[0]]
    song = pafy.new(sh[0])
    dur = song.duration.split(':')
    if dur[0]=="00":
        dur.pop(0)
    dur = ":".join(dur)
    await ctx.send(sh[0]+" **[{}]**".format(dur), delete_after=song.length+1)
    audio = song.getbestaudio()

    
    # effected = board(audio.url)
    src = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS),volume=volf)
    vc = ctx.voice_client
    if vc.is_playing():
        vc.stop()
    vc.play(source=src, after=None)
@bot.command()
async def stop(ctx):
    ctx.voice_client.stop()
@bot.command()
async def vol(ctx, volume: int):
    if volume > 100:
        await ctx.send('Garsas virs _**100**_ !!!\n**[Distorted]**')
    global volf
    volf = volume / 100
    await ctx.send('Mase paturbinta iki {}\nPasigirs kitam muzone'.format(volf))

@bot.command()
async def isjunk(ctx):
    time.sleep(1)
    await ctx.send(API.response("isjunk"))
    await ctx.voice_client.disconnect()
    await bot.close()
# @bot.command()
# async def effect(ctx, fx: str):
#     # Something later

@bot.command()
async def disc(ctx):
    await ctx.voice_client.disconnect()
@bot.command(hidden=True)
@mod_ch()
async def say(ctx, ch: discord.TextChannel, arg):
    if ctx.message.attachments != []:
        obj = ctx.message.attachments[0].filename
        await ctx.message.attachments[0].save(obj)
        await ch.send(file=discord.File(obj))
    else:
        await ch.send(arg)

@bot.command(hidden=True)
@mod_ch()
async def load(ctx, ext):
    bot.load_extension(f'cogs.{ext}')

@bot.command(hidden=True)
@mod_ch()
async def unload(ctx, ext):
    bot.unload_extension(f'cogs.{ext}')

@bot.command(hidden=True)
@mod_ch()
async def reload(ctx, ext):
    bot.unload_extension(f'cogs.{ext}')
    bot.load_extension(f'cogs.{ext}')

for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(open('token').readline())
# permision id: 2080898167
# bot invite link: https://discord.com/oauth2/authorize?client_id=764198572975194134&permissions=2080898167&scope=bot