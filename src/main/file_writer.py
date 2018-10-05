import datetime
import logging
import os

from jinja2 import Environment, FileSystemLoader


def save_tv_show_states(tv_show_states, save_path, username):
    if not os.path.isdir(save_path):
        raise ValueError('save_path "{}" does not exist'.format(save_path))

    logging.info('Saving data to "{}"'.format(save_path))

    started_shows = []
    not_started_shows = []
    for show in tv_show_states:
        if _check_tv_show_started(show):
            started_shows.append(show)
        else:
            not_started_shows.append(show)

    now = datetime.datetime.now()
    file_name = '{}_{:%d.%m.%Y_%H.%M.%S}.html'.format(username, now)
    file_path = os.path.join(save_path, file_name)

    with open(file_path, 'w+', errors='ignore') as file:
        environment = Environment(
            loader=FileSystemLoader(os.path.join(os.path.abspath(__file__), '..', '..', 'resources', 'templates')),
            autoescape=True
        )

        template = environment.get_template('file_writer.html')

        render = template.render(
            date='{:%H:%M:%S %d.%m.%Y}'.format(now),
            username=username,
            started_shows=sorted(started_shows, key=lambda show: show['title']),
            not_started_shows=sorted(not_started_shows, key=lambda show: show['title'])
        )

        file.write(render)


def _check_tv_show_started(show):
    if len(show['data']) > 0:
        for season_data in show['data'].values():
            for episode_data in season_data.values():
                if episode_data['state'] is True:
                    return True
    return False
