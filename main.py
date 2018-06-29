import logging
import sys

from src.tv_time_extractor import TvTimeExtractor

if __name__ == '__main__':
    logging.basicConfig(filename='tv_time_export.log',
                        format='%(asctime)s %(levelname)s %(message)s',
                        level=logging.INFO)

    try:
        extractor = TvTimeExtractor()
        data = extractor.get_data()
        extractor.save_data(data)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        logging.exception(e)
        sys.exit()
