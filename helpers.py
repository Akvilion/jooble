import requests
from bs4 import BeautifulSoup
import concurrent.futures
from constant import HEADER
import re


def getDomainUrls(url="") -> list[str]:
    urls: list = []
    if url:

        domainName = re.search('https?://([A-Za-z_0-9.-]+).*', url).group(1)
        data = requests.get(url, HEADER)
        soup = BeautifulSoup(data.text, 'html.parser')
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and domainName in href:
                urls.append(href)

    return urls 


def getStatus(url) -> int:

    response = requests.get(url, HEADER)
    return response.status_code


def checkStatus(urls) -> list:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures: list = []
        statusList: list = []
        for url in urls:
            futures.append(executor.submit(getStatus, url=url))

        for future in concurrent.futures.as_completed(futures):
            statusList.append(future.result())
    return statusList