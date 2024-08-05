import pandas as pd
import pyodbc
from sqlalchemy import create_engine, types
import urllib
import re
from datetime import datetime

server = 'localhost'
database = 'TREND'
username = 'sa'
password = 'Joochou259@'

connection_string = f"DRIVER=/opt/homebrew/lib/libmsodbcsql.17.dylib;SERVER={server};DATABASE={database};UID={username};PWD={password}"
params = urllib.parse.quote_plus(connection_string)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

def insert_categories(file_path): 
    try: 
        df = pd.read_csv(file_path)
        df['name'].to_sql('categories', con=engine, if_exists='append', index=False)
        print("Categories inserted successfully!")
    except Exception as e:
        print(f"Error inserting categories: {e}")

def parse_timestamp(timestamp_str):
    try:
        #timestamp_str = timestamp_str.replace('GMT+7', '').strip()
        return datetime.strptime(timestamp_str, '%d-%m-%Y')
    except ValueError as e:
        print(f"Timestamp parsing error: {e}")
        return None

def insert_articles(file_path, dtypes1):
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip() 
        df['timestamp'] = df['timestamp'].apply(parse_timestamp)
        df.drop(columns=['id'], inplace=True)
        df[['category_id', 'timestamp', 'title', 'url']].to_sql('articles', con=engine, if_exists='append', index=False, dtype=dtypes1)
        print("Articles inserted successfully!")
    except Exception as e:
        print(f"Error inserting articles: {e}")

# def insert_articles(file_path, dtypes1):
#     try:
#         df = pd.read_csv(file_path)
#         df['timestamp'] = df['timestamp'].apply(parse_timestamp)
        
#         print("DataFrame before insertion:")
#         print(df)
        
#         df[['category_id', 'timestamp', 'title', 'url']].to_sql('articles', con=engine, if_exists='append', index=False, dtype=dtypes1)
        
#         inserted_articles = pd.read_sql("SELECT * FROM articles", con=engine)
#         print("Inserted articles:")
#         print(inserted_articles)
        
#         print("Articles inserted successfully!")
#     except Exception as e:
#         print(f"Error inserting articles: {e}")

def parse_keywords(keywords_str):
    if keywords_str.startswith('"""""""[') and keywords_str.endswith(']"""""""'):
        keywords_str = keywords_str[8:-8]

    keywords_str = keywords_str.strip('[]"')
    keywords = re.split(r',\s*(?![^\'"]*[\'"][^\'"]*$)', keywords_str)

    keywords = [kw.strip().strip("'\"").replace("_", " ") for kw in keywords]
    return keywords

def insert_keywords(file_path, dtypes2):
    try:
        df = pd.read_csv(file_path)
        
        if 'keywords tuple' not in df.columns:
            print("Error: 'keywords tuple' column missing in data")
            return

        existing_article_ids = pd.read_sql("SELECT id FROM articles", con=engine)['id'].tolist()

        for i, row in df.iterrows():
            article_id = row['article_id']

            if article_id not in existing_article_ids:
                print(f"Warning: article_id {article_id} does not exist in the articles table. Skipping.")
                continue

            keywords = parse_keywords(row['keywords tuple'])
            keyword_data = [{'article_id': article_id, 'keyword': k} for k in keywords]
            df_keywords = pd.DataFrame(keyword_data)
            df_keywords.to_sql('keywords', con=engine, if_exists='append', index=False, dtype=dtypes2)

        print("Keywords inserted successfully!")
    except Exception as e:
        print(f"Error inserting keywords: {e}")

categories_csv = 'categories.txt'

articles1_csv = 'finalres_pt1_old.csv'
articles2_csv = 'finalres_pt1.csv'
articles3_csv = 'finalres_pt1_new.csv'
dtypes1 = {
    'timestamp': types.DateTime(),
    'title': types.NVARCHAR(length=255),
    'url': types.NVARCHAR(length=255),
}

keywords1_csv = 'finalres_pt2_old.csv'
keywords2_csv = 'finalres_pt2.csv'
keywords3_csv = 'finalres_pt2_new.csv'
dtypes2 = {
    'article_id' : types.INTEGER(),
    'keyword' : types.NVARCHAR(length=255),
}

insert_categories(categories_csv)
insert_articles(articles1_csv,dtypes1)
insert_articles(articles2_csv,dtypes1)
insert_articles(articles3_csv,dtypes1)
insert_keywords(keywords1_csv, dtypes2)
insert_keywords(keywords2_csv, dtypes2)
insert_keywords(keywords3_csv, dtypes2)