from bs4 import BeautifulSoup
import grequests
from io import BytesIO
from PIL import Image,ImageDraw,ImageFont
import matplotlib.pyplot as plt
import mplcyberpunk
import urllib.request

from numpy import place

plt.style.use("cyberpunk")
large_font = ImageFont.truetype('../setofont.ttf', 40)
font = ImageFont.truetype('../setofont.ttf', 30)
medium_font = ImageFont.truetype('../setofont.ttf', 26) 
small_font = ImageFont.truetype('../setofont.ttf', 22)

im = Image.new('RGBA', (600, 1200), (33,41,70, 255))

title = ["Overall", "Season 23", "General"]
links = ["https://r6.tracker.network/profile/pc/WhiteCloud_TW",
         "https://r6.tracker.network/profile/pc/ggnoobwillplay",
         "https://r6.tracker.network/profile/pc/David_Wu",
         "https://r6.tracker.network/profile/pc/David_Wu",
         "https://r6.tracker.network/profile/pc/David_Wu"]

splittext=["WhiteCloud_TW", "ggnoobwillplay", "David_Wu", "David_Wu", "David_Wu"]

reqs = (grequests.get(link) for link in links)  # 建立請求集合
response = grequests.imap(reqs, grequests.Pool(len(links)))  # 平行發送請求


now = 0
x = []
y = []
players = []
place = 50
# img


for r in response:
    
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
im.show()

