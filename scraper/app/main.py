import requests
from bs4 import BeautifulSoup
import json
import logging
import time
from elasticsearch import Elasticsearch

def get_url_from_redis():
    # try TODO: Catch connection problems
    # url = requests.get("http://binger-api.default.svc.cluster.local/url")
    url = "https://kafka.apache.org/intro"
    return url

def get_body(da_link):
    r = requests.get(da_link)
    # encoding = r.encoding
    body = r.text
    title = BeautifulSoup(body).title.text
    return {"body": body, "title": title}

def send_body_to_elastic(body, url, urls, title):

    es_body = {"doc":{"body":body, "url": url, "links": list(urls), "title": title, "timestamp": time.time()}}
    print("******************** body_to_elastic ********************")
    print(es_body)
    # try:
    #     # title, timestamp, links
    #     es = Elasticsearch(["http://elasticsearch:9200/"])
    #     es.update(body=es_body)
    # except:
    #     logging.warn("What am i doing with my life???????")

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
    # print(links)
    try:
        result = requests.post("http://binger-api.default.svc.cluster.local/url", data=json.dumps(list(links)))
        if result.status_code != 200:
            logging.warn(f'Redis replied with a {result.status_code}')
    except:
        logging.warn(" Says: This is fucking awkward, we can't connect, we are gonna dieeeee")

while True:
    url = get_url_from_redis()
    if url :
        res = get_body(url)
        urls = get_urls_from_body(res['body'], url)
        send_body_to_elastic(res['body'], url, urls, res['title'])
        send_urls_to_redis(urls)
    else:
        time.sleep(10)