from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import re
import concurrent.futures
from constant import HEADER


app = Flask(__name__)


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


@app.route("/one", methods=['POST'])
def one():

    url: str = request.args.get('url')
    response = requests.get(url)
    statusCode: int = response.status_code   
    soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')
    title: str = soup.find('title').get_text()
    domainName: str = re.search('https?://([A-Za-z_0-9.-]+).*', url).group(1)

    finalUrl: str = response.url if response.url != url else ""
    
    return jsonify({
        "final_url": finalUrl,
        "status_code": statusCode,
        "title": title,
        "domain_name": domainName
    })



@app.route("/two", methods=['POST'])
def two():

    url: str = request.args.get('url')
    domainUrls: list = getDomainUrls(url)
    urlsCount: int = len(domainUrls)

    domainUrlStatus: list = checkStatus(domainUrls)
    activeUrl: int = len([i for i in domainUrlStatus if i==200])

    res: dict[str: int] = {domainUrls[i]: domainUrlStatus[i] for i in range(len(domainUrlStatus))}
    urlsWithOkStatus: list[str] = [key for key, val in res.items() if val == 200]

    return jsonify({
        "active_page_count": activeUrl,
        "page_count": urlsCount,
        "url_list": urlsWithOkStatus
    })


if __name__ == '__main__':
    app.run(debug=True)