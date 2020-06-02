from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/history', methods=['POST'])
def button_click():
		# 클라이언트로부터 데이터를 받는 부분
    requester1_receive = request.form['requester1_give']
    requester2_receive = request.form['requester2_give']
    price_input_receive = request.form['price_input_give']
    price_output_receive = request.form['price_output_give']
    time_receive = request.form['time_give']

		# mongoDB에 넣는 부분
    doc = {'성': requester1_receive, 
    '이름': requester2_receive, 
    '입금액' : price_input_receive,
    '구매량' : price_output_receive,
    '구매시간' : time_receive} 

    db.history.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '잘 저장되었습니다.'})


@app.route('/history', methods=['GET'])
def history():
		# 1. 모든 reviews의 문서를 가져온 후 list로 변환합니다.
    histories = list(db.history.find({},{'_id':0}))
		# 2. 성공 메시지와 함께 리뷰를 보냅니다.
    return jsonify({'result': 'success', 'all_histories': histories})

@app.route('/read_history')
def read_history():
  return render_template('read_history.html')



if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)