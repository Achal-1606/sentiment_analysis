from gensim.models import word2vec

class Model(object):

    def __init__(self, modelname="model/jawiki_gensim.pkl", corpus=""):
        try:
            self.m = self.load_model(modelname)
        except Exception:
            self.m = self.make_load_model(corpus)
            self.save_model(modelname)

    def load_model(self, modelname):
        return word2vec.Word2Vec.load(modelname)

    def save_model(self, modelname):
        self.m.save(modelname)

    def make_load_model(self, corpus):
        sentences = word2vec.Text8Corpus(corpus)
        _m = word2vec.Word2Vec(sentences)
        return _m

    def similarity(self, w1, w2):
        return self.m.similarity(w1, w2)

    def word_similarity_enum(self, w):
        return self.m.most_similar(positive=[w])
