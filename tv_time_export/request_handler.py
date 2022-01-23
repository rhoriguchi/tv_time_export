import logging
import re
from multiprocessing.dummy import Pool as ThreadPool
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

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

    @staticmethod
    def _get_session():
        session = requests.session()
        session.headers.update({'User-agent': 'Mozilla/5.0'})
        return session

    def login(self):
        logger.info(f'Logging in to TV Time with user "{self._username}"')

        url = urljoin(PAGE_URL, 'signin')
        data = {'username': self._username, 'password': self._password}
        response = self._session.post(url, data=data)

        self._check_response(response)
        soup = BeautifulSoup(response.content, 'html.parser')

        for link in soup.find_all('a'):
            match = re.search(r'^.*/user/(\d*)/profile$', link.get('href'))

            if match is not None and match.group(1) is not None:
                self._profile_id = match.group(1)

    def logout(self):
        logger.info('Logging out of TV Time')

        url = urljoin(PAGE_URL, 'signout')
        self._session.get(url)

        self._profile_id = None

    def get_all_tv_show_states(self):
        tv_show_ids = self._get_tv_show_ids()

        with ThreadPool() as pool:
            tv_show_states = list(pool.imap(self._get_tv_show_states, tv_show_ids))

        return tv_show_states

    def _get_tv_show_states(self, tv_show_id):
        seasons = {}

        url = urljoin(PAGE_URL, f'show/{tv_show_id}/')
        response = self._session.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        title_raw = soup.find(id='top-banner') \
            .find_all('h1')[0] \
            .text
        title = self._remove_extra_spaces(title_raw)

        logger.info(f'Collecting state for "{title}"')

        season_number = 1
        while True:
            episodes = {}

            season = soup.find(id=f'season{season_number}-content')
            if season is None:
                break

            for episode in season.find_all('li', {'class': 'episode-wrapper'}):
                episode_number_raw = episode.find_all('span', {'class': 'episode-nb-label'})[0] \
                    .text
                episode_number = self._remove_extra_spaces(episode_number_raw)

                is_active = episode.find_all('a', {'class': 'watched-btn'})[0] \
                    .attrs['class']

                if 'active' in is_active:
                    episode_state = True
                else:
                    episode_state = False

                episode_title_raw = episode.find_all('span', {'class': 'episode-name'})[0] \
                    .text
                episode_title = self._remove_extra_spaces(episode_title_raw.replace('\n', ''))

                if episode_state or episode_title:
                    episodes[episode_number] = {
                        'watched': episode_state,
                        'title': episode_title
                    }

            if episodes:
                seasons[season_number] = episodes

            season_number += 1

        return {
            'id': tv_show_id,
            'title': title,
            'seasons': seasons,
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
            raise ValueError(
                f'TV Time returned status code {response.status_code} with reason: {response.reason}')

    @staticmethod
    def _check_response_content(response):
        for error_message in TV_TIME_ERROR_MESSAGES:
            if error_message in str(response.content):
                raise ValueError(f'TV Time returned: {error_message}')

    def _get_tv_show_ids(self):
        url = urljoin(PAGE_URL, f'user/{self._profile_id}/profile')
        response = self._session.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find(id='all-shows') \
            .find_all('ul', {'class': 'shows-list'})[0] \
            .find_all('a')

        tv_show_ids = set()
        for link in links:
            match = re.search(r'^.*/show/(\d*)', link.get('href'))
            tv_show_ids.add(match.group(1))

        logger.info(f'Collected {len(tv_show_ids)} show ids')

        return tv_show_ids
