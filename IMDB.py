# -*- coding:utf-8 -*-
#Author:shenshi
#date:2018/5/29 10:04
import re
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
def get_top250_movies_list():
    url = "http://www.imdb.com/chart/top"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            movies = soup.select('tbody tr')
            for movie in movies:
                poster = movie.select_one('.posterColumn')
                score = poster.select_one('span[name="ir"]')['data-value']
                movie_link = movie.select_one('.titleColumn').select_one('a')['href']
                year_str = movie.select_one('.titleColumn').select_one('span').get_text()
                year_pattern = re.compile('\d{4}')
                year = int(year_pattern.search(year_str).group())
                id_pattern = re.compile(r'(?<=tt)\d+(?=/?)')
                movie_id = int(id_pattern.search(movie_link).group())
                movie_name = movie.select_one('.titleColumn').select_one('a').string

                lst= '''
                '电影ID': %s,
                '电影名字': %s,
                '上映年份': %s,
                '链接': https://www.imdb.com%s,
                '电影评分': %s
                    '''%(movie_id,movie_name,year,movie_link,float(score))

                print(lst)
        else:
            print("URL错误")
    except RequestException:
        print("请求失败")
        return None
get_top250_movies_list()
