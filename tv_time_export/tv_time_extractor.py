import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import yaml

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
        save_path = Path(self._content['save_path'])
        username = self._content['username']

        if not save_path.is_dir():
            raise ValueError(f'save_path "{save_path}" does not exist')

        datetime_string = datetime.now().isoformat('T', 'seconds') \
            .replace('-', '') \
            .replace(':', '')
        file_name = f'{username}_{datetime_string}.json'

        file_path = save_path.joinpath(file_name)

        logger.info(f'Saving data to "{file_path}"')

        with open(file_path, 'w+') as file:
            file.write(json.dumps(tv_show_states, separators=(',', ':')))

    @staticmethod
    def _get_config_path():
        argv = sys.argv

        if len(argv) >= 2:
            config_path = Path(argv[1])

            if config_path.is_absolute():
                return config_path
            else:
                return Path.cwd().joinpath(config_path)
        else:
            return Path.cwd().joinpath('config.yaml')

    def _read_config(self):
        config_path = self._get_config_path()

        if not config_path.exists():
            raise ValueError(f'Config path "{config_path}" does not exist')

        logger.info(f'Reading "{config_path}"')

        with open(config_path, 'r') as stream:
            content = yaml.safe_load(stream)

            if 'username' not in content or content['username'] is None:
                raise ValueError('username is empty in config.yaml')

            if 'password' not in content or content['password'] is None:
                raise ValueError('password is empty in config.yaml')

            if 'save_path' not in content or content['save_path'] is None:
                content['save_path'] = Path.cwd()

            content['save_path'] = Path(content['save_path'])

            if not content['save_path'].exists():
                raise ValueError(f'Config path "{content["save_path"]}" does not exist')

            log_content = dict(content)
            log_content['password'] = '*' * len(log_content['password'])
            log_content['save_path'] = str(log_content['save_path'])

            logger.info(f'Config values: {log_content}')

            return content
