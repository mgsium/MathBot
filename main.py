# Third-Party Libs
import discord
from bs4 import BeautifulSoup

# Standard Libs
import random
import os
import requests

# Local Imports
from config import Config

# Discord Client Initialization
client = discord.Client()

# Meme Info
new_meme_msg = ["Sending a meme!", "You asked for it...", "Meme coming up!", "Meme on the way!", "Of course!"]
filenames = os.listdir("math_memes")
n = 9

# Plus Automation Article Scraping
URL = "https://plus.maths.org/content/Article"
response = requests.get(URL)

soup = BeautifulSoup(response.text, "html.parser")
articles = soup.findAll("div", {"class": "col-xs-12"})
articleData = []

articleLinks = [f"https://plus.maths.org{article.find('a')['href']}" for article in articles]

# When Connecting to Discord...
@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    print(client.guilds[0])

# When a new memeber joins...
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Welcome f{member.name}!")

# When a message is sent...
@client.event
async def on_message(message):
    global n
    if "hi mathbot" in message.content.lower():
        await message.channel.send(f"Hello {message.author}!")
    # When a new meme is requested...
    elif "new meme" in message.content.lower():
        await message.channel.send(random.choice(new_meme_msg), file=discord.File(f"math_memes/{filenames[n]}"))
        n += 1
    # When a plus magazine article is requested...
    elif "plus article" in message.content.lower():
        articleLink = random.choice(articleLinks)
        await message.channel.send(articleLink)
        articleLinks.remove(articleLink)



# Run Client
client.run(Config.TOKEN)