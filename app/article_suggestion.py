import json
import pandas as pd
import psutil
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import warnings
from app.app_utils import get_project_root
warnings.filterwarnings("ignore")


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


def userinput(user_input, btc):
    # removing the previous row that included a visitory query for subsequent questions
    btc = btc[btc['title'] != 'visitor_query']
    btc.loc[len(btc.index)] = ['visitor_query', None, user_input, None, None]
    return btc


def preprocess(btc2):
    btcc = btc2
    indices = pd.Series(btcc.index, index=btcc['title']).drop_duplicates()
    content = btcc['body']
    vect = TfidfVectorizer(
                       stop_words='english',
                       strip_accents='unicode',
                       analyzer='word',
                       sublinear_tf=False,
                       norm='l2',
                       use_idf=True,
                       ngram_range=(1, 2),
                       max_features=10000       # Not allowing more than 10k features/dimensions in our model
                       )

    tfidf_matrix = vect.fit_transform(content)
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    return btcc, cosine_similarities


def get_recommendations(df, column, value, cosine_similarities, limit=10):
    """Return a dataframe of content recommendations based on TF-IDF cosine similarity.
    
    Args:
        df (object): Pandas dataframe containing the text data. 
        column (string): Name of column used, i.e. 'title'. 
        value (string): Name of title to get recommendations for, i.e. 1982 Ferrari 308 GTSi For Sale by Auction
        cosine_similarities (array): Cosine similarities matrix from linear_kernel
        limit (int, optional): Optional limit on number of recommendations to return. 
        
    Returns: 
        Pandas dataframe. 
    """
    
    # Return indices for the target dataframe column and drop any duplicates
    indices = pd.Series(df.index, index=df[column])

    # Get the index for the target value
    target_index = indices[value]

    # Get the cosine similarity scores for the target value
    cosine_similarity_scores = list(enumerate(cosine_similarities[target_index]))

    # Sort the cosine similarities in order of closest similarity
    cosine_similarity_scores = sorted(cosine_similarity_scores, key=lambda x: x[1], reverse=True)

    # Return tuple of the requested closest scores excluding the target item and index
    cosine_similarity_scores = cosine_similarity_scores[1:limit+1]

    # Extract the tuple values
    index = (x[0] for x in cosine_similarity_scores)
    scores = (x[1] for x in cosine_similarity_scores)    

    # Get the indices for the closest items
    recommendation_indices = [i[0] for i in cosine_similarity_scores]

    # Get the actutal recommendations
    recommendations = df[column].iloc[recommendation_indices]

    # Return a dataframe
    df = pd.DataFrame(list(zip(index, recommendations, scores)), 
                      columns=['index','recommendation', 'cosine_similarity_score']) 

    return df


def return_suggestion(recommendations, btcc):
    recommendations = recommendations.rename(columns = {'recommendation': 'title'})                                  
    recommendationsss = recommendations.merge(btcc, on=["index", "title"], how="left", sort=False)
    return recommendationsss




def suggest_article(user_input):
    "Main Function"

    root = get_project_root()
    data_path = f"{root}/datasets/knowledge_datasets/bitcoin_knowledge_regexed_2022-05-14-1718.json"

    btc = wrangle_jsonl(data_path)
    btc2 = userinput(user_input, btc)
    btcc, cosine_similarities = preprocess(btc2)
    btcc.reset_index(inplace=True)
    recommendations = get_recommendations(btcc,
                                      'title',
                                      'visitor_query',
                                      cosine_similarities)
    suggestion = return_suggestion(recommendations, btcc)
    return suggestion
