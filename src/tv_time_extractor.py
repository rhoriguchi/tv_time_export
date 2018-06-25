import os

import yaml

from src.request_handler import RequestHandler


class TvTimeExtractor(object):
    def get_data(self):
        content = self._read_config()
        request_handler = RequestHandler(content['username'], content['password'])

        try:
            request_handler.login()
            request_handler.get_data()
        except ValueError as e:
            print(str(e))
        finally:
            request_handler.logout()

    @staticmethod
    def _read_config():
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))
        content = None

        with open(path, 'r') as stream:
            try:
                content = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

            if content['username'] is None or content['password'] is None:
                raise ValueError('Username or password not defined in config.yaml')

            return content
