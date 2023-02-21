import requests
from bs4 import BeautifulSoup
import re


def getDomainUrls(url=""):
  urls = []
  if url:
    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    domainName = re.search('https?://([A-Za-z_0-9.-]+).*', url).group(1)
    print(domainName)
    data = requests.get(url, headers=header)
    soup = BeautifulSoup(data.text, 'html.parser')
    
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and domainName in href:
          urls.append(href)

  return urls

print(getDomainUrls())