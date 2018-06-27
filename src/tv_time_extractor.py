import datetime
import os

import yaml

from src.request_handler import RequestHandler


class TvTimeExtractor(object):
    def get_data(self):
        content = self._read_config()
        request_handler = RequestHandler(content['username'], content['password'])

        try:
            request_handler.login()
            data = request_handler.get_data()
        finally:
            request_handler.logout()

        return data

    def save_data(self, data):
        print('INFO Saving data')

        content = self._read_config()
        file_path = os.path.join(content['save_path'], 'tv_time_backup.txt')

        f = open(file_path, "w+")
        f.write('%s' % datetime.datetime.now().date())

        for show in sorted(data, key=lambda show: show[0]):
            title = show[0]
            f.write('\n\n\n%s' % title)
            f.write('\n%s\n' % ('-' * len(title)))

            for season_number, season in show[1].items():
                for episode_number, episode in season.items():
                    if episode is True:
                        state = 'watched'
                    else:
                        state = 'unwatched'

                    f.write('\nS%02dE%02d %s' % (int(season_number), int(episode_number), state))

        f.close()

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
