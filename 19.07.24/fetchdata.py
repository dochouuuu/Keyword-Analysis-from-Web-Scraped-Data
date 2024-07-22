import pyodbc
import re
import pandas as pd
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

def fetch_keywords_for_date_and_category(selected_date, category_id):
    conn = pyodbc.connect(connection)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT keyword
    FROM keywords k
    JOIN articles a ON k.article_id = a.id
    WHERE CAST(a.timestamp AS DATE) = ?
    """, selected_date)

    keywords = cursor.fetchall()
    conn.close()

    return [keyword[0] for keyword in keywords]

def generate_wordcloud(keywords):
    all_keywords = " ".join(keywords)
    all_keywords_cleaned = re.sub(r'[^\w\s]', '', all_keywords).lower()

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_keywords_cleaned)
    return wordcloud

def display_wordcloud(wordcloud, date):
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.imshow(wordcloud)
    ax.axis('off')
    formatted_date = date.strftime('%d %B %Y')
    ax.set_title(f"Keyword Trends for {formatted_date}")
    st.pyplot(fig)

def main():
    st.title('Keyword Trends Day By Day')
    selected_date = st.date_input("Select a date", datetime.today().date())
    keywords = fetch_keywords_for_date(selected_date)
    
    if keywords:
        wordcloud = generate_wordcloud(keywords)
        display_wordcloud(wordcloud, selected_date)
    else:
        st.write("No keywords available for the selected date.")
main()
