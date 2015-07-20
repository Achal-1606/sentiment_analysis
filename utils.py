from tweepy.error import TweepError
import tweepy
import MeCab
import configparser
import re
import csv


rqt = re.compile(r'.*(RT|QT).*')
reply = re.compile(r'.*@[a-zA-Z0-9_].*')
url = re.compile(r'.*http(|s)://[a-zA-Z0-9\-\.\/].*')
dust = re.compile(r'( |\u3000|\n)')
hashtag = re.compile(r'\#.* ')


class Auth(object):

    def __init__(self, configfile):
        self.config = configparser.ConfigParser()
        self.config.read(configfile)
        self.consumerkey = self.config["TWITTER"]["ConsumerKey"]
        self.consumersec = self.config["TWITTER"]["ConsumerSecret"]
        self.accesstoken = self.config["TWITTER"]["AccessToken"]
        self.accesssec = self.config["TWITTER"]["AccessSecret"]

    def make_api(self):
        auth = tweepy.OAuthHandler(self.consumerkey, self.consumersec)
        auth.set_access_token(self.accesstoken, self.accesssec)
        return tweepy.API(auth)

auth = Auth("twitter.cfg")
api = auth.make_api()


def readlines(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    return lines


def readlines_to_lists(filename):
    with open(filename, "r") as f:
        _lines = f.readlines()
    lines = [line.rstrip("\n").split(" ") for line in _lines]
    return lines


def output_csv(filename, lists):
    with open(filename, "w") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(lists)


def wakati_sentence(sentence):
    keywords = []

    tagger = MeCab.Tagger("-Owakati")
    #wakatied = tagger.parse(sentence)
    node = tagger.parseToNode(sentence)
    while node:
        pos = node.feature.split(",")[0]
        word = node.feature.split(",")[6]
        if word == "*":
            node = node.next
            continue
        if pos == "名詞":
            keywords.append(word)
        elif pos == "動詞":
            keywords.append(word)
        elif pos == "形容詞":
            keywords.append(word)
        node = node.next

    return keywords


def search_tweets(query, filename):
    tweets = []

    while len(tweets) < 1000:
        try:
            for tweet in api.search(q=query, count=200):
                status = tweet.text
                status = re.sub(dust, "", status)
                status = re.sub(hashtag, "", status)
                if rqt.match(status) == None and reply.match(status) == None and url.match(status) == None:
                    tweets.append(status + "\n")
        except TweepError as e:
            break

    return tweets
