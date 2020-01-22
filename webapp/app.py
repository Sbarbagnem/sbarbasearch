from flask import Flask, jsonify, request, render_template, redirect, url_for
from elasticsearch import Elasticsearch
from search import query_search

app = Flask(__name__)
es = Elasticsearch()

@app.route('/')
def home():
        return render_template('index.html', tweets = [],)

@app.route('/search', methods=['GET', 'POST'])
def search():

    query = request.args.get('search')
    count = request.args.get('number_result')
    user = request.args.get('profile')
    topic = request.args.get('topic')

    #print('Voglio trovare ', count, ' tweet')

    res = query_search(query, count_result=count, user=user, topic=topic)

    return render_template('index.html', tweets=res, search_term=query)


if __name__ == "__main__":
    app.run(debug=True)