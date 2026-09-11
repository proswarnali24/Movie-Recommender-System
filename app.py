import os
import pickle
import urllib.parse
import requests
import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Glassmorphism CSS Styling
# ---------------------------------------------------------
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Main background theme */
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #0f172a 50%, #1e1b4b 100%);
        color: #f8fafc;
    }

    /* Header Banner */
    .header-container {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem 1rem;
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }

    .header-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 400;
        max-width: 650px;
        margin: 0 auto;
    }

    /* Movie Cards */
    .movie-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 12px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        backdrop-filter: blur(8px);
        margin-bottom: 1.5rem;
    }

    .movie-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 30px rgba(99, 102, 241, 0.25);
        border-color: rgba(168, 85, 247, 0.4);
    }

    .movie-poster {
        width: 100%;
        border-radius: 12px;
        object-fit: cover;
        aspect-ratio: 2/3;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
    }

    .movie-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-top: 10px;
        margin-bottom: 4px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .match-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        margin-bottom: 8px;
    }

    .meta-info {
        font-size: 0.8rem;
        color: #cbd5e1;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 4px;
        margin-bottom: 8px;
    }

    .rating-badge {
        color: #fbbf24;
        font-weight: 700;
    }

    .genre-tag {
        display: inline-block;
        background: rgba(99, 102, 241, 0.15);
        color: #a5b4fc;
        border: 1px solid rgba(165, 180, 252, 0.2);
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.7rem;
        margin-right: 4px;
        margin-bottom: 4px;
    }

    .trailer-btn {
        display: block;
        width: 100%;
        text-align: center;
        padding: 6px 0;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: #ffffff !important;
        font-weight: 600;
        font-size: 0.8rem;
        border-radius: 8px;
        text-decoration: none !important;
        margin-top: 8px;
        transition: background 0.2s ease;
    }

    .trailer-btn:hover {
        background: linear-gradient(135deg, #4338ca 0%, #6d28d9 100%);
        opacity: 0.95;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# Load Dataset & Models
# ---------------------------------------------------------
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    movie_list_path = os.path.join(base_dir, "model", "movie_list.pkl")
    similarity_path = os.path.join(base_dir, "model", "similarity.pkl")

    if not os.path.exists(movie_list_path) or not os.path.exists(similarity_path):
        st.error("Model files not found! Running processing script...")
        os.system(f"python3 {os.path.join(base_dir, 'process_data.py')}")

    with open(movie_list_path, "rb") as f:
        movies_df = pickle.load(f)

    with open(similarity_path, "rb") as f:
        similarity_matrix = pickle.load(f)

    return movies_df, similarity_matrix

movies, similarity = load_data()

# ---------------------------------------------------------
# Poster Fetching with TMDB API & Dynamic Fallback
# ---------------------------------------------------------
TMDB_API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

@st.cache_data(ttl=86400)
def fetch_poster(movie_id, title="Movie"):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception:
        pass
    
    # Fallback SVG styled poster if image fetch fails or API is unavailable
    encoded_title = urllib.parse.quote(str(title)[:18])
    return f"https://placehold.co/400x600/1e293b/ffffff?text={encoded_title}"

# ---------------------------------------------------------
# Recommendation Core Function
# ---------------------------------------------------------
def recommend_movies(selected_movie_title, top_n=5):
    try:
        index = movies[movies['title'] == selected_movie_title].index[0]
    except IndexError:
        return []

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommendations = []
    for i in distances[1:top_n+1]:
        movie_row = movies.iloc[i[0]]
        movie_id = movie_row.movie_id
        score = float(i[1])
        
        poster_url = fetch_poster(movie_id, movie_row.title)
        
        genres = movie_row.genres_list if hasattr(movie_row, 'genres_list') else []
        director = movie_row.director if hasattr(movie_row, 'director') else 'Unknown'
        cast = movie_row.cast_list if hasattr(movie_row, 'cast_list') else []
        rating = float(movie_row.vote_average) if hasattr(movie_row, 'vote_average') else 0.0
        year = str(movie_row.release_year) if hasattr(movie_row, 'release_year') else 'N/A'
        runtime = f"{int(movie_row.runtime)} mins" if hasattr(movie_row, 'runtime') and pd.notnull(movie_row.runtime) else 'N/A'

        trailer_query = urllib.parse.quote(f"{movie_row.title} {year} official trailer")
        trailer_url = f"https://www.youtube.com/results?search_query={trailer_query}"

        recommendations.append({
            'title': movie_row.title,
            'poster': poster_url,
            'match_score': int(score * 100),
            'rating': rating,
            'year': year,
            'runtime': runtime,
            'director': director,
            'cast': cast[:2],
            'genres': genres[:2],
            'overview': str(movie_row.overview),
            'trailer_url': trailer_url
        })

    return recommendations

# ---------------------------------------------------------
# UI Header
# ---------------------------------------------------------
st.markdown("""
<div class="header-container">
    <div class="header-title">🎬 Movie Recommender System</div>
    <div class="header-subtitle">
        Intelligent Content-Based Movie Recommendation Engine. Discover films tailored precisely to your cinematic taste.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------
st.sidebar.markdown("### ⚙️ Engine Settings")
top_n_count = st.sidebar.slider("Number of Recommendations", min_value=4, max_value=12, value=6, step=2)

view_mode = st.sidebar.radio("Explore Mode", ["🎯 Similarity Recommender", "🎭 Genre Explorer", "⭐ Top Rated Movies"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Dataset Info")
st.sidebar.info(f"**Total Movies:** {len(movies):,}\n\n**Feature Vectors:** CountVectorizer & Cosine Similarity\n\n**Source:** TMDB 5000 Database")

# ---------------------------------------------------------
# MAIN TAB 1: SIMILARITY RECOMMENDER
# ---------------------------------------------------------
if view_mode == "🎯 Similarity Recommender":
    st.markdown("### 🔍 Select a Movie You Love")
    
    movie_list = sorted(movies['title'].values)
    default_index = movie_list.index("Avatar") if "Avatar" in movie_list else 0
    
    selected_movie = st.selectbox(
        "Search or choose a title from 4,800+ films:",
        movie_list,
        index=default_index
    )

    if st.button("🚀 Generate Recommendations", type="primary", use_container_width=True):
        with st.spinner("Analyzing cinematic patterns and plot features..."):
            recs = recommend_movies(selected_movie, top_n=top_n_count)
            
        if recs:
            st.markdown(f"### 💡 Movies Similar to *'{selected_movie}'*")
            
            # Display grid dynamically in rows of 3 or 4
            num_cols = 3 if top_n_count <= 6 else 4
            cols = st.columns(num_cols)
            
            for idx, rec in enumerate(recs):
                col = cols[idx % num_cols]
                with col:
                    genre_tags_html = "".join([f'<span class="genre-tag">{g}</span>' for g in rec['genres']])
                    
                    st.markdown(f"""
                    <div class="movie-card">
                        <div>
                            <img class="movie-poster" src="{rec['poster']}" alt="{rec['title']}" loading="lazy"/>
                            <div class="movie-title" title="{rec['title']}">{rec['title']}</div>
                            <span class="match-badge">⚡ {rec['match_score']}% Match</span>
                            <div class="meta-info">
                                <span>📅 {rec['year']}</span>
                                <span class="rating-badge">★ {rec['rating']:.1f}/10</span>
                            </div>
                            <div style="margin-bottom: 6px;">
                                {genre_tags_html}
                            </div>
                            <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 4px;">
                                👤 <b>Director:</b> {rec['director']}
                            </div>
                        </div>
                        <div>
                            <a href="{rec['trailer_url']}" target="_blank" class="trailer-btn">▶ Watch Trailer</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("📖 Story Overview"):
                        st.write(rec['overview'])

# ---------------------------------------------------------
# MAIN TAB 2: GENRE EXPLORER
# ---------------------------------------------------------
elif view_mode == "🎭 Genre Explorer":
    st.markdown("### 🎭 Explore Movies by Genre")
    
    # Extract unique genres
    all_genres = set()
    for g_list in movies['genres_list']:
        if isinstance(g_list, list):
            all_genres.update(g_list)
            
    sorted_genres = sorted(list(all_genres))
    selected_genre = st.selectbox("Select Genre:", sorted_genres)
    
    # Filter movies by selected genre
    def has_genre(row_genres):
        return isinstance(row_genres, list) and selected_genre in row_genres
        
    genre_movies = movies[movies['genres_list'].apply(has_genre)].sort_values(by='popularity', ascending=False)
    
    st.markdown(f"#### Displaying top popular films in **{selected_genre}**:")
    
    cols = st.columns(4)
    for idx, (_, row) in enumerate(genre_movies.head(top_n_count).iterrows()):
        col = cols[idx % 4]
        with col:
            poster_url = fetch_poster(row.movie_id, row.title)
            year = str(row.release_year) if hasattr(row, 'release_year') else 'N/A'
            rating = float(row.vote_average) if hasattr(row, 'vote_average') else 0.0
            
            trailer_query = urllib.parse.quote(f"{row.title} {year} official trailer")
            trailer_url = f"https://www.youtube.com/results?search_query={trailer_query}"

            st.markdown(f"""
            <div class="movie-card">
                <div>
                    <img class="movie-poster" src="{poster_url}" alt="{row.title}"/>
                    <div class="movie-title">{row.title}</div>
                    <div class="meta-info">
                        <span>📅 {year}</span>
                        <span class="rating-badge">★ {rating:.1f}/10</span>
                    </div>
                </div>
                <div>
                    <a href="{trailer_url}" target="_blank" class="trailer-btn">▶ Watch Trailer</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------
# MAIN TAB 3: TOP RATED MOVIES
# ---------------------------------------------------------
elif view_mode == "⭐ Top Rated Movies":
    st.markdown("### ⭐ Highest Rated Movies (Min 500 Votes)")
    
    top_rated = movies[movies['vote_count'] >= 500].sort_values(by='vote_average', ascending=False)
    
    cols = st.columns(4)
    for idx, (_, row) in enumerate(top_rated.head(top_n_count).iterrows()):
        col = cols[idx % 4]
        with col:
            poster_url = fetch_poster(row.movie_id, row.title)
            year = str(row.release_year) if hasattr(row, 'release_year') else 'N/A'
            rating = float(row.vote_average) if hasattr(row, 'vote_average') else 0.0
            
            trailer_query = urllib.parse.quote(f"{row.title} {year} official trailer")
            trailer_url = f"https://www.youtube.com/results?search_query={trailer_query}"

            st.markdown(f"""
            <div class="movie-card">
                <div>
                    <img class="movie-poster" src="{poster_url}" alt="{row.title}"/>
                    <div class="movie-title">{row.title}</div>
                    <div class="meta-info">
                        <span>📅 {year}</span>
                        <span class="rating-badge">★ {rating:.1f}/10 ({int(row.vote_count):,} votes)</span>
                    </div>
                </div>
                <div>
                    <a href="{trailer_url}" target="_blank" class="trailer-btn">▶ Watch Trailer</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 1rem 0;">
    Movie Recommender System • Powered by CountVectorizer, Cosine Similarity & TMDB Database
</div>
""", unsafe_allow_html=True)
