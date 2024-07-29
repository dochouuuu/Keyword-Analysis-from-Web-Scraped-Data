CREATE DATABASE TREND; 
GO

USE TREND; 
GO

DROP TABLE if exists keywords; 
DROP TABLE if exists articles; 
DROP TABLE if exists categories; 

CREATE TABLE categories (
    id INT PRIMARY KEY IDENTITY, 
    name VARCHAR(255) NOT NULL
);

CREATE TABLE articles (
    id INT PRIMARY KEY IDENTITY,
    category_id INT REFERENCES categories(id), 
    timestamp DATETIMEOFFSET NOT NULL, 
    title NVARCHAR(255) NOT NULL,
    url NVARCHAR(255) NOT NULL
);

CREATE TABLE keywords (
    id INT PRIMARY KEY IDENTITY,
    article_id INT REFERENCES articles(id),
    keyword NVARCHAR(255) NOT NULL
);

SELECT * FROM categories; 
SELECT * FROM articles; 
SELECT * FROM keywords; 
