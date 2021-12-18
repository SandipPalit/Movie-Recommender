import pickle
import streamlit as st
import requests
import numpy as np

st.set_page_config(page_title="Movie Recommender",page_icon="🎥")
st.markdown(""" <style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}footer:after {content:'Built with ❤ by Sandip Palit'; visibility: visible;color:grey;display: block;position: relative;text-align: center;padding: 0px;}</style> """, unsafe_allow_html=True)
st.markdown(f""" <style>.reportview-container .main .block-container{{padding-top: 5px;padding-right: 10px;padding-left: 10px;padding-bottom: 0px;}} </style> """, unsafe_allow_html=True)
st.markdown("""<style>button[title="View fullscreen"]{visibility: hidden;}</style>""", unsafe_allow_html=True)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=<YOUR_API_KEY>&language=en-US".format(movie_id) # REPLACE <YOUR_API_KEY> WITH YOUR OWN API KEY FROM TMDB
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names,recommended_movie_posters


movies = pickle.load(open('model/movie.pkl','rb'))
similarity = pickle.load(open('model/similarity.pkl','rb'))
movie_list = movies['title'].values
movie_list = np.insert(movie_list, 0, "", axis=0)

st.header('Movie Recommender System')
selected_movie = st.selectbox("Please type or select a movie from the dropdown",movie_list)

if st.button('Show Recommendation'):
    if selected_movie=="":
        st.error("Please type or select a movie from the dropdown!!")
    else:
        try:
            with st.spinner('We are finding the best recommendations for you.. Please wait!!'):
                recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
                col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.image(recommended_movie_posters[0])
                st.write(recommended_movie_names[0])
            with col2:
                st.image(recommended_movie_posters[1])
                st.write(recommended_movie_names[1])
            with col3:
                st.image(recommended_movie_posters[2])
                st.write(recommended_movie_names[2])
            with col4:
                st.image(recommended_movie_posters[3])
                st.write(recommended_movie_names[3])
            with col5:
                st.image(recommended_movie_posters[4])
                st.write(recommended_movie_names[4])

        except:
            st.error("We are unable to find this movie.. Please try another movie!!")