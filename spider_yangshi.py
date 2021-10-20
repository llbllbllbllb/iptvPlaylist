from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import datetime

from selenium import webdriver

curTime = datetime.datetime.now()
url = 'http://iptv807.com/?tid=ys'

hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

req = Request(url,headers=hdr)
page = urlopen(req)

soup = BeautifulSoup(page, 'html.parser')

contentDiv = soup.find(attrs={"data-role":"content"})

urlList = contentDiv.find_all('a')

# https://github.com/mozilla/geckodriver/releases
browser = webdriver.Chrome(executable_path='/Users/ivanleung/Desktop/iptvPlaylist/chromedriver')

resultMap = {}
for url in urlList:
  name = url.decode_contents() 
  href = url['href']
  streamUrl = 'http://m.iptv807.com/' + href
  browser.get(streamUrl)
  html = browser.page_source
  soup = BeautifulSoup(html, 'html.parser')
  videoTag = soup.find('video')
  if videoTag['src']:
    print(name + ":" + videoTag['src'])
    resultMap[name] = videoTag['src']
  else:
    print("cannot find " + name + " url")
  
browser.close()
print(resultMap)
f = open("央视.m3u", "w")
f.write("#EXTM3U\n")
for key, value in resultMap.items():
  f.write("#EXTINF:-1 ," + key + "\n")
  f.write(value + "\n")

f.close()