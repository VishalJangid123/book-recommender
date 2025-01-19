import streamlit as st
import pickle
import os
import numpy as np

current_path = os.path.dirname(__file__)
rel_path = "models"
abs_file = os.path.join(current_path, rel_path)
print(abs_file)

st.header('Book Recommentdation')

model = pickle.load(open(abs_file + '/model.pkl', 'rb'))
book_name = pickle.load(open(abs_file + '/book_name.pkl', 'rb'))
final_book_rating = pickle.load(open(abs_file + '/final_book_rating.pkl', 'rb'))
book_pivot = pickle.load(open(abs_file + '/book_pivot.pkl', 'rb'))

selected_books = st.selectbox(
   'Type or select a book', book_name 
)

def get_recommended_books(book_name):
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distace, suggestions = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1, -1), n_neighbors=6)

    poster_urls = fetch_poster(suggestions)

    book_list = []
    for i in range(len(suggestions)):
        books = book_pivot.index[suggestions[i]]
        for j in books:
            book_list.append(j)
    return book_list, poster_urls

def fetch_poster(suggestions):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestions:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]:
        ids = np.where(final_book_rating['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_book_rating.iloc[idx]['img_url']
        poster_url.append(url)

    return poster_url



if st.button("Show recommended books"):
    recommended_books, urls = get_recommended_books(selected_books)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_books[1])
        st.image(urls[1])  
    with col2:
        st.text(recommended_books[2])
        st.image(urls[2])
    with col3:
        st.text(recommended_books[3])
        st.image(urls[3])    
    with col4:
        st.text(recommended_books[4])
        st.image(urls[4])  
    with col5:
        st.text(recommended_books[5])
        st.image(urls[5])  