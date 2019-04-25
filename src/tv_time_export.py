import logging
import os
import sys

from main.tv_time_extractor import TvTimeExtractor


def _init_logger():
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tv_time_export.log')
    file_handler = logging.FileHandler(filename=log_path)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter('%(message)s'))

    logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])


if __name__ == '__main__':
    _init_logger()

    try:
        extractor = TvTimeExtractor()
        tv_show_states = extractor.get_all_tv_show_states()
        extractor.save_tv_show_states(tv_show_states)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as ex:
        logging.exception(ex)
        sys.exit()
