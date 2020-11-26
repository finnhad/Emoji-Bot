import discord
from discord.ext import commands
import re

bot = commands.Bot(command_prefix='!')

allowDM = True # global var to allow role DMs


@bot.event
async def on_shard_ready():
    print("hi")
    print(roleChannel)

    roleChannel = bot.get_channel(int(744294091516411974)) # get role channel

    await roleSetup(roleChannel) # called on bot boot



@commands.command()
async def hello(ctx):
    """Hello world"""
    await ctx.send(f"Hello, {ctx.author.display_name}") # debug message


bot.add_command(hello)


@commands.has_permissions(administrator=True)
@commands.command()
async def roledm(ctx):
    """Toggles confirmation DM"""
    global allowDM
    allowDM = not allowDM # whether or not bot can DM
    await ctx.channel.send("Role DMs set to " + ("on" if allowDM else "off"))

bot.add_command(roledm)


@commands.has_permissions(administrator=True)
@commands.command()
async def roles(ctx):
    """(Re)Populates role data structure. Automatically called on startup"""

    channel = ctx.channel  # get channel Object
    await channel.last_message.delete() # remove command
    await roleSetup(channel)

bot.add_command(roles)


roleDict = {} # to be filled on $setup and kept during runtime
async def roleSetup(channel):
    """Creates role data structure"""

    async for message in channel.history(oldest_first = True): # all messages in role channel, chronological order just cus
        roleDict[message.id] = {} # dictionary entry
        roles = message.content.split('\n') # split message by lines ([emoji] role name)
        for line in roles:
            split = line.strip().split(' ', 1) # split line by spaces, max 2 results (emoji and role)
            if (re.search(r'^.*\w.*$', split[0])) is None: # avoid heading message ("__School of X__", "*major category*)
                roleDict[message.id][split[0]] = split[1].strip() # add dictionary entry for message entry (emoji : role name)


@commands.has_permissions(administrator=True)
@commands.command()
async def emojis(ctx):
    """Checks all messages in the channel and reacts with emojis in the message"""

    channel = ctx.channel  # get channel Object
    await channel.last_message.delete()  # remove command
    async with channel.typing():  # let user know command is running
        async for message in channel.history(oldest_first=True):  # all messages in role channel, chronological order just cus
            emojiList = re.findall(r'[^a-zA-Z0-9\s_&()\'!,*:/\-]+', message.content)  # regex to remove all except unicode emojis - works for *most* emojis
            await message.clear_reactions() # remove all old reactions
            for e in emojiList:
                await message.add_reaction(e)  # does not work for non space-separated emojis

bot.add_command(emojis)


@bot.event
async def on_raw_reaction_add(payload):
    guild = discord.utils.find(lambda g : g.id == payload.guild_id, bot.guilds) # get guild Object

    if (bot.user.id == payload.user_id):
        return # don't react to self

    role = None # default
    if payload.message_id in roleDict.keys(): # check if reaction added was on a role message
        if payload.emoji.name in roleDict[payload.message_id].keys(): # check if emoji represents a role
            role = discord.utils.get(guild.roles, name=roleDict[payload.message_id][payload.emoji.name]) # get role Object

    if role is not None:
        member = await guild.fetch_member(payload.user_id)  # get user Object
        if member is not None:
            if not(member in role.members): # check if user exists and doesn't already have role
                await member.add_roles(role) # add role
                if(allowDM):
                    await member.send(f"Added {role.name} role") # send confirmation DM to user
            # else:
            #     if(allowDM):
            #         await member.send(f"User already has {role.name} role. Cannot add.") # send error DM to user


@bot.event
async def on_raw_reaction_remove(payload):
    guild = discord.utils.find(lambda g: g.id == payload.guild_id, bot.guilds)  # get guild Object

    role = None # default
    if payload.message_id in roleDict.keys(): # check if reaction removed was on a role message
        if payload.emoji.name in roleDict[payload.message_id].keys(): # check if emoji represents a role
            role = discord.utils.get(guild.roles, name=roleDict[payload.message_id][payload.emoji.name]) # get role Object

    if role is not None:
        member = await guild.fetch_member(payload.user_id) # get user Object
        if member is not None:
            if not(member in role.members): # check if user exists and already has role
                await member.remove_roles(role) # remove role
                if(allowDM):
                    await member.send(f"Removed {role.name} role") # send confirmation DM to user
            # else:
            #     if(allowDM):
            #         await member.send(f"User does not have {role.name} role. Cannot remove.") # send error DM to user


keyFile = open('key.txt', 'r')
key = keyFile.readline()
bot.run(key)
keyFile.close()
