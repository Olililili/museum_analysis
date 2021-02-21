import bs4
import pandas as pd
import urllib
import wikipedia

from src.log_handler import get_logger

log = get_logger()
MOST_VISITED_MUSEUMS_PAGE_NAME = 'List_of_most-visited_museums'


def create_museum_dataframe():
    wiki_links = fetch_most_visited_museum_list()
    museums_df = most_visited_museum_to_dataframe(wiki_links)

    log.info('Fetching museum characters from wikipedia...')
    all_museums_detail = []
    for museum_wiki_page_name in museums_df['wiki_link']:
        museum_detail = fetch_museum_detail_dict(museum_wiki_page_name)
        all_museums_detail.append(museum_detail)
    log.info('''Finished fetching all museums' characters.''')

    museum_details_df = pd.DataFrame(all_museums_detail)

    museum_all_data_df = pd.concat([museums_df, museum_details_df], axis=1)

    return museum_all_data_df


def fetch_most_visited_museum_list():
    log.info('Fetching the most visited museum list from '
             'https://en.wikipedia.org/wiki/List_of_most_visited_museums.')
    try:
        # Get wikipedia page html source
        soup = bs4.BeautifulSoup(wikipedia.page(MOST_VISITED_MUSEUMS_PAGE_NAME).html(), 'lxml')
        log.info(f'Successfully opened wikipedia page {MOST_VISITED_MUSEUMS_PAGE_NAME}.')
    except wikipedia.exceptions.PageError as e:
        log.error(f'Error while opening wikipedia page {MOST_VISITED_MUSEUMS_PAGE_NAME}: {e}.')

    museum_wiki_pages = []
    for each_museum_info in soup.findAll('tr'):

        href = each_museum_info.find('a', href=True)['href'].title()

        if href == '#Cite_Note-13':
            continue

        if 'Redlink' in href:
            log.info(f'Redlink found in {href}, add None to the museum info.')
            museum_wiki_pages.append(None)
            continue

        museum_wiki_pages.append(urllib.parse.unquote(href).split('/Wiki/')[-1])

    log.info(f'Finished fetching all wikipedia links for all museums from {MOST_VISITED_MUSEUMS_PAGE_NAME}')

    return museum_wiki_pages


def most_visited_museum_to_dataframe(wiki_links):
    df = pd.read_html(wikipedia.page(MOST_VISITED_MUSEUMS_PAGE_NAME).html())[0]
    df.columns = ['name', 'city', 'visitors', 'year_reported']
    df = df[['name', 'city', 'visitors']]
    df['wiki_link'] = wiki_links
    return df


def fetch_museum_detail_dict(museum_wiki_page_name):
    # Return empty dict if no wiki page link is found
    if museum_wiki_page_name is None:
        return {}

    try:
        # Get wikipedia page html source
        soup = bs4.BeautifulSoup(wikipedia.page(museum_wiki_page_name).html(), 'lxml')
    except wikipedia.exceptions.PageError as e:
        log.error(f'Error while opening wikipedia page {museum_wiki_page_name}: {e}')

    # info_table is the table on the right side of the page which contains museum character info
    info_table = soup.find("table", {"class": "infobox vcard"})
    if info_table is None:
        return {}

    museum_data = {}

    # Iterating across the rows in the info_table
    for info_field in info_table.findAll('tr'):
        # If there is no 'th', means there is no data in this row
        if len(info_field.findAll('th')) == 0:
            continue

        key = info_field.find('th').text

        # For Coordinates, extract values in geo tag
        if key == 'Coordinates':
            geo = info_field.find('span', {'class': 'geo'}).text.split('; ')
            lat = geo[0]
            lon = geo[1]
            museum_data.update({'latitude': lat})
            museum_data.update({'longitude': lon})
            continue

        if info_field.find('td') is None:
            continue

        # Convert special characters
        value = info_field.find('td').text.encode('ascii', 'ignore').decode()
        museum_data.update({key: value})

    return museum_data
