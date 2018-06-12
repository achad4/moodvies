import os
from os import environ


GENRE_SEARCH_URLS = {
    'movies' : {
        'dramas': 'https://www.netflix.com/browse/genre/5763?bc=34399',
        'action' : 'https://www.netflix.com/browse/genre/1365?bc=34399',
        'comedies' : 'https://www.netflix.com/browse/genre/6548?bc=34399',
        'classics': 'https://www.netflix.com/browse/genre/31574?bc=34399',
        'cult': 'https://www.netflix.com/browse/genre/7627?bc=34399',
        'documentaries': 'https://www.netflix.com/browse/genre/2243108?bc=34399',
        'international': 'https://www.netflix.com/browse/genre/78367?bc=34399'
    }
}

MONGO = {
    'conn_string': environ.get('MONGODB_URI')
}

WEBDRIVER = {
    'docker': environ.get('Docker') is not None
}