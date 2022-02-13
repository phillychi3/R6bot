import discord
from discord.ext import commands
from PIL import Image
import pytesseract
import grequests
import requests
import random
import shutil
import os
from bs4 import BeautifulSoup
from io import BytesIO
import matplotlib.pyplot as plt
import mplcyberpunk
import urllib.request
from PIL import Image,ImageDraw,ImageFont

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # PATH tesseract.exe

bot = commands.Bot(command_prefix= 'r')
#bot.remove_command("help")
title=["Overall","Season 23","General"]
large_font = ImageFont.truetype('./setofont.ttf', 40)
font = ImageFont.truetype('./setofont.ttf', 30)
medium_font = ImageFont.truetype('./setofont.ttf', 26) 
small_font = ImageFont.truetype('./setofont.ttf', 22)


def lol(data):
    try:
        name=data["data"][0]["username"]
        lv=data["data"][0]["progressionStats"]["level"]
        kd=data["data"][0]["genericStats"]["general"]["kd"]
        return name, lv, kd
    except:
        name="ERROR"
        lv="ERROR"
        kd="ERROR"
        return name, lv, kd  

@bot.event
async def on_ready():
    print('R6機器人已上線喔')

@bot.command()
async def ping(ctx):
    await ctx.send(F'{round(bot.latency*1000)} (ms)')

@bot.command(aliases=['p'])
async def player(ctx,player):

    im = Image.new('RGBA', (600, 1000), (44, 44, 44, 255))



    url=f"https://r6.tracker.network/profile/pc/{player}"
    response=requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    name = soup.find("span",class_="trn-profile-header__name").text
    name = name.lstrip()

    img=soup.find("div",class_="trn-profile-header__avatar trn-roundavatar trn-roundavatar--white")
    img=img.find("img")
    img=img.get("src")
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    headers = {'User-Agent': user_agent}
    req = urllib.request.Request(img ,headers=headers)
    with urllib.request.urlopen(req) as response:
        img = response.read()

    avatar=Image.open(BytesIO(img))
    avatar = avatar.resize((200, 200))
    im.paste(avatar, (400, 0))
    im_draw = ImageDraw.Draw(im)

    im_draw.text((40,40), name, font=large_font, fill=(255, 255, 255, 255))

    season = soup.find("ul", class_="trn-card__header-tabs")
    season = season.find("li", class_="trn-card__header-tab")
    title[1]=season.text

    trnimgs=soup.find("div",class_="trn-defstat mb0 top-operators")
    trnimgs=trnimgs.find("div",class_="trn-defstat__value")
    trnimgs=trnimgs.find_all("img")

    im_draw.text((50,140), "TOP OPERATORS", font=medium_font, fill=(255, 255, 255, 255))

    pos=30
    for i in range(len(trnimgs)):
        trnimg=trnimgs[i].get("src")
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        headers = {'User-Agent': user_agent}
        req = urllib.request.Request(trnimg ,headers=headers)
        with urllib.request.urlopen(req) as response:
            img = response.read()
            # img = img.resize((100, 100))
        im.paste(Image.open(BytesIO(img)),(pos,180))
        pos+=100 

    soupln=soup.find_all("div",class_="trn-defstat__name")
    soupl=soup.find_all("div",class_="trn-defstat__value-stylized")
    for i in range(len(soupln)):
        if soupln[i].string =="Level":
            im_draw.text((43,80), f"Level:{soupl[i].string.strip()}", font=large_font, fill=(255, 255, 255, 255)) # username

            break

    sour=soup.find_all("div",class_="trn-defstats trn-defstats--width4  ")
    sour=soup.find_all("div",class_="trn-defstats trn-defstats--width4")
    pos = 300
    for i in range(0,3):
        w, h = im_draw.textsize(title[i], font=font) 
        im_draw.rectangle((0, pos, 600, pos+h+20), fill=(73,188,215,255), width=2)
        im_draw.line((0,pos,600,pos), fill=(255, 255, 255, 255), width=2)
        im_draw.text(((600-w)/2,pos+10), title[i], font=font, fill=(255, 255, 255, 255))
        im_draw.line((0,pos+h+20,600,pos+h+20), fill=(255, 255, 255, 255), width=2)


        soup1=sour[i].find_all("div",class_="trn-defstat__name")
        soup2=sour[i].find_all("div",class_="trn-defstat__value")
        pos2 = 30
        for j in range(len(soup1)):
            if soup2[j].string!="\n":
                w, h = im_draw.textsize(soup1[j].string, font=small_font)
                if j >=4:
                    if j % 4 == 0:
                        pos2=30
                        pos+=100
                    im_draw.text((pos2,pos+60), f"{soup1[j].string.strip()}\n\n{soup2[j].string.strip()}", font=small_font, fill=(255, 255, 255, 255))

                else:
                    im_draw.text((pos2,pos+60), f"{soup1[j].string.strip()}\n\n{soup2[j].string.strip()}", font=small_font, fill=(255, 255, 255, 255))



                pos2=pos2+w+30
        pos+=140

    buffer = BytesIO()
    im.save(buffer, 'png')
    buffer.seek(0)
    await ctx.send(file=discord.File(fp=buffer, filename='r6player.png'))



@bot.command()
async def invite(ctx):
    await ctx.send("https://discord.com/api/oauth2/authorize?client_id=919278942265950259&permissions=8&scope=bot")


@bot.command(aliases=['i'])
async def img(ctx):
    try:
        url = ctx.message.attachments[0].url
    except IndexError:
        print("no")
    else:
        if url[0:26] == "https://cdn.discordapp.com":
            r= requests.get(url,stream=True)
#            try:
            imgid=random.randint(1,100000)
            image = str(imgid) +".jpg"
            with open(image,"wb") as f:
                print("save")
                shutil.copyfileobj(r.raw,f)
#            except:
#                await ctx.send("error and idk")
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
        links.append(f"https://r6.tracker.network/profile/pc/{page}" )


    reqs = (grequests.get(link) for link in links)  # 建立請求集合
    response = grequests.imap(reqs, grequests.Pool(len(splittext)))  # 平行發送請求

    im = Image.new('RGBA', (600, 1200), (33,41,70, 255))
    plt.style.use("cyberpunk")


    now = 0
    x = []
    y = []
    players = []
    place = 50
    #img


    for r in response:

        try:
        
            player={
                "level": 0,
                "name": splittext[now],
                "kd": 0,
                "wins": 0
            }

            soup = BeautifulSoup(r.text, "html.parser")

            img = soup.find(
                "div", class_="trn-profile-header__avatar trn-roundavatar trn-roundavatar--white")
            img = img.find("img")
            img = img.get("src")

            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            headers = {'User-Agent': user_agent}    
            req = urllib.request.Request(img ,headers=headers)
            with urllib.request.urlopen(req) as response:
                img = response.read()
            avatar=Image.open(BytesIO(img))
            avatar = avatar.resize((100, 100))
            im.paste(avatar, (0, place))


            im_draw = ImageDraw.Draw(im)

            
            

            
            season = soup.find("ul", class_="trn-card__header-tabs")
            season = season.find("li", class_="trn-card__header-tab")


            soupln = soup.find_all("div", class_="trn-defstat__name")
            soupl = soup.find_all("div", class_="trn-defstat__value-stylized")
            for i in range(len(soupln)):
                if soupln[i].string == "Level":
                    player["level"] = soupl[i].string.strip()
                    break

            im_draw.rectangle((0, place-50, 600, place), fill=(73,188,215,255), width=2)
            ptitle = splittext[now] + " LV." + player["level"]
            w, h = im_draw.textsize(ptitle, font=large_font)   
            im_draw.text(((600-w)/2,place-50), ptitle, font=large_font, fill=(255, 255, 255, 255))

            sour = soup.find_all("div", class_="trn-defstats trn-defstats--width4  ")
            sour = soup.find_all("div", class_="trn-defstats trn-defstats--width4")
            soup1 = sour[0].find_all("div", class_="trn-defstat__name")
            soup2 = sour[0].find_all("div", class_="trn-defstat__value")

            place2 = 130
            for j in range(len(soup1)):
                if soup1[j].string.strip() == "Wins":
                    player["wins"] = soup2[j].string.strip()
                    im_draw.text((place2,place+20), soup1[j].string.strip() + "\n" +player["wins"] , font=font, fill=(255, 255, 255, 255))         
                if soup1[j].string.strip() == "KD":
                    player["kd"] = soup2[j].string.strip()
                    im_draw.text((place2,place+20), soup1[j].string.strip() + "\n" +player["kd"], font=font, fill=(255, 255, 255, 255))  
                place2 += 30   

            place2 = 300
            trnimgs=soup.find("div",class_="trn-defstat mb0 top-operators")
            trnimgs=trnimgs.find("div",class_="trn-defstat__value")
            trnimgs=trnimgs.find_all("img")
            for i in range(len(trnimgs)):
                trnimg=trnimgs[i].get("src")
                user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                headers = {'User-Agent': user_agent}
                req = urllib.request.Request(trnimg ,headers=headers)
                with urllib.request.urlopen(req) as response:
                    img = response.read()
                    img = BytesIO(img)
                    img=Image.open(img)
                    img = img.resize((100, 100))
                im.paste(img,(place2,place))
                place2+=100 
            
            now += 1
            players.append(player)
            place+=150

        except:
            now += 1
            pass

    for i in range(len(players)):
        x.append(players[i]["name"])
        y.append(float(players[i]["kd"]))

    plt.figure()
    plt.bar(x, y, align =  'center') 
    plt.ylabel('KD') 
    plt.xlabel('Player') 
    mplcyberpunk.add_glow_effects()


    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    pltim = Image.open(img_buf)
    pltim = pltim.resize((600, 400))
    im.paste(pltim, (0, place))

    buffer = BytesIO()
    im.save(buffer, 'png')
    buffer.seek(0)
    await ctx.send(file=discord.File(fp=buffer, filename='r6players.png'))

    os.remove(image)

# @bot.command()
# async def servers(ctx):

#     message = ""
#     count=0
#     server_c=len(bot.guilds)
    
#     for guild in bot.guilds:
#         count+=guild.member_count
#         message += f"伺服器名稱:{guild.name}，伺服器人數:{guild.member_count}\n"
        
#     message += f"----------------------------------------------------------\n"
#     message += f"機器人總人數:{count}\n"
#     message += f"總伺服器數:{server_c}"
#     try:
#         await ctx.send(message)
#     except:
#         nmessage=""
#         nmessage += f"----------------------------------------------------------\n"
#         nmessage += f"機器人總人數:{count}\n"
#         nmessage += f"總伺服器數:{server_c}\n"
#         nmessage += f"----------------------------------------------------------\n"
#         await ctx.send(nmessage)



    
    
bot.run('OTE5Mjc4OTQyMjY1OTUwMjU5.YbTfOw.0-FNKEe0SZ-iRvIgfJyjDNgNpS8')