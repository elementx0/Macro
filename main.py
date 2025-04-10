import os
import discord
import requests
from discord.ext import tasks, commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
NEWS_API = os.getenv("NEWS_API")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    send_news.start()

@tasks.loop(minutes=30)  # Change to desired interval
async def send_news():
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("❌ Channel not found")
        return

    url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={NEWS_API}"
    response = requests.get(url).json()
    if response["status"] == "ok":
        articles = response["articles"][:1]  # send only the latest one
        for article in articles:
            headline = article["title"]
            link = article["url"]
            msg = f"**{headline}**
[Read More]({link})"
            await channel.send(msg)

bot.run(TOKEN)
