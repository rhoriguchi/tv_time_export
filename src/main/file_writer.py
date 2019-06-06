import datetime
import logging
import os

import htmlmin
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)


def save_tv_show_states(tv_show_states, save_path, username):
    if not os.path.isdir(save_path):
        raise ValueError('save_path "{}" does not exist'.format(save_path))

    now = datetime.datetime.now()
    file_name = '{}_{:%d.%m.%Y_%H.%M.%S}.html'.format(username, now)
    file_path = os.path.join(save_path, file_name)

    logger.info('Saving data to "{}"'.format(file_path))

    with open(file_path, 'w+', errors='ignore') as file:
        environment = Environment(
            loader=FileSystemLoader(os.path.abspath(os.path.join(__file__, '..', '..', 'resources', 'templates'))),
            autoescape=True
        )

        template = environment.get_template('export.html')

        render = template.render(
            date='{:%H:%M:%S %d.%m.%Y}'.format(now),
            username=username,
            tv_show_states=sorted(tv_show_states, key=lambda show: show['title']),
        )

        render_min = htmlmin.minify(render, remove_comments=True, remove_empty_space=True)

        file.write(render_min)
