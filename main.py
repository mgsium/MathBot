# Third-Party Libs
import discord
from bs4 import BeautifulSoup
import wolframalpha

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
n = 26

# Plus Automation Article Scraping
urls = ["https://plus.maths.org/content/Article"]
[urls.append(f"https://plus.maths.org/content/Article?page={n}") for n in range(1, 10)]
articleLinks = []
for URL in urls:
    response = requests.get(URL)

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.findAll("div", {"class": "col-xs-12"})
    [articleLinks.append(f"https://plus.maths.org{article.find('a')['href']}") for article in articles]

# Wolfram Alpha
cl = wolframalpha.Client("8PAT4Y-X56329GVYQ")

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
    elif "answer this" in message.content.lower():
        query = message.content.lower().split("answer this")
        query = query[len(query) - 1]
        print(query)
        res = cl.query(query)
        out = ""
        await message.channel.send("I found this...")
        n = 0
        try:
            for pod in res.pods:
                for sub in pod.subpods:
                    if n == 1 and sub.plaintext is not None:
                        out += f"{sub.plaintext}\n"
                        break
                    n += 1
            await message.channel.send(out)
        except Exception as e:
            pass

# Run Client
client.run(Config.TOKEN)