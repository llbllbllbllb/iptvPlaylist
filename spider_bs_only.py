from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import datetime

import time


curTime = datetime.datetime.now()
url = 'http://m.iptv807.com/?tid=gt&t=' + curTime.strftime('%Y') + curTime.strftime('%m') + curTime.strftime('%d')

hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

req = Request(url,headers=hdr)
page = urlopen(req)

soup = BeautifulSoup(page, 'html.parser')

contentDiv = soup.find(attrs={"data-role":"content"})

urlList = contentDiv.find_all('a')

resultMap = {}
for url in urlList:
  name = url.decode_contents() 
  href = url['href']
  streamUrl = 'http://m.iptv807.com/' + href
  # session = HTMLSession()
  # r = session.get(streamUrl)
  # r.html.render(timeout=20)
  r = urlopen(req)
  time.sleep(10)
  soup = BeautifulSoup(r , 'html.parser')
  videoTag = soup.find('video')
  print(videoTag['src'])
  
  resultMap[name] = videoTag['src']
  
print(resultMap)
# f = open("港澳.m3u", "w")
# f.write("#EXTM3U\n")
# for key, value in resultMap.items():
#   f.write("#EXTINF:-1 ," + key + "\n")
#   f.write(value + "\n")

# f.close()