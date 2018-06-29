import sys
import traceback

from src.tv_time_extractor import TvTimeExtractor

if __name__ == '__main__':
    try:
        extractor = TvTimeExtractor()
        data = extractor.get_data()
        extractor.save_data(data)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print('\nERROR %s' % str(e))
        traceback.print_exc()
        sys.exit()
