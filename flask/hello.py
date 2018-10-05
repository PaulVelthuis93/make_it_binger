from flask import Flask
from flask import request, abort
import redis
import time
import traceback
import json

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
    if not request.json or not 'urls' in request.json:
        abort(400)
    postjson = json.loads(request.json)
    urllist = postjson['urls']

    for url in urllist:
        r.rpush("q", url)
    return "\'" + str(urllist) + "\' posted to redis!"


def main():
    app.run(port=6666, host="0.0.0.0")

if __name__ == '__main__':
    main()