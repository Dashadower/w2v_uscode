from gensim.models import Word2Vec
model = Word2Vec.load("word2vec_usc.model")

print(model.wv.most_similar(positive=["Canton"], topn=5))