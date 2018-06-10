from lib.netflix_scraper import NetflixSession
from config.moodvies_config import GENRE_SEARCH_URLS
from pymongo import MongoClient


def get_movies_collection():
    client = MongoClient('localhost', 27017)
    db = client.moodvies
    return db['movies']

def scrape():
    session = NetflixSession()
    for url in GENRE_SEARCH_URLS:
        session.load_cookies_into_browser()
        session.load_streaming_movies_from_page(search_url='https://www.netflix.com/browse/genre/34399')
        print("URL BROO\n\n\n")
        print(url)
        print(session.movies)
    movie_collection = get_movies_collection()
    movie_collection.insert(session.movies)

if __name__ == '__main__':
    scrape()