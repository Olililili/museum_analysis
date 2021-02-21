CREATE_CITY_TABLE_SQL = '''CREATE TABLE city (
  city_id INTEGER PRIMARY KEY, city TEXT, country TEXT, population NUMBER);'''

CREATE_MUSEUM_TABLE_SQL = '''CREATE TABLE museum (
  id INTEGER PRIMARY KEY, name TEXT, city_id INTEGER, visitors NUMBER, 
  wiki_link TEXT, location TEXT, latitude NUMBER, longitude NUMBER, 
  collection_size TEXT, visitors_rank TEXT, director TEXT, 
  public_transit_access TEXT, website TEXT, architect TEXT, 
  established_year TEXT, is_art_museum INTEGER, is_history_museum INTEGER, 
  is_natural_museum INTEGER, is_culture_museum INTEGER, is_science_museum INTEGER,
  FOREIGN KEY(city_id) REFERENCES city(id));'''
