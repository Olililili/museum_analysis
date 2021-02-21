import pandas as pd
import sqlite3
from sqlite3 import Cursor
from src.log_handler import get_logger

log = get_logger()


class DatabaseOperations:
    """A class for database operations"""
    def __init__(self, database_path: str) -> None:
        """Connect to database"""
        try:
            self.conn = sqlite3.connect(database_path)
            self.cursor = self.conn.cursor()
            log.info(f'Successfully connected to {database_path}.')
        except sqlite3.Error as e:
            log.error(f'Error while connecting to db: {e}.')

    def execute(self, query: str) -> Cursor:
        """Execute sql statement"""
        try:
            self.cursor.execute(query)
            self.conn.commit()
            log.info(f'Successfully executed query: {query}')
        except sqlite3.Error as e:
            log.error(f'SQLite error while executing query: {query}, error message: {e}.')
        return self.cursor

    def df_to_db_table(self, df: pd.DataFrame(), table_name: str) -> None:
        """Convert dataframe to database table"""
        df.to_sql(table_name, self.conn, if_exists='replace', index=False)
        log.info(f'Successfully saved dataframe values to db table {table_name}.')

    def close_conn(self) -> None:
        """Destroy instance and connection"""
        self.cursor.close()
        self.conn.close()
        log.info('Successfully closed db connection.')
