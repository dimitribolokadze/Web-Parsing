import requests
from bs4 import BeautifulSoup
import csv
import time


def scrape_movie_ratings():
    base_url = 'https://www.imdb.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    movie_data = []

    for page in range(1, 6):
        url = f'{base_url}/chart/top?sort=rk,asc&mode=simple&page={page}'

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        movie_items = soup.find_all('td', class_='titleColumn')

        for item in movie_items:
            title = item.find('a').text.strip()
            rating = item.find_next_sibling(
                'td', class_='ratingColumn').find('strong').text.strip()

            movie_data.append({'Title': title, 'Rating': rating})

        print(f'Scraped page {page}')

        # დაყოვნება
        time.sleep(15)

    # დატას შენახვა cvs
    with open('movie_ratings.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['Title', 'Rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(movie_data)

    print('Scraping complete!')


# ფუნქციის გამოძახება
scrape_movie_ratings()
