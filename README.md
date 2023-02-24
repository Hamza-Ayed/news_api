# news_api
This API allows you to scrape news articles from various sources and view them. It also allows you to delete all articles at once.

## Endpoints
GET /news/
This endpoint returns a list of news articles scraped from various sources.

GET /news/goal
This endpoint allows you to add news articles related to football goals.

GET /news/dawriSaudi
This endpoint allows you to add news articles related to football in Saudi Arabia.

GET /news/youm7
This endpoint allows you to add news articles related to sports from Youm7 website.

GET /news/beinsport
This endpoint allows you to add news articles related to sports from beIN Sports website.

GET /news/360
This endpoint allows you to add news articles related to sports from Sport360 website.

POST /news/delete-all/
This endpoint allows you to delete all the news articles from the database.

GET /news/<int:pk>/
This endpoint returns details of a specific news article.

GET /wordpress/
This endpoint allows you to view the list of articles from WordPress.

## Usage
To use this API, simply make a GET or POST request to the desired endpoint. You can view the list of news articles by making a GET request to /news/. To view a specific article, make a GET request to /news/<int:pk>/. To delete all news articles, make a POST request to /news/delete-all/.

## Data
The API returns data in JSON format. The returned data includes the news title, description, author, and publication date.

## Authorization
This API does not require any authentication or authorization.

## Attribution
This API scrapes news articles from various sources. The sources include Youm7, beIN Sports, Sport360, and WordPress. The API does not claim ownership of the articles or their content.



