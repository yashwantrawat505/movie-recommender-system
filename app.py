import streamlit as st
import pandas as pd
import pickle
import bz2

st.set_page_config(page_title="Movie Recommender", layout="centered")

@st.cache_resource
def load_data():
    # Load movie titles
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    
    # Decompress similarity matrix
    with bz2.BZ2File('similarity.pbz2', 'rb') as f:
        similarity = pickle.load(f)
        
    return movies, similarity

movies, similarity = load_data()

def recommend(movie_title):
    movie_index = movies[movies['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

st.title("🎬 Movie Recommender System")
st.write("Select a movie from the dropdown to get 5 similar recommendations.")

selected_movie_name = st.selectbox(
    "Select a Movie:",
    movies['title'].values
)

if st.button("Recommend"):
    recommendations = recommend(selected_movie_name)
    st.subheader("Recommended Movies:")
    for idx, movie in enumerate(recommendations, 1):
        st.write(f"**{idx}. {movie}**")
        