import json
import pandas as pd
import psutil
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import warnings
warnings.filterwarnings("ignore")

data_path = '/Users/pretermodernist/coding-projects/bitcoin-knowledge-bot/datasets/knowledge_datasets/bitcoin_knowledge_regexed_2022-01-14-1806.json'



cores = psutil.cpu_count()
cores_used = int(cores/3)
vect = TfidfVectorizer(
                       stop_words='english',
                       ngram_range=(1, 2),
                       max_features=10000
                       )
# Reading in our bitcoin data from a json lines file with a reproducible function


def wrangle_jsonl(path: str):
    '''
    Reads in our bitcoin data from a json lines file

    Parameters
    ----------
    None
    
    Returns
    -------
    df: pandas datafarme 
        Contains text data from several reputable BTC news and historical sources
    '''
    with open(path) as l:
        lines = l.read().splitlines()
    df_inter = pd.DataFrame(lines)
    df_inter.columns = ['json_element']
    df_inter['json_element'].apply(json.loads)
    df = pd.json_normalize(df_inter['json_element'].apply(json.loads))

    return df

btc = wrangle_jsonl(data_path)
btc_knn = pd.DataFrame(btc['body'])
## USER INPUT EXAMPLE ##
# Swapping this out later for user-submitted inquiry to GPT3 chatbot
user_input = ["What's the blockchain?"]

btc_knn.loc[len(btc_knn.index)] = user_input
dtm = vect.fit_transform(btc_knn['body'])
dtm = pd.DataFrame(dtm.toarray(), columns=vect.get_feature_names())
nn = NearestNeighbors(
    n_neighbors = 25,
    algorithm = 'ball_tree',
    n_jobs = cores_used
    )

nn.fit(dtm)

doc_index = -1
doc = [dtm.iloc[doc_index].values]
neigh_dist, neigh_index = nn.kneighbors(doc)
for doc in neigh_index:
    recommendation = btc_knn.iloc[doc]

def return_suggestion(recommendation, btc):
    '''
    Returns a pandas dataframe row containing an article suggestion from a mapped k-NN index

    Parameters
    ----------
    Subset dataframe used for k-NN query indexed by DTM
    Original dataframe
    
    Returns
    -------
    knn_recommendation: pandas datafarme row
        Contains title, body, image, and url data from our user submitted queries' nearest neighbor
    '''
    knn_recommendation = btc[btc["body"].str.contains(recommendation.iloc[1].values[0])==True]
    return knn_recommendation

suggestion = return_suggestion(recommendation, btc)
print(suggestion)
