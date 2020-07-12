import discord
import re

client = discord.Client()

allowDM = True # global var to allow role DMs
debug = True

@client.event # text commands
async def on_message(message):
    if message.author == client.user:
        return # don't react to self

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!") # debug message

    if message.content.startswith("$roleDM"):
        if (debug):
            print("roledm")

        guild = message.guild  # get guild Object
        role = discord.utils.get(guild.roles, name="Admin")
        if message.author in role.members: # only admins can toggle
            global allowDM
            allowDM = not allowDM # whether or not bot can DM
            await message.channel.send("Role DMs set to " + ("on" if allowDM else "off"))


emojidict = {
    "0": "0️⃣",
    "1": "1️⃣",
    "2": "2️⃣",
    "3": "3️⃣",
    "4": "4️⃣",
    "5": "5️⃣",
    "6": "6️⃣",
    "7": "7️⃣"
}

roleRef = {
    730909127307559034: {
        "1️⃣": "Engineering",
        "2️⃣": "Communications",
        "3️⃣": "Natural Sciences"
    }

}

messageID = {
    730909127307559034: "School",
    731045317839028234: "Class",
    731643953199448156: "Student"
}


@client.event
async def on_raw_reaction_add(payload):
    guild = discord.utils.find(lambda g : g.id == payload.guild_id, client.guilds) # get guild Object
    if (client.user.id == payload.user_id):
        return # don't react to self

    if(debug):
        print("\nReaction Add by " + payload.member.display_name)
        print(payload.emoji.name)
        # print(messageID[payload.message_id])

    if payload.emoji.name == "🧅": # TODO: fix flag emojis
        if(debug):
            print("onion setup")

        guild = discord.utils.find(lambda g: g.id == payload.guild_id, client.guilds)  # get guild Object
        member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)  # get user Object
        channel = discord.utils.find(lambda c: c.id == payload.channel_id, guild.channels) # get channel Object
        msg = await channel.fetch_message(payload.message_id) # get message Object

        await msg.remove_reaction(payload.emoji, member)  # remove onion setup emoji
        if(debug):
            print(msg.content)

        emojiList = re.findall(r'([^a-zA-Z\s_&(),*:/\-\uFE0F])', msg.content) # regex to remove all except unicode emojis
        if(debug):
            print(emojiList)
        for e in emojiList:
            await msg.add_reaction(e) # put all the emojis on message

        return # skip role selection section

    role = None # default
    if payload.message_id in roleRef.keys(): # check if reaction added was on a role message
        if(debug):
            print('message found')
        if payload.emoji.name in roleRef[payload.message_id].keys(): # check if emoji represents a role
            if(debug):
                # print('emoji found ' + payload.emoji.name)
            role = discord.utils.get(guild.roles, name=roleRef[payload.message_id][payload.emoji.name]) # get role Object
            if(debug):
                print(role)

    if role is not None:
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members) # get user Object
        if member is not None and not(member in role.members): # check if user exists and doesn't already have role
            await member.add_roles(role) # add role
            if(allowDM):
                await member.send("Added " + role.name + " role") # send confirmation DM to user
            if(debug):
                print("added role")
        else:
            if(allowDM):
                await member.send("User already has " + role.name + " role. Cannot add") # send error DM to user
            if(debug):
                print("already has role")


@client.event
async def on_raw_reaction_remove(payload):
    guild = discord.utils.find(lambda g: g.id == payload.guild_id, client.guilds)  # get guild Object
    if(debug):
        print("\nReaction Remove by " + discord.utils.find(lambda m: m.id == payload.user_id, guild.members).display_name)
        print(messageID[payload.message_id])

    role = None # default
    if payload.message_id in roleRef.keys(): # check if reaction removed was on a role message
        if(debug):
            print('message found')
        if payload.emoji.name in roleRef[payload.message_id].keys(): # check if emoji represents a role
            if(debug):
                # print('emoji found ' + payload.emoji.name)
            role = discord.utils.get(guild.roles, name=roleRef[payload.message_id][payload.emoji.name]) # get role Object
            if(debug):
                print(role)

    if role is not None:
        member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members) # get user Object
        if member is not None and member in role.members: # check if user exists and already has role
            await member.remove_roles(role) # remove role
            if(allowDM):
                await member.send("Removed " + role.name + " role") # send confirmation DM to user
            if(debug):
                print("removed role")
        else:
            if(allowDM):
                await member.send("User does not have " + role.name + " role. Cannot remove") # send error DM to user
            if(debug):
                print("doesn't have role")


keyFile = open('key.txt', 'r')
key = keyFile.readline()
client.run(key)
keyFile.close()
