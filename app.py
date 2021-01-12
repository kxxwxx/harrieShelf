from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.harrie


@app.route('/')
def get_form_page():
    return render_template('form.html')


@app.route('/write', methods=['POST'])
def write_review():
    # 1. 클라이언트가 준 user, type, title, author, url, sentence, memo 가져오기.
    user = request.form['user']
    type = request.form['type']
    title = request.form['title']
    author = request.form['author']
    url = request.form['url']
    sentence = request.form['sentence']
    memo = request.form['memo']

    # 2. DB에 정보 삽입하기
    review = {
        'user': user,
        'type': type,
        'title': title,
        'author': author,
        'url': url,
        'sentence': sentence,
        'memo': memo
    }

    db.reviews.insert_one(review)

    # 3. 성공 여부 & 성공 메시지 반환하기
    return jsonify({'result': 'success', 'msg': '기록해주셔서 감사합니다!'})


@app.route('/myshelf')
def get_myshelf_page():
    return render_template('myShelf.html')

@app.route('/profile')
def get_profile_page():
    return render_template('profile.html')


@app.route('/write', methods=['GET'])
def read_reviews():
    # 1. DB에서 리뷰 정보 모두 가져오기
    reviews = list(db.reviews.find({}, {'_id': 0}))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'reviews': reviews})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
