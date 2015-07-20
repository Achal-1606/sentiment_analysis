from model import Model
from utils import readlines_to_lists


class RecognizeWord2Vec(object):

    def __init__(self):
        self.w2v = Model()

    def count_sentiment_words(self, words, sent):
        sentdic = {}

        for w in words:
            for s in sent:
                try:
                    dist = self.w2v.similarity(w, s)
                    if dist > 0.0:
                        sentdic[(w, s)] = dist
                except KeyError:
                    pass

        return sentdic


    def calc_each_sentiment(self, words):
        dic = []
        sentiments = readlines_to_lists("sentiment.txt")

        for sent in sentiments:
            sentdic = self.count_sentiment_words(words, sent)
            dic.append(sum(sentdic.values()) / len(sentdic))

        return dic
