# Keyword Trends Visualization

This project fetches articles and keywords from a SQL Server database and visualizes keyword trends using a word cloud. Users can select a date and a category to generate the word cloud for keywords from articles on that date and category.

## Project Description

This project scrapes websites to retrieve articles and their associated keywords. The data is stored in a SQL Server database with the following schema:

- `categories` table to store categories of articles.
- `articles` table to store articles with a reference to their categories.
- `keywords` table to store keywords associated with each article.

A Streamlit app allows users to visualize keyword trends by generating word clouds. Users can select a specific date and category to view the trends.
