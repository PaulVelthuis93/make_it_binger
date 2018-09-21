import requests
from bs4 import BeautifulSoup
import json
import logging
import time


def get_url_from_redis():
    # url = requests.get("http://redis-restapi.nl/get-url")
    url = "https://kafka.apache.org/intro"
    return url

def get_body(da_link):
    r = requests.get(da_link)
    # encoding = r.encoding
    body = r.text
    return body

def send_body_to_elastic(body):
    print("******************** body_to_elastic ********************")
    print(body)
    pass

def get_urls_from_body(body, url):
    soup = BeautifulSoup(body)
    links = set()
    for link in soup.find_all("a"):
        da_awesome_link = link.get("href")
        if da_awesome_link.startswith('/'):
            da_awesome_link = f'{url}{da_awesome_link}'
        links.add(da_awesome_link)
    return links

def send_urls_to_redis(links):
    # send to redis
    print("******************** urls_to_redis ********************")
    print(links)
    try:
        result = requests.post("http://redis-restapi.nl/dump-urls", data=json.dumps(list(links)))
        if result.status_code != 200:
            logging.warn(f'Redis replied with a {result.status_code}')
    except:
        logging.warn(" Says: This is fucking awkward, we can't connect, we are gonna dieeeee")

while True:
    url = get_url_from_redis()
    if url :
        body = get_body(url)
        send_body_to_elastic(body)
        urls = get_urls_from_body(body, url)
        send_urls_to_redis(urls)
    else:
        time.sleep(10)