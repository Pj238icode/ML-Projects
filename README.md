Movie Recommender System

Live Demo → https://ml-projects-msbm.onrender.com

🚀 Project Overview

This project presents a web‑based movie recommendation system built with Python and deployed on Streamlit. Users select a movie and get top 5 recommended movies with posters fetched in realtime.

🛠 Features

Select a movie from a large catalogue and receive recommendations.

Poster images retrieved via the OMDb API.

Precomputed similarity matrix for fast recommendations.

Cloud‑hosted files (pickled datasets) and environment‑variable driven config for secure deployment.

Easy deployment on platforms like Render.

📍 How It Works

On startup, the app downloads two pickle‑files: movies.pkl (movie metadata) and similarity.pkl (similarity matrix).

Users choose a movie title from a dropdown.

The system finds the index of the selected movie, retrieves distances from the similarity matrix, sorts them, and picks the top 5.

For each recommended movie, the OMDb API is queried to fetch the poster image.

The UI displays the recommended movie titles and posters in a row.

🧪 Tech Stack

Python

Streamlit for the web interface

Pandas / NumPy for data handling

Requests for API calls

Pickle for loading precomputed data

Cloud storage for hosting large model files

Environment variables for keys and URLs

🔧 Setup & Deployment Instructions

Clone the repo:

git clone <your‑repo‑url>
cd Movie_Recommender_System


Create and activate a virtual environment (optional):

python3 -m venv venv  
source venv/bin/activate  


Install dependencies:

pip install -r requirements.txt  


Set environment variables:

export MOVIES_URL="https://cloudbucket100io.s3.ap-south-1.amazonaws.com/uploads/movies.pkl"  
export SIMILARITY_URL="https://cloudbucket100io.s3.ap-south-1.amazonaws.com/uploads/similarity.pkl"  
export OMDB_API_KEY="<your‑omdb‑api‑key>"  


Run locally:

streamlit run app.py  
