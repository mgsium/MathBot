# Third-Party Libs
import discord
from bs4 import BeautifulSoup
import wolframalpha
import numpy as np
import matplotlib.pyplot as plt

# Standard Libs
import random
import os
import requests
import re

# Local Imports
from config import Config
from util import ParodyLoader

# Discord Client Initialization
client = discord.Client()

# Misc Class Initialization
parodyLoader = ParodyLoader()

# Meme Info
new_meme_msg = ["Sending a meme!", "You asked for it...", "Meme coming up!", "Meme on the way!", "Of course!"]
filenames = os.listdir("math_memes")
n = 66

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

# Name config
# name_change_pattern = f"call me ([\w+])"

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
    elif "answer this" in message.content.lower() or "hey mathbot" in message.content.lower():
        await message.channel.send("Searching for you...")
        query = message.content.lower().split("answer this" if "answer this" in message.content.lower() else "hey mathbot")
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
    elif "show me code parodies" in message.content.lower():
        options = ""
        for i, k in enumerate(parodyLoader.links):
           options += f"[{i + 1}] {k}\n"
        await message.channel.send(f"The options:\n{options}")
    elif re.match(parodyLoader.get_parody_selection_pattern(), message.content.lower()):
        match = re.compile(parodyLoader.get_parody_selection_pattern()).search(message.content.lower()).group(1)
        index = int(match) - 1
        matched = False
        for i, k in enumerate(parodyLoader.links):
           if i ==  index:
               await message.channel.send(parodyLoader.links[k])
               matched  = True
        if not matched:
            await message.channel.send("Sorry, I could find that.")
    elif "plot" in message.content.lower():
        plt.clf()
        msg = message.content.lower().split("plot")[-1].strip()
        equation = msg
        x = np.array(range(-100, 100))
        y = eval(equation)
        plt.plot(x, y)
        n = len(os.listdir('./graphs'))
        plt.savefig(f"./graphs/{n}.png")
        await message.channel.send(file=discord.File(f"./graphs/{n}.png"))
        n+=1
        try:
            os.remove(f"./graphs/{n-2}.png")
        except:
            pass
    elif "call me" in message.content.lower():
        pass



# Run Client
client.run(Config.TOKEN)