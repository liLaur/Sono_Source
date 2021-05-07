import discord
from discord.ext import commands, tasks
from itertools import cycle
import asyncio
from pafy import new
import os

prefix = "!"
client = commands.Bot(command_prefix=prefix)
status = cycle([f'{prefix}cmd | for help', 'games', 'Python', 'YouTube'])

devs = ["Lauru#9407"]

users = []
urls = []

#====up time====
sec = 0
min = 0
hour = 0
day = 0
up_time = ""

@tasks.loop(seconds=1)
async def timer():
    global sec, min, hour, day, up_time
    sec += 1
    if sec > 59:
        min += 1
        sec = 0
    if min > 59:
        hour += 1
        min = 0
    if hour > 24:
        day += 1
        hour = 0
    up_time = f"{day}:{hour}:{min} (DD:HH:MM)"
#====up time====

@tasks.loop(seconds=20)
async def update_status():
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(next(status)))

#====Evenimente====
@client.event #ready============
async def on_ready():
    update_status.start()
    timer.start()
    print("Ready")

    e = discord.Embed(title="I'M BACK!")
    e.set_thumbnail(url="https://cdn.discordapp.com/app-icons/834128397122404463/a5b6d32e724423c0dac74ba514a4f113.png?size=64")
    for g in client.guilds:
        try:
            await g.system_channel.send(embed=e)
        except:
            continue

@client.event #on join server=========
async def on_guild_join(guild):
    await guild.system_channel.send("Hello there! I'm Sono, I'm here to let you know when a new member joins a voice channel. To see the available commands, type '{p}cmd'. Add me on other servers: <https://bit.ly/32CT5DI>".format(p=prefix))
    await guild.system_channel.send(file=discord.File('HowToUse.docx'))

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
                server = member.guild.voice_client
                try:
                    await server.disconnect()
                except:
                    pass
                
                try:
                    global voice
                    voice = await after.channel.connect()
                except:
                    await member.guild.system_channel.send("I am already in a channel")
                #====Play mp3====
                
                video = new(urls[int(idx)])
                audio = video.getbestaudio().url
                voice.play(discord.FFmpegPCMAudio(audio), after=None)
                duration = video.duration
                await asyncio.sleep(float(duration.replace(':', '')))
                await voice.disconnect()
#====Evenimente====

#====Comenzi====
@client.command(aliases=['l'])
async def leave(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()

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

    video = new(url)
    if float(video.duration.replace(':', '')) <= 17:
        if str(user) != str(client.user):
            if users == []:
                users.append(str(user))
                urls.append(str(url))
                await ctx.send("Now when {us} enters a voice channel, {ur} will be played".format(us=user, ur=url))
                sv = ctx.guild
                with open('Saves/{g}_users.txt'.format(g=sv), 'w') as f:
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
                        await ctx.send("Now when {us} enters a voice channel, {ur} will be played".format(us=user, ur=url))
                        sv = ctx.guild
                        with open('Saves/{g}_users.txt'.format(g=sv), 'w') as f:
                            for x in users:
                                f.write(x + ',')
                        
                        with open('Saves/{g}_urls.txt'.format(g=sv), 'w') as f:
                            for x in urls:
                                f.write(x + ',')
                A = True
        else:
            await ctx.send("You can't add me on the list")

    else:
        await ctx.send("The video is too long. It must have a maximum of 15 seconds")

@client.command(aliases = ["d", "del"]) #delete user============
async def delete(ctx, user : discord.Member):

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

    for idx, x in enumerate(users):
        if x == str(user):
            users.remove(users[idx])
            urls.remove(urls[idx])

    await ctx.send("{us} has been removed from the list".format(us=user))
    
    sv = ctx.guild
    with open('Saves/{g}_users.txt'.format(g=sv), 'w') as f:
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

        with open('Saves/{g}_users.txt'.format(g=sv), 'w') as f:
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
        e = discord.Embed(title="Users:")
        for idx, u in enumerate(users):
            e.add_field(name=u, value=urls[int(idx)], inline=True)
        await ctx.send(embed=e)
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
    e = discord.Embed(
        title = "Commands",
        color = discord.Color.red()
    )
    e.add_field(name=f"{prefix}add", value=f'{prefix}add user_mention youtube_url', inline=True)
    e.add_field(name=f"{prefix}delete", value=f'{prefix}delete user_mention', inline=True)
    e.add_field(name=f"{prefix}reset", value=f'{prefix}reset', inline=True)
    e.add_field(name=f"{prefix}list", value=f'{prefix}list', inline=True)
    e.add_field(name=f"{prefix}clear", value=f'{prefix}clear amount', inline=True)
    e.add_field(name=f"{prefix}cmd", value=f'{prefix}cmd', inline=True)
    e.add_field(name=f"{prefix}link", value=f'{prefix}link - bot invite link', inline=True)
    e.add_field(name=f"{prefix}debug", value=f'{prefix}debug', inline=True)
    e.add_field(name=f"{prefix}leave (only when needed)", value=f'{prefix}leave', inline=True)
    e.add_field(name=f"{prefix}send (only devs)", value=f'{prefix}send(_)', inline=False)

    await ctx.send(embed=e)

@client.command()
async def link(ctx):
    await ctx.send("Here is my add link: https://discord.com/api/oauth2/authorize?client_id=833559792105553920&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com%2Fapi%2Foauth2%2Fauthorize&scope=bot")

@client.command()
async def debug(ctx):
    e = discord.Embed(
        title = "Debug info",
        color = discord.Color.blue()
    )
    e.set_footer(text="Client Version 1.0.1")
    e.set_thumbnail(url="https://cdn.discordapp.com/app-icons/833559792105553920/c5e72a5418e4d0308ce1eea12d350654.png?size=64")
    e.add_field(name="Up time:", value=up_time, inline=False)
    e.add_field(name="My Instagram", value="https://www.instagram.com/viorelaurentiu/", inline=False)
    e.add_field(name="My Discord Server", value="https://discord.gg/7TaJn7vrHc", inline=False)
    e.add_field(name="Number of active Servers:", value=len(client.guilds), inline=False)
    e.add_field(name="Creator:", value="Laurențiu Rădulescu", inline=False)

    await ctx.send(embed=e)

@client.command()
async def send(ctx, type : str):
    if str(ctx.author) in devs:
        if type == "update":
            for g in client.guilds:
                try:
                    await g.system_channel.send("I will soon be offline for a while, updating a few things here and there. :pensive: But I'll be back as soon as I can! :smiley:")
                except:
                    continue
        elif type == "review":
            for g in client.guilds:
                try:
                    await g.system_channel.send("Hey, do you like me? :upside_down: If so, go to my server and do a review. :pray: <https://discord.gg/CyE4jEJzKD>")
                except:
                    continue

        else:
            for g in client.guilds:
                try:
                    await g.system_channel.send(type.replace('_', ' '))
                except:
                    continue
#====Comenzi====

client.run("ODMzNTU5NzkyMTA1NTUzOTIw.YH0HDQ.ktETyulCZrNYi-TVSNcov6G45Yk")