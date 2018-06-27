import sys

from src.tv_time_extractor import TvTimeExtractor

if __name__ == '__main__':
    try:
        extractor = TvTimeExtractor()
        data = extractor.get_data()
        extractor.save_data(data)
    except Exception as e:
        print('\nERROR %s' % str(e))
        sys.exit()
