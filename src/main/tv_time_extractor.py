import logging
import os

import yaml

from main import file_writer
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
        file_writer.save_tv_show_states(tv_show_states, self._content['save_path'], self._content['username'])

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
