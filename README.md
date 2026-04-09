# 🤖 NEXUS Discord Bot

A fully-featured Discord bot that runs 24/7 on Railway (free tier).

## ✅ Commands

| Command | Description |
|---|---|
| `!ping` | Check bot latency |
| `!hello` | Bot says hi |
| `!serverinfo` | Show server stats |
| `!userinfo [@user]` | Show user info |
| `!say <message>` | Bot repeats message (mod only) |
| `!clear [amount]` | Delete messages (mod only) |
| `!kick @user [reason]` | Kick a member (mod only) |
| `!ban @user [reason]` | Ban a member (mod only) |
| `!poll "Question?" "A" "B"` | Create a reaction poll |

## 🚀 Deploy to Railway (Free, 24/7)

### Step 1 — Create your bot
1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Click **New Application** → name it → go to **Bot** tab
3. Click **Reset Token** → copy the token (keep it secret!)
4. Enable **Message Content Intent** and **Server Members Intent**
5. Go to **OAuth2 → URL Generator** → check `bot` + `applications.commands`
6. Check permissions: Send Messages, Read Messages, Manage Messages, Kick/Ban Members
7. Copy the generated URL and open it to invite the bot to your server

### Step 2 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial bot setup"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 3 — Deploy on Railway
1. Go to [railway.app](https://railway.app) and sign in with GitHub
2. Click **New Project → Deploy from GitHub repo**
3. Select your bot repository
4. Go to **Variables** tab and add:
   - `DISCORD_TOKEN` = your bot token from Step 1
   - `PREFIX` = `!` (or whatever you want)
5. Railway auto-detects the Procfile and starts your bot
6. That's it — your bot is live 24/7! 🎉

### Alternative: Deploy on Render (also free)
1. Go to [render.com](https://render.com) → New → **Background Worker**
2. Connect your GitHub repo
3. Set **Start Command**: `python bot.py`
4. Add environment variable: `DISCORD_TOKEN=your_token`
5. Deploy!

## 🔧 Adding More Commands

Edit `bot.py` and add a new command:

```python
@bot.command(name="mycommand")
async def mycommand(ctx):
    await ctx.send("Hello!")
```

Or create a file in `/cogs/` — the bot auto-loads all cog files on startup.

## 📁 Project Structure

```
discord-bot-project/
├── bot.py           ← Main bot file (edit this!)
├── requirements.txt ← Python packages
├── Procfile         ← Tells Railway how to run the bot
├── runtime.txt      ← Python version
├── .env.example     ← Template for environment variables
├── .gitignore       ← Keeps your token off GitHub
└── cogs/            ← (optional) Put extension files here
```

## ⚠️ Security

- **NEVER** put your bot token directly in `bot.py`
- **NEVER** commit your `.env` file to GitHub
- Always use environment variables (Railway's Variables tab)
