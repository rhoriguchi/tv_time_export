import logging
import os
import sys

import yaml

from tv_time_export import file_writer
from tv_time_export.request_handler import RequestHandler

logger = logging.getLogger(__name__)


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
    def _get_config_path():
        argv = sys.argv

        if len(argv) >= 2:
            if os.path.isabs(argv[1]):
                return argv[1]
            else:
                return os.path.join(os.getcwd(), argv[1])
        else:
            return os.path.join(os.getcwd(), 'config.yaml')

    def _read_config(self):
        config_path = self._get_config_path()

        if not os.path.exists(config_path):
            raise ValueError(f'Config path \'{config_path}\' does not exist')

        logger.info(f'Reading {config_path}')

        with open(config_path, 'r') as stream:
            content = yaml.safe_load(stream)

            if "username" not in content or content['username'] is None:
                raise ValueError('username is empty in config.yaml')

            if "password" not in content or content['password'] is None:
                raise ValueError('password is empty in config.yaml')

            if "save_path" not in content or content['save_path'] is None:
                content['save_path'] = os.path.join(os.getcwd())
            else:
                if not os.path.exists(content['save_path']):
                    raise ValueError(f'Config path \'{content["save_path"]}\' does not exist')

            return content
