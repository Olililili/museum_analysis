from src.fetch_museum_data import create_museum_dataframe
from src.clean_museum_data import clean_museum_character_data
from src.add_city_population import add_city_population_to_museum
from src.create_museum_db import build_museum_db
from src.correlate_pop_visitor import correlate_population_visitors
from src.log_handler import get_logger

log = get_logger()


def main():
    log.info('Start to fetch museum data...')
    museum_all_data_df = fetch_museum_data()
    log.info('Finished fetching museum data.')

    log.info('Start to build museum db...')
    build_database(museum_all_data_df)
    log.info('Finished building museum db.')

    log.info('Start to correlate city population and influx of visitors...')
    correlate_population_and_influx_of_visitors(museum_all_data_df)
    log.info('Finished correlating city population and influx of visitors.')


def fetch_museum_data():
    museum_all_data_df = create_museum_dataframe()
    museum_all_data_df = clean_museum_character_data(museum_all_data_df)
    museum_all_data_df = add_city_population_to_museum(museum_all_data_df)

    return museum_all_data_df


def build_database(museum_all_data_df):
    build_museum_db(museum_all_data_df)


def correlate_population_and_influx_of_visitors(museum_all_data_df):
    correlate_population_visitors(museum_all_data_df)


if __name__ == '__main__':
    main()
