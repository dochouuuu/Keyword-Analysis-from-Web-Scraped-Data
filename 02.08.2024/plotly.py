import pandas as pd
import pyodbc
from wordcloud import WordCloud
import re
import plotly.express as px
import streamlit as st
from datetime import datetime
from collections import Counter
from io import BytesIO
from PIL import Image
import base64
import icu

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

def fetch_keywords_for_date_range_and_category(start_date, end_date, category_id):
    conn = pyodbc.connect(connection)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT k.keyword, a.title, a.url
    FROM keywords k
    JOIN articles a ON k.article_id = a.id
    WHERE CAST(a.timestamp AS DATE) BETWEEN ? AND ? AND a.category_id = ?
    """, start_date, end_date, category_id)

    rows = cursor.fetchall()
    conn.close()

    keywords = []
    keyword_to_articles = {}

    for row in rows:
        keyword = re.sub(r'[^\w\s]', '', row[0]).upper().replace("_", " ")  
        title = row[1]
        url = row[2]
        
        keywords.append(keyword)

        if keyword not in keyword_to_articles:
            keyword_to_articles[keyword] = []
        
        keyword_to_articles[keyword].append((title, url))

    return keywords, keyword_to_articles

def generate_wordcloud(frequencies, font_path=None):
    try:
        wordcloud = WordCloud(
            width=1080, height=720, background_color='white', max_font_size=50, 
            font_path=font_path if font_path else None
        ).generate_from_frequencies(frequencies)
    except ValueError as e:
        print(f"Error with font_path: {e}")
        wordcloud = WordCloud(width=1080, height=720, background_color='white', max_font_size=50).generate_from_frequencies(frequencies)
    return wordcloud

def display_wordcloud(wordcloud, keyword_to_articles, selected_keyword):
    image = wordcloud.to_image()
    
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    fig = px.imshow(Image.open(BytesIO(buffer.getvalue())))
    fig.update_layout(
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    if selected_keyword:
        st.sidebar.write(f"Articles for keyword: {selected_keyword}")
        articles = keyword_to_articles.get(selected_keyword, [])
        for title, url in articles:
            st.sidebar.write(f"[{title}]({url})")

def sort_vietnamese(words):
    collator = icu.Collator.createInstance(icu.Locale('vi_VN'))
    return sorted(words, key=collator.getSortKey)

def main():
    st.title('Keyword Trends by Date and Category')

    date_range = st.sidebar.date_input("Select date range", [datetime.today().date(), datetime.today().date()])
    start_date = date_range[0]
    end_date = date_range[1] if len(date_range) > 1 else start_date  # Handle single day selection

    if end_date < start_date:
        st.write("End date must be after the start date.")
        return

    categories = fetch_categories()
    category_names = [name for _, name in categories]
    category_ids = [id for id, _ in categories]
    selected_category_name = st.sidebar.radio("Select a category", category_names)
    selected_category_id = category_ids[category_names.index(selected_category_name)]

    keywords, keyword_to_articles = fetch_keywords_for_date_range_and_category(start_date, end_date, selected_category_id)

    if keywords:
        keyword_frequencies = Counter(keywords)
        font_path = 'NotoSans-Regular.ttf'  
        wordcloud = generate_wordcloud(keyword_frequencies, font_path)

        unique_keywords = set(keyword_to_articles.keys())
        sorted_keywords = sort_vietnamese(list(unique_keywords))
        selected_keyword = st.sidebar.selectbox("Select a keyword", sorted_keywords)
        display_wordcloud(wordcloud, keyword_to_articles, selected_keyword)
    else:
        st.write("No keywords available for the selected date range and category.")

main()