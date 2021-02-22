import pandas as pd

from src.fetch_museum_data import create_museum_dataframe
from src.clean_museum_data import clean_museum_character_data
from src.add_city_population import add_city_population_to_museum
from src.create_museum_db import build_museum_db
from src.correlate_pop_visitor import correlate_population_visitors
from src.log_handler import get_logger

log = get_logger()


def fetch_museum_data():
    '''
    Fetch all museum data from wikipedia page.

    :return: museum_all_data_df: a dataframe which contains all main character data of the museums
    '''

    museum_all_data_df = create_museum_dataframe()
    museum_all_data_df = clean_museum_character_data(museum_all_data_df)
    museum_all_data_df = add_city_population_to_museum(museum_all_data_df)
    return museum_all_data_df


def build_database(museum_all_data_df: pd.DataFrame()) -> pd.DataFrame():
    '''
    Build museum_analysis database.

    :param museum_all_data_df: a dataframe which contains all main character data of the museums
    :return: None
    '''

    build_museum_db(museum_all_data_df)


def correlate_population_and_influx_of_visitors(museum_all_data_df: pd.DataFrame()) -> pd.DataFrame():
    '''
    Correlate city population and the influx of visitors of the museums.

    :param museum_all_data_df: a dataframe which contains all main character data of the museums
    :return: None
    '''

    correlate_population_visitors(museum_all_data_df)


def main():
    '''
    Main function of museum_analysis.

    :return: None
    '''

    log.info('Start to fetch museum data...')
    museum_all_data_df = fetch_museum_data()
    log.info('Finished fetching museum data.')

    log.info('Start to build museum db...')
    build_database(museum_all_data_df)
    log.info('Finished building museum db.')

    log.info('Start to correlate city population and influx of visitors...')
    correlate_population_and_influx_of_visitors(museum_all_data_df)
    log.info('Finished correlating city population and influx of visitors.')


if __name__ == '__main__':
    main()
