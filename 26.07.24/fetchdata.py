import pyodbc
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime

connection = (
    'SERVER=localhost;'
    'DATABASE=TREND;'
    'UID=sa;'
    'PWD=Joochou259@;'
    'DRIVER=/opt/homebrew/lib/libmsodbcsql.17.dylib'
)

def fetch_categories():
    conn = pyodbc.connect(connection)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()
    conn.close()
    return categories

def fetch_keywords_for_date_and_category(selected_date, category_id):
    conn = pyodbc.connect(connection)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT k.keyword
    FROM keywords k
    JOIN articles a ON k.article_id = a.id
    WHERE CAST(a.timestamp AS DATE) = ? AND a.category_id = ?
    """, selected_date, category_id)
    keywords = cursor.fetchall()
    conn.close()
    return Counter(keyword[0] for keyword in keywords)

def generate_wordcloud(frequencies):
    wordcloud = WordCloud(width=800, height=400, background_color='white', max_font_size=50, max_words=100).generate_from_frequencies(frequencies)
    return wordcloud

def display_wordcloud(wordcloud, date, category_name):
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    formatted_date = date.strftime('%d %B %Y')
    ax.set_title(f"Keyword Trends for {formatted_date} - Category: {category_name}")
    st.pyplot(fig)

def main():
    st.title('Keyword Trends by Date and Category')
    
    selected_date = st.sidebar.date_input("Select a date", datetime.today().date())
    
    categories = fetch_categories()
    category_names = [name for _, name in categories]
    category_ids = [id for id, _ in categories]

    selected_category_name = st.sidebar.radio("Select a category", category_names)
    selected_category_id = category_ids[category_names.index(selected_category_name)]

    frequencies = fetch_keywords_for_date_and_category(selected_date, selected_category_id)
    
    if frequencies:
        wordcloud = generate_wordcloud(frequencies)
        display_wordcloud(wordcloud, selected_date, selected_category_name)
    else:
        st.write("No keywords available for the selected date and category.")

main()