import streamlit as st
import pickle
import requests
import os

# =======================
# Environment variables
# =======================
MOVIES_URL = os.environ.get("MOVIES_URL")
SIMILARITY_URL = os.environ.get("SIMILARITY_URL")
OMDB_API_KEY = os.environ.get("OMDB_API_KEY")



st.write("MOVIES_URL:", MOVIES_URL)
st.write("SIMILARITY_URL:", SIMILARITY_URL)
st.write("OMDB_API_KEY:", OMDB_API_KEY)


MOVIES_FILE = "movies.pkl"
SIMILARITY_FILE = "similarity.pkl"

# =======================
# Helper function to download files
# =======================
def download_file_from_url(url, filename):
    if not os.path.exists(filename):
        r = requests.get(url)
        if r.status_code == 200:
            with open(filename, "wb") as f:
                f.write(r.content)
        else:
            st.error(f"Failed to download {filename}. Status code: {r.status_code}")
            st.stop()

# Download the pickle files
download_file_from_url(MOVIES_URL, MOVIES_FILE)
download_file_from_url(SIMILARITY_URL, SIMILARITY_FILE)

# =======================
# Load pickle files
# =======================
movies_df = pickle.load(open(MOVIES_FILE, "rb"))
similarity = pickle.load(open(SIMILARITY_FILE, "rb"))

# =======================
# Fetch movie poster
# =======================
def fetch_poster(movie_name, api_key):
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={movie_name}"
    response = requests.get(url)
    data = response.json()
    return data.get("Poster")

# =======================
# Recommendation function
# =======================
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

# =======================
# Streamlit UI
# =======================
st.title("🎬 Movie Recommender System")

movie_name = st.selectbox("Select a movie:", movies_df['title'].values)

if st.button("Recommend"):
    recommended_movies = recommend(movie_name, OMDB_API_KEY)
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

