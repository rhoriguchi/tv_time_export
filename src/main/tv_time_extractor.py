import datetime
import logging
import os
import sys

import yaml

from src.main.request_handler import RequestHandler


class TvTimeExtractor(object):
    def __init__(self):
        self._content = self._read_config()
        self.__init_logger()

    def __init_logger(self):
        level = logging.INFO
        if self._content is not None \
                and 'debug' in self._content \
                and self._content['debug'] is True:
            level = logging.DEBUG

        file_handler = logging.FileHandler(filename='tv_time_export.log')
        stdout_handler = logging.StreamHandler(sys.stdout)
        handlers = [file_handler, stdout_handler]

        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=handlers
        )

    def get_data(self):
        request_handler = RequestHandler(self._content['username'], self._content['password'])

        try:
            request_handler.login()
            data = request_handler.get_data()
        finally:
            request_handler.logout()

        return data

    def save_data(self, data):
        logging.info('Saving data to %s' % self._content['save_path'])

        if not os.path.isdir(self._content['save_path']):
            raise ValueError('save_path dir does not exist')

        date_time = datetime.datetime.now().strftime('%d.%m.%Y_%H.%M.%S')
        file_name = '%s_%s.txt' % (self._content['username'], date_time)
        file_path = os.path.join(self._content['save_path'], file_name)

        f = open(file_path, "w+")

        for show in sorted(data, key=lambda show: show[0]):
            title = show[0]
            f.write('%s' % title)
            f.write('\n%s\n' % ('-' * len(title)))

            for season_number, season in show[1].items():
                for episode_number, episode in season.items():
                    if episode is True:
                        state = 'watched'
                    else:
                        state = 'unwatched'

                    f.write('\nS%02dE%02d %s' % (int(season_number), int(episode_number), state))

            f.write('\n\n\n')

        f.close()

    @staticmethod
    def _read_config():
        logging.info('Reading config.yaml')

        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))
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
