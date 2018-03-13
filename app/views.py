from elasticsearch2 import Elasticsearch
from flask import jsonify
from flask import render_template
from flask import request

from app import app
from app import docSummary

es = Elasticsearch(['https://73efa8624ce5b1aa7b0636a629e2d9f1.us-west-1.aws.found.io:9243/'],
                   http_auth=('admin', 'jfnN6ArBrfnlD6accc0WatAy'),
                   scheme="https")


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', name='index')


@app.route('/query/', methods=['GET'])
def query():
    search_word = request.args.get('q')
    term = {
        "query": {
            "filtered": {
                "query": {
                    "query_string": {
                        "query": "(" + search_word + "~1) AND (NOT(#REDIRECT)) AND (NOT(.*jpg))",
                        "fields": [
                            "text",
                            "title"
                        ],
                        "fuzziness": 0,
                        "phrase_slop": 1,
                        "default_operator": "AND"
                    }
                },
                "filter": {
                    "term": {
                        "_type": "page"
                    }
                }
            }
        },
        "size": 10,
        "_source": [
            "text",
            "title"
        ]
    }
    res = es.search(index="wiki", body=term)

    print("Got %d Hits:" % res['hits']['total'])
    results = []
    for hit in res['hits']['hits'][0:10]:
        # temp = hit['_source']['text']
        result = docSummary.clean(hit['_source']['text'])
        summary = docSummary.summarize(result, 5)
        result = {"title": hit['_source']['title'],"text": summary}
        results.append(result)

    return render_template('index.html',q=search_word,results=results)
