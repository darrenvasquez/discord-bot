import discord
import sys
import sqlite3
from discord.ext import commands

cmdtest = commands.Bot(command_prefix=';')

enabled = True

### Events

@cmdtest.command()
async def test(ctx, arg):
    await ctx.send("hello!")
    pass

@cmdtest.command()
async def count(ctx, user: discord.User):
    if user:
        for row in cr.execute(''' SELECT * FROM users where id='{0}' '''.format(user.id)):
            #print(row)
            await ctx.channel.send('{0} has sent {1} messages while this bot was online.'.format(user.mention, row[1]))
            return
        await ctx.channel.send('{0} has sent 0 messages while this bot was online.'.format(user.mention))
    else:
        for row in cr.execute(''' SELECT * FROM users where id='{0}' '''.format(ctx.author.id)):
            #print(row)
            await ctx.channel.send('{0} has sent {1} messages while this bot was online.'.format(ctx.author.mention, row[1]))
            return
        await ctx.channel.send('{0} has sent 0 messages while this bot was online.'.format(ctx.author.mention))
        return

@cmdtest.command()
async def exit(ctx):
    if ctx.author.id == 94951931172098048:
        await cmdtest.logout()
        db.close()
        sys.exit("[SYSTEM] Exiting...")
    else:
        await ctx.author.send("You do not have permission to shut down this bot. Please contact @Darren#0268 for help.")


@cmdtest.event
async def on_ready():
    print('[SYSTEM] Logged in as {0.user}'.format(cmdtest))
    await cmdtest.change_presence(activity=discord.Activity(name='chat games', type=discord.ActivityType.playing))

@cmdtest.event
async def on_message(message):
    if message.author == cmdtest.user:
        return
    elif ':YEP:' in message.content:
        emoji = discord.utils.get(message.guild.emojis, name='YEP')
        #print('found')
        if emoji:
            await message.add_reaction(emoji)
        return
    else:
        cr.execute(''' SELECT * FROM users where id='{0}' '''.format(message.author.id))
        if cr.fetchone():
            cr.execute(''' UPDATE users SET msgCount = msgCount + 1 WHERE id='{0}' '''.format(message.author.id))
            db.commit()
            #print("msgCount incremented for {0}".format(message.author.id))
        else:
            cr.execute(''' INSERT INTO users VALUES('{0}', 1)'''.format(message.author.id))
            db.commit()
            print("inserted row for user {0}".format(message.author.id))
    if 'bot' in message.channel.name:
        print("bot channel!")
    await cmdtest.process_commands(message)

### Setup

db = sqlite3.connect('test.db')
cr = db.cursor()
cr.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ''')
if cr.fetchone()[0] != 1:
    cr.execute(''' CREATE TABLE users (id text, msgCount integer) ''')
    db.commit()
