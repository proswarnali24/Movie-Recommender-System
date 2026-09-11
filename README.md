# 🎬 Movie Recommender System

A content-based movie recommendation system built with **Python**, **Scikit-Learn (CountVectorizer & Cosine Similarity)**, and **Streamlit**, trained on the **TMDB 5000 Movies & Credits Dataset**.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-ff4b4b?style=for-the-badge&logo=streamlit&logoColor=white)](https://proswarnali24-movie-recommender-system-app-ajvvsv.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-CountVectorizer%20%26%20Cosine%20Similarity-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-proswarnali24-181717?style=for-the-badge&logo=github&logoColor=white)

---

## 🌐 Live Application

Access the live deployed application here:  
👉 **[https://proswarnali24-movie-recommender-system-app-ajvvsv.streamlit.app/](https://proswarnali24-movie-recommender-system-app-ajvvsv.streamlit.app/)**

---

## 🌟 Features

- **🎯 Smart Recommendations**: Analyzes natural language plot overviews, genres, keywords, top cast members, and directors to compute precise content-based movie matches.
- **⚡ Match Score Percentage**: Displays similarity match confidence percentage (e.g., `⚡ 98% Match`).
- **🖼️ High-Res Poster Art**: Fetches live movie poster art via TMDB API with resilient fallback SVG cards.
- **🎭 Multi-Mode Exploration**:
  - **Similarity Recommender**: Choose any movie from 4,800+ titles to get 4–12 tailored recommendations.
  - **Genre Explorer**: Discover top popular films filtered by genre (Action, Sci-Fi, Animation, Drama, etc.).
  - **Top Rated Movies**: Browse highest-rated titles across the TMDB catalog.
- **▶️ Direct Trailer Links**: Watch official movie trailers on YouTube with a single click.

---

## 🏗️ Architecture & Model Pipeline

1. **Dataset Integration**: Loads `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv`.
2. **Feature Extraction & Text Processing**:
   - `overview`: Plot summary tokenization.
   - `genres` & `keywords`: Extracted tag names.
   - `cast`: Top 4 lead actors.
   - `crew`: Extracted Director name.
3. **Vectorization**: `CountVectorizer` (max features: 5,000, English stop words removed).
4. **Similarity Computation**: `Cosine Similarity` matrix calculation.
5. **Model Export**: Serializes model objects to `model/movie_list.pkl`, `model/similarity.pkl`, and `model/movies_data.json`.

---

## 📂 Project Structure

```
Movie-Recommender-System/
├── app.py              # Main Streamlit Web Application
├── process_data.py     # Automated Data Cleaning & Model Generation Pipeline
├── requirements.txt    # Python Package Dependencies
├── Procfile            # Heroku / Render Deployment Configuration
├── setup.sh            # Streamlit Server Configuration Script
├── runtime.txt         # Python Runtime Version Specification
├── README.md           # Documentation
├── .gitignore          # Git Ignored Files
└── model/
    ├── movie_list.pkl      # Cleaned Movie Metadata DataFrame Pickle
    ├── similarity.pkl      # 4806x4806 Cosine Similarity Matrix Pickle
    └── movies_data.json    # JSON Dataset for Lightweight Web Access
```

---

## 🚀 How to Run Locally

### Prerequisites
Make sure you have Python 3.10+ installed.

### Steps:
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/proswarnali24/Movie-Recommender-System.git
   cd Movie-Recommender-System
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate Models (Optional - Pre-built models included)**:
   ```bash
   python process_data.py
   ```

4. **Launch Streamlit App**:
   ```bash
   streamlit run app.py
   ```

5. Open `http://localhost:8501` in your web browser.

---

## ☁️ Deployment Guide

### Streamlit Community Cloud (Live Production App)

- **Live URL**: [https://proswarnali24-movie-recommender-system-app-ajvvsv.streamlit.app/](https://proswarnali24-movie-recommender-system-app-ajvvsv.streamlit.app/)

---

### Deploy on Heroku

The repository includes `Procfile`, `setup.sh`, `requirements.txt`, and `runtime.txt`:

1. Go to **[dashboard.heroku.com/new-app](https://dashboard.heroku.com/new-app)**.
2. Create an app (e.g., `movie-recommender-system-app`).
3. Under **Deployment Method**, select **GitHub** and connect `proswarnali24/Movie-Recommender-System`.
4. Click **Deploy Branch** (`main`).

---

## 👤 Author

- **Live Application**: [Streamlit Live Demo](https://proswarnali24-movie-recommender-system-app-ajvvsv.streamlit.app/)
- **GitHub**: [@proswarnali24](https://github.com/proswarnali24)
- **Repository**: [Movie-Recommender-System](https://github.com/proswarnali24/Movie-Recommender-System)
