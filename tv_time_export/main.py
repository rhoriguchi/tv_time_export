import logging
import sys

from tv_time_export.tv_time_extractor import TvTimeExtractor


def main():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    logging.basicConfig(level=logging.INFO, handlers=[console_handler])

    try:
        extractor = TvTimeExtractor()
        tv_show_states = extractor.get_all_tv_show_states()
        extractor.save_tv_show_states(tv_show_states)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as ex:
        logging.exception(ex)
        sys.exit()


if __name__ == '__main__':
    main()
