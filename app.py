import logging
import os
import pickle
import re
import sys
import json
from collections import Counter
from flask import Flask, jsonify, render_template

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


@webapp.route("/moodvies", methods=['GET'])
def load():
    images = os.listdir(os.path.join(app.static_folder, "images"))
    return render_template('index.html', images=images)

@webapp.route("/mood/<mood>", methods=['GET'])
def get_relevant_content(mood):
    return jsonify({'mood': mood})

if __name__ == '__main__':
    logging.info('loading data...')
    logging.info('running the web app...')
    webapp.run("0.0.0.0", port=DEFAULT_PORT)