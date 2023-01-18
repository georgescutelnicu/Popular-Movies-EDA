
import datetime
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re

pages = np.arange(1, 100, 50)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:96.0) Gecko/20100101 Firefox/96.0'}
current_year = datetime.datetime.now().year
imdb_year_interval = [f'{current_year - i-1}-01-01,{current_year - i-1}-12-31' for i in range(20)]

title = []
rating = []
year = []
month = []
certificate = []
runtime = []
directors = []
stars = []
genre = []
location = []
budget = []
income = []
country_of_origin = []


for interval in imdb_year_interval:

  print(f'\n{interval}')

  for page in pages:

    response = requests.get(f'https://www.imdb.com/search/title/?title_type=feature&year={interval}&start={page}&ref_=adv_nxt')
    soup = BeautifulSoup(response.text, 'html.parser')
    movies = soup.find_all(name='div', class_='lister-item mode-advanced')

    i=0
    print(f'\nPage number: {np.where(pages == page)[0].item() + 1}\n')

    for movie in movies:

      time.sleep(np.random.randint(1, 4))

      movie_title = movie.select_one('.lister-item-header a').text.strip()

      try:
        movie_rating = float(movie.select_one('.ratings-imdb-rating').text.strip())
      except:
        movie_rating = None
      
      try:
        movie_year = ''.join(re.findall(r'\d+', movie.select_one('.lister-item-year').text))
      except:
        movie_year = interval.split('-')[0]

      try:
        movie_runtime = movie.select_one('.runtime').text.split(' ')[0]
      except:
        movie_runtime = 'Unknown'

      try:
        movie_certificate = movie.select_one('.certificate').text
      except:
        movie_certificate = None
      
      try:
        movie_genre = movie.select_one('.genre').text.strip()
      except:
        movie_genre = 'Unknown'

      try:
        director_and_stars = [x.text.strip() for x in movie.select('.lister-item-content p')[2:3]]
        director_and_stars = ''.join([re.sub('[^a-zA-Z0-9,:]+', ' ', _) for _ in director_and_stars])
        movie_director = director_and_stars[director_and_stars.index(':'): director_and_stars.index(' Stars')].split(': ')[1]
        movie_stars = director_and_stars[director_and_stars.index('Stars:'):].split(': ')[1]
      except:
        movie_director = 'Unknown'
        movie_stars = 'Unknown'

      movie_link = movie.select_one('.lister-item-header a')['href']
      response = requests.get(f'https://www.imdb.com{movie_link}', headers=headers)
      soup = BeautifulSoup(response.text, 'html.parser')

      try:
        movie_month = soup.select('.ipc-inline-list__item a[href*="releaseinfo"]')[1].text
        movie_month = movie_month.split(' ')[0]
      except:
        movie_month = 'Unknown'

      try:
        movie_location = soup.select_one('.ipc-inline-list a[href*="location"]').text
        movie_location = movie_location.split(', ')[-1]
      except:
        movie_location = 'Unknown'

      try:
        movie_budget = soup.find('li', attrs={'data-testid': 'title-boxoffice-budget'}).select_one('label').text
        movie_budget = movie_budget.split(' ')[0]
      except:
        movie_budget = 'Unknown'

      try:
        movie_income = soup.find('li', attrs={'data-testid': 'title-boxoffice-cumulativeworldwidegross'}).select_one('label').text
        movie_income = movie_income.split(' ')[0]
      except:
        movie_income = 'Unknown'
      
      try:
        movie_country = [x.text for x in soup.select('a[href*="country_of_origin"]')]
        movie_country = ', '.join(movie_country)
      except:
        movie_country = 'Unknown'

      title.append(movie_title)
      rating.append(movie_rating)
      year.append(movie_year)
      month.append(movie_month)
      runtime.append(movie_runtime)
      certificate.append(movie_certificate)
      directors.append(movie_director)
      stars.append(movie_stars)
      genre.append(movie_genre)
      location.append(movie_location)
      budget.append(movie_budget)
      income.append(movie_income)
      country_of_origin.append(movie_country)
      

      print(f'Movie number: {page + i}')
      i+=1

df_dict = {'Title': title,
           'Rating': rating,
           'Year': year,
           'Month': month,
           'Certificate': certificate,
           'Runtime': runtime,
           'Directors': directors,
           'Stars': stars,
           'Genre': genre,
           'Filming_location': location,
           'Budget': budget,
           'Income': income,
           'Country_of_origin': country_of_origin
            }

df = pd.DataFrame(df_dict)

from google.colab import files
df.to_csv('movies.csv', index = False, encoding = 'utf-8-sig') 
files.download('movies.csv')
