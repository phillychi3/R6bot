from io import BytesIO
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import mplcyberpunk
import urllib.request
from PIL import Image,ImageDraw,ImageFont
from requests_toolbelt import user_agent 

# 美化 睡覺
plt.style.use("cyberpunk")

large_font = ImageFont.truetype('../GenWanMin-L.ttc', 40)
font = ImageFont.truetype('../GenWanMin-L.ttc', 30)
medium_font = ImageFont.truetype('../GenWanMin-L.ttc', 26) 
small_font = ImageFont.truetype('../GenWanMin-L.ttc', 20)

title=["Overall","Season 23","General"]
im = Image.new('RGBA', (600, 1000), (44, 44, 44, 255))


response = requests.get(f"https://r6.tracker.network/profile/pc/WhiteCloud_TW")
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
    im_draw.line((0,pos,600,pos), fill=(255, 255, 255, 255), width=2)
    w, h = im_draw.textsize(title[i], font=font)    
    im_draw.text(((600-w)/2,pos+10), title[i], font=font, fill=(255, 255, 255, 255))
    im_draw.line((0,pos+h+20,600,pos+h+20), fill=(255, 255, 255, 255), width=2)
    print(title[i])
    print("-------------------")

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


            print(soup1[j].string,soup2[j].string)
            pos2=pos2+w+30
    pos+=140

mplcyberpunk.add_glow_effects()
im.show()
#plt.show()