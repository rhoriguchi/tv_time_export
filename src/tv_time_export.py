import logging
import sys

from main.tv_time_extractor import TvTimeExtractor


def _init_logger():
    file_handler = logging.FileHandler(filename='tv_time_export.log')
    stdout_handler = logging.StreamHandler(sys.stdout)

    handlers = [file_handler, stdout_handler]

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=handlers
    )


if __name__ == '__main__':
    _init_logger()

    try:
        extractor = TvTimeExtractor()
        data = extractor.get_data()
        extractor.save_data(data)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        logging.exception(e)
        sys.exit()
