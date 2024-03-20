import os
import unittest
from imdb_scraper import scrape_imdb, save_to_json

class TestIMDBScraper(unittest.TestCase):
    def test_scrape_imdb(self):
        search_query = "comedy"
        pagination = 1
        movies_data = scrape_imdb(search_query, pagination)
        self.assertTrue(len(movies_data) > 0)

    def test_save_to_json(self):
        data = [{'id': 'tt1234567', 'title': 'Test Movie', 'description': 'A test movie', 'imdbRating': '8.0'}]
        search_query = "test"
        file_path = save_to_json(data, search_query)
        self.assertTrue(file_path.endswith('.json'))
        os.remove(file_path)

if __name__ == '__main__':
    unittest.main()
