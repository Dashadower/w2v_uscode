from gensim.models import word2vec
import string
import glob
from nltk.tokenize import word_tokenize, sent_tokenize

translate_table = dict((ord(char), None) for char in string.punctuation)

sentences = []

text_files = glob.glob("text/*.txt") + glob.glob("DEFT_train/formatted_*.txt")
for file in text_files:
    data = open(file).read().strip().translate(translate_table)
    sent = sent_tokenize(data)
    for s in sent:
        tokens = word_tokenize(s)
        sentences.append(tokens)
print("start training")
model = word2vec.Word2Vec(sentences=sentences, vector_size=150, workers=6)

model.save("word2vec_usc.model")


