from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

## URL 별로 함수명이 같거나,
## route('/') 등의 주소가 같으면 안됩니다.
client = MongoClient('localhost', 27017)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/restaurant/list', methods=["GET"])
def get_vegan():
    type = request.args.get('type')
    vegan_list = list(db.vegan.find({'type': type}, {'_id': False}))
    print(list(db.vegan.find({}, {'_id': False})))

    return jsonify({'result': 'success', 'vegan_list': vegan_list})


if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)