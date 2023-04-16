import pandas as pd
import glob
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

text_files = glob.glob("text/*.txt")
print(len(text_files))

tfidf_vectorizer = TfidfVectorizer(input='filename', stop_words='english')
tfidf_vector = tfidf_vectorizer.fit_transform(text_files)

print(tfidf_vector)
print(tfidf_vectorizer.get_feature_names_out())

feature_names = np.array(tfidf_vectorizer.get_feature_names_out())

def get_top_tf_idf_words(response, top_n=5):
    sorted_nzs = np.argsort(response.data)[:-(top_n + 1):-1]
    names = feature_names[response.indices[sorted_nzs]]
    return list(names)


csv_files = glob.glob("parsed/*.csv")
for csv in csv_files:
    #print(csv)
    df = pd.read_csv(csv, quotechar='"')
    text = df["text"]
    tfidf_vectorizer.input = "content"
    responses = tfidf_vectorizer.transform(text)
    #print(responses)
    df["keywords"] = [":".join(get_top_tf_idf_words(response)) for response in responses]
    df.to_csv(csv, index=False)
