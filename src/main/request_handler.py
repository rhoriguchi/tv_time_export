import logging
import re
from multiprocessing.dummy import Pool as ThreadPool
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from main.atomic_counter import AtomicCounter

PAGE_URL = 'https://www.tvtime.com/'

TV_TIME_ERROR_MESSAGES = [
    'This user does not exist',
    'You did not give the correct password for this username'
]

logger = logging.getLogger(__name__)


class RequestHandler(object):
    def __init__(self, username, password):
        self._session = self._get_session()
        self._username = username
        self._password = password
        self._profile_id = None
        self._counter = AtomicCounter()

    @staticmethod
    def _get_session():
        session = requests.session()
        session.headers.update({'User-agent': 'Mozilla/5.0'})
        return session

    def login(self):
        logger.info('Logging in to Tv Time with user "{}"'.format(self._username))

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
        logger.info('Logging out of Tv Time')

        url = urljoin(PAGE_URL, 'signout')
        self._session.get(url)

        self._profile_id = None

    def get_all_tv_show_states(self):
        logger.info('Collecting data from Tv Time')

        tv_show_ids = self._get_all_tv_show_ids()
        self._counter.init(len(tv_show_ids))

        with ThreadPool() as pool:
            tv_show_states = list(pool.imap(self._get_tv_show_states, tv_show_ids))

        return tv_show_states

    def _get_tv_show_states(self, tv_show_id):
        season_data = {}

        url = urljoin(PAGE_URL, ('show/{}/'.format(tv_show_id)))
        response = self._session.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        title_raw = soup.find(id='top-banner').find_all('h1')[0].text
        title = self._remove_extra_spaces(title_raw)

        logger.info('{:0=3d}-{:0=3d} < Collection state for "{}"'.format(self._counter.get_count(), self._counter.initial, title))

        episode_count = 0
        watched_episode_count = 0

        i = 1
        while True:
            episode_data = {}

            season_episode_count = 0
            season_watched_episode_count = 0

            season = soup.find(id='season{}-content'.format(i))
            if season is None:
                break

            episodes = season.find_all('li', {'class': 'episode-wrapper'})
            for episode in episodes:
                episode_count += 1
                season_episode_count += 1

                number_raw = episode.find_all('span', {'class': 'episode-nb-label'})[0].text
                number = self._remove_extra_spaces(number_raw)

                link = episode.find_all('a', {'class': 'watched-btn'})[0]
                if 'active' in link.attrs['class']:
                    episode_state = True
                    watched_episode_count += 1
                    season_watched_episode_count += 1
                else:
                    episode_state = False

                episode_title_raw = episode.find_all('span', {'class': 'episode-name'})[0].text
                episode_title = self._remove_extra_spaces(episode_title_raw.replace('\n', ''))

                if episode_state or episode_title:
                    episode_data[number] = {
                        'state': episode_state,
                        'title': episode_title
                    }

            if episode_data:
                season_data[i] = {
                    'data': episode_data,
                    'episode_count': season_episode_count,
                    'watched_episode_count': season_watched_episode_count
                }

            i += 1

        logger.info(
            '{:0=3d}-{:0=3d} < Done collecting state for "{}"'.format(self._counter.decrement(), self._counter.initial, title))

        return {
            'id': tv_show_id,
            'title': title,
            'data': season_data,
            'episode_count': episode_count,
            'watched_episode_count': watched_episode_count
        }

    @staticmethod
    def _remove_extra_spaces(text):
        return ' '.join(text.split())

    def _check_response(self, response):
        self._check_response_status_code(response)
        self._check_response_content(response)

    @staticmethod
    def _check_response_status_code(response):
        if not response.ok:
            raise ValueError('Tv Time returned status code {} with reason: {}'.format(response.status_code, response.reason))

    @staticmethod
    def _check_response_content(response):
        content = str(response.content)
        for error_message in TV_TIME_ERROR_MESSAGES:
            if error_message in content:
                raise ValueError('Tv Time returned: {}'.format(error_message))

    def _get_all_tv_show_ids(self):
        logger.info('Collecting all show ids')

        url = urljoin(PAGE_URL, ('user/{}/profile'.format(self._profile_id)))
        response = self._session.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('ul', {'class': 'shows-list'})[1].find_all('a')

        tv_show_ids = set()
        for link in links:
            match = re.search('^.*/show/(\d*)', link.get('href'))
            tv_show_ids.add(match.group(1))

        logger.info('Collected {} show ids'.format(len(tv_show_ids)))

        return tv_show_ids
