import os
from webbrowser import get
import discord
import asyncpraw
import asyncio
from aiohttp import ClientSession
import random
import json
from discord.ext import commands
client = commands.Bot(command_prefix = ',', activity = discord.Streaming(name="discord.gg/aegean", url="https://twitch.tv/00xn"), status = discord.Status.online, intents = discord.Intents.all())
if os.path.exists(os.getcwd() + "/token.json"):
    with open("./token.json") as f:
        conf = json.load(f)
token = conf["token"]

@client.event
async def on_ready():
  print(f'{client.user}')

@client.event
async def on_command_error(ctx, err):
    if isinstance(err, discord.ext.commands.errors.CommandNotFound):
        emb = discord.Embed(color = 0x2f3136, type = 'rich', description = ":x: komut bulunamadı")
        await ctx.send(embed = emb)
    elif isinstance(err, discord.ext.commands.errors.MemberNotFound):
        emb = discord.Embed(color = 0x2f3136, type = 'rich', description = ":x: kullanıcı bulunamadı")
        await ctx.send(embed = emb)
    elif isinstance(err, discord.ext.commands.errors.UserNotFound):
        emb = discord.Embed(color = 0x2f3136, type = 'rich', description = ":x: kullanıcı bulunamadı")
        await ctx.send(embed = emb)
    elif isinstance(err, discord.ext.commands.errors.ChannelNotFound):
        emb = discord.Embed(color = 0x2f3136, type = 'rich', description = ":x: kanal bulunamadı")
        await ctx.send(embed = emb)
    elif isinstance(err, discord.ext.commands.errors.EmojiNotFound):
        emb = discord.Embed(color = 0x2f3136, type = 'rich', description = ":x: emoji bulunamadı")
        await ctx.send(embed = emb)

@client.event
async def on_message_delete(ctx):
    global smc
    global sma
    global smav
    global smt
    smc = ctx.content
    sma = ctx.author
    smav = ctx.author.avatar
    await asyncio.sleep(60)
    sma = None
    smc = None
    smav = None

@client.command(name = 'cmds', aliases = ['cmd', 'command', 'commands'])
async def help(ctx):
    emb = discord.Embed(color=0x2f3136, type='rich', description = f"prefix: `,`\ndoküman: https://aeg.gitbook.io/ginseng")
    await ctx.send(embed = emb)

@client.command(name = 'ping', aliases = ['ms', 'latency', 'hey', 'p'])
async def ping(ctx):
    emb = discord.Embed(color=0x2f3136, type='rich', description = f"{client.latency} ms (websocket)")
    await ctx.send(embed = emb)

@client.command(name = 'kick')
async def kick(ctx, member : discord.Member = None, *, reason = None):
    if ctx.author.guild_permissions.kick_members:
        if member == ctx.author:
            emb = discord.Embed(color = 0x2f3136, type = 'rich', description = f":x: kendini atamazsın")
            await ctx.send(embed = emb)
        elif member == None:
            emb = discord.Embed(color = 0x2f3136, type = 'rich', description = f":x: atılacak kişiyi yazmalısın")
            await ctx.send(embed = emb)
        elif member.top_role >= ctx.author.top_role:
            emb = discord.Embed(color = 0x2f3136, type = 'rich', description = f":x: rolü senle aynı veya senden yüksek olan kişileri atamazsın")
            await ctx.send(embed = emb)
        else:
            if reason == None:
                emb1 = discord.Embed(color=0x2f3136, type='rich', description = f":white_check_mark: {member.mention} sunucudan atıldı\n__sebep:__ belirtilmedi")
                emb2 = discord.Embed(color = 0x2f3136, type = 'rich', description = f"kullanıcının dm'leri kapalı olduğu için kick mesajı gönderilemedi")
                dm = f"""**{ctx.guild.name}** sunucusundan atıldın\n__sebep:__ belirtilmedi"""
                try:
                    await member.send(dm)
                    await member.kick(reason = reason)
                    await ctx.send(embed = emb1)
                except:
                    await ctx.send(embed = emb1)
                    await member.kick(reason = reason)
                    await ctx.send(embed = emb2)
            else:
                emb = discord.Embed(color= 0x2f3136, type = 'rich', description = f":white_check_mark: {member.mention} sunucudan atıldı\n__sebep:__ {reason}")
                dm = f"""**{ctx.guild.name}** sunucusundan atıldın\n__sebep:__ {reason}"""
                try:
                    await member.send(dm)
                    await member.kick(reason = reason)
                    await ctx.send(embed = emb1)
                except:
                    await ctx.send(embed = emb1)
                    await member.kick(reason = reason)
                    await ctx.send(embed = emb2)
    else:
        emb = discord.Embed(color = 0x2f3136, type = 'rich', description = f":x: yetkin yok")
        await ctx.send(embed = emb)

@client.command(name = 'ban')
async def ban(ctx, member : discord.Member = None, *, reason = None):
    if ctx.author.guild_permissions.ban_members:
        if member == ctx.author:
            emb = discord.Embed(color = 0x2f3136, type = 'rich', description = f":x: kendini yasaklayamazsın")
            await ctx.send(embed = emb)
        elif member == None:
            emb = discord.Embed(color = 0x2f3136, type = 'rich', description = f":x: banlanacak kişiyi yazmalısın")
            await ctx.send(embed = emb)
        elif member.top_role >= ctx.author.top_role:
            emb = discord.Embed(color = 0x2f3136, type = 'rich', description = f":x: rolü senle aynı veya senden yüksek olan kişileri yasaklayamazsın")
            await ctx.send(embed = emb)
        else:
            if reason == None:
                emb1 = discord.Embed(color = 0x2f3136, type = 'rich', description = f":white_check_mark: {member.mention} sunucudan yasaklandı\n__sebep:__ belirtilmedi")
                emb2 = discord.Embed(color = 0x2f3136, type = 'rich', description = f"kullanıcının dm'leri kapalı olduğu için ban mesajı gönderilemedi")
                dm = f"""**{ctx.guild.name}** sunucusundan yasaklandın\n__sebep:__ belirtilmedi"""
                try:
                    await member.send(dm)
                    await member.ban(reason = reason)
                    await ctx.send(embed = emb1)
                except:
                    await ctx.send(embed = emb1)
                    await member.ban(reason = reason)
                    await ctx.send(embed = emb2)
            else:
                emb1 = discord.Embed(color = 0x2f3136, type = 'rich', description = f":white_check_mark: {member.mention} sunucudan yasaklandı\n__sebep:__ {reason}")
                emb2 = discord.Embed(color = 0x2f3136, type = 'rich', description = f"kullanıcının dm'leri kapalı olduğu için ban mesajı gönderilemedi")
                dm = f"""**{ctx.guild.name}** sunucusundan yasaklandın\n__sebep:__ {reason}"""
                try:
                    await member.send(dm)
                    await member.ban(reason = reason)
                    await ctx.send(embed = emb1)
                except:
                    await ctx.send(embed = emb1)
                    await member.ban(reason = reason)
                    await ctx.send(embed = emb2)
    else:
        emb = discord.Embed(color = 0x2f3136, type = 'rich', description = f":x: yetkin yok")
        await ctx.send(embed = emb)

@client.command(name = 'unban')
async def unban(ctx, user: discord.User):
    if ctx.author.guild_permissions.ban_members:
        try:
            emb = discord.Embed(color = 0x2f3136, type = 'rich', description = f":white_check_mark: {user} kullanıcısının yasağı kaldırıldı")
            await ctx.guild.unban(user)
            await ctx.send(embed = emb)
        except:
            emb = discord.Embed(color = 0x2f3136, type = 'rich', description = ":x: böyle birisi yok ya da yasaklı değil")
            await ctx.send(embed = emb)
    else:
        emb = discord.Embed(color = 0x2f3136, type = 'rich', description = ":x: yetkin yok")
        await ctx.send(embed = emb)

@client.command(name = 'avatar', aliases = ['a', 'av', 'avt'])
async def avatar(ctx, *, member : discord.Member = None):
    if member == None:
        member = ctx.author
    emb = discord.Embed(color = 0x2f3136, type = 'rich', title = f'{member.name}#{member.discriminator}')
    emb.set_image(url = member.avatar)
    await ctx.send(embed = emb)

@client.command(name = 'serveravatar', aliases = ['sa', 'sav', 'savt', 'savatar'])
async def serveravatar(ctx, *, member : discord.Member = None):
    if member == None:
        member = ctx.author
    emb = discord.Embed(color = 0x2f3136, type = 'rich', title = f'{member.name}#{member.discriminator}')
    emb.set_image(url = member.display_avatar)
    await ctx.send(embed = emb)

@client.command(name = 'banner', aliases = ['b'])
async def banner(ctx, *, user: discord.Member = None):
    if user == None:
        req = await client.http.request(discord.http.Route("GET", "/users/{uid}", uid = ctx.author.id))
        banner_id = req["banner"]
        if banner_id:
            banner_url = f"https://cdn.discordapp.com/banners/{ctx.author.id}/{banner_id}?size=1024"
            emb = discord.Embed(color = 0x2f3136, type = 'rich', title = f'{ctx.author.name}#{ctx.author.discriminator}')
            emb.set_image(url = banner_url)
            emb.set_footer(text = "discord'un embed yapısı yüzünden gifleri oynatamıyorum. almaya çalıştığınız banner gif ise linki tarayıcıda açarak gif halini görüntüleyebilirsiniz")
            await ctx.send(embed = emb)
        else:
            if ctx.author.accent_color == None:
                emb = discord.Embed(color = 0x2f3136, type = 'rich', title = f'{ctx.author.name}#{ctx.author.discriminator} kullanıcısının banneri yok. banner rengi: rengi kendisi ayarlamadığı için accent_color değerini alamıyorum.')
                await ctx.send(embed = emb)
            else:
                emb = discord.Embed(color = 0x2f3136, type = 'rich', title = f'{ctx.author.name}#{ctx.author.discriminator} kullanıcısının banneri yok. banner rengi: {ctx.author.accent_color}')
                await ctx.send(embed = emb)
    else:
        req = await client.http.request(discord.http.Route("GET", "/users/{uid}", uid = user.id))
        banner_id = req["banner"]
        if banner_id:
            banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
            emb = discord.Embed(color = 0x2f3136, type = 'rich', title = f'{user.name}#{user.discriminator}')
            emb.set_image(url = banner_url)
            emb.set_footer(text= "discord'un embed yapısı yüzünden gifleri oynatamıyorum. almaya çalıştığınız banner gif ise linki tarayıcıda açarak gif halini görüntüleyebilirsiniz")
            await ctx.send(embed = emb)
        else:
            if user.accent_color == None:
                emb = discord.Embed(color = 0x2f3136, type = 'rich', title = f'{user.name}#{user.discriminator} kullanıcısının banneri yok. banner rengi: rengi kendisi ayarlamadığı için accent_color değerini alamıyorum.')
                await ctx.send(embed = emb)
            else:
                emb = discord.Embed(color = 0x2f3136, type = 'rich', title = f'{user.name}#{user.discriminator} kullanıcısının banneri yok. banner rengi: {user.accent_color}')
                await ctx.send(embed = emb)

@client.command(name = 'picsthatgohard', aliases = ['ptgh'])
async def ptgh(ctx):
    reddit = asyncpraw.Reddit("BOT", user_agent = "ginsengpowered")
    subreddit = await reddit.subreddit("picsthatgohard")
    all_subs = []
    async for submission in subreddit.top(limit = 50):
        all_subs.append(submission)
    emb = discord.Embed(color=0x2f3136, type='rich')
    emb.set_image(url = random.choice(all_subs).url)
    emb.set_footer(text = f"r/picsthatgohard")
    await ctx.send(embed = emb)

@client.command(name = 'sil', aliases = ['del', 'delete', 'clr', 'clear', 'purge'])
async def sil(ctx, amount = 1):
    if ctx.author.guild_permissions.administrator:
        emb = discord.Embed(color = 0x2f3136, type = 'rich', description = f":white_check_mark: {amount} adet mesaj temizlendi.")
        await ctx.channel.purge(limit = amount + 1)
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(color = 0x2f3136, type = 'rich', description = f":x: yetkin yok")
        await ctx.send(embed = emb)

@client.command(name = 'discordia')
async def discordia(ctx):
    gif = ['https://media.discordapp.net/attachments/976622181012344915/1022546827104501790/attachment.gif', 'https://media.discordapp.net/attachments/976622181012344915/1021470797325422662/attachment.gif', 'https://media.discordapp.net/attachments/976622181012344915/1021838218120921138/attachment.gif']
    await ctx.send(random.choice(gif))

@client.command(name = 'snipe', aliases = ['s'])
async def snipe(ctx):
    if smc == None:
        emb = discord.Embed(color = 0x2f3136, type = 'rich', description = f":x: son 60 saniyede silinen bir mesaj yok")
        await ctx.send(embed = emb)
    elif ctx.embeds:
        emb = discord.Embed(color = 0x2f3136, type = 'rich', description = f":x: embed mesajların içeriklerini yükleyemiyorum")
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(color = 0x2f3136, type = 'rich', description = f"{smc}")
        emb.set_footer(text = f"{sma} tarafından", icon_url = f"{smav}")
        await ctx.send(embed = emb)

@client.command(name = 'mute', pass_context = True)
async def mute(ctx, *, member: discord.Member = None, reason = None):
    if ctx.author.guild_permissions.manage_roles:
        if member == ctx.author:
            emb = discord.Embed(color = 0x2f3136, type = 'rich', description = f":x: kendine mute atamazsın")
            await ctx.send(embed = emb)
        elif member == None:
            emb = discord.Embed(color = 0x2f3136, type = 'rich', description = f":x: mute atılacak kişiyi yazmalısın")
            await ctx.send(embed = emb)
        elif member.top_role >= ctx.author.top_role:
            emb = discord.Embed(color = 0x2f3136, type = 'rich', description = f":x: rolü senle aynı veya senden yüksek olan kişilere mute atamazsın")
            await ctx.send(embed = emb)
        else:
            if reason == None:
                emb1 = discord.Embed(color = 0x2f3136, type = 'rich', description = f":white_check_mark: {member.mention} mute yedi\n__sebep:__ belirtilmedi")
                emb2 = discord.Embed(color = 0x2f3136, type = 'rich', description = f"kullanıcının dm'leri kapalı olduğu için mute mesajı gönderilemedi")
                dm = f"""**{ctx.guild.name}** sunucusunda susturuldun\n__sebep:__ belirtilmedi"""
                try:
                    await member.send(dm)
                    await member.add_roles(roles = int(1032259022625185802), reason = reason)
                    await ctx.send(embed = emb1)
                except:
                    await ctx.send(embed = emb1)
                    await member.add_roles(roles = int(1032259022625185802), reason = reason)
                    await ctx.send(embed = emb2)
            else:
                emb1 = discord.Embed(color = 0x2f3136, type = 'rich', description = f":white_check_mark: {member.mention} mute yedi\n__sebep:__ {reason}")
                emb2 = discord.Embed(color = 0x2f3136, type = 'rich', description = f"kullanıcının dm'leri kapalı olduğu için mute mesajı gönderilemedi")
                dm = f"""**{ctx.guild.name}** sunucusunda susturuldun\n__sebep:__ {reason}"""
                try:
                    await member.send(dm)
                    await member.add_roles(roles = int(1032259022625185802), reason = reason)
                    await ctx.send(embed = emb1)
                except:
                    await ctx.send(embed = emb1)
                    await member.add_roles(roles = int(1032259022625185802), reason = reason)
                    await ctx.send(embed = emb2)
    else:
        emb = discord.Embed(color = 0x2f3136, type = 'rich', description = f":x: yetkin yok")
        await ctx.send(embed = emb)

client.run(token)
