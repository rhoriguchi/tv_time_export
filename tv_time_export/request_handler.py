from multiprocessing.dummy import Pool as ThreadPool

import jwt
import logging
import requests
from retrying import retry

URL = 'https://app.tvtime.com/sidecar'

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
        return session

    def login(self):
        logger.info(f'Logging in to TV Time with user "{self._username}"')

        anonymous_tokens = self._session.post(
            URL,
            params={'o': 'https://api2.tozelabs.com/v2/user'}
        ).json()['tvst_access_token']

        response = self._session.post(
            URL,
            params={'o': 'https://auth.tvtime.com/v1/login'},
            headers={'Authorization': f'Bearer {anonymous_tokens}'},
            json={'username': self._username, 'password': self._password}
        )

        if not response.ok:
            raise ValueError(
                f'TV Time returned status code {response.status_code} with reason: {response.reason}')

        token = response.json()['data']['jwt_token']

        self._session.headers.update({'Authorization': f'Bearer {token}'})

        self._profile_id = jwt.decode(token, options={"verify_signature": False})['id']

    def get_all_tv_show_states(self):
        tv_show_ids = self._get_tv_show_ids()

        with ThreadPool() as pool:
            tv_show_states = list(pool.imap(self._get_tv_show_states, tv_show_ids))

        return sorted(tv_show_states, key=lambda state: state['title'])

    @retry(stop_max_attempt_number=3, wait_fixed=30 * 1_000)
    def _get_tv_show_states(self, tv_show_id):
        response = self._session.get(
            URL,
            params={'o': f'https://api2.tozelabs.com/v2/show/{tv_show_id}/extended'}
        )

        tv_show = response.json()
        title = tv_show["name"]

        logger.info(f'Collecting state for "{title}"')

        seasons = {}

        for season in tv_show['seasons']:
            episodes = {}

            for episode in season['episodes']:
                episodes[episode['number']] = {
                    'id': episode['id'],
                    'title': episode['name'],
                    'watched': episode['is_watched']
                }

            if episodes:
                seasons[season['number']] = episodes

        return {
            'id': tv_show_id,
            'title': title,
            'first_air_date': tv_show['first_air_date'],
            'seasons': seasons
        }

    @retry(stop_max_attempt_number=3, wait_fixed=30 * 1_000)
    def _get_tv_show_ids(self):
        limit = 500
        offset = 0

        tv_show_ids = []

        while True:
            response = self._session.get(
                URL,
                params={
                    'o': f'https://api2.tozelabs.com/v2/user/{self._profile_id}',
                    'fields': f'shows.fields(id).offset({offset}).limit({limit})'
                }
            )

            shows = response.json()['shows']

            for show in shows:
                tv_show_ids.append(show['id'])

            if len(shows) != limit:
                break

            offset = offset + limit

        return sorted(tv_show_ids)
