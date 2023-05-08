import csv
from scraper.imdb_scraper import IMDbScraper

if __name__ == "__main__":
    scraper = IMDbScraper()
    top_movies = scraper.scrape_top_movies()

    with open("top_movies.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Rating", "Summary"])
        writer.writerows(top_movies)

    print("Data scraped successfully and stored in top_movies.csv")
