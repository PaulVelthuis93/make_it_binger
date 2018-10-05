from flask import Flask
from flask import request, abort
import redis
import time
from elasticsearch import Elasticsearch

app = Flask(__name__)
# TODO fix exception
r = redis.StrictRedis(host='redis.default.svc.cluster.local', port=6379)                          # Connect to local Redis instance

@app.route("/")
def hello():
    lines= """Hello World! <br> You can go to endpoint get to get the information, <br> or post to post the information """
    return lines

@app.route("/url", methods=["GET"])
def get():
    message = r.lpop('q')                                             # Checks for message
    if message is None:
        return "https://kafka.apache.org/intro"
    return message.decode("utf-8")

@app.route("/url", methods=["POST"])
def post():
    if not request.json or not 'url' in request.json:
        abort(400)
    urlstring = request.json['url']
    r.rpush("q", urlstring)
    return "\'" + urlstring + "\' posted to redis!"

@app.route("/urls", methods=["POST"])
def postlist():
    if not request.json or not 'url' in request.json or not 'title' in request.json or not 'urls' in request.json or not 'body' in request.json:
        abort(400)
    postjson = request.json
    send_body_to_elastic(**postjson)
    urllist = postjson['urls']
    for url in urllist:
        r.rpush("q", url)
    return "\'" + str(urllist) + "\' posted to redis!"


def send_body_to_elastic(body, url, urls, title):
    es_body = {"doc":{"body":body, "url": url, "links": urls, "title": title, "timestamp": time.time()}}
    try:
        # title, timestamp, links
        es = Elasticsearch(["http://elasticsearch:9200/"])
        es.update(body=es_body)
    except:
        logging.warning("What am i doing with my life???????")


def main():
    app.run(port=6666, host="0.0.0.0")

if __name__ == '__main__':
    main()