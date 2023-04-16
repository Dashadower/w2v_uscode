from gensim.models import Word2Vec
import pandas as pd
import textwrap
import itertools
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

keyword_index_df = pd.read_csv("keyword_index.csv")
word2vec_model = Word2Vec.load("word2vec_usc.model")

usc_df = pd.read_csv("merged_usc.csv")

keywords = keyword_index_df.keyword.unique().tolist()
print(len(keywords), "unique keywords")

word = "terminates"

def get_vector(word):
    try:
        return word2vec_model.wv.get_vector(word, norm=True)
    except KeyError:
        word = word[0].upper()+word[1:] if word[0].islower() else word[0].lower()+word[1:]
        return word2vec_model.wv.get_vector(word, norm=True)


keyword_wv = np.stack([get_vector(word) for word in keywords])

def np_argmax_n(arr, n):
    return np.argpartition(arr, -n)[-n:]

def get_identifiers_by_keyword(keyword):
    try:
        return keyword_index_df.loc[keyword_index_df.keyword == keyword].identifier.unique().tolist()
    except:
        keyword = keyword[0].upper()+keyword[1:] if keyword[0].islower() else keyword[0].lower()+keyword[1:]
        return keyword_index_df.loc[keyword_index_df.keyword == keyword].identifier.unique().tolist()

while True:
    keyword = input("영문 키워드 입력:")
    try:
        keyword_vec = get_vector(keyword).reshape(1, -1)
    except KeyError:
        print("w2v 내에 존재하는 단어가 아님")
        continue

    similarity = cosine_similarity(keyword_vec, keyword_wv)[0, :]
    top5_keywords = [keywords[n] for n in np_argmax_n(similarity, 5)]

    target_identifiers = list(itertools.chain(*[get_identifiers_by_keyword(key) for key in top5_keywords]))

    for index, identifier in enumerate(target_identifiers):
        record = usc_df.loc[usc_df.identifier == identifier]
        print(f"{index} - ({record.identifier.values[0]}) {record.heading.values[0]}")
    while True:
        selection = input("열람 항목 번호 입력(q를 입력하여 재검색):")
        if selection.lower() == "q": break
        else: selection = int(selection)

        if selection >= len(target_identifiers):
            print("인덱스 초과")
            continue

        selected_identifier = target_identifiers[selection]
        record = usc_df.loc[usc_df.identifier == selected_identifier]

        print("-" * 10)
        print(f"({record.identifier.values[0]}) {record.heading.values[0]}")
        lines = textwrap.fill(record.text.values[0], 80)
        print(lines)





