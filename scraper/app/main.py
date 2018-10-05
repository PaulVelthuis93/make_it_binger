import requests
from bs4 import BeautifulSoup
import json
import logging
import time


def get_url_from_redis():
    # try TODO: Catch connection problems
    try:
        url = requests.get("http://binger-api:6666/url")
    except:
        logging.info('Bleuh', exc_info=True)
        return None
    return url.text

def get_body(da_link):
    try:
        r = requests.get(da_link)
        body = r.text
        title = BeautifulSoup(body).title.text
        return {"body": body, "title": title}
    except:
        logging.debug(f"Invalid link: {da_link}")
        return {"body": None, "title": None}


def get_urls_from_body(body, url):
    links = set()
    try:
        soup = BeautifulSoup(body)

        for link in soup.find_all("a"):
            da_awesome_link = link.get("href")
            if da_awesome_link and da_awesome_link.startswith(('/', '#', '?')): # TODO: fix #
                da_awesome_link = f'{url}{da_awesome_link}'
            links.add(da_awesome_link)
    except:
        logging.debug(f"Invalid url: {url}")
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
        send_urls_to_redis(urls)
    else:
        logging.warning("no url in queue")
        time.sleep(10)