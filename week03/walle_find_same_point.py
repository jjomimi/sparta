import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta

wall_e = db.movies.find_one({'title':'월-E'})

same_point_movies = list(db.movies.find( #list로 항상 감싸줘야 함
    {'point':wall_e['point']}
))
print(same_point_movies)

for movie in same_point_movies:
    print(movie['title'])