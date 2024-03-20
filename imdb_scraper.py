import os
import requests
import json
import logging
import re

logging.basicConfig(filename='scraper.log', level=logging.INFO)


def retrieve_movie_data(url, regexPattern):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Referer': 'https://www.imdb.com/?ref_=vp_close',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
    }
    response = requests.get(url, headers=headers)
    data = response.text
    json_data_list = re.findall(regexPattern, data)
    json_obj = json.loads(json_data_list[0])
    return json_obj


def search_imdb_graphql(cursor, search_query):
    url = "https://caching.graphql.imdb.com/"
    params = {
        "operationName": "FindPageSearch",
        "variables": '{"after":"' + cursor + '","includeAdult":false,"isExactMatch":false,"locale":"en-GB","numResults":25,"searchTerm":"' + search_query + '","skipHasExact":true,"typeFilter":"TITLE"}',
        "extensions": '{"persistedQuery":{"sha256Hash":"b0d26e3b2d527e932ee754fb3fc10eadeac11289122a6846a910fb401f918131","version":1}}'
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "X-Imdb-Client-Name": "imdb-web-next",
        "X-Imdb-Client-Rid": "EMJM38N16GG5AB5NYRD3",
        "X-Imdb-User-Country": "GB",
        "X-Imdb-User-Language": "en-GB",
        "X-Imdb-Weblab-Treatment-Overrides": '{"IMDB_DESKTOP_SEARCH_ALGORITHM_UPDATES_577300":"T1","IMDB_NAV_PRO_FLY_OUT_Q1_REFRESH_848923":"T2"}'
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        logging.error("Error:", response.status_code)
        return None


def scrape_imdb(searchQuery,pagination):
    base_url = 'https://www.imdb.com'
    movies_data = []
    try:
        movieData = retrieve_movie_data(f'{base_url}/find/?q={searchQuery}&ref_=nv_sr_sm', 
            r'(?:<script id="__NEXT_DATA__" type="application\/json">)(.*?)(?=<\/script>)')

        titleResults = movieData['props']['pageProps']['titleResults']
        nextCursor = titleResults['nextCursor']

        if pagination>0:
            cacheData=[]
            for i in range(pagination):
                graphql_data = search_imdb_graphql(nextCursor, searchQuery)
                nextCursor = graphql_data['data']['results']['pageInfo']['endCursor']
                cacheData.append(graphql_data)
            for mds in cacheData:
                for md in mds['data']['results']['edges']:
                    entity = md['node']['entity']
                    if 'id' in entity and entity['id'] is not None:
                        dic = {
                        'id': entity['id'], 
                        'titleNameText': entity['originalTitleText']['text'], 
                        'titleReleaseText': str(entity['releaseYear']['year']) if entity['releaseYear'] is not None else ''
                        }
                        titleResults['results'].append(dic)

        for result in titleResults['results']:
            if 'id' in result and result['id'] is not None:
                movie_data = {}
                movieDetails = retrieve_movie_data(f'''{base_url}/title/{result['id']}/?ref_=fn_al_tt_1''', 
                    r'(?:<script type="application\/ld\+json">)(.*?)(?=<\/script>)')

                moviPloteDetails = retrieve_movie_data(f'''{base_url}/title/{result['id']}/plotsummary/?ref_=fn_al_tt_1''', 
                    r'(?:<script id="__NEXT_DATA__" type="application\/json">)(.*?)(?=<\/script>)')

                for movieBrief in moviPloteDetails['props']['pageProps']['contentData']['categories']:
                    if movieBrief['id'] == 'summaries':
                        movieSummary = ''
                        for movSum in movieBrief['section']['items']:
                            movieSummary = movieSummary+' '+movSum['htmlContent']

                movie_data['id'] = result['id']
                movie_data['type'] = movieDetails['@type'] if '@type' in movieDetails else ''
                movie_data['url'] = movieDetails['url'] if 'url' in movieDetails else ''
                movie_data['title'] = movieDetails['name'] if 'name' in movieDetails else ''
                movie_data['description'] = movieDetails['description'] if 'description' in movieDetails else ''
                movie_data['releaseDate'] = result['titleReleaseText'] if 'titleReleaseText' in result else ''
                movie_data['imdbRating'] = movieDetails['aggregateRating']['ratingValue'] if 'aggregateRating' in movieDetails else ''
                movie_data['cast'] = movieDetails['actor'] if 'actor' in movieDetails else []
                movie_data['director'] = movieDetails['director'] if 'director' in movieDetails else []
                movie_data['creator'] = movieDetails['creator'] if 'creator' in movieDetails else []
                movie_data['plotSummary'] = movieSummary
                movies_data.append(movie_data)
    except Exception as e:
        logging.error(f'Error scraping IMDb search results: {e}')
    return movies_data

def save_to_json(data, searchQuery):
    file_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], f'{searchQuery}_movies.json')
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    return file_path

def get_user_input():
    while True:
        search_query = input("Enter genre or keyword to search (press Enter to quit): ")
        if search_query:
            return search_query
        else:
            break

def get_pagination_input():
    while True:
        try:
            pagination = int(input("Enter maximum number of pages to scrape (0 to 25): "))
            if 0 <= pagination <= 25:
                return pagination
            else:
                print("Pagination must be a number between 0 and 25.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    searchQuery = get_user_input() # comedy
    pagination = get_pagination_input() # 1
    movies_data = scrape_imdb(searchQuery,pagination)
    if len(movies_data) > 0:
        file_path = save_to_json(movies_data,searchQuery)
        logging.info(f"Data saved to {file_path}")




