import discord
import sys
import sqlite3
from discord.ext import commands

cmdtest = commands.Bot(command_prefix=';')

enabled = True

### Events

@cmdtest.command()
async def test(ctx, arg: str=None):
    await ctx.send("hello!")
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
    if ctx.author.id == 94951931172098048:
        await cmdtest.logout()
        db.close()
        sys.exit("[SYSTEM] Exiting...")
    else:
        await ctx.author.send("You do not have permission to shut down this bot. Please contact @Darren#0268 for help.")

@cmdtest.command()
async def leaderboard(ctx, arg: str=None, amt: str=None):
    if arg:
        if arg == "day":
            wow = 1
            temp = "```Daily Message Leaderboard:\n"
            for row in cr.execute(''' SELECT tag, msgCount as 'amt' FROM users WHERE day=date('now') GROUP BY id ORDER BY amt desc LIMIT {0} '''.format(5 if amt == None else amt)):
                temp += (str(wow) + ". " + str(row[0]) + " (" + str(row[1]) + " messages)") + "\n"
                wow+=1
            temp += "```"
            await ctx.channel.send(temp)
        elif arg == "total":
            wow = 1
            temp = "```Cumulative Message Leaderboard:\n"
            for row in cr.execute(''' SELECT tag, SUM(msgCount) as 'amt' FROM users GROUP BY id ORDER BY amt desc LIMIT {0} '''.format(5 if amt == None else amt)):
                temp += (str(wow) + ". " + str(row[0]) + " (" + str(row[1]) + " messages)") + "\n"
                wow+=1
            temp += "```"
            await ctx.channel.send(temp)
        else:
            await ctx.channel.send("```Usage: ;leaderboard (day|total) [limit]```")
    else:
        await ctx.channel.send("```Usage: ;leaderboard (day|total) [limit]```")

@cmdtest.event
async def on_ready():
    print('[SYSTEM] Logged in as {0.user}'.format(cmdtest))
    await cmdtest.change_presence(activity=discord.Activity(name='with ur mom', type=discord.ActivityType.playing))

@cmdtest.event
async def on_message(message):
    if message.author == cmdtest.user:
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

db = sqlite3.connect('test.db')
cr = db.cursor()
cr.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ''')
if cr.fetchone()[0] != 1:
    cr.execute(''' CREATE TABLE users (id text, tag text, day date, msgCount integer) ''')
    db.commit()

cmdtest.run('<key here>')