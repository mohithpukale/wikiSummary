import pysolr
from elasticsearch2 import Elasticsearch
from flask import render_template
from flask import request

from app import app
from app import docSummary

es = Elasticsearch(['https://73efa8624ce5b1aa7b0636a629e2d9f1.us-west-1.aws.found.io:9243/'],
                   http_auth=('admin', 'jfnN6ArBrfnlD6accc0WatAy'),
                   scheme="https")

solr = pysolr.Solr('http://user:UV7DCYSGnPao@35.230.16.178/solr/wiki', timeout=10)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', name='index')


@app.route('/query/es/', methods=['GET'])
def query_es():
    search_word = request.args.get('q')
    term = {
        "query": {
            "filtered": {
                "query": {
                    "query_string": {
                        "query": "(" + search_word + "~1) AND (NOT(#redirect)) AND (NOT(#REDIRECT)) AND (NOT(.*jpg))",
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
        "size": 50,
        "_source": [
            "text",
            "title"
        ]
    }

    res = es.search(index="wiki", body=term)
    results = []
    count = 0

    for hit in res['hits']['hits']:
        # temp = hit['_source']['text']
        if (count < 10 and len(hit['_source']['text']) > 100):
            result = docSummary.clean(hit['_source']['text'])
            summary = docSummary.summarize(result, 5)
            result = {"title": hit['_source']['title'], "text": summary}
            results.append(result)
            count += 1
            print("Hello")
            if count == 10:
                break

    return render_template('index.html', q=search_word, results=results)


@app.route('/query/solr/', methods=['GET'])
def query_solr():
    search_word = request.args.get('q')
    hits = solr.search(search_word)
    print(search_word)
    results = []
    for hit in hits:
        text = docSummary.clean(hit['text'])
        summary = docSummary.summarize(text, 3)
        result = {"title": hit['title'], "text": summary}
        results.append(result)

    print(results)
    return render_template('index.html', q=search_word, results=results)
