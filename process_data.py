import os
import ast
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("Starting Movie Data Processing Pipeline...")

DATABASE_DIR = "/Users/sornalisen/Desktop/database"
PROJECT_DIR = "/Users/sornalisen/Desktop/movie_recommender_system"
MODEL_DIR = os.path.join(PROJECT_DIR, "model")

os.makedirs(MODEL_DIR, exist_ok=True)

movies_path = os.path.join(DATABASE_DIR, "tmdb_5000_movies.csv")
credits_path = os.path.join(DATABASE_DIR, "tmdb_5000_credits.csv")

print(f"Loading datasets from {DATABASE_DIR}...")
movies = pd.read_csv(movies_path)
credits = pd.read_csv(credits_path)

print(f"Movies shape: {movies.shape}, Credits shape: {credits.shape}")

# Merge datasets on title
movies = movies.merge(credits, on="title")

# Select relevant columns for features and display
selected_cols = [
    'movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew',
    'vote_average', 'vote_count', 'popularity', 'release_date', 'tagline', 'runtime'
]

# Ensure movie_id exists (from credits or movies)
if 'movie_id' not in movies.columns and 'id' in movies.columns:
    movies['movie_id'] = movies['id']

movies = movies[selected_cols]
movies.dropna(subset=['overview', 'title'], inplace=True)
movies.reset_index(drop=True, inplace=True)

print(f"Dataset after cleaning nulls: {len(movies)} rows.")

def parse_names(text_str, limit=None):
    if not isinstance(text_str, str):
        return []
    try:
        data = ast.literal_eval(text_str)
        names = [item['name'] for item in data if isinstance(item, dict) and 'name' in item]
        return names[:limit] if limit else names
    except Exception:
        return []

def parse_director(text_str):
    if not isinstance(text_str, str):
        return "Unknown"
    try:
        data = ast.literal_eval(text_str)
        for item in data:
            if isinstance(item, dict) and item.get('job') == 'Director':
                return item.get('name', 'Unknown')
        return "Unknown"
    except Exception:
        return "Unknown"

# Parse structured JSON columns
print("Parsing genres, keywords, cast, and director...")
movies['genres_list'] = movies['genres'].apply(lambda x: parse_names(x))
movies['keywords_list'] = movies['keywords'].apply(lambda x: parse_names(x))
movies['cast_list'] = movies['cast'].apply(lambda x: parse_names(x, limit=4))
movies['director'] = movies['crew'].apply(parse_director)

# Extract release year
def extract_year(date_str):
    if isinstance(date_str, str) and len(date_str) >= 4:
        return date_str[:4]
    return "N/A"

movies['release_year'] = movies['release_date'].apply(extract_year)

# Collapse spaces in tags for NLP token uniqueness (e.g., "Johnny Depp" -> "JohnnyDepp")
def collapse_list(L):
    return [i.replace(" ", "") for i in L]

movies['genres_clean'] = movies['genres_list'].apply(collapse_list)
movies['keywords_clean'] = movies['keywords_list'].apply(collapse_list)
movies['cast_clean'] = movies['cast_list'].apply(collapse_list)
movies['director_clean'] = movies['director'].apply(lambda x: [x.replace(" ", "")] if x != "Unknown" else [])

movies['overview_tokens'] = movies['overview'].apply(lambda x: str(x).split())
movies['tags'] = (
    movies['overview_tokens'] +
    movies['genres_clean'] +
    movies['keywords_clean'] +
    movies['cast_clean'] +
    movies['director_clean']
)

movies['tags_str'] = movies['tags'].apply(lambda x: " ".join(x).lower())

print("Computing Bag of Words vectors and Cosine Similarity Matrix...")
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags_str']).toarray()

similarity = cosine_similarity(vectors).astype(np.float32)

print(f"Similarity matrix calculated. Shape: {similarity.shape}")

# Save pickled models
movie_list_pkl = os.path.join(MODEL_DIR, "movie_list.pkl")
similarity_pkl = os.path.join(MODEL_DIR, "similarity.pkl")
movies_json = os.path.join(MODEL_DIR, "movies_data.json")

print("Saving models to disk...")
with open(movie_list_pkl, "wb") as f:
    pickle.dump(movies, f)

with open(similarity_pkl, "wb") as f:
    pickle.dump(similarity, f)

# Also prepare a JSON dump for quick web rendering
movies_records = movies[[
    'movie_id', 'title', 'overview', 'genres_list', 'cast_list', 'director',
    'vote_average', 'vote_count', 'release_year', 'tagline', 'runtime'
]].to_dict(orient='records')

with open(movies_json, "w") as f:
    json.dump(movies_records, f, indent=2)

print(f"Successfully generated:")
print(f"  - {movie_list_pkl} ({os.path.getsize(movie_list_pkl) / 1e6:.2f} MB)")
print(f"  - {similarity_pkl} ({os.path.getsize(similarity_pkl) / 1e6:.2f} MB)")
print(f"  - {movies_json} ({os.path.getsize(movies_json) / 1e6:.2f} MB)")

print("Pipeline completed successfully!")
