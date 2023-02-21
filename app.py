from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import re
import helpers
from constant import HEADER


app = Flask(__name__)


@app.route("/one", methods=['POST'])
def one():

    url: str = request.args.get('url')

    response = requests.get(url, headers=HEADER)
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
    domainUrls: list = helpers.getDomainUrls(url)
    
    cleanUrls: list[str] = helpers.urlCleaner(domainUrls)

    urlsCount: int = len(cleanUrls)

    domainUrlStatus: list = helpers.checkStatus(cleanUrls)
    activeUrl: int = len([i for i in domainUrlStatus if i==200])

    res: dict[str: int] = {cleanUrls[i]: domainUrlStatus[i] for i in range(len(domainUrlStatus))}
    urlsWithOkStatus: list[str] = [key for key, val in res.items() if val == 200]

    return jsonify({
        "active_page_count": activeUrl,
        "page_count": urlsCount,
        "url_list": urlsWithOkStatus,
        "x": len(urlsWithOkStatus)
    })


if __name__ == '__main__':
    app.run(debug=True)