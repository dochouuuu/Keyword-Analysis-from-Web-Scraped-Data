CREATE DATABASE TREND; 
GO

USE TREND; 
GO

DROP TABLE if exists keywords; 
DROP TABLE if exists articles; 

CREATE TABLE articles (
    id INT PRIMARY KEY IDENTITY,
    timestamp DATETIMEOFFSET NOT NULL, 
    title NVARCHAR(255) NOT NULL,
    url NVARCHAR(255) NOT NULL
);

CREATE TABLE keywords (
    id INT PRIMARY KEY IDENTITY,
    article_id INT REFERENCES articles(id),
    keyword NVARCHAR(255) NOT NULL
);
GO
  
SELECT * FROM articles; 
SELECT * FROM keywords; 
