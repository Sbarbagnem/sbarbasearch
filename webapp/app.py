import os
from flask import Flask, jsonify, request, render_template, redirect, url_for
from elasticsearch import Elasticsearch
from webapp.search import query_search

app = Flask(__name__, static_url_path = "/static", static_folder = "static")
es = Elasticsearch()


@app.route("/")
def home():
    return render_template("index.html", tweets=[],)


@app.route("/search", methods=["GET", "POST"])
def search():

    query = request.args.get("search")
    count = request.args.get("number_result")
    
    # se settato aggiungo bow del profilo alla query
    user = request.args.get("profile")

    # se settato cerco solo nei tweet con quello specifico tweet
    topic = request.args.get("topic")
    method = request.args.get("method")

    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if lat != '' and lon !='':
        location_search = [int(lat),int(lon)]
    else:
        location_search = 'None'

    res = query_search(
        query, count_result=count, user=user, topic=topic, method=method,
        location_search=location_search
    )

    return render_template("index.html", tweets=res, search_term=query)


if __name__ == "__main__":
    app.run(debug=True)
