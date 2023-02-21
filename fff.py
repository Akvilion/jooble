import requests
from bs4 import BeautifulSoup

headers = {
  "User-Agent": "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36 EdgA/46.1.2.5140"
}

url = "https://cyberchimps.com/"
# domainName = re.search('https?://([A-Za-z_0-9.-]+).*', url).group(1)
data = requests.get(url, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
urls = []
for link in soup.find_all('a'):
    urls.append(link.get('href'))
    print(link.get('href'))


page_count = len(urls)