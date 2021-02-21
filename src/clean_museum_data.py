import math
import re
from src.log_handler import get_logger

log = get_logger()


def clean_museum_character_data(df):
    log.info('Start to clean museum character data...')
    log.info('Reducing columns which has more than 90% NaN values...')
    df = reduce_columns_with_most_nan(df)

    log.info('Cleaning Established, leave only the established year...')
    df['Established_year'] = df['Established'].apply(lambda x: clean_established(x))
    df = df.drop('Established', axis=1)

    log.info('Renaming Visitors to Visitors_rank...')
    df = df.rename({'Visitors': 'Visitors_rank'}, axis=1)

    log.info('Applying One-Hot encoding for Type...')
    one_hot_column_list = ['is_art_museum', 'is_history_museum', 'is_natural_museum',
                           'is_culture_museum', 'is_science_museum']
    df[one_hot_column_list] = df.apply(one_hot_encoding_museum_type, axis=1, result_type='expand')

    log.info('Dropping Type column...')
    df = df.drop('Type', axis=1)

    log.info('Successfully finished museum character data cleaning.')

    return df


def reduce_columns_with_most_nan(df):
    significant_columns = (df.isna().sum() / len(df)).where(lambda x: x < 0.9).dropna().keys()
    df = df[significant_columns]

    return df


def clean_established(value):
    if not type(value) == str and math.isnan(value):
        return value

    # Matches years from 1000 to 2999
    return str(re.match(r'.*([1-2][0-9]{3})', value).group(1))


def one_hot_encoding_museum_type(values):
    value = values['Type']
    if not type(value) == str and math.isnan(value):
        return 0, 0, 0, 0, 0

    is_art_museum = 1 if 'art' in value.lower() else 0
    is_history_museum = 1 if 'history' in value.lower() else 0
    is_natural_museum = 1 if 'natural' in value.lower() else 0
    is_culture_museum = 1 if 'culture' or 'archaeology' in value.lower() else 0
    is_science_museum = 1 if 'science' in value.lower() else 0

    return is_art_museum, is_history_museum, is_natural_museum, is_culture_museum, is_science_museum
