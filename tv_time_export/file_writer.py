import datetime
import json
import logging
import os

logger = logging.getLogger(__name__)


def save_tv_show_states(tv_show_states, save_path, username):
    if not os.path.isdir(save_path):
        raise ValueError('save_path "{}" does not exist'.format(save_path))

    file_name = f'{username}_{datetime.datetime.now().isoformat("_", "seconds")}'
    file_path = os.path.join(save_path, file_name)

    logger.info('Saving data to "{}"'.format(file_path))

    with open(file_path, 'w+', errors='ignore') as file:
        file.write(json.dumps(tv_show_states, indent=2))
