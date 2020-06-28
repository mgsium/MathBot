# Third-Party Libs
import discord
from bs4 import BeautifulSoup
import wolframalpha

# Standard Libs
import random
import os
import requests
import re

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

# Code Parodies
parody_links = {
    "Game of Codes": "https://www.youtube.com/watch?v=3vI_7os2V_o",
    "The Java Life Rap": "https://www.youtube.com/watch?v=b-Cr0EWwaTk",
    "You Give REST a Bad Name": "https://www.youtube.com/watch?v=nSKp2StlS6s",
    "Writing Bad": "https://www.youtube.com/watch?v=DGa6MAibjzA",
    "Write in Go": "https://www.youtube.com/watch?v=LJvEIjRBSDA",
    "Database Skills": "https://www.youtube.com/watch?v=0vPt7GI-2kc",
    "SUSE.Yes Please.": "https://www.youtube.com/watch?v=M9bq_alk-sw",
    "House Codes": "https://www.youtube.com/watch?v=WUAzr-3DVP8"
}
parody_selection_pattern = "show me parody ([1-8])"

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
        for i, k in enumerate(parody_links):
           options += f"[{i + 1}] {k}\n"
        await message.channel.send(f"The options:\n{options}")
    elif re.match(parody_selection_pattern, message.content.lower()):
        match = re.compile(parody_selection_pattern).search(message.content.lower()).group(1)
        index = int(match) - 1
        matched = False
        for i, k in enumerate(parody_links):
           if i ==  index:
               await message.channel.send(parody_links[k])
               matched  = True
        if not matched:
            await message.channel.send("Sorry, I could find that.")


# Run Client
client.run(Config.TOKEN)