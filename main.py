import discord

client = discord.Client()

# TODO: run emojiPicker as Cog
# TODO: set up DB


keyFile = open('key.txt', 'r')
key = keyFile.readline()
client.run(key)
keyFile.close()
