import streamlit as st
import pickle
import requests
import boto3
import os


BUCKET_NAME = "cloudbucket100io"
MOVIES_FILE = "movies.pkl"
SIMILARITY_FILE = "similarity.pkl"
REGION_NAME = "ap-south-1"

s3 = boto3.client('s3', region_name=REGION_NAME)


def download_from_s3(filename):
    if not os.path.exists(filename):
        s3.download_file(BUCKET_NAME, filename, filename)

# Download files
download_from_s3(MOVIES_FILE)
download_from_s3(SIMILARITY_FILE)

# Load pickle files
movies_df = pickle.load(open(MOVIES_FILE, 'rb'))
similarity = pickle.load(open(SIMILARITY_FILE, 'rb'))


# Function to fetch poster URL
def fetch_poster(movie_name, api_key):
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={movie_name}"
    response = requests.get(url)
    data = response.json()
    return data.get('Poster')


# Recommendation function
def recommend(movie_name, api_key):
    movie_index = movies_df[movies_df['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []

    for i in movie_list:
        movie_title = movies_df.iloc[i[0]].title
        poster_url = fetch_poster(movie_title, api_key)
        recommended_movies.append((movie_title, poster_url))

    return recommended_movies


# Streamlit UI
st.title("🎬 Movie Recommender System")

movie_name = st.selectbox("Select a movie:", movies_df['title'].values)

if st.button("Recommend"):
    api_key = '72a89250'
    recommended_movies = recommend(movie_name, api_key)

    st.success(f"Recommendations for **{movie_name}**:")

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        if idx < len(recommended_movies):
            movie_title, poster_url = recommended_movies[idx]
            col.text(movie_title)
            if poster_url:
                col.image(poster_url)
            else:
                col.write("Poster not available.")

