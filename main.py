from src.tv_time_extractor import TvTimeExtractor

if __name__ == '__main__':
    extractor = TvTimeExtractor()
    data = extractor.get_data()
    extractor.save_data(data)
