import streamlit as st
import pickle
import requests
import boto3
import os

# ========================
# Environment Variables
# ========================
BUCKET_NAME = os.environ.get("S3_BUCKET")
REGION_NAME = os.environ.get("S3_REGION")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
OMDB_API_KEY = os.environ.get("OMDB_API_KEY")

# Local filenames
MOVIES_FILE = "movies.pkl"
SIMILARITY_FILE = "similarity.pkl"

# S3 object keys (with folder path)
MOVIES_KEY = "uploads/movies.pkl"
SIMILARITY_KEY = "uploads/similarity.pkl"

# ========================
# Check environment variables
# ========================
st.write("Checking environment variables...")
st.write("AWS_ACCESS_KEY_ID exists:", AWS_ACCESS_KEY_ID is not None)
st.write("AWS_SECRET_ACCESS_KEY exists:", AWS_SECRET_ACCESS_KEY is not None)
st.write("OMDB_API_KEY exists:", OMDB_API_KEY is not None)
st.write("S3_BUCKET exists:", BUCKET_NAME is not None)
st.write("S3_REGION exists:", REGION_NAME is not None)

# ========================
# S3 client
# ========================
s3 = boto3.client(
    's3',
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# ========================
# Download files from S3
# ========================
def download_from_s3(local_filename, s3_key):
    if not os.path.exists(local_filename):
        st.write(f"Downloading {s3_key} from S3...")
        s3.download_file(BUCKET_NAME, s3_key, local_filename)
    else:
        st.write(f"{local_filename} already exists locally.")

download_from_s3(MOVIES_FILE, MOVIES_KEY)
download_from_s3(SIMILARITY_FILE, SIMILARITY_KEY)

# ========================
# Load pickle files
# ========================
movies_df = pickle.load(open(MOVIES_FILE, 'rb'))
similarity = pickle.load(open(SIMILARITY_FILE, 'rb'))

# ========================
# Helper Functions
# ========================
def fetch_poster(movie_name, api_key):
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={movie_name}"
    response = requests.get(url)
    data = response.json()
    return data.get('Poster')

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

# ========================
# Streamlit UI
# ========================
st.title("🎬 Movie Recommender System")

movie_name = st.selectbox("Select a movie:", movies_df['title'].values)

if st.button("Recommend"):
    recommended_movies = recommend(movie_name, OMDB_API_KEY)
    st.success(f"Recommendations for **{movie_name}**:")
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        if idx < len(recommended_movies):
            title, poster_url = recommended_movies[idx]
            col.text(title)
            if poster_url:
                col.image(poster_url)
            else:
                col.write("Poster not available.")
