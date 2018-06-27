import os

import yaml

from src.request_handler import RequestHandler


class TvTimeExtractor(object):
    def get_data(self):
        data = None

        content = self._read_config()
        request_handler = RequestHandler(content['username'], content['password'])

        try:
            request_handler.login()
            data = request_handler.get_data()
        except ValueError as e:
            print(str(e))
        finally:
            request_handler.logout()

        return data

    @staticmethod
    def save_data(data):
        print("")

    @staticmethod
    def _read_config():
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))
        content = None

        with open(path, 'r') as stream:
            try:
                content = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

            if content['username'] is None or \
                    content['password'] is None or \
                    content['save_path'] is None:
                raise ValueError('config.yaml not correct')

            return content
