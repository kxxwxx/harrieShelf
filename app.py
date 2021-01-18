from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.harrie


@app.route('/')
def get_profile_page():
    return render_template('profile.html')


@app.route('/write')
def get_form_page():
    login_user = request.args.get('login_user')
    user = login_user
    return render_template('form.html', user=user, login_user=login_user)


@app.route('/home')
def get_main_page():
    login_user = request.args.get('login_user')
    user = login_user
    return render_template('harrieShelf.html', user=user, login_user=login_user)


@app.route('/myshelf')
def get_myshelf_page():
    login_user = request.args.get('login_user')
    user = request.args.get('user')
    return render_template('myShelf.html', user=user, login_user=login_user)


@app.route('/reviews', methods=['POST'])
def write_review():
    user = request.form['user']
    type = request.form['type']
    title = request.form['title']
    author = request.form['author']
    url = request.form['url']
    memo = request.form['memo']
    like = int(request.form['like'])
    learn = int(request.form['learn'])
    angry = int(request.form['angry'])

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    image = ''
    if og_image is not None:
        image = og_image['content']

    review = {
        'user': user,
        'type': type,
        'title': title,
        'author': author,
        'url': url,
        'image': image,
        'memo': memo,
        'like': like,
        'learn': learn,
        'angry': angry
    }

    db.reviews.insert_one(review)
    return jsonify({'result': 'success', 'msg': '기록해주셔서 감사합니다!'})


@app.route('/reviews', methods=['GET'])
def read_reviews():
    # 1. DB에서 리뷰 정보 모두 가져오기
    user = request.args.get('user')
    reviews = list(db.reviews.find({'user': user}, {'_id': 0}))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'reviews': reviews})


@app.route('/types', methods=['GET'])
def read_articles():
    # 1. DB에서 리뷰 정보 모두 가져오기
    type = request.args.get('type')
    reviews = list(db.reviews.find({'type': type}, {'_id': 0}).limit(4))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'reviews': reviews})

@app.route('/api/like', methods=['POST'])
def like():
    title = request.form['title']
    book = db.reviews.find_one({'title': title})
    new_like = book['like'] + 1
    db.reviews.update_one({'title': title}, {'$set': {'like': new_like}})
    return jsonify({'result': 'success'})


@app.route('/api/learn', methods=['POST'])
def learn():
    title = request.form['title']
    book = db.reviews.find_one({'title': title})
    new_learn = book['learn'] + 1
    db.reviews.update_one({'title': title}, {'$set': {'learn': new_learn}})
    return jsonify({'result': 'success'})


@app.route('/api/angry', methods=['POST'])
def angry():
    title = request.form['title']
    book = db.reviews.find_one({'title': title})
    new_angry = book['angry'] + 1
    db.reviews.update_one({'title': title}, {'$set': {'angry': new_angry}})
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
