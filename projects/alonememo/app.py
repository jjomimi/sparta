from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/memo', methods=['POST'])
def post_article():

    url = request.form['url']
    comment = request.form['comment']


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    url_image = og_image['content']
    url_title = og_title['content']
    url_description = og_description['content']

    print(url,comment, url_image, url_title, url_description)
    db.reviews.insert_one({
       'url':url,
       'title':url_title,
       'image':url_image,
       'description':url_description,
       'comment':comment
    })


    return jsonify({'result': 'success', 'msg': 'POST 연결되었습니다!'})



@app.route('/memo', methods=['GET'])
def read_articles():
    memos = list(db.reviews.find({}, {'_id': False}))
    print(memos)
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)
    # 2. articles라는 키 값으로 articles 정보 보내주기
    return jsonify({'result': 'success', 'msg': memos})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)