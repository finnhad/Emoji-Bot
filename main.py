import discord
from discord.ext import commands
import re

bot = commands.Bot(command_prefix='$')

allowDM = True # global var to allow role DMs
debug = True


# TODO: turn print debugging into logging



@bot.event # a little script to automatically generate all server roles
async def on_raw_reaction_add(payload):
    print("reaction!")
    guild = discord.utils.find(lambda g : g.id == payload.guild_id, bot.guilds) # get guild Object
    if (bot.user.id == payload.user_id):
        return # don't react to self

    if (payload.emoji.name == '🤔'):

        channel = discord.utils.find(lambda c : c.id == payload.channel_id, guild.channels)
        message = await channel.fetch_message(payload.message_id)
        roles = message.content.split('\n')  # split message by lines ([emoji] role name)
        for line in roles:
            split = line.split(' ', 1)  # split line by spaces, max 2 results (emoji and role)
            if (re.search(r'^.*\w.*$', split[0])) is None:  # avoid heading message ("__School of X__", "*major category*)
                await guild.create_role(name=split[1]) # add colour param if needed (color= discord.Colour(0x579d42))
                print(f'added role {split[1]}')


keyFile = open('key.txt', 'r')
key = keyFile.readline()
bot.run(key)
keyFile.close()
