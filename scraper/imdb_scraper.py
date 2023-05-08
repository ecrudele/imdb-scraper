import requests
from bs4 import BeautifulSoup
import concurrent.futures

BASE_URL = "https://www.imdb.com"

# HTTP requests should have a header like this one as a way to avoid "403 Forbidden" responses
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

class IMDbScraper:
    def __init__(self, url: str = BASE_URL, headers: dict = DEFAULT_HEADERS):
        self.base_url = url
        self.headers = headers

    def scrape_top_movies(self, amount: int = 10) -> list:
        top_movies_url = f"{self.base_url}/chart/top"
        response = self.http_get_request(top_movies_url)
        soup = BeautifulSoup(response.text, "html.parser")
        rows = self.get_rows(amount, soup)

        # Fetch and process information from all movies concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self.process_row, rows)
        
        return list(results)

    def http_get_request(self, url: str) -> requests.Response:
        return requests.get(url, headers=self.headers)

    def get_rows(self, amount: int, soup: BeautifulSoup) -> list:
        table_body = soup.find("tbody")
        rows = table_body.find_all("tr")[:amount]
        return rows

    def process_row(self, row: BeautifulSoup) -> list:
        title_column = row.find("td", {"class": "titleColumn"})
        title = title_column.a.text
        rating = row.find("td", {"class": "ratingColumn imdbRating"}).strong.text

        movie_url = f"{self.base_url}{title_column.a['href']}"
        summary = self.get_summary(movie_url)
        
        return [title, rating, summary]

    def get_summary(self, movie_url: str):
        movie_response = self.http_get_request(movie_url)
        movie_soup = BeautifulSoup(movie_response.text, "html.parser")

        summary_pageelement = movie_soup.find("span", {"data-testid": "plot-xs_to_m"})
        summary = summary_pageelement.text.strip()
        return summary
