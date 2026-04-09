import discord
from discord.ext import commands
import os
import asyncio

# ─── CONFIG ──────────────────────────────────────────
# Set your token in Railway / Render / .env as: DISCORD_TOKEN=your_token_here
TOKEN = os.environ.get("DISCORD_TOKEN")
PREFIX = os.environ.get("PREFIX", "!")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable not set!")

# ─── BOT SETUP ───────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# ─── EVENTS ──────────────────────────────────────────
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print(f"   Prefix: {PREFIX}")
    print(f"   Servers: {len(bot.guilds)}")
    await bot.change_presence(activity=discord.Game(name=f"{PREFIX}help"))

@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"👋 Welcome to **{member.guild.name}**, {member.mention}!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ Unknown command. Use `{PREFIX}help` to see all commands.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to do that.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing argument: `{error.param.name}`")
    else:
        await ctx.send(f"❌ Error: {error}")
        raise error

# ─── COMMANDS ────────────────────────────────────────
@bot.command(name="ping")
async def ping(ctx):
    """Check bot latency."""
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Latency: **{latency}ms**")

@bot.command(name="hello")
async def hello(ctx):
    """Say hello."""
    await ctx.send(f"👋 Hey {ctx.author.mention}! I'm alive and running 24/7!")

@bot.command(name="serverinfo")
async def serverinfo(ctx):
    """Show server information."""
    guild = ctx.guild
    embed = discord.Embed(title=f"📊 {guild.name}", color=0x00ffaa)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Channels", value=len(guild.channels), inline=True)
    embed.add_field(name="Roles", value=len(guild.roles), inline=True)
    embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
    embed.add_field(name="Created", value=guild.created_at.strftime("%b %d, %Y"), inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    await ctx.send(embed=embed)

@bot.command(name="userinfo")
async def userinfo(ctx, member: discord.Member = None):
    """Show user info. Usage: !userinfo @user"""
    member = member or ctx.author
    embed = discord.Embed(title=f"👤 {member.display_name}", color=member.color)
    embed.add_field(name="Username", value=str(member), inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%b %d, %Y"), inline=True)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%b %d, %Y"), inline=True)
    embed.add_field(name="Roles", value=", ".join([r.name for r in member.roles[1:]]) or "None", inline=False)
    embed.set_thumbnail(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="say")
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, message: str):
    """Make the bot say something. Usage: !say Hello world"""
    await ctx.message.delete()
    await ctx.send(message)

@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    """Clear messages. Usage: !clear 10"""
    deleted = await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🗑️ Deleted **{len(deleted) - 1}** messages.")
    await asyncio.sleep(3)
    await msg.delete()

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason given"):
    """Kick a member. Usage: !kick @user reason"""
    await member.kick(reason=reason)
    await ctx.send(f"👢 **{member}** has been kicked. Reason: {reason}")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason given"):
    """Ban a member. Usage: !ban @user reason"""
    await member.ban(reason=reason)
    await ctx.send(f"🔨 **{member}** has been banned. Reason: {reason}")

@bot.command(name="poll")
async def poll(ctx, question: str, *options):
    """Create a poll. Usage: !poll "Question?" "Option 1" "Option 2" """
    if len(options) < 2:
        await ctx.send("❌ Need at least 2 options!")
        return
    if len(options) > 9:
        await ctx.send("❌ Maximum 9 options!")
        return
    emojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
    description = "\n".join([f"{emojis[i]} {opt}" for i, opt in enumerate(options)])
    embed = discord.Embed(title=f"📊 {question}", description=description, color=0x00c8ff)
    embed.set_footer(text=f"Poll by {ctx.author.display_name}")
    msg = await ctx.send(embed=embed)
    for i in range(len(options)):
        await msg.add_reaction(emojis[i])

# ─── LOAD COGS (optional extensions) ─────────────────
async def load_extensions():
    """Auto-load any cogs in the /cogs folder."""
    if os.path.isdir("cogs"):
        for filename in os.listdir("cogs"):
            if filename.endswith(".py") and not filename.startswith("_"):
                try:
                    await bot.load_extension(f"cogs.{filename[:-3]}")
                    print(f"   ✅ Loaded cog: {filename}")
                except Exception as e:
                    print(f"   ❌ Failed to load {filename}: {e}")

# ─── MAIN ─────────────────────────────────────────────
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
