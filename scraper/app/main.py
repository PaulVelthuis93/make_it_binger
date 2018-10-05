import requests
from bs4 import BeautifulSoup
import json
import logging
import time
from elasticsearch import Elasticsearch

def get_url_from_redis():
    # try TODO: Catch connection problems
    try:
        url = requests.get("http://binger-api:6666/url")
    except:
        logging.info('Bleuh', exc_info=True)
        return None
    return url.text

def get_body(da_link):
    r = requests.get(da_link)
    # encoding = r.encoding
    body = r.text
    title = BeautifulSoup(body).title.text
    return {"body": body, "title": title}

def send_body_to_elastic(body, url, urls, title):
    print("Scraped: " + str(urls))
    es_body = {"doc":{"body":body, "url": url, "links": list(urls), "title": title, "timestamp": time.time()}}
    # try:
    #     # title, timestamp, links
    #     es = Elasticsearch(["http://elasticsearch:9200/"])
    #     es.update(body=es_body)
    # except:
    #     logging.warning("What am i doing with my life???????")

def get_urls_from_body(body, url):
    soup = BeautifulSoup(body)
    links = set()
    for link in soup.find_all("a"):
        da_awesome_link = link.get("href")
        if da_awesome_link and da_awesome_link.startswith('/'): # TODO: fix #
            da_awesome_link = f'{url}{da_awesome_link}'
        links.add(da_awesome_link)
    return links

def send_urls_to_redis(links):
    headers = {'Content-type': 'application/json'}
    for link in links:
        try:
            if link:
                result = requests.post("http://binger-api:6666/url", headers=headers, data=json.dumps({"url": link}))
                if result.status_code != 200:
                    logging.warning(f'Redis replied with a {result.status_code}')
        except:
            logging.warning(f"Exception while accessing link:\n{link}")
            logging.info('Bleuh', exc_info=True)

while True:
    url = get_url_from_redis()
    if url:
        res = get_body(url)
        urls = get_urls_from_body(res['body'], url)
        send_body_to_elastic(res['body'], url, urls, res['title'])
        send_urls_to_redis(urls)
    else:
        logging.warning("no url in queue")
        time.sleep(10)