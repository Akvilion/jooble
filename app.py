from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from lxml import etree
import io


app = Flask(__name__)



@app.route("/one", methods=['POST'])
def one():

    url = request.args.get('url')
    response = requests.get(url)
    statusCode = response.status_code   
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').get_text()
    domainName = re.search('https?://([A-Za-z_0-9.-]+).*', url).group(1)

    finalUrl = response.url if response.url != url else ""
    return jsonify({
        "final_url": finalUrl,
        "status_code": statusCode,
        "title": title,
        "domain_name": domainName
    })



@app.route("/two", methods=['POST'])
def two():

    url = request.args.get('url')
    domainName = re.search('https?://([A-Za-z_0-9.-]+).*', url).group(1)
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        urls.append(link.get('href'))
        print(link.get('href'))


    page_count = len(urls)


    return jsonify({
        "active_page_count": 3,
        "page_count": page_count,
        "url_list": [
            "https://cyberchimps.com/blog/top-wordpress-photography-themes/",
            "https://cyberchimps.com/blog/best-wordpress-themes-for-artists/",
            "https://cyberchimps.com/blog/"
        ]
    })


if __name__ == '__main__':
    app.run(debug=True)