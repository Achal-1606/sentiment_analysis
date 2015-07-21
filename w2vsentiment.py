import utils
import recognize
import sys

sentlabel = ["喜び", "信頼", "不安", "驚き", "悲しみ", "嫌気", "怒り", "予測"]


def w2vsentiment(w2v, sentence):
    sims = []

    testdata = utils.wakati_sentence(sentence)

    dic = w2v.calc_each_sentiment(testdata)

    for ratio in dic:
        sims.append(ratio / sum(dic))

    return sims


if __name__ == '__main__':
    ratios = [sentlabel]

    w2v = recognize.RecognizeWord2Vec()
    documents = utils.readlines(sys.argv[1])

    for doc in documents:
        ratios.append(w2vsentiment(w2v, doc))

    utils.output_csv(sys.argv[2], ratios)
