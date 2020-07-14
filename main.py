import discord
import re

client = discord.Client()
debug = True

# TODO: run emojiPicker as Cog
    # https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html

# TODO: set up DB
    # figure out scraping

# TODO: make sure no missing roles


keyFile = open('key.txt', 'r')
key = keyFile.readline()
client.run(key)
keyFile.close()
