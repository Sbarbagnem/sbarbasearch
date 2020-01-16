from flask import Flask, jsonify, request, render_template, redirect, url_for
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch()

@app.route('/')
def home():
        return render_template('index.html', tweets = [],)

@app.route('/search', methods=['GET', 'POST'])
def search():

    query = request.args.get('search')

    body = {
            "sort" : [
                { "followers_count": {"order" : "desc"}},
                "_score",
                { "retweet": {"order": "desc"}}
            ],
            "query": {
                "match" : {
                    "text" : {
                        "query": query
                    }
                }
            }
        }

    # per ridurre i dati ritornati
    #filter_path=['hits.hits._id', 'hits.hits._type']

    # size --> number of tweet come back
    res = es.search(index="index_twitter", body=body, size=100)

    res = res['hits']['hits']

    return render_template('index.html', tweets=res, search_term=query)


if __name__ == "__main__":
    app.run(debug=True)