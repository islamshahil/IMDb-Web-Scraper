# IMDb Movie Scraper

The IMDb Movie Scraper is a Python script that allows users to scrape movie data from IMDb based on a given search query. It retrieves detailed information about movies such as plot summary, ratings, cast, release date, etc., and saves the results to a JSON file for further analysis or usage.

## Installation and Dependencies

To run the IMDb Movie Scraper, you need Python installed on your system. Additionally, you need to install the required dependencies using pip. Run the following command to install the dependencies:

```bash
pip install requests
```


## How to Run the Scraper

1. Clone the repository or download the `imdb_movie_scraper.py` file to your local machine.

2. Open a terminal or command prompt and navigate to the directory containing `imdb_movie_scraper.py`.

3. Run the script by executing the following command:

```bash
python imdb_movie_scraper.py
```


4. Follow the prompts:
   - Enter a genre or keyword to search for movies on IMDb.
   - Enter the maximum number of pages to scrape (0 to 25).

5. The script will start scraping IMDb based on your input. Once the scraping is complete, it will save the scraped movie data to a JSON file.

## Additional Information

- **Pagination**: You can specify the maximum number of pages to scrape. IMDb limits the number of results per page, and each page contains a maximum of 25 results. Therefore, pagination allows you to retrieve more search results.

- **Logging**: The scraper logs information about the scraping process, including errors, to a file named `scraper.log`. You can refer to this log file for troubleshooting or debugging purposes.

- **Output Format**: The scraped movie data is saved to a JSON file with a filename based on the search query. Each movie's details are stored in JSON format, making it easy to parse and analyze the data programmatically.

- **Contributing**: Contributions to the IMDb Movie Scraper project are welcome. If you encounter any issues, have suggestions for improvements, or want to add new features, feel free to open an issue or submit a pull request on GitHub.

- **Disclaimer**: This script is intended for educational and personal use only. Use it responsibly and ensure compliance with IMDb's terms of service and data usage policies.
