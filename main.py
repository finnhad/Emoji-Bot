import discord

client = discord.Client()




keyFile = open('key.txt', 'r')
key = keyFile.readline()
client.run(key)
keyFile.close()
