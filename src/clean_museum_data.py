import math
import pandas as pd
import re

from src.onehot_enum import YesOrNo;
from typing import Tuple, Union
from src.log_handler import get_logger

log = get_logger()


def clean_museum_character_data(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Clean museum characters and only leave main characters for analysis.

    :param df: a dataframe which contains all museums character data
    :return: df: a dataframe which contains all main character data of the museums
    '''

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


def reduce_columns_with_most_nan(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Reduce columns in the dataframe which contains more than 90% of NaN value

    :param df: a dataframe which contains all museums character data
    :return: df: a dataframe which contains all main character data of the museums
    '''

    significant_columns = (df.isna().sum() / len(df)).where(lambda x: x < 0.9).dropna().keys()
    df = df[significant_columns]
    return df


def clean_established(value: Union[int, str]) -> str:
    '''
    Clean values in Established column, only keep the value as a year in between of 1000 to 2999.

    :param value: an Integer or a String value from the Established column
    :return: A String of the value as a year
    '''

    if not type(value) == str and math.isnan(value):
        return value

    # Matches years from 1000 to 2999
    return str(re.match(r'.*([1-2][0-9]{3})', value).group(1))


def one_hot_encoding_museum_type(values: pd.DataFrame) -> Tuple[int, int, int, int, int]:
    '''
    Apply one hot encoding for Type column, separate the Type column to 5 different columns:
    is_art_museum, is_history_museum, is_natural_museum, is_culture_museum, is_science_museum

    :param values: a dataframe which contains the series of Type column
    :return:
        is_art_museum: whether the museum is an art museum
        is_history_museum: whether the museum is a history museum
        is_natural_museum: whether the museum is a natural museum
        is_culture_museum: whether the museum is a culture museum
        is_science_museum: whether the museum is a science museum
    '''

    value = values['Type']
    if not type(value) == str and math.isnan(value):
        return YesOrNo.No.value, YesOrNo.No.value, YesOrNo.No.value, YesOrNo.No.value, YesOrNo.No.value

    is_art_museum = YesOrNo.Yes if 'art' in value.lower() else YesOrNo.No
    is_history_museum = YesOrNo.Yes if 'history' in value.lower() else YesOrNo.No
    is_natural_museum = YesOrNo.Yes if 'natural' in value.lower() else YesOrNo.No
    is_culture_museum = YesOrNo.Yes if 'culture' or 'archaeology' in value.lower() else YesOrNo.No
    is_science_museum = YesOrNo.Yes if 'science' in value.lower() else YesOrNo.No
    return is_art_museum.value, is_history_museum.value, is_natural_museum.value \
        , is_culture_museum.value, is_science_museum.value
