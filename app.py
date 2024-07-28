import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=3164edc1f4904e3b59fdaaac8fb28a63')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies_df.iloc[i[0]].movie_id  # Assuming 'movie_id' column exists
        
        recommended_movies.append(movies_df.iloc[i[0]].title)
        
        # Fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_df = pickle.load(open('D:\ML\Movie Recommender System\movies.pkl', 'rb'))
movies_list = movies_df['title'].values

similarity = pickle.load(open('D:\ML\Movie Recommender System\similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select a movie",
    movies_list
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    for i in range(5):
        with [col1, col2, col3, col4, col5][i]:
            st.text(names[i])
            st.image(posters[i])
