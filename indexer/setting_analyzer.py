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
                        "filter": [
                            "lowercase",
                            "delete_link_end",
                            "porter_stem"
                        ]
                    }
                },
                "filter": {
                    "delete_link_end": {
                        "type": "pattern_replace",
                        "pattern": "^https?:\/\/.*[\r\n]*",
                        "replacement": ""
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
                    "analyzer" : "custom_analyzer"
                },
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
                }
            }
        }
    }

ANALYZER = {
    "analyzer": {
        "custom_analyzer": {
            "type": "custom",
            "tokenizer": "whitespace",
            "filter":[
                "lowercase"
            ]
        }
    }
}