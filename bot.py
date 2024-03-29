import discord
from discord.ext import commands
import os
import requests
import random
import asyncio
import sys
import datetime

start_time = datetime.datetime.now()
bot_owner_ids = [1186151012512321552, 1213799919920484364, 1112662961757098074, 1201215798446923939]
os.system("cls")
intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)
afk_users = {}
premium_users = {}
def is_premium(ctx):
    return ctx.author.id in premium_users or ctx.author.id in bot_owner_ids

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} with ID: {bot.user.id}')
    with open('premium_users.txt', 'r') as file:
        for line in file: premium_users[int(line.strip())] = True

@bot.command()
async def staff(ctx):
     await ctx.send(embed=discord.Embed(title="Staff", description=f"Owner: ranxlus\nCo-Owner: user0_07161\nAdmins: dathecat", color=discord.Color.blue()))

@bot.command()
@commands.check(is_premium)
async def premperks(ctx):
     await ctx.send(embed=discord.Embed(title="Perks", description=f">tictactoe @user @user\n>destroy @user", color=discord.Color.blue()))

#tictactoe start
player1 = ""
player2 = ""
turn = ""
gameOver = True
board = []
winningConditions = [
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [3, 6, 9],
    [1, 5, 9],
    [1, 4, 7],
    [2, 5, 8],
    [4, 5, 6],
    [0, 4, 8],
    [2, 4, 6],
    [7, 8, 9],
    [1, 2, 3],
    [3, 5, 7]
]

@bot.command()
@commands.check(is_premium)
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0
        player1 = p1
        player2 = p2
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                line = ""
            else:
                line += " " + board[x]
        num = random.randint(1, 2)
        if num == 1:
            await ctx.send(f"It's {p1.mention} Turn!")
            turn = player1
        elif num == 2:
            await ctx.send(f"It's {p2.mention} Turn!")
            turn = player2
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@bot.command()
@commands.check(is_premium)
async def place(ctx, pos: int):
    await ctx.message.delete()
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver
    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")
                if turn == player1:
                    await ctx.send(f"It's {player1.mention} Turn!")
                    turn = player2
                elif turn == player2:
                    await ctx.send(f"It's {player2.mention} Turn!")
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")
def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True
@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")
@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")
#tictactoe end
@bot.command()
async def premcheck(ctx, member: discord.Member):
    if member in premium_users or bot_owner_ids:
        await ctx.send(f"{member.mention} Is a Premium Member!")
    else:
        await ctx.send(f"{member.mention} Is not a Premium Member!")
@bot.command()
async def prem(ctx, action: str, user: discord.User):
    if ctx.author.id in bot_owner_ids:
        if action.lower() == "add":
            if user.id not in premium_users:
                premium_users[user.id] = True
                await ctx.send(f"{user.mention} has been granted premium status.")
                with open('premium_users.txt', 'w') as file:
                    for user_id in premium_users:
                        file.write(str(user_id) + '\n') 
            else:
                await ctx.send(f"{user.mention} is already a premium user.")
        elif action.lower() == "remove":
            if user.id in premium_users:
                del premium_users[user.id]
                await ctx.send(f"{user.mention}'s premium status has been revoked.")
                with open('premium_users.txt', 'w') as file:
                    for user_id in premium_users:
                        file.write(str(user_id) + '\n')
            else:
                await ctx.send(f"{user.mention} is not a premium user.")
        else:
            await ctx.send("Invalid action. Use 'add' or 'remove'.")
    else:
        await ctx.send("You are not authorized to use this command.")


@bot.command()
@commands.check(is_premium)
async def destroy(ctx, member: discord.Member):
    await ctx.send(f"DESTROYING {member.mention}")
    await member.send(f"YOU HAVE BEEN DESTROYED {member.mention}")

@destroy.error
async def destroy_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You need to be a premium user to use this command.")

@bot.command()
async def echo(ctx, *, text):
    await ctx.send(text)

@bot.command()
async def afk(ctx, *, reason="AFK"):
    afk_users[ctx.author.id] = reason

@bot.command()
async def unafk(ctx):
    if ctx.author.id in afk_users:
        del afk_users[ctx.author.id]

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        await message.channel.send("What's up?")
        await bot.process_commands(message)
    if message.author.id in afk_users:
        afk_message = f"{message.author.mention} is currently AFK: {afk_users[message.author.id]}"
        await message.channel.send(afk_message)
        del afk_users[message.author.id]
    await bot.process_commands(message)

@bot.command()
async def uptime(ctx):
    uptime_delta = datetime.datetime.now() - start_time
    uptime_hours = uptime_delta.total_seconds() / 3600
    await ctx.send(f"Uptime: {uptime_hours:.2f} hours")

@bot.command()
async def test(ctx):
    await ctx.send("Servers are up!")

@bot.command()
async def shutdown(ctx):
    if ctx.author.id in bot_owner_ids:
        await ctx.send("Shutting down...")
        bot.close()
        sys.exit()

@bot.command()
async def restart(ctx):
    if ctx.author.id in bot_owner_ids:
        await ctx.send("Restarting...")
        os.execl(sys.executable, sys.executable, *sys.argv)

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return
        await ctx.send(f'Could not find banned user with name {member_name}')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def timeout(ctx, member: discord.Member, duration: int, *, reason=None):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, read_message_history=True, read_messages=True)
        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f'Timed out {member.mention} for {duration} seconds.')
        await asyncio.sleep(duration)
        await member.remove_roles(muted_role)
        await ctx.send(f'{member.mention} has been unmuted.')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx, channel: discord.TextChannel, *, message):
    await channel.send(message)
    await ctx.send(f"✅ Message sent to {channel.mention}")

@bot.command()
async def smack(ctx, member: discord.Member):
    await ctx.delete()
    await ctx.send(f"Smacked {member.mention} 🧑🫲 ***DING***") 

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("⚠️ You do not have the required permissions to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Please specify a channel and message to send.")

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    roles = [role.name for role in member.roles if role != ctx.guild.default_role]
    joined_at = member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
    created_at = member.created_at.strftime("%Y-%m-%d %H:%M:%S")
    embed = discord.Embed(title=f"User Info - {member}", color=member.color)
    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
    else:
        embed.set_thumbnail(url=member.default_avatar.url)
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="Display Name", value=member.display_name, inline=False)
    embed.add_field(name="Bot", value=member.bot, inline=False)
    embed.add_field(name="Created At", value=created_at, inline=False)
    embed.add_field(name="Joined At", value=joined_at, inline=False)
    embed.add_field(name=f"Roles ({len(roles)})", value=", ".join(roles) if roles else "None", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def troll(ctx):
    for _ in range(10):
        await ctx.send("https://ranxlus.github.io/5680-trollege.gif")
        
@bot.command()
async def ping(ctx):
    await ctx.send(embed=discord.Embed(title="Pong! 🏓", description=f"Latency: {round(bot.latency * 1000)}ms", color=discord.Color.green()))

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been kicked for: {reason}")
    except discord.Forbidden:
        await ctx.send("I don't have permission to kick members.")
    except discord.HTTPException:
        await ctx.send("Failed to kick member. An error occurred.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned for: {reason}")
    except discord.Forbidden:
        await ctx.send("I don't have permission to ban members.")
    except discord.HTTPException:
        await ctx.send("Failed to ban  member. An error occurred.")

@bot.command()
async def cp(ctx, member: discord.Member):
    permissions = member.guild_permissions
    permissions_text = "\n".join([f"{perm}: {value}" for perm, value in permissions])
    await ctx.send(f"Permissions of {member.mention}:\n{permissions_text}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    if amount <= 0:
        return await ctx.send("Please provide a positive number of messages to delete!")
    if amount > 1000:
        return await ctx.send("You can only delete up to 1000 messages at a time!")
    try:
        print(f"Deleted {len(await ctx.channel.purge(limit=amount + 1)) - 1} messages.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to manage messages.")
    except discord.HTTPException:
        await ctx.send("Failed to delete messages. An error occurred.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send("🔒 This channel has been locked.")
    
@lock.error
async def lock_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("⚠️ You do not have the required permissions to lock the channel.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send("🔓 This channel has been unlocked.")

@unlock.error
async def unlock_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("⚠️ You do not have the required permissions to unlock the channel.")

@bot.command()
async def roll(ctx, max_val: int = 6):
    result = random.randint(1, max_val)
    await ctx.send(f"🎲 You rolled a {result}!")

@bot.command()
async def flipcoin(ctx):
    result = random.choice(["Heads", "Tails"])
    await ctx.send(f"🪙 It's {result}!")

@bot.command()
async def cat(ctx):
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    data = response.json()
    cat_url = data[0]['url']
    await ctx.send(cat_url)

@bot.command()
async def dog(ctx):
    response = requests.get("https://api.thedogapi.com/v1/images/search")
    data = response.json()
    dog_url = data[0]['url']
    await ctx.send(dog_url)    

@bot.command()
async def rps(ctx, choice: str):
    choices = ['rock', 'paper', 'scissors']
    bot_choice = random.choice(choices)
    result = ''
    if choice.lower() not in choices:
        await ctx.send("Invalid choice. Please choose either rock, paper, or scissors.")
        return
    if choice.lower() == bot_choice:
        result = "It's a tie!"
    elif (choice.lower() == 'rock' and bot_choice == 'scissors') or \
            (choice.lower() == 'paper' and bot_choice == 'rock') or \
            (choice.lower() == 'scissors' and bot_choice == 'paper'):
        result = "You win!"
    else:
        result = "You lose!"
    await ctx.send(f"You chose: {choice.capitalize()}\nBot chose: {bot_choice.capitalize()}\nResult: {result}")

@bot.command()
async def quote(ctx):
    response = requests.get("https://api.quotable.io/random")
    data = response.json()
    quote = f"\"{data['content']}\" - {data['author']}"
    await ctx.send(quote)

@bot.command()
@commands.has_permissions(ban_members=True)
async def nuke(ctx):
    print(f"Deleted {len(await ctx.channel.purge(limit=10000000000 + 1)) - 1} messages.")

@bot.command()
async def dadjoke(ctx):
    response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
    data = response.json()
    joke = data['joke']
    await ctx.send(joke)
    
trivia_questions = {
    "What is the capital of France?": "Paris",
    "What is the largest mammal in the world?": "Blue whale",
    "Who painted the Mona Lisa?": "Leonardo da Vinci",
    "What year did the Titanic sink?": "1912",
    "Which planet is known as the Red Planet?": "Mars"
}

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title="Server Information", color=discord.Color.blue())
    embed.set_thumbnail(url=guild.icon_url)
    embed.add_field(name="Server Name", value=guild.name, inline=False)
    embed.add_field(name="Server ID", value=guild.id, inline=False)
    embed.add_field(name="Owner", value=guild.owner, inline=False)
    embed.add_field(name="Region", value=str(guild.region).capitalize(), inline=False)
    embed.add_field(name="Total Members", value=guild.member_count, inline=False)
    embed.add_field(name="Creation Date", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, user: discord.Member = None):
    user = user or ctx.author
    embed = discord.Embed(title=f"{user}'s Avatar", color=user.color)
    embed.set_image(url=user.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def roleinfo(ctx, role: discord.Role):
    embed = discord.Embed(title=f"Role Information - {role.name}", color=role.color)
    embed.add_field(name="Role ID", value=role.id, inline=False)
    embed.add_field(name="Members", value=len(role.members), inline=False)
    embed.add_field(name="Created At", value=role.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    embed.add_field(name="Mentionable", value=role.mentionable, inline=False)
    embed.add_field(name="Hoisted", value=role.hoist, inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def channelinfo(ctx, channel: discord.TextChannel):
    embed = discord.Embed(title=f"Channel Information - {channel.name}", color=discord.Color.blue())
    embed.add_field(name="Channel ID", value=channel.id, inline=False)
    embed.add_field(name="Category", value=channel.category.name if channel.category else "None", inline=False)
    embed.add_field(name="Position", value=channel.position, inline=False)
    embed.add_field(name="NSFW", value=channel.is_nsfw(), inline=False)
    embed.add_field(name="Created At", value=channel.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def trivia(ctx):
    question, answer = random.choice(list(trivia_questions.items()))
    await ctx.send(f"**Question**: {question}")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel 
    try:
        msg = await bot.wait_for('message', timeout=20.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send(f"Time's up! The correct answer was: {answer}")
    else:
        if msg.content.lower() == answer.lower():
            await ctx.send("Correct!")
        else:
            await ctx.send(f"Wrong! The correct answer was: {answer}")

@bot.command()
async def eightball(ctx, *, question: str):
    responses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes – definitely.", "You may rely on it.",
                 "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
                 "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.",
                 "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.",
                 "Outlook not so good.", "Very doubtful."]
    response = random.choice(responses)
    await ctx.send(f"Question: {question}\nAnswer: {response}")

@bot.command()
async def compliment(ctx, user: discord.Member):
    compliments = ["You're amazing!", "You're a star!", "You're a hero!", "You're awesome!",
                   "You're incredible!", "You're fantastic!", "You're a rockstar!"]
    compliment = random.choice(compliments)
    await ctx.send(f"{user.mention}, {compliment}")

@bot.command()
async def insult(ctx, user: discord.Member):
    insults = ["You're a potato.", "You're as useful as a screen door on a submarine.",
               "You're a walking, talking reason for birth control.",
               "If brains were dynamite, you wouldn't have enough to blow your nose.",
               "You're a pizza burn on the roof of the world's mouth.", "You're a fail.",
               "You're the reason the gene pool needs a lifeguard."]
    insult = random.choice(insults)
    await ctx.send(f"{user.mention}, {insult}")  

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use >help to see available commands.")  

bot.run('MTIwMjI5NzEzMDEwNzI3MzI5Ng.GWptju.0Qhfs7wX9se6WnyUgqV10alH-Z65JcWuwH0JS4')