import pandas as pd

from src.db_operations import DatabaseOperations
from src.log_handler import get_logger
from src.queries import CREATE_CITY_TABLE_SQL
from src.queries import CREATE_MUSEUM_TABLE_SQL

log = get_logger()
DATABASE_PATH = 'museum_analysis.db'
CITY_TABLE_NAME = 'city'
MUSEUM_TABLE_NAME = 'museum'


def build_museum_db(museum_all_data_df):
    log.info('Preparing dataframes for creating db tables...')
    city_df_for_sql, museum_df_for_sql = prepare_df_for_db_creat(museum_all_data_df)
    log.info('Successfully created dataframes for city and museum tables.')

    log.info('Creating museum_analysis db...')
    create_db(city_df_for_sql, museum_df_for_sql)
    log.info('Successfully created museum_analysis db and closed db connection.')


def prepare_df_for_db_creat(museum_all_data_df):
    city_df_for_sql = museum_all_data_df[['city', 'country', 'population']].drop_duplicates('city')
    city_df_for_sql['city_id'] = range(1, len(city_df_for_sql) + 1)

    # Merge the two dataframes in order to have city_id in museum_all_data_df.
    # Based on the assignment requirement, we are trying to create a small database.
    # If in future we need to enlarge the scale of this database,
    # we do not need to merge the dataframe and can just save all cities to the city table
    merged_museum_city_for_sql = pd.merge(left=museum_all_data_df, right=city_df_for_sql,
                                          how='left', left_on=['city', 'country', 'population'],
                                          right_on=['city', 'country', 'population'], sort=False)

    museum_df_for_sql = merged_museum_city_for_sql[['name', 'city_id', 'visitors', 'wiki_link',
                                                    'Location', 'latitude', 'longitude',
                                                    'Collection size', 'Visitors_rank',
                                                    'Director', 'Public transit access',
                                                    'Website', 'Architect',
                                                    'Established_year', 'is_art_museum',
                                                    'is_history_museum', 'is_natural_museum',
                                                    'is_culture_museum', 'is_science_museum']]

    museum_df_for_sql = museum_df_for_sql.rename(columns={'Location': 'location', 'Collection size': 'collection_size',
                                                          'Visitors_rank': 'visitors_rank', 'Director': 'director',
                                                          'Public transit access': 'public_transit_access',
                                                          'Website': 'website', 'Architect': 'architect',
                                                          'Established_year': 'established_year'})

    museum_df_for_sql['id'] = range(1, len(museum_df_for_sql) + 1)

    return city_df_for_sql, museum_df_for_sql


def create_db(city_df_for_sql, museum_df_for_sql):
    db = DatabaseOperations(DATABASE_PATH)

    db.execute(CREATE_CITY_TABLE_SQL)
    db.execute(CREATE_MUSEUM_TABLE_SQL)

    db.df_to_db_table(city_df_for_sql, CITY_TABLE_NAME)
    db.df_to_db_table(museum_df_for_sql, MUSEUM_TABLE_NAME)

    db.close_conn()
