
import grequests







links=["https://r6.tracker.network/profile/pc/WhiteCloud_TW",
"https://r6.tracker.network/profile/pc/guestlFNz",
"https://r6.tracker.network/profile/pc/ggnoobwillplay",
"https://r6.tracker.network/profile/pc/Ian_10024",
"https://r6.tracker.network/profile/pc/David_Wu"]





reqs = (grequests.get(link) for link in links)  # 建立請求集合
response = grequests.imap(reqs, grequests.Pool(len(links)))  # 平行發送請求


now = 0
#img


for r in response: