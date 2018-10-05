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



def send_request_to_elastic(keywords):
    query = f"""\
    {
    'query': {
        'multi_match' : {
            'query': '{keywords}',
            'fields': ['body']
        }
    },
        '_source': ['title', 'body', 'url']
    }    
    """
    
    results = requests.post("http://elasticsearch:9200/", data=query)
    
    reply = {
        'response': results,
        'status': 200,
        'mimetype': 'application/json'}
    
    # es_body = {"doc":{"body":body, "url": url, "links": urls, "title": title, "timestamp": time.time()}}
    # try:
    #     # title, timestamp, links
    #     es = Elasticsearch([])
    #     es.index(index='urls', doc_type='doc', body=es_body)
    #     return "\'" + str(url) + "\' posted to elasticsearch!"
    # except:
    #     logging.warning('Bleuh', exc_info=True)
    return reply
    
    
# def sort_results():
#     pass


@app.route('/bing-it', methods=['POST'])
def post():
    keywords = requests.json['keywords']  # TODO: keywords must be list
    elastic_response = send_request_to_elastic(keywords)
    return Response(**elastic_response)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
