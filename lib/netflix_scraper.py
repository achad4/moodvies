"""This module contains the NetflixSession class."""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from time import sleep
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from fuzzywuzzy import fuzz
import re
import pickle
import logging
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class NetflixSession:
    """This is a class capable of scraping DVD Netflix pages."""

    # Configure logfile for debugging
    logging.basicConfig(filename='session.log',
                        filemode='w', level=logging.INFO)
    logging.info('Opening log file')

    def __init__(self, cookies_file='./cookie.pkl'):
        """
        Create instance of class for scraping movie.  Tries to load a
            set of cookies with this instance, which are required to view
            unavailable movies/shows, and are needed to get ratings.

        cookies_file: string of path to pickle file containing cookies
                        (if cookies aren't loaded, script will continue
                        without them)
        """
        self.movies = []
        self.driver = None
        try:
            with open('config/cookies.json') as f:
                self.cookies = json.load(f)
            # self.cookies = pickle.load(open(cookies_file, "rb"))
            logging.info('Cookies loaded from ' + cookies_file)
        except IOError:
            self.cookies = None
            logging.info('No cookies were loaded on init')
 
    def load_cookies_into_browser(self):
        logging.info('Starting chrome driver')
        options = ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=options)
        # self.driver = webdriver.Remote(command_executor='http://hub:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
        if self.cookies:
            self.driver.get('https://www.netflix.com/NotFound?prev=http%3A%2F%2Fwww.netflix.com%2F404')
            for i in range(len(self.cookies)):
                self.driver.add_cookie(self.cookies[i])

    def load_streaming_movies_from_page(self, search_url='https://www.netflix.com/browse'):
        self.driver.get(search_url)
        html = self.driver.page_source
        delay = 5
        try:
            WebDriverWait(self.driver, delay).until(
                EC.presence_of_element_located((By.ID, 'appMountPoint')))
        except TimeoutException:
            logging.error("Search results did not load.")
            self.driver.quit()
            raise Exception('Search results did not load.')

        results_page = BeautifulSoup(html, "html.parser")
        available_movies = results_page.find_all(attrs={"class": "slider-refocus"})
        logging.info('search url: ' + search_url)
        for result in available_movies:
            title = result.find(attrs={"class": "fallback-text"}).string
            if title in self.movies:
                continue
            try:
                title_element = self.driver.find_element_by_partial_link_text(title)
                ActionChains(self.driver).move_to_element(title_element).click().perform()
                WebDriverWait(self.driver, delay).until(EC.element_to_be_clickable((By.CLASS_NAME, 'meta-lists')))
                html = self.driver.page_source
                results_page = BeautifulSoup(html, "html.parser")
                links = results_page.find_all('a', href=True)
                genres = [link.text for link in links if 'genre' in link.attrs['href']]
                synopsis = results_page.find_all(attrs={"class": "synopsis"})[0]
                watch_url = [link.attrs['href'] for link in links if 'aria-label' in link.attrs and link.attrs['aria-label'] == 'Play'][0]
                logging.debug(genres)
                movie = {}
                movie['title'] = title
                movie['genres'] = genres
                movie['watch_url'] = watch_url
                movie['synopsis'] = synopsis.text
                self.movies.append(movie)
            except Exception as e:
                logging.error(title)
                logging.error(e)
                continue