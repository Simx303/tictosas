import discord
from discord.ext import commands
import bimbim


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='.',intents=intents)
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.command()
async def tick(ctx, tic: str):
    bimbim.tick(tic)
    print(tic)

bot.run(open('token').readline())