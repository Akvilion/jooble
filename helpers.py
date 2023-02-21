import requests
from bs4 import BeautifulSoup
import concurrent.futures
from constant import HEADER
import re


def getDomainUrls(url: str="") -> list[str]:
    urls: list = []
    if url:

        domainName = re.search('https?://([A-Za-z_0-9.-]+).*', url).group(1)
        data = requests.get(url, headers=HEADER)
        soup = BeautifulSoup(data.text, 'html.parser')
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and domainName in href:
                urls.append(href)

    return urls 


def getStatus(url: str="") -> int:

    if url == "mailto:admin@drpriyanka.com":
        a = 2
    response = requests.get(url, headers=HEADER)
    return response.status_code


def checkStatus(urls: list[str]=[]) -> list:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures: list = []
        statusList: list = []
        for url in urls:
            futures.append(executor.submit(getStatus, url=url))

        for future in concurrent.futures.as_completed(futures):
            statusList.append(future.result())
    return statusList


def urlCleaner(urls: list) -> list:
    nonDuplicateUrls: list = list(set(urls))  # delete duplicates
    emailValidatePattern = r"^\S+@\S+\.\S+$"
    cleanedUrls  = [i for i in nonDuplicateUrls if not re.match(emailValidatePattern, i)]  # delete email
    return cleanedUrls
