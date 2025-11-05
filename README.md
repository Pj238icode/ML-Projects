# 🎬 Movie Recommender System

[![Python](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.49.1-orange)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Live Demo: [https://ml-projects-msbm.onrender.com](https://ml-projects-msbm.onrender.com)

---

## 🚀 Project Overview

A web-based movie recommendation system that suggests top 5 movies based on the selected movie.  
It uses **content-based filtering** with **TF-IDF** vectors to compute similarity between movie descriptions. Poster images are fetched dynamically using the OMDb API. The app is built with Python and Streamlit and deployed on Render.

---

## 🛠 Features

- Select a movie from a large catalogue.
- Get top 5 recommended movies with posters.
- Uses **TF-IDF based content similarity** for recommendations.
- Cloud-hosted dataset for efficient access.
- Environment-variable driven configuration for secure keys.

---

## 📍 How It Works

1. Downloads two pickle files on startup:
   - `movies.pkl` → Contains movie metadata and descriptions.
   - `similarity.pkl` → Contains precomputed **TF-IDF similarity matrix**.
2. Users select a movie from the dropdown.
3. Retrieves the index of the movie, calculates similarity scores using **content-based filtering**, and picks top 5.
4. Fetches poster images for recommended movies from OMDb API.
5. Displays recommended movies and posters in the UI.

---

## 🧪 Tech Stack

- **Python**  
- **Streamlit** – Web interface  
- **Pandas / NumPy** – Data handling  
- **Requests** – API calls  
- **Pickle** – Load precomputed data  
- **AWS S3** – Hosting movie and similarity pickle files  
- **Scikit-learn** – TF-IDF vectorization and similarity computation  

---

## 🔧 Setup & Installation

1. **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd Movie_Recommender_System

2. Create and activate virtual environment (optional):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  
   venv\Scripts\activate     # Windows
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Set environment variables:
   ```bash
   export MOVIES_URL="https://cloudbucket100io.s3.ap-south-1.amazonaws.com/uploads/movies.pkl"
   export SIMILARITY_URL="https://cloudbucket100io.s3.ap-south-1.amazonaws.com/uploads/similarity.pkl"
   export OMDB_API_KEY="<your-omdb-api-key>"
5. Run locally:
   ```bash
   streamlit run app.py


 
