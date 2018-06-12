from lib.netflix_scraper import NetflixSession
from config.moodvies_config import GENRE_SEARCH_URLS, MONGO
from pymongo import MongoClient
import pymongo


MONGO_CONN = MONGO['conn_string']

def get_movies_collection():
    client = MongoClient(MONGO_CONN)
    db = client[MONGO_CONN.split('/')[-1]]
    if db.movies.count() > 0:
        db.movies.drop()
    return db.movies

def scrape():
    session = NetflixSession()
    movie_collection = get_movies_collection()
    movie_collection.create_index([("title", pymongo.DESCENDING)],unique=True)
    for genre, url in GENRE_SEARCH_URLS.get('movies').items():
        print(url)
        session.load_cookies_into_browser()
        session.load_streaming_movies_from_page(search_url=url)
        cleaned_movies = session.movies
        for movie in cleaned_movies:
            genres = []
            for genre in movie['genres']:
                cleaned_genre = ''.join(c.lower() for c in genre if not c.isspace())
                genres.append(cleaned_genre)
            movie['genres'] = genres
            try:
                movie_collection.insert(movie)
            except pymongo.errors.DuplicateKeyError as e:
                print(e)
        #ordered=False so it attempts all document inserts
        session.movies = []

if __name__ == '__main__':
    scrape()