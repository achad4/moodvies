from lib.netflix_scraper import NetflixSession
from config.moodvies_config import GENRE_SEARCH_URLS, MONGO
from pymongo import MongoClient


MONGO_CONN = MONGO['conn_string']

def get_movies_collection():
    client = MongoClient(MONGO_CONN)
    db = client.moodvies
    if db.movies.count() > 0:
        db.movies.drop()
    return db.movies

def scrape():
    session = NetflixSession()
    for url in GENRE_SEARCH_URLS:
        session.load_cookies_into_browser()
        session.load_streaming_movies_from_page(search_url='https://www.netflix.com/browse/genre/34399')
    movie_collection = get_movies_collection()
    cleaned_movies = session.movies
    for movie in cleaned_movies:
        genres = []
        for genre in movie['genres']:
            cleaned_genre = ''.join(c.lower() for c in genre if not c.isspace())
            genres.append(cleaned_genre)
        movie['genres'] = genres
    movie_collection.insert(session.movies)

if __name__ == '__main__':
    scrape()