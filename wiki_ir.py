from flask import Flask, jsonify
from elasticsearch2 import Elasticsearch
import docSummary

app = Flask(__name__)
es = Elasticsearch(['https://73efa8624ce5b1aa7b0636a629e2d9f1.us-west-1.aws.found.io:9243/'], http_auth=('admin', 'jfnN6ArBrfnlD6accc0WatAy'),
    scheme="https")

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/wikiSummarizer/api/results/<searchWord>', methods=['GET'])
def get_tasks(searchWord):
    term = {
  "query": {
    "bool": {
      "must_not": [
        {
          "match": {
            "text": "#REDIRECT"
          }
        }
      ],
      "must": [
        {
          "match_phrase": {
            "text": searchWord
          }
        }
      ]
    }
  },
  "size":15,
  "_source": [
    "text",
    "title"
  ]
}
    res = es.search(index="wiki", body= term)

    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        temp = hit['_source']['text']
        result = docSummary.clean(hit['_source']['text'])
        summary = docSummary.summarize(result, 5)
        hit['_source']['text'] = summary

    '''
    print('Original String\n\n')
    print(temp)
    print('Cleaned String\n\n')
    print(result)
    print('Summarized String\n\n')
    print(summary)'''
    return jsonify({'results': res['hits']})


if __name__ == '__main__':
    app.run()
