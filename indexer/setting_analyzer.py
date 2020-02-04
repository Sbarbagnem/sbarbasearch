MAPPING = {
    "settings": {
        "index": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "similarity": {
                "my_similarity": {"type": "LMJelinekMercer", "lambda": "0.2"}
            },
        },
        "analysis": {
            "analyzer": {
                "custom_analyzer": {
                    "type": "custom",
                    "tokenizer": "whitespace",
                    "char_filter": ["html_strip"],
                    "filter": [
                        "classic",
                        "lowercase",
                        "remove_digit_token",
                        "remove_link_token",
                        "remove_puntuaction",
                        "remove_length_less_two",
                        "my_stemmer",
                    ],
                }
            },
            "filter": {
                "my_stemmer" : {
                    "type" : "stemmer",
                    "name" : "porter2"
                },
                "remove_digit_token": {
                    "type": "pattern_replace",  # remove token made of only number
                    "pattern": "^[0-9]+",
                    "replacement": "",
                },
                "remove_link_token": {
                    "type": "pattern_replace",  # remove link
                    "pattern": "^https?:\/\/.*[\r\n]*",
                    "replacement": "",
                },
                "remove_puntuaction": {
                    "type": "pattern_replace",  #  remove non alpha-numeric in token but not @ #
                    "pattern": "[^0-9A-Za-z@#]",
                    "replacement": "",
                },
                "remove_length_less_two": {"type": "length", "min": 2},
            },
        },
    },
    "mappings": {
        "properties": {
            "created_at": {"type": "date"},
            "text": {
                "type": "text",
                "analyzer": "custom_analyzer",
                "similarity": "my_similarity",
            },
            "user": {"type": "text", "index": False},
            "like": {"type": "integer", "index": False},
            "retweet": {"type": "integer", "index": False},
            "profile_image": {"type": "keyword", "index": False},
            "tweet_url": {"type": "keyword", "index": False},
            "topic": {"type": "keyword", "index": True},
            "country": {"type": "keyword", "index": True},
        }
    },
}
