import re
import html
import emoji
import nltk
import regex
import string
import contractions
from tqdm import tqdm
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize.casual import TweetTokenizer

MIN_YEAR = 1900
MAX_YEAR = 2100


def get_url_pattern():
    return re.compile(
        r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))"
        r"[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})"
    )


def get_emojis_pattern():
    # try:
    #     # UCS-4
    #     emojis_pattern = re.compile(
    #         u"([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])"
    #     )
    # except re.error:
    #     # UCS-2
    #     emojis_pattern = re.compile(
    #         u"([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])"
    #     )
    # return emojis_pattern
    return emoji.get_emoji_regexp()


def get_hashtags_pattern():
    return re.compile(r"#(\w*)")


def get_single_letter_words_pattern():
    return re.compile(r"(?<![\w\-])\w(?![\w\-])")


def get_blank_spaces_pattern():
    return re.compile(r"\s{2,}|\t")


def get_twitter_reserved_words_pattern():
    return re.compile(r"(RT|rt|FAV|fav|VIA|via)")


def get_mentions_pattern():
    return re.compile(r"@\w*")


def get_negations_pattern():
    negations_ = {
        "isn't": "is not",
        "can't": "can not",
        "couldn't": "could not",
        "hasn't": "has not",
        "hadn't": "had not",
        "won't": "will not",
        "wouldn't": "would not",
        "aren't": "are not",
        "haven't": "have not",
        "doesn't": "does not",
        "didn't": "did not",
        "don't": "do not",
        "shouldn't": "should not",
        "wasn't": "was not",
        "weren't": "were not",
        "mightn't": "might not",
        "mustn't": "must not",
    }
    return re.compile(r"\b(" + "|".join(negations_.keys()) + r")\b")


def is_year(text):
    if len(text) == 4 and (MIN_YEAR < int(text) < MAX_YEAR):
        return True
    else:
        return False


def get_full_url_pattern():
    return re.compile(
        # u"^"
        # protocol identifier
        u"(?:(?:(?:https?|ftp):)?//)"
        # user:pass authentication
        u"(?:\S+(?::\S*)?@)?" u"(?:"
        # IP address exclusion
        # private & local networks
        u"(?!(?:10|127)(?:\.\d{1,3}){3})"
        u"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
        u"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
        # IP address dotted notation octets
        # excludes loopback network 0.0.0.0
        # excludes reserved space >= 224.0.0.0
        # excludes network & broadcast addresses
        # (first & last IP address of each class)
        u"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
        u"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
        u"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
        u"|"
        # host & domain names, may end with dot
        # can be replaced by a shortest alternative
        # u"(?![-_])(?:[-\w\u00a1-\uffff]{0,63}[^-_]\.)+"
        # u"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
        # # domain name
        # u"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
        u"(?:"
        u"(?:"
        u"[a-z0-9\u00a1-\uffff]"
        u"[a-z0-9\u00a1-\uffff_-]{0,62}"
        u")?"
        u"[a-z0-9\u00a1-\uffff]\."
        u")+"
        # TLD identifier name, may end with dot
        u"(?:[a-z\u00a1-\uffff]{2,}\.?)" u")"
        # port number (optional)
        u"(?::\d{2,5})?"
        # resource path (optional)
        u"(?:[/?#]\S*)?"
        # u"$",
        ,
        flags=re.I,
    )


def get_numbers_pattern():
    return regex.compile(
        r"(\d+)(?<!#\d+)"
    )  # Match numbers only if they're not hashtags


def get_uppercase_pattern():
    return re.compile(r"([A-Z][a-z]+)")


def get_non_alphanum_pattern():
    return re.compile(r"\W+")  # Match everything that is not contained in [a-zA-Z0-9_]


class TweetPreprocess:

    blank_spaces_pattern = get_blank_spaces_pattern()
    emojis_pattern = get_emojis_pattern()
    full_url_pattern = get_full_url_pattern()
    hashtags_pattern = get_hashtags_pattern()
    mentions_pattern = get_mentions_pattern()
    numbers_pattern = get_numbers_pattern()
    negations_pattern = get_negations_pattern()
    non_alphanum_pattern = get_non_alphanum_pattern()
    single_letter_words_pattern = get_single_letter_words_pattern()
    twitter_reserved_words_pattern = get_twitter_reserved_words_pattern()
    uppercase_pattern = get_uppercase_pattern()
    url_pattern = get_url_pattern()
    whitespace_trans = str.maketrans(string.punctuation, " " * len(string.punctuation))
    non_whitespace_trans = str.maketrans("", "", string.punctuation)
    stop_words = set(stopwords.words("english"))

    @classmethod
    def preprocess(cls, tweet, tokenizer="nltk", verbose=False):
        tokens = []
        yeah_tokens = []
        tokenizer = word_tokenize
        if tokenizer == "twitter":
            tokenizer = TweetTokenizer().tokenize
        if verbose:
            print("* BEFORE")
            print(tweet)
        tweet = html.unescape(html.unescape(tweet))
        tweet = cls.remove_urls(tweet, full=True)
        tweet = cls.remove_mentions(tweet)
        tweet = cls.remove_emojis(tweet)
        # It must be called before removing hashtags, because it splits up on numbers that do not start with an hashtag
        tweet = cls.remove_numbers(tweet, preserve_years=True)
        tweet = cls.remove_hashtags(tweet, split_capital_letter=True)
        tweet = contractions.fix(tweet)
        tweet = cls.remove_punctuation(tweet, repl=" ")
        if verbose:
            print("* AFTER REGEXES PREPROCESSING")
            print(tweet)
        tokens = tokenizer(tweet)
        if verbose:
            print("* AFTER TOKENIZATION")
            print(tokens)
        for token in tokens:
            token = token.lower()
            if not (
                token == "rt"
                or token in cls.stop_words
                or cls.non_alphanum_pattern.match(token)
                or (token.isalpha() and len(token) < 2)
            ):
                yeah_tokens.append(token)
        return yeah_tokens

    @classmethod
    def remove_urls(cls, tweet, full=True):
        if full:
            tweet = cls.full_url_pattern.sub(repl=" ", string=tweet)
        else:
            tweet = cls.url_pattern.sub(repl=" ", string=tweet)
        return tweet

    @classmethod
    def remove_punctuation(cls, tweet, repl=" "):
        if repl == " ":
            tweet = tweet.translate(cls.whitespace_trans)
        else:
            tweet = tweet.translate(cls.non_whitespace_trans)
        return tweet

    @classmethod
    def remove_emojis(cls, tweet):
        tweet = cls.emojis_pattern.sub(repl=" ", string=tweet)
        return tweet

    @classmethod
    def remove_mentions(cls, tweet):
        tweet = cls.mentions_pattern.sub(repl=" ", string=tweet)
        return tweet

    @classmethod
    def split_by_capital_letter(cls, m: re.Match):
        return " ".join(
            [token for token in cls.uppercase_pattern.split(m.group(1)) if token]
        )

    @classmethod
    def remove_hashtags(cls, tweet, split_capital_letter=True):
        if split_capital_letter:
            tweet = cls.hashtags_pattern.sub(
                repl=cls.split_by_capital_letter, string=tweet,
            )
        else:
            tweet = cls.hashtags_pattern.sub(repl=" ", string=tweet)
        return tweet

    @classmethod
    def remove_twitter_reserved_words(cls, tweet):
        tweet = cls.twitter_reserved_words_pattern.sub(repl=" ", string=tweet)
        return tweet

    @classmethod
    def remove_single_letter_words(cls, tweet):
        tweet = cls.single_letter_words_pattern.sub(repl=" ", string=tweet)
        return tweet

    @classmethod
    def remove_blank_spaces(cls, tweet):
        tweet = cls.blank_spaces_pattern.sub(repl=" ", string=tweet)
        return tweet

    @classmethod
    def remove_stopwords(cls, tweet, extra_stopwords=None):
        if extra_stopwords is None:
            extra_stopwords = []
        text = nltk.word_tokenize(tweet)

        new_sentence = []
        for w in text:
            if w not in cls.stop_words and w not in extra_stopwords:
                new_sentence.append(w)
        tweet = " ".join(new_sentence)
        return tweet

    @classmethod
    def remove_numbers(cls, tweet, preserve_years=False):
        text_list = cls.numbers_pattern.split(tweet)
        for text in text_list:
            if text.isnumeric():
                if preserve_years:
                    if not is_year(text):
                        text_list.remove(text)
                else:
                    text_list.remove(text)

        tweet = " ".join(text_list)
        return tweet

    @classmethod
    def lowercase(cls, tweet):
        tweet = tweet.lower()
        return tweet

    @classmethod
    def handle_negations(cls, tweet):
        tweet = cls.negations_pattern.sub(repl=" ", string=tweet)
        return tweet
