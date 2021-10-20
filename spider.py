from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import datetime

from selenium import webdriver
import os

os.system('git status')
exit()


curTime = datetime.datetime.now()
url = 'http://m.iptv807.com/?tid=gt&t=' + curTime.strftime('%Y') + curTime.strftime('%m') + curTime.strftime('%d')

hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

req = Request(url,headers=hdr)
page = urlopen(req)

soup = BeautifulSoup(page, 'html.parser')

contentDiv = soup.find(attrs={"data-role":"content"})

urlList = contentDiv.find_all('a')


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
# https://github.com/mozilla/geckodriver/releases
browser = webdriver.Chrome(
  executable_path='/Users/ivanleung/Desktop/iptvPlaylist/chromedriver',
  chrome_options=chrome_options
)

resultMap = {}
for url in urlList:
  name = url.decode_contents() 
  href = url['href']
  streamUrl = 'http://m.iptv807.com/' + href
  try: 
    browser.get(streamUrl)
  except:
    print("can not parse " + name)
  html = browser.page_source
  soup = BeautifulSoup(html, 'html.parser')
  videoTag = soup.find('video')
  print(videoTag['src'])
  
  resultMap[name] = videoTag['src']
  
browser.close()
print(resultMap)
f = open("港澳.m3u", "w")
f.write("#EXTM3U\n")
for key, value in resultMap.items():
  f.write("#EXTINF:-1 ," + key + "\n")
  f.write(value + "\n")

f.close()