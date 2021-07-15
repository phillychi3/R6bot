import discord
from discord.ext import commands
from PIL import Image
import pytesseract
import grequests
import requests
import time
import shutil
import json
import uuid
import os
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # PATH tesseract.exe

bot = commands.Bot(command_prefix= 'r')
#bot.remove_command("help")


def lol(data):
    name=data["data"][0]["username"]
    lv=data["data"][0]["progressionStats"]["level"]
    kd=data["data"][0]["genericStats"]["general"]["kd"]
    return name, lv, kd

@bot.event
async def on_ready():
    print('R6機器人已上線喔')

@bot.command()
async def ping(ctx):
    await ctx.send(F'{round(bot.latency*1000)} (ms)')



@bot.command()
async def img(ctx):
    try:
        url = ctx.message.attachments[0].url
    except IndexError:
        print("no")
    else:
        if url[0:26] == "https://cdn.discordapp.com":
            r= requests.get(url,stream=True)
            try:
                imgid=uuid.uuid4()
                image = imgid +".jpg"
                with open(image,"wb") as f:
                    print("save")
                    shutil.copyfileobj(r.raw,f)
            except:
                await ctx.send("error and idk")
    img = Image.open(image)
    text = pytesseract.image_to_string(img)
    splittext=text.split("\n")
    try:
        for i in range(len(splittext)):

            if splittext[i] == "":
                del splittext[i]
            if splittext[i] == " ":
                del splittext[i]
            if splittext[i] == "\x0c":
                del splittext[i]
                
    except:
        try:
            for i in range(len(splittext)):

                if splittext[i] == "":
                    del splittext[i]
                if splittext[i] == " ":
                    del splittext[i]
                if splittext[i] == "\x0c":
                    del splittext[i]
        except:
            try:
                for i in range(len(splittext)):

                    if splittext[i] == "":
                        del splittext[i]
                    if splittext[i] == " ":
                        del splittext[i]
                    if splittext[i] == "\x0c":
                        del splittext[i]
            except:
                for i in range(len(splittext)):

                    if splittext[i] == "":
                        del splittext[i]
                    if splittext[i] == " ":
                        del splittext[i]
                    if splittext[i] == "\x0c":
                        del splittext[i]
                
    for i in range(len(splittext)):
        splittext[i]=splittext[i].replace(" ", "")
    links=[]


    for page in splittext:
        links.append(f"https://r6stats.com/api/player-search/{page}/pc" )


    reqs = (grequests.get(link) for link in links)  # 建立請求集合
    response = grequests.imap(reqs, grequests.Pool(5))  # 平行發送請求


    embed = discord.Embed(color=ctx.author.colour, timestamp=ctx.message.created_at)

    for r in response:

        name, lv, kd=lol(r.json())
        embed.add_field(name=name, value=f"lv:{lv}  kd:{kd}",inline=False)

    await ctx.send(embed=embed)
    os.remove(image)
bot.run('ODY1MTY5MTI1MDgzNzA5NDQw.YPAFiQ.WyR9pTZouTNl2iaPYyuQ9gOehKc')