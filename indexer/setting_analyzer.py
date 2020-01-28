MAPPING = {
    "settings" : {
        "index" : {
            "number_of_shards" : 1,
            "number_of_replicas" : 0
        },
        "analysis": {
            "analyzer": {
                "custom_analyzer": {
                    "type": "custom",
                    "tokenizer": "whitespace",
                    "char_filter": [
                        "html_strip"
                    ],
                    "filter": [
                        "classic",
                        "lowercase",
                        "remove_digit_token",
                        "remove_link_token",
                        "remove_puntuaction",
                        "remove_length_less_two",
                        "porter_stem"
                    ]
                }
            },
            "filter":{
                "remove_digit_token": {
                    "type": "pattern_replace", # remove token made og only number
                    "pattern": "^[0-9]+",
                    "replacement": ""                   
                },
                "remove_link_token": {
                    "type": "pattern_replace", # remove link
                    "pattern": "^https?:\/\/.*[\r\n]*",
                    "replacement": ""
                },
                "remove_puntuaction": {
                    "type": "pattern_replace", # remove non alpha-numeric in token but not @ # 
                    "pattern": "[^0-9A-Za-z@#]",
                    "replacement": ""
                },
                "remove_length_less_two": {
                    "type": "length",
                    "min": 2
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "created_at": {
                "type": "date",
                "index": False,
                "store" : True
            },
            "text": {
                "type": "text",
                "store" : True,
                "analyzer" : "custom_analyzer"
            },
            "user": {
                "type": "text",
                "store" : True,
                "analyzer" : "standard"
            },
            "popularity": {
                "type": "rank_features"
            },
            '''
            "followers_count": {
                "type": "integer",
                "index": False,
                "store" : True
            },
            "like": {
                "type": "integer",
                "index": False,
                "store" : True
            },
            "retweet": {
                "type": "integer",
                "index": False,
                "store" : True
            },
            '''
            "profile_image": {
                "type": "keyword",
                "index": False,
                "store" : True
            },
            "tweet_url": {
                "type": "keyword",
                "index": False,
                "store" : True
            },
            "topic": {
                "type": "keyword",
                "index": True,
                "store": True
            },
            "country": {
                "type": "keyword",
                "index": True,
                "store": True
            }
        }
    }
}
