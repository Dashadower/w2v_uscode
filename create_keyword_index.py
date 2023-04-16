import pandas as pd
import glob
import itertools
from gensim.models import Word2Vec

word2vec_model = Word2Vec.load("word2vec_usc.model")

def get_vector(word):
    if word == "null":
        return False
    try:
        word2vec_model.wv.get_vector(word, norm=True)
    except KeyError:
        try:
            word = word[0].upper()+word[1:] if word[0].islower() else word[0].lower()+word[1:]
            word2vec_model.wv.get_vector(word, norm=True)
        except KeyError:
            return False
        else:
            return True
    except:
        return False
    else:
        return True

usc_dfs = glob.glob("parsed/*.csv")

entries = []

def create_entry(identifier, keywords):
    print(identifier, keywords)
    if not isinstance(keywords, str):
        return []

    return [{"keyword": keyword, "identifier": identifier} for keyword in keywords.split(":") if get_vector(keyword)]

for df_dir in usc_dfs:
    print(df_dir)
    df = pd.read_csv(df_dir)
    entries.extend(itertools.chain(*[create_entry(identifier, keywords) for identifier, keywords in zip(df["identifier"], df["keywords"])]))

index = pd.DataFrame(entries)
index.dropna(inplace=True)
index.to_csv("keyword_index.csv", index=False)