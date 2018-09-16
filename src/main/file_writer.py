import datetime
import logging
import os

from jinja2 import Environment, PackageLoader, FileSystemLoader


def save_tv_show_states(tv_show_states, save_path, username):
    if not os.path.isdir(save_path):
        raise ValueError('save_path \'{}\' does not exist'.format(save_path))

    logging.info('Saving data to {}'.format(save_path))

    started_shows = []
    not_started_shows = []
    for show in tv_show_states:
        if _check_tv_show_started(show):
            started_shows.append(show)
        else:
            not_started_shows.append(show)

    date = '{:%d.%m.%Y_%H.%M.%S}'.format(datetime.datetime.now())
    file_name = '{}_{}.html'.format(username, date)
    file_path = os.path.join(save_path, file_name)

    with open(file_path, 'w+') as file:
        environment = Environment(
            loader=FileSystemLoader(os.path.join(os.path.abspath(__file__), '..', 'resources', 'templates')),
        )

        template = environment.get_template('file_writer.html')

        render = template.render(
            date=date,
            username=username,
            shows=sorted(tv_show_states, key=lambda show: show['title']),
            started_shows=sorted(started_shows, key=lambda show: show['title']),
            not_started_shows=sorted(not_started_shows, key=lambda show: show['title'])
        )

        file.write(render)


def _check_tv_show_started(show):
    if len(show['states']) > 0:
        for season_number, season in show['states'].items():
            for episode_number, state in season.items():
                if state is True:
                    return True
    return False
