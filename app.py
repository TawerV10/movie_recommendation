import streamlit as st
import pandas as pd
import requests
import pickle
import dotenv
import os

dotenv.load_dotenv()

api_key = os.getenv('THEMOVIEDB_API')
movies_dict = pickle.load(open('data/movies.pkl', 'rb'))
similarity_dict = pickle.load(open('data/similarity.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)
similarity = pd.DataFrame(similarity_dict)

movies_list = movies['original_title'].values

def get_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    data = requests.get(url).json()

    return 'https://image.tmdb.org/t/p/w500' + data['poster_path']

def recommend(movie):
    movie_id = movies.query('original_title == @movie').index[0]
    distances = similarity[movie_id]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = [movies.iloc[movie[0]]['original_title'] for movie in movies_list]
    recommended_ids = [movies.iloc[movie[0]]['id'] for movie in movies_list]
    recommended_posters = [get_poster(recommended_id) for recommended_id in recommended_ids]

    return recommended_movies, recommended_posters

st.title('Movie Recommendation System')

option = st.selectbox('Choose movie', movies_list)

if st.button('Recommend'):
    recommended_movies, recommended_posters = recommend(option)

    col1, col2, col3, col4, col5 = st.columns(5)
    with st.container():
        with col1:
            st.write(recommended_movies[0])
        with col2:
            st.write(recommended_movies[1])
        with col3:
            st.write(recommended_movies[2])
        with col4:
            st.write(recommended_movies[3])
        with col5:
            st.write(recommended_movies[4])

    col1, col2, col3, col4, col5 = st.columns(5)
    with st.container():
        with col1:
            st.image(recommended_posters[0])
        with col2:
            st.image(recommended_posters[1])
        with col3:
            st.image(recommended_posters[2])
        with col4:
            st.image(recommended_posters[3])
        with col5:
            st.image(recommended_posters[4])