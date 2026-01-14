# Keyword Analysis from Web-Scraped Data

This project was developed during my **internship** at FPT Software and focuses on **analyzing keyword trends from large-scale web-scraped news data**, inspired by the concept of **Google Trends**.

The system collects news articles from multiple Vietnamese online newspapers, extracts relevant keywords using a **Large Language Model (LLM)**, and visualizes keyword popularity over time through interactive word clouds.

The version published in this repository reflects **incremental weekly work and experimentation**, rather than a finalized production system.

---

## Project Objectives

- Scrape news articles from Vietnamese online newspapers  
- Automatically extract meaningful keywords from article content  
- Store structured data in a relational database  
- Visualize keyword trends by date and category  
- Provide an interactive interface for exploratory analysis  

---

## System Architecture

### Data Collection
- Web scraping is used to retrieve articles from various Vietnamese news websites.
- Article content is processed using an **LLM-based keyword extraction pipeline**.

### Data Storage
All extracted data is stored in a **SQL Server database** with the following schema:

- **categories**  
  Stores article categories (e.g., politics, economy, society).

- **articles**  
  Stores article metadata and content, with a reference to its category.

- **keywords**  
  Stores keywords associated with each article.

### Data Visualization

A **Streamlit web application** is used to visualize keyword trends:

- Users can select:
  - a **specific date**
  - a **news category**
- A **word cloud** is generated to display the most frequent keywords for the selected parameters.
- The visualization allows quick identification of trending topics for a given day.

---

## Repository Notes

This repository represents a **work-in-progress snapshot** of the project during the internship period.  
It primarily serves as:
- a **weekly progress record**, and
- a reference for experimentation and iterative development.

---

## Author

- Anh Tuan DINH
- Tran Minh Chau DO
