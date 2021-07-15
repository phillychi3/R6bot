from PIL import Image
import pytesseract
import grequests
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # PATH tesseract.exe
img = Image.open('unknown.png')
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
       
print(splittext)

for r in response:
    print(r)