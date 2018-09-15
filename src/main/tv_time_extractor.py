import datetime
import logging
import os

import yaml

from main.request_handler import RequestHandler


class TvTimeExtractor(object):
    def __init__(self):
        self._content = self._read_config()

    def get_all_tv_show_states(self):
        request_handler = RequestHandler(self._content['username'], self._content['password'])

        try:
            request_handler.login()
            tv_show_states = request_handler.get_all_tv_show_states()
        finally:
            request_handler.logout()

        return tv_show_states

    def save_tv_show_states(self, tv_show_states):
        if not os.path.isdir(self._content['save_path']):
            raise ValueError('save_path dir does not exist')

        logging.info('Saving data to {}'.format(self._content['save_path']))

        file_name = '{}_{:%d.%m.%Y_%H.%M.%S}.txt'.format(self._content['username'], datetime.datetime.now())
        file_path = os.path.join(self._content['save_path'], file_name)

        with open(file_path, 'w+') as file:
            not_started_shows = []
            for show in sorted(tv_show_states, key=lambda show: show[0]):
                if self._check_tv_show_started(show):
                    title = show[0]
                    states = show[1]

                    file.write('{}'.format(title))
                    file.write('\n{}\n'.format('-' * len(title)))

                    for season_number, season in states.items():
                        for episode_number, state in season.items():
                            if state is True:
                                state = 'watched'
                            else:
                                state = 'unwatched'

                            file.write('\nS{:02d}E{:02d} {}'.format(int(season_number), int(episode_number), state))

                    file.write('\n\n\n')
                else:
                    not_started_shows.append(show)

            file.write('Not started:\n')
            for show in not_started_shows:
                file.write(' - {}\n'.format(show[0]))

    @staticmethod
    def _check_tv_show_started(show):
        if len(show[1]) > 0:
            for season_number, season in show[1].items():
                for episode_number, state in season.items():
                    if state is True:
                        return True
        return False

    @staticmethod
    def _read_config():
        logging.info('Reading config.yaml')

        path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.yaml'))
        if not os.path.exists(path):
            raise ValueError('config.yaml does not exist')

        with open(path, 'r') as stream:
            content = yaml.safe_load(stream)

            if content['username'] is None:
                raise ValueError('username is empty in config.yaml')

            if content['password'] is None:
                raise ValueError('password is empty in config.yaml')

            if content['save_path'] is None:
                raise ValueError('save_path is empty in config.yaml')

            return content
