import discord
import sys
import sqlite3
from discord.ext import commands
from datetime import datetime

cmdtest = commands.Bot(command_prefix=';')

enabled = False

admins = [94951931172098048, 94954503819759616]

starboard_posts = []

starboard_emojis = ["🌟", "😂", "⭐", "💫", "✨", "🌠"]

### Events

@cmdtest.command()
async def setup(ctx, arg: str=None):
    await ctx.send("hello! this is a temporary command")
    pass

@cmdtest.command()
async def count(ctx, user: discord.User=None):
    today = 0
    total = 0
    if user:
        for row in cr.execute(''' SELECT * FROM users where id='{0}' and day=date('now') '''.format(user.id)):
            today = row[3]
        for row in cr.execute(''' SELECT SUM(msgCount) FROM users where id='{0}' '''.format(user.id)):
            total = row[0]
        await ctx.channel.send('{0} has sent {1} messages today, and {2} total messages while this bot was online.'.format(user.mention, today, total))
    else:
        for row in cr.execute(''' SELECT * FROM users where id='{0}' and day=date('now') '''.format(ctx.author.id)):
            today = row[3]
        for row in cr.execute(''' SELECT SUM(msgCount) FROM users where id='{0}' '''.format(ctx.author.id)):
            total = row[0]
        await ctx.channel.send('{0} has sent {1} messages today, and {2} total messages while this bot was online.'.format(ctx.author.mention, today, total))
    return

@cmdtest.command()
async def exit(ctx):
    if ctx.author.id in admins:
        await cmdtest.logout()
        db.close()
        sys.exit("[SYSTEM] Exiting...")
    else:
        await ctx.author.send("You do not have permission to shut down this bot. Please contact @Darren#0268 for help.")

@cmdtest.command()
async def toggletroll(ctx):
    global enabled
    if ctx.author.id in admins:
        if enabled:
            enabled = False
            await ctx.channel.send("disabled!")
        else:
            enabled = True
            await ctx.channel.send("enabled!")

@cmdtest.command()
async def leaderboard(ctx, arg: str=None, amt: str=6):
    if arg:
        if arg == "day":
            wow = 1
            embedMsg = discord.Embed(title="Daily Message Leaderboard", description="Total messages sent in this server today", color=0x32a895)
            #temp = "```Daily Message Leaderboard:\n"
            for row in cr.execute(''' SELECT tag, msgCount as 'amt' FROM users WHERE day=date('now') GROUP BY id ORDER BY amt desc LIMIT {0} '''.format(amt)):
                #temp += (str(wow) + ". " + str(row[0]) + " (" + str(row[1]) + " messages)") + "\n"
                embedMsg.add_field(name=(str(wow) + ". " + str(row[0])), value=(str(row[1]) + " messages"), inline=True)
                wow+=1
            #temp += "```"
            #await ctx.channel.send(temp)
            await ctx.channel.send(embed=embedMsg)
        elif arg == "total":
            wow = 1
            embedMsg = discord.Embed(title="Cumulative Message Leaderboard", description="Total messages sent in this server", color=0x32a895)
            #temp = "```Cumulative Message Leaderboard:\n"
            for row in cr.execute(''' SELECT tag, SUM(msgCount) as 'amt' FROM users GROUP BY id ORDER BY amt desc LIMIT {0} '''.format(amt)):
                #temp += (str(wow) + ". " + str(row[0]) + " (" + str(row[1]) + " messages)") + "\n"
                embedMsg.add_field(name=(str(wow) + ". " + str(row[0])), value=(str(row[1]) + " messages"), inline=True)
                wow+=1
            #temp += "```"
            #await ctx.channel.send(temp)
            await ctx.channel.send(embed=embedMsg)
        else:
            await ctx.channel.send("```Usage: ;leaderboard (day|total) [limit]```")
    else:
        await ctx.channel.send("```Usage: ;leaderboard (day|total) [limit]```")

@cmdtest.command()
async def dump(ctx):
    if ctx.author.id in admins:
        await ctx.channel.send("Dumping DB file to {0}...".format(ctx.author.mention))
        with open('data.db', 'rb') as fp:
            await ctx.author.send(file=discord.File(fp))
    else:
        await ctx.channel.send("You do not have permission to execute this command!")

@cmdtest.event
async def on_reaction_add(reaction, user):
    if reaction.message.guild:
        if isinstance(reaction.emoji, str) and reaction.emoji in starboard_emojis:
            for react in reaction.message.reactions:
                if (isinstance(reaction.emoji, str)) and (reaction.emoji in starboard_emojis):
                    react_users = await react.users().flatten()
                    count = 0 # temporary, go back to 0
                    for react_user in react_users:
                        if not react_user.id == user.id:
                            count += 1
                    if count > 2: # temporary, go back to 2
                        if not reaction.message.id in starboard_posts:
                            for channel in reaction.message.guild.text_channels:
                                if "starboard" in channel.name:
                                    ### Message Contents Created Here
                                    embed=discord.Embed(title=reaction.message.content)
                                    embed.set_author(name="{0}#{1} {2}".format(reaction.message.author.name, reaction.message.author.discriminator, reaction.emoji), url=reaction.message.jump_url, icon_url=reaction.message.author.avatar_url)
                                    #embed.add_field(value=reaction.message.content)
                                    embed.set_footer(text="click username to jump to message")
                                    #embedMsg.add_field(name="", value="value")
                                    if reaction.message.attachments:
                                        embed.set_image(url=reaction.message.attachments[0].proxy_url)
                                    await channel.send(embed=embed)
                                    starboard_posts.append(reaction.message.id)
                                    break
                    break


@cmdtest.event
async def on_ready():
    print('[SYSTEM] Logged in as {0.user}'.format(cmdtest))
    await cmdtest.change_presence(activity=discord.Activity(name='Minecraft', type=discord.ActivityType.playing))

@cmdtest.event
async def on_message(message):
    if message.author == cmdtest.user:
        return
    if message.author.bot and message.embeds:
        print("[{0} - {1}:{2}] {3} || {4} || {5}".format(datetime.now(), message.author.name, message.author.discriminator, message.embeds[0].title, message.embeds[0].description, message.embeds[0].footer))
        if enabled and "h!trick" in message.embeds[0].description:
            await message.channel.send("h!trick")
            emoji = discord.utils.get(message.guild.emojis, name='robDab')
            if emoji:
                await message.add_reaction(emoji)
        elif enabled and "h!treat" in message.embeds[0].description:
            await message.channel.send("h!treat")
            emoji = discord.utils.get(message.guild.emojis, name='robDab')
            if emoji:
                await message.add_reaction(emoji)
        return
    if (not message.content.startswith(";")) and (not "bot" in message.channel.name):
        cr.execute(''' SELECT * FROM users where id='{0}' and day=date('now') '''.format(message.author.id))
        if cr.fetchone():
            cr.execute(''' UPDATE users SET msgCount = msgCount + 1 WHERE id='{0}' and day=date('now') '''.format(message.author.id))
            db.commit()
            #print("msgCount incremented for {0}".format(message.author.id))
        else:
            cr.execute(''' INSERT INTO users VALUES('{0}', '{1}', date('now'), 1)'''.format(message.author.id, message.author.name))
            db.commit()
            print("inserted row for user {0} ({1})".format(message.author.name, message.author.id))
    if ':YEP:' in message.content:
        emoji = discord.utils.get(message.guild.emojis, name='YEP')
        #print('found')
        if emoji:
            await message.add_reaction(emoji)
        return
    await cmdtest.process_commands(message)

### Setup

db = sqlite3.connect('data.db')
cr = db.cursor()
cr.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ''')
if cr.fetchone()[0] != 1:
    cr.execute(''' CREATE TABLE users (id text, tag text, day date, msgCount integer) ''')
    db.commit()
cr.execute(''' SELECT count(*) FROM sqlite_master WHERE type='table' AND name='starboard' ''')
if cr.fetchone()[0] != 1:
    cr.execute(''' CREATE TABLE starboard (orginal_id text, starboard_id text, lastUpdated datetime) ''')
    db.commit()

key = None

# assume key file is already set up.

with open("key", "r") as file:
    key=file.read().replace('\n', '')

if key:
    cmdtest.run(key)
else:
    print("[SYSTEM] Key not found!")
    db.close()
    sys.exit("[SYSTEM] Exiting...")