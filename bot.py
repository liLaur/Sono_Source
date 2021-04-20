import discord
from discord.ext import commands
import asyncio
from pafy import new
import os

prefix = "s!"
client = commands.Bot(command_prefix=prefix)

users = []
urls = []

if os.path.isfile('Saves/users.txt'):
		with open('Saves/users.txt', 'r') as f:
			tempus = f.read()
			tempus = tempus.split(',')
			users = [x for x in tempus if x.strip()]

if os.path.isfile('Saves/urls.txt'):
		with open('Saves/urls.txt', 'r') as f:
			tempur = f.read()
			tempur = tempur.split(',')
			urls = [x for x in tempur if x.strip()]

print (users)
print (urls)

#====Evenimente====
@client.event #ready============
async def on_ready():
    print("Ready")
    for guild in client.guilds:
        await guild.system_channel.send("Ready. Careful maximum lenght is 10 seconds.")
    


@client.event
async def on_guild_join(guild):
    # for guild in client.guilds:
    await guild.system_channel.send("Hello there! I am Sono, I am here to notify you when a new member joins in a voice channel. To see available commands type in '{p}cmd'. Careful maximum lenght is 10 seconds.".format(p=prefix))

@client.event #user join============
async def on_voice_state_update(member : discord.Member, before, after):
    if before.channel is None and after.channel is not None:
        for idx, u in enumerate(users):
            if str(member) == u:
                #====Play mp3====
                voice = await after.channel.connect()

                # voice.play(discord.FFmpegPCMAudio('dau_flash.mp3'), after=None)
                
                video = new(urls[int(idx)])
                audio = video.getbestaudio().url
                voice.play(discord.FFmpegPCMAudio(audio), after=None)
                await asyncio.sleep(15)
                await voice.disconnect()
#====Evenimente====

#====Comenzi====
@client.command(aliases = ["salut", "Sal", "SALL", "sall"])
async def sal(ctx):
    await ctx.send("Salut")

@client.command(aliases = ["a"]) #add user============
async def add(ctx, user : discord.Member, url):
    users.append(str(user))
    urls.append(str(url))

    await ctx.send("Now when {us} enter a voice channel will play {ur}".format(us=user, ur=url))

    with open('Saves/users.txt', 'w') as f:
        for x in users:
            f.write(x + ',')
    
    with open('Saves/urls.txt', 'w') as f:
        for x in urls:
            f.write(x + ',')

@client.command(aliases = ["d", "del"]) #delete user============
async def delete(ctx, user : discord.Member):
    for idx, x in enumerate(users):
        if x == str(user):
            users.remove(users[idx])
            urls.remove(urls[idx])

    await ctx.send("{us} has been removed from the list".format(us=user))
    
    with open('Saves/users.txt', 'w') as f:
        for x in users:
            f.write(x + ',')
    
    with open('Saves/urls.txt', 'w') as f:
        for x in urls:
            f.write(x + ',')

@client.command(aliases = ["r", "res"]) #reset list============
async def reset(ctx):
    users = []
    urls = []
    await ctx.send("There is nobody on the list anymore")

    with open('Saves/users.txt', 'w') as f:
        for x in users:
            f.write(x + ',')
    
    with open('Saves/urls.txt', 'w') as f:
        for x in urls:
            f.write(x + ',')

@client.command()
async def list(ctx):
    if users != []:
        st = ""
        for idx, u in enumerate(users):
            if idx < len(users) - 1:
                st = st + u + ", "
            else:
                st = st + u
        await ctx.send("These are the users on the list: "+st)
    else:
        await ctx.send("There are no users")

@client.command()
async def clear(ctx, nr = 2):
    await ctx.channel.purge(limit = nr)

@client.command()
async def cmd(ctx):
    await ctx.send("My commands are: {p}add({p}add user_mention youtube_url); {p}delete({p}delete user_mention); {p}reset; {p}list; {p}clear({p}clear amount); {p}cmd".format(p=prefix))

#====Comenzi====

client.run(TOKEN)
