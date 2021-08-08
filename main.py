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
from datetime import datetime, timedelta

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
n = 106

# Plus Automation Article Scraping
"""
urls = ["https://plus.maths.org/content/Article"]
[urls.append(f"https://plus.maths.org/content/Article?page={n}") for n in range(1, 10)]
articleLinks = []
for URL in urls:
    response = requests.get(URL)

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.findAll("div", {"class": "col-xs-12"})
    [articleLinks.append(f"https://plus.maths.org{article.find('a')['href']}") for article in articles]
"""

# Wolfram Alpha
cl = wolframalpha.Client(Config.WOLFRAM_ALPHA_CLIENT_KEY)

# Name config
# name_change_pattern = f"call me ([\w+])"



# When Connecting to Discord...
@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    print(client.guilds[0])
    # channel = client.get_channel(690154591102304318)
    # await channel.send("Formatting Fixed!!")#"So you thought I was gone....well here I am, with a brand new feature.\nType `:results day` to find out how long until you discover your fate.\nFor a special message, type `:results day helen` instead!")

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
    elif ":results day helen" in message.content.lower():
        if (message.author.bot): return
        now_time = datetime.now()
        results_time = datetime.strptime("2021-08-10", "%Y-%m-%d")
        results_time = results_time.replace(minute=30, hour=8)
        delta = results_time-now_time
        delta_s = delta.seconds
        hours, remainder = divmod(delta_s, 3600)
        minutes, seconds = divmod(remainder, 60)
        days = delta.days
        quote = random.choice(["https://twitter.com/JeremyClarkson/status/1293826911752392705?s=20", "https://twitter.com/JeremyClarkson/status/499876794364092416?s=20", "https://twitter.com/JeremyClarkson/status/631715075175370752?s=20", "https://twitter.com/JeremyClarkson/status/1161920575910088705?s=20", "https://twitter.com/JeremyClarkson/status/898101177040162816?s=20", "https://twitter.com/JeremyClarkson/status/766162139736371200?s=20"])
        await message.channel.send( f"Achtung!! Only { f'{days} day ' if days > 0 else ''} {hours} hour(s), {minutes} minute(s) and {seconds} second(s) until the harrowing and ineluctable realisation of the limits of your own intelligence! But don't worry, here is a comforting word from Jeremy Clarkson: \n {quote}")
    elif ":results day" in message.content.lower():
        if (message.author.bot): return
        now_time = datetime.now()
        results_time = datetime.strptime("2021-08-10", "%Y-%m-%d")
        results_time = results_time.replace(minute=30, hour=8)
        delta = results_time-now_time
        delta_s = delta.seconds
        hours, remainder = divmod(delta_s, 3600)
        minutes, seconds = divmod(remainder, 60)
        days = delta.days
        await message.channel.send( f"Achtung!! Only { f'{days} day ' if days > 0 else ''} {hours} hour(s), {minutes} minute(s) and {seconds} second(s) until results!")

# Run Client
client.run(Config.TOKEN)