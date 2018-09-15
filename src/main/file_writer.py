import datetime
import logging
import os


def save_tv_show_states(tv_show_states, save_path, username):
    if not os.path.isdir(save_path):
        raise ValueError('save_path \'{}\' does not exist'.format(save_path))

    logging.info('Saving data to {}'.format(save_path))

    file_name = '{}_{:%d.%m.%Y_%H.%M.%S}.txt'.format(username, datetime.datetime.now())
    file_path = os.path.join(save_path, file_name)

    with open(file_path, 'w+') as file:
        not_started_shows = []
        for show in sorted(tv_show_states, key=lambda show: show[0]):
            if _check_tv_show_started(show):
                title = show[0]
                states = show[1]

                file.write('{}'.format(title))
                file.write('\n{}\n'.format('-' * len(title)))

                for season_number, season in states.items():
                    for episode_number, state in season.items():
                        if state is True:
                            state = 'watched'
                        else:
                            state = 'unwatched'

                        file.write('\nS{:02d}E{:02d} {}'.format(int(season_number), int(episode_number), state))

                file.write('\n\n\n')
            else:
                not_started_shows.append(show)

        file.write('Not started:\n')
        for show in not_started_shows:
            file.write(' - {}\n'.format(show[0]))


def _check_tv_show_started(show):
    if len(show[1]) > 0:
        for season_number, season in show[1].items():
            for episode_number, state in season.items():
                if state is True:
                    return True
    return False
