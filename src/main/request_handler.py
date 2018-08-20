import logging
import re
from multiprocessing.dummy import Pool as ThreadPool
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

PAGE_URL = 'https://www.tvtime.com/'
NUMBER_OF_SIMULTANEOUS_DOWNLOADS = 20

TV_TIME_ERROR_MESSAGES = [
    'This user does not exist',
    'You did not give the correct password for this username'
]


class RequestHandler(object):
    def __init__(self, username, password):
        self._session = self._init_session()
        self._username = username
        self._password = password
        self._profile_id = None

    def _init_session(self):
        session = requests.session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=NUMBER_OF_SIMULTANEOUS_DOWNLOADS,
                                                pool_maxsize=NUMBER_OF_SIMULTANEOUS_DOWNLOADS)
        # TODO figure out why both are needed
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def login(self):
        logging.info('Logging in to Tv Time with user "{}"'.format(self._username))

        url = urljoin(PAGE_URL, 'signin')
        credentials = {'username': self._username, 'password': self._password}
        response = self._session.post(url, data=credentials)

        self._check_response(response)
        soup = BeautifulSoup(response.content, 'html.parser')

        for link in soup.find_all('a'):
            match = re.search('^.*/user/(\d*)/profile$', link.get('href'))
            if match is not None and match.group(1) is not None:
                self._profile_id = match.group(1)

    def logout(self):
        logging.info('Logging out of Tv Time')

        url = urljoin(PAGE_URL, 'signout')
        self._session.get(url)

        self._profile_id = None

    def get_data_async(self):
        logging.info('Collecting data from Tv Time')

        ids = self._get_all_show_ids()

        with ThreadPool(processes=NUMBER_OF_SIMULTANEOUS_DOWNLOADS) as pool:
            data = pool.map(self._get_tv_show_data, ids)

        return data

    def _get_tv_show_data(self, tv_show_id):
        status = {}

        url = urljoin(PAGE_URL, ('show/{}/'.format(tv_show_id)))
        response = self._session.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        title_raw = soup.find(id='top-banner').find_all('h1')[0].text
        title = self._remove_extra_spaces(title_raw)

        logging.info('Collecting data from "{}"'.format(title))

        i = 1
        while True:
            season_status = {}

            season = soup.find(id='season{}-content'.format(i))
            if season is None:
                break

            episodes = season.find_all('li', {'class': 'episode-wrapper'})
            for episode in episodes:
                number_raw = episode.find_all('span', {'class': 'episode-nb-label'})[0].text
                number = self._remove_extra_spaces(number_raw)

                link = episode.find_all('a', {'class': 'watched-btn'})[0]
                if 'active' in link.attrs['class']:
                    season_status[number] = True
                else:
                    season_status[number] = False

            status[i] = season_status
            i += 1

        return title, status

    @staticmethod
    def _remove_extra_spaces(text):
        return ' '.join(text.split())

    @staticmethod
    def _check_response(response):
        content = str(response.content)
        for error_message in TV_TIME_ERROR_MESSAGES:
            if error_message in content:
                raise ValueError('Tv Time returned: {}'.format(error_message))

    def _get_all_show_ids(self):
        logging.info('Collecting all show ids')

        url = urljoin(PAGE_URL, ('user/{}/profile'.format(self._profile_id)))
        response = self._session.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('ul', {'class': 'shows-list'})[1].find_all('a')

        shows = set()
        for link in links:
            match = re.search('^.*/show/(\d*)', link.get('href'))
            shows.add(match.group(1))

        return shows
