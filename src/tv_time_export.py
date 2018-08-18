import logging
import sys

from src.main.tv_time_extractor import TvTimeExtractor

if __name__ == '__main__':
    try:
        extractor = TvTimeExtractor()
        data = extractor.get_data()
        extractor.save_data(data)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        logging.exception(e)
        sys.exit()
