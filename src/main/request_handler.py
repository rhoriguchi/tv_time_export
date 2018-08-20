import logging
import re
from multiprocessing.dummy import Pool as ThreadPool
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

PAGE_URL = 'https://www.tvtime.com/'
# TODO make configurable
NUMBER_OF_SIMULTANEOUS_DOWNLOADS = 8

TV_TIME_ERROR_MESSAGES = [
    'This user does not exist',
    'You did not give the correct password for this username'
]


class RequestHandler(object):
    def __init__(self, username, password):
        self._session = requests.Session()
        self._username = username
        self._password = password
        self._profile_id = None

    def login(self):
        logging.info('Logging in to Tv Time with user %s' % self._username)

        url = urljoin(PAGE_URL, 'signin')
        data = {'username': self._username, 'password': self._password}
        response = self._session.post(url, data=data)

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

        pool = ThreadPool(processes=NUMBER_OF_SIMULTANEOUS_DOWNLOADS)
        data = pool.map(self._get_tv_show_data, ids)
        pool.join()
        pool.close()

        return data

    def _get_tv_show_data(self, tv_show_id):
        status = {}

        url = urljoin(PAGE_URL, ('show/%s/' % tv_show_id))
        response = self._session.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        title_raw = soup.find(id='top-banner').find_all('h1')[0].text
        title = self._remove_extra_spaces(title_raw)

        logging.info('Collecting data from "%s"' % title)

        i = 1
        while True:
            season_status = {}

            season = soup.find(id='season%s-content' % i)
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
                raise ValueError('Tv Time returned: %s' % error_message)

    def _get_all_show_ids(self):
        logging.info('Collecting all show ids')

        url = urljoin(PAGE_URL, ('user/%s/profile' % self._profile_id))
        response = self._session.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('ul', {'class': 'shows-list'})[1].find_all('a')

        shows = set()
        for link in links:
            match = re.search('^.*/show/(\d*)', link.get('href'))
            shows.add(match.group(1))

        return shows
