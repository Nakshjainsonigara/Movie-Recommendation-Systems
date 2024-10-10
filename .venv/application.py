import streamlit as st
import pickle
import requests

# Function to fetch movie posters
def fetch_posters(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=4640198e80f9755eb3edcf761323bf46&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w185/" + data['poster_path']

# Function to recommend movies
def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_indices:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movies.append(movies_df.iloc[i[0]]['title'])
        recommended_movies_posters.append(fetch_posters(movie_id))
    return recommended_movies, recommended_movies_posters

# Page title with custom styling
st.markdown("""
    <style>
        body {
            background-color: #f4f4f4;
        }
        .title {
            color: #e74c3c;
            font-family: 'Merriweather', sans-serif;
            font-size: 42px;
            text-align: center;
            margin-bottom: 20px;
        }
        .stSelectbox label {
            color: #2c3e50;
            font-size: 20px;
        }
        .recommend-btn button {
            background-color: #e74c3c;
            color: white;
            font-size: 18px;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
        }
        .recommend-btn button:hover {
            background-color: #c0392b;
        }
        .movie-text {
            font-size: 16px;
            color: #2c3e50;
            font-weight: bold;
            text-align: center;
        }
        .movie-poster {
            border-radius: 10px;
            margin: 5px 0;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Movie Recommendation System</div>', unsafe_allow_html=True)

# Load movies data
movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie selection box
movies_list = movies_df['title'].values
selected_movie_name = st.selectbox('Select a Movie', movies_list)

# Recommend button with custom style
if st.button('Recommend', use_container_width=True, key="recommend-btn"):
    names, posters = recommend(selected_movie_name)
    
    # Display recommended movies in a responsive grid layout
    cols = st.columns(5)
    
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f'<div class="movie-text">{names[idx]}</div>', unsafe_allow_html=True)
            st.image(posters[idx], use_column_width='always', caption=names[idx])
