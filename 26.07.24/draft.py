import pyodbc
import re
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime
from collections import Counter
import json

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
    SELECT k.keyword, a.title, a.url
    FROM keywords k
    JOIN articles a ON k.article_id = a.id
    WHERE CAST(a.timestamp AS DATE) = ? AND a.category_id = ?
    """, selected_date, category_id)

    rows = cursor.fetchall()
    conn.close()

    keywords = []
    keyword_to_articles = {}

    for row in rows:
        keyword = row[0]
        title = row[1]
        url = row[2]
        
        keywords.append(keyword)

        if keyword not in keyword_to_articles:
            keyword_to_articles[keyword] = []
        
        keyword_to_articles[keyword].append((title, url))

    return keywords, keyword_to_articles

def generate_wordcloud(frequencies):
    wordcloud = WordCloud(width=800, height=400, background_color='white', max_font_size=50).generate_from_frequencies(frequencies)
    return wordcloud

def display_wordcloud_html(wordcloud_data):
    wordcloud_js = """
    <script src="https://cdn.rawgit.com/timdream/wordcloud2.js/master/src/wordcloud2.js"></script>
    <div id="wordcloud" style="width: 100%%; height: 400px;"></div>
    <script>
        console.log("Debug: JavaScript is running");
        var wordcloudData = %s;
        console.log("Debug: Wordcloud Data: ", wordcloudData);
        WordCloud(document.getElementById('wordcloud'), { list: wordcloudData });
    </script>
    """
    html_code = wordcloud_js % json.dumps(wordcloud_data)
    st.components.v1.html(html_code, height=400)

def main():
    st.title('Keyword Trends by Date and Category')
    
    selected_date = st.sidebar.date_input("Select a date", datetime.today().date())

    categories = fetch_categories()
    category_names = [name for _, name in categories]
    category_ids = [id for id, _ in categories]

    selected_category_name = st.sidebar.radio("Select a category", category_names)
    selected_category_id = category_ids[category_names.index(selected_category_name)]

    keywords, keyword_to_articles = fetch_keywords_for_date_and_category(selected_date, selected_category_id)

    if keywords:
        keyword_frequencies = Counter(keywords)
        wordcloud_data = [[word, freq] for word, freq in keyword_frequencies.items()]
        
        selected_keyword = st.sidebar.selectbox("Select a keyword", list(keyword_to_articles.keys()))
        display_wordcloud_html(wordcloud_data)
    else:
        st.write("No keywords available for the selected date and category.")

if __name__ == "__main__":
    main()
