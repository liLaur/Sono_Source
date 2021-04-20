import discord
from discord.ext import commands
import asyncio
from pafy import new
import os

prefix = "s!"
client = commands.Bot(command_prefix=prefix)

users = []
urls = []

#====Evenimente====
@client.event #ready============
async def on_ready():
    print("Ready")
    


@client.event
async def on_guild_join(guild):
    # for guild in client.guilds:
    await guild.system_channel.send("Hello there! I am Sono, I am here to notify you when a new member joins in a voice channel. To see available commands type in '{p}cmd'. Careful maximum lenght is 10 seconds.".format(p=prefix))

    with open('Saves/{g}_users.txt'.format(g=guild), 'w') as f:
        for x in users:
            f.write(x + ',')
    
    with open('Saves/{g}_urls.txt'.format(g=guild), 'w') as f:
        for x in urls:
            f.write(x + ',')


@client.event #user join============
async def on_voice_state_update(member : discord.Member, before, after):
    global users, urls
    if before.channel is None and after.channel is not None:

        sv = member.guild
        if os.path.isfile('Saves/{g}_users.txt'.format(g=sv)):
        		with open('Saves/{g}_users.txt'.format(g=sv), 'r') as f:
        			tempus = f.read()
        			tempus = tempus.split(',')
        			users = [x for x in tempus if x.strip()]

        if os.path.isfile('Saves/{g}_urls.txt'.format(g=sv)):
        		with open('Saves/{g}_urls.txt'.format(g=sv), 'r') as f:
        			tempur = f.read()
        			tempur = tempur.split(',')
        			urls = [x for x in tempur if x.strip()]


        for idx, u in enumerate(users):
            if str(member) == u:
                #====Play mp3====
                voice = await after.channel.connect()

                # voice.play(discord.FFmpegPCMAudio('dau_flash.mp3'), after=None)
                
                video = new(urls[int(idx)])
                audio = video.getbestaudio().url
                voice.play(discord.FFmpegPCMAudio(audio), after=None)

                duration = video.duration
                await asyncio.sleep(float(duration.replace(':', '')))
                await voice.disconnect()

#====Evenimente====

#====Comenzi====
@client.command(aliases = ["a"]) #add user============
async def add(ctx, user : discord.Member, url):
    A = True
    sv = ctx.guild
    if os.path.isfile('Saves/{g}_users.txt'.format(g=sv)):
    		with open('Saves/{g}_users.txt'.format(g=sv), 'r') as f:
    			tempus = f.read()
    			tempus = tempus.split(',')
    			users = [x for x in tempus if x.strip()]
    if os.path.isfile('Saves/{g}_urls.txt'.format(g=sv)):
    		with open('Saves/{g}_urls.txt'.format(g=sv), 'r') as f:
    			tempur = f.read()
    			tempur = tempur.split(',')
    			urls = [x for x in tempur if x.strip()]

    print(users)

    if users == []:
        users.append(str(user))
        urls.append(str(url))
        await ctx.send("Now when {us} enter a voice channel will play {ur}".format(us=user, ur=url))
        sv = ctx.guild
        with open('Saves/{g}_users.txt.'.format(g=sv), 'w') as f:
            for x in users:
                f.write(x + ',')
                  
        with open('Saves/{g}_urls.txt'.format(g=sv), 'w') as f:
            for x in urls:
                f.write(x + ',')
    else:
        if str(user) in users:
            await ctx.send("The user is already on the list")
            A = False
        else:
            if A == True:
                A = False
                users.append(str(user))
                urls.append(str(url))
                await ctx.send("Now when {us} enter a voice channel will play {ur}".format(us=user, ur=url))
                sv = ctx.guild
                with open('Saves/{g}_users.txt.'.format(g=sv), 'w') as f:
                    for x in users:
                        f.write(x + ',')
                
                with open('Saves/{g}_urls.txt'.format(g=sv), 'w') as f:
                    for x in urls:
                        f.write(x + ',')
        A = True

@client.command(aliases = ["d", "del"]) #delete user============
async def delete(ctx, user : discord.Member):
    for idx, x in enumerate(users):
        if x == str(user):
            users.remove(users[idx])
            urls.remove(urls[idx])

    await ctx.send("{us} has been removed from the list".format(us=user))
    
    sv = ctx.guild

    with open('Saves/{g}_users.txt.'.format(g=sv), 'w') as f:
        for x in users:
            f.write(x + ',')
    
    with open('Saves/{g}_urls.txt'.format(g=sv), 'w') as f:
        for x in urls:
            f.write(x + ',')

@client.command(aliases = ["r", "res"]) #reset list============
async def reset(ctx):
    sv = ctx.guild
    if os.path.isfile('Saves/{g}_users.txt'.format(g=sv)):
    		with open('Saves/{g}_users.txt'.format(g=sv), 'r') as f:
    			tempus = f.read()
    			tempus = tempus.split(',')
    			users = [x for x in tempus if x.strip()]
    if os.path.isfile('Saves/{g}_urls.txt'.format(g=sv)):
    		with open('Saves/{g}_urls.txt'.format(g=sv), 'r') as f:
    			tempur = f.read()
    			tempur = tempur.split(',')
    			urls = [x for x in tempur if x.strip()]
    if users == []:
        await ctx.send("The list is already empty")
    else:
        await ctx.send("There is nobody on the list anymore")

        sv = ctx.guild

        with open('Saves/{g}_users.txt.'.format(g=sv), 'w') as f:
            f.write("")
        
        with open('Saves/{g}_urls.txt'.format(g=sv), 'w') as f:
            f.write("")

@client.command()
async def list(ctx):

    sv = ctx.guild
    if os.path.isfile('Saves/{g}_users.txt'.format(g=sv)):
    		with open('Saves/{g}_users.txt'.format(g=sv), 'r') as f:
    			tempus = f.read()
    			tempus = tempus.split(',')
    			users = [x for x in tempus if x.strip()]

    if os.path.isfile('Saves/{g}_urls.txt'.format(g=sv)):
    		with open('Saves/{g}_urls.txt'.format(g=sv), 'r') as f:
    			tempur = f.read()
    			tempur = tempur.split(',')
    			urls = [x for x in tempur if x.strip()]


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

@client.command(aliases = ["c"])
async def clear(ctx, nr = 2):
    try:
        await ctx.channel.purge(limit = nr)
    except:
        await ctx.send("I don't have permission to do that")

@client.command()
async def cmd(ctx):
    await ctx.send("My commands are: {p}add({p}add user_mention youtube_url); {p}delete({p}delete user_mention); {p}reset; {p}list; {p}clear({p}clear amount); {p}cmd".format(p=prefix))

#====Comenzi====

client.run("ODMzNTU5NzkyMTA1NTUzOTIw.YH0HDQ.Qsjic35jGADKQahGVURNWWadm_k")