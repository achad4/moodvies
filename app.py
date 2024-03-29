import logging
import os
import pickle
import re
import sys
import json
from collections import Counter
from flask import Flask, jsonify, render_template
from pymongo import MongoClient
from config.moodvies_config import MONGO

FORMAT = '%(asctime)s  %(levelname)s    %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT, stream=sys.stdout)
  
webapp = Flask(
    __name__,
    static_url_path='/moodvies/static',
    static_folder='./static',
    template_folder='./templates'
)
webapp.config["DEBUG"] = True
 
DEFAULT_PORT = 8080
app = Flask(__name__)
MONGO_CONN = MONGO['conn_string']

with open('config/moods.json') as f:
    MOODS = json.load(f)

def get_movies_collection():
    client = MongoClient(MONGO_CONN)
    db = client[MONGO_CONN.split('/')[-1]]
    return db.movies

@webapp.route("/", methods=['GET'])
def load():
    images = os.listdir(os.path.join(app.static_folder, "images"))
    return render_template('index.html', images=images)

@webapp.route("/mood/<mood>", methods=['GET'])
def get_relevant_content(mood):
    movie_collection = get_movies_collection()
    filename, file_extension = os.path.splitext(mood)
    cursor = movie_collection.find({"genres": {"$in": MOODS[filename]}}, {"title": 1, "genres": 1, "sysnopsis": 1, "watch_url": 1, "_id": 0})    
    results = list(cursor)
    logging.info(results)
    return render_template('movie_results.html', results=results)

if __name__ == '__main__':
    logging.info('loading data...')
    logging.info('running the web app...')
    port = int(os.environ.get('PORT', 5000))
    webapp.run(host='0.0.0.0', port=port, debug=True)
    # webapp.run(debug=True, use_reloader=True)
    # webapp.run("0.0.0.0", port=DEFAULT_PORT)