import pandas as pd
import numpy as np
import math

# The strategy used to choose the top 100 “most popular” movies 
# is prioritizing movies that have the largest number of reviews 
# above a specified rating threshold (set as 4.0 here).
movies = pd.read_csv('popular_100.csv')
S = pd.read_csv('pop_100_S.csv', index_col=False)
S.index = S.columns

def myIBCF(w):
    # Identify unrated movies
    unrated_movies = w[w.isna()].index

    # Compute predictions for unrated movies
    predictions = []
    for movie_idx in unrated_movies:
        similar_movies = S.loc[movie_idx].dropna().index
        rated_similar_movies = similar_movies.intersection(w.dropna().index)

        if len(rated_similar_movies) > 0:
            numerator = np.sum(S.loc[movie_idx, rated_similar_movies] * w.loc[rated_similar_movies])
            denominator = np.sum(S.loc[movie_idx, rated_similar_movies])
            prediction = numerator / denominator
            predictions.append((movie_idx, prediction))
        else:
            predictions.append((movie_idx, np.nan))

    # Sort predictions by descending order
    predictions.sort(key=lambda x: float(x[1]) if not math.isnan(x[1]) else float('-inf'), reverse=True)


    # Select top 10 predictions
    top_10_predictions = predictions[:10]

    # Get movie names for top 10 predictions
    top_10_movie_ids = [movie_idx for movie_idx, _ in top_10_predictions]

    # Handle cases where fewer than 10 predictions are non-NA
    if len(top_10_movie_ids) < 10:
        
        # Filter out already rated movies and already predicted movies
        remaining_movies = movies["movie_id"][
            ~((movies["movie_id"].isin(w.dropna().index) | movies["movie_id"].isin(top_10_movie_ids)))
        ]
        # select top popular ones
        top_remaining_movie_ids = remaining_movies[:10 - len(top_10_movie_ids)]
        
        top_10_movie_ids = top_10_movie_ids.tolist() + top_remaining_movie_ids.tolist()

    return movies[movies['movie_id'].astype(str).isin(top_10_movie_ids)]

def get_displayed_movies():
    return movies.head(100)

def get_recommended_movies(new_user_ratings):
    # new_user_ratings 转成 w格式的
    w = pd.Series(np.nan, index=S.columns)
    for id, rating in new_user_ratings.items():
        id = str(id)
        w[id] = rating
    return myIBCF(w)