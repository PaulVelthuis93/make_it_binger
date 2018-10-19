from flask import Flask, jsonify, Response
import requests

import logging

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)

logging.basicConfig(filename='output.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Flask has by default 404 not found, change it to 406 not acceptable - api team requirements
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "The requested url is not allowed"}), 406


def send_request_to_elastic(keywords="", fields = "[\"body\", \"title\"]", source = "[\"title\", \"url\"]"):
    query = '{"query": {"multi_match": {"query": {}, "fields": {}}}, ' \
            '"_source": {}}'.format(keywords, fields, source)
    results = requests.post("http://elasticsearch:9200/", data=query)
    logger.debug("Query submitted:\n{}".format(query))
    reply = {
        'response': results,
        'status': 200,
        'mimetype': 'application/json'}
    return reply


@app.route('/bing-it', methods=['POST'])
def post():
    r = requests.json
    elastic_response = send_request_to_elastic(
        keywords=(r['keywords']),
        fields=(r['fields']),
        source=(r['source']))
    return Response(**elastic_response)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
