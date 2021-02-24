import os
import pandas as pd

from src.log_handler import get_logger

log = get_logger()
WORLD_CITIES_POPULATION_FILE_PATH = '../doc/worldcities.csv'


def add_city_population_to_museum(museum_all_data_df: pd.DataFrame) -> pd.DataFrame:
    '''
    Add city, population and country to the main museum dataframe.

    :param museum_all_data_df: a dataframe which contains all main character data of the museums
    :return: museum_all_data_df: a dataframe which contains all main character, plus population and country
    '''

    world_cities_df = fetch_world_cities_df()

    log.info('Merging museum dataframe and population dataframe...')
    museum_all_data_df = pd.merge(left=museum_all_data_df, right=world_cities_df, how='left',
                                  left_on=['city'], right_on=['city'])
    log.info('Successfully added population and country to museum dataframe.')
    return museum_all_data_df


def fetch_world_cities_df() -> pd.DataFrame:
    '''
    Fetch city, coutry and population data from the world cities csv file.

    :return: df: a dataframe which contains world city, country and population data
    '''

    current_dir = os.path.dirname(__file__)
    world_cities_population_file = os.path.join(current_dir, WORLD_CITIES_POPULATION_FILE_PATH)

    try:
        log.info(f'Reading csv file for world cities population: {WORLD_CITIES_POPULATION_FILE_PATH}.')
        df = pd.read_csv(world_cities_population_file)
    except IOError as e:
        log.error(f'Error while opening csv file {WORLD_CITIES_POPULATION_FILE_PATH}: {e}.')

    df = df[['city', 'country', 'population']]

    # The file is already sorted based on population.
    # If there are duplicated city names, keep the one with the most population.
    # Given the problem does not have many cities in the museum list, this is sufficient.
    df = df.drop_duplicates('city')

    # Rename 3 city names in the city dataframe to keep it same with values in museum dataframe
    df['city'] = df['city'].replace('New York', 'New York City')
    df['city'] = df['city'].replace('Washington', 'Washington, D.C.')
    df['city'] = df['city'].replace("Xi’an", "Xi'an")

    log.info(f'Successfully read csv file {WORLD_CITIES_POPULATION_FILE_PATH} and saved the values to dataframe.')
    return df
