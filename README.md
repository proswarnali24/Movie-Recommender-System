# 🎬 CineMind AI - Movie Recommender System

A content-based movie recommendation system built with **Python**, **Scikit-Learn (TF-IDF & Cosine Similarity)**, and **Streamlit**, using the **TMDB 5000 Movies & Credits Dataset**.

![CineMind Banner](https://img.shields.io/badge/Streamlit-App-ff4b4b?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Machine Learning](https://img.shields.io/badge/ML-TF--IDF%20%26%20Cosine%20Similarity-22c55e?style=for-the-badge)

---

## 🌟 Key Features

- **🎯 Smart Recommendations**: Calculates natural language plot & metadata similarity to match movies based on overview, genres, cast, director, and keywords.
- **⚡ Match Score Percentage**: Displays similarity match confidence (e.g. `98% Match`).
- **🖼️ High-Res Poster Art**: Fetches live movie poster art via TMDB API with resilient SVG fallback cards.
- **🎭 Multi-Mode Exploration**:
  - **Similarity Recommender**: Pick any movie to get 4–12 tailored recommendations.
  - **Genre Explorer**: Discover top-rated titles filtered by genre (Action, Sci-Fi, Animation, Drama, etc.).
  - **Top Rated Movies**: Browse highest-rated titles across the 4,800+ film catalog.
- **▶️ Direct Trailer Links**: Instantly watch official movie trailers on YouTube with a single click.

---

## 📂 Project Structure

```
movie_recommender_system/
├── app.py                  # Main Streamlit web app
├── process_data.py         # Data processing & TF-IDF model generator
├── requirements.txt        # Python package dependencies
├── Procfile                # Heroku / Render deployment file
├── setup.sh                # Streamlit server config script
├── README.md               # Documentation
└── model/
    ├── movie_list.pkl      # Cleaned DataFrame pickle
    ├── similarity.pkl      # 4806x4806 Cosine Similarity matrix pickle
    └── movies_data.json    # JSON metadata for fast API/web access
```

---

## 🚀 How to Run Locally

1. **Clone or navigate to project directory**:
   ```bash
   cd /Users/sornalisen/Desktop/movie_recommender_system
   ```

2. **Generate the model files (if not generated already)**:
   ```bash
   python3 process_data.py
   ```

3. **Launch the Streamlit app**:
   ```bash
   python3 -m streamlit run app.py
   ```

4. Open your browser at `http://localhost:8501`.

---

## ☁️ Deployment Instructions

### Deploy on Streamlit Community Cloud (Recommended - Free)
1. Push this directory to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Connect your repository and select `app.py` as the main file path.
4. Click **Deploy**!

### Deploy on Render / Heroku
Use the included `Procfile` and `setup.sh` to deploy directly as a web service.
