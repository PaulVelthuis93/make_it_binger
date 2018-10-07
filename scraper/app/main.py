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
        logging.warning('Bleuh', exc_info=True)
        return None
    return url.text

def get_body(da_link):
    try:
        r = requests.get(da_link)
        body = r.text
        title = BeautifulSoup(body).title.text
        return {"body": body, "title": title, "url": da_link}
    except:
        logging.debug(f"Invalid link: {da_link}")
        return {"body": None}


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

def send_data_to_binger(meta_data):
    headers = {'Content-type': 'application/json'}
    try:
        result = requests.post("http://binger-api:6666/urls", headers=headers, data=json.dumps(meta_data))
        if result.status_code != 200:
            logging.warning(f'Binger api replied with a {result.status_code}')
        return result
    except:
        logging.warning('Bleuh', exc_info=True)

while True:
    url = get_url_from_redis()
    if url:
        res = get_body(url)
        res['urls'] = list(get_urls_from_body(res['body'], url))
        answer = send_data_to_binger(res)
        logging.warning(answer)
    else:
        logging.warning("no url in queue")
        time.sleep(10)