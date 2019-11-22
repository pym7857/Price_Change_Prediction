from flask import Flask, render_template, request

import tensorflow as tf
import numpy as np
from pandas.io.parsers import read_csv

app = Flask(__name__)

X = tf.compat.v1.placeholder(tf.float32, shape=[None, 5])
Y = tf.compat.v1.placeholder(tf.float32, shape=[None, 1])
W = tf.Variable(tf.random.normal([5, 1]), name="weight")
b = tf.Variable(tf.random.normal([1]), name="bias")

hypothesis = tf.matmul(X, W) + b

# 저장된 학습모델 불러오기 위한 초기화
saver = tf.compat.v1.train.Saver()
model = tf.compat.v1.global_variables_initializer()
sess = tf.compat.v1.Session()
sess.run(model)

save_path = "model/saved.cpkt"
saver.restore(sess, save_path)      # 해당 세션에 저장된 학습모델을 불러온다.

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
      return render_template('index.html')
    if request.method == 'POST':
        avg_temp = float(request.form['avg_temp'])
        min_temp = float(request.form['min_temp'])
        max_temp = float(request.form['max_temp'])
        rain_fall = float(request.form['rain_fall'])
        moist = float(request.form['moist'])
        user_date = str(request.form['user_date']) # 날짜

    # ---------------- LSTM 예측가격 처리부분 ----------------
    data = read_csv('test.csv', sep=',')  # 토큰 = ','
    xy = np.array(data)  # xy 변수에 2차원 배열 행렬 형태로 해당 데이터를 담는다.
    x_data = xy[:, 0]  # 첫번째 열 (날짜 배열)
    y_data = xy[:, 1]  # 두번째 열 (가격 배열)

    index = -1
    for i in range(len(x_data)):
        if user_date == x_data[i]:
            index = i
            break
    print(index)
    if index == -1:
        res = 'None'
    else:
        res = float(y_data[index])

    # ---------------- 텐서플로우 예측가격 처리부분 ----------------
    data = ((avg_temp, min_temp, max_temp, rain_fall, moist),)
    arr = np.array(data, dtype=np.float32)

    x_data = arr[0: 5]
    dict = sess.run(hypothesis, feed_dict={X: x_data})

    price = dict[0]
    return render_template('index.html', price=price, res=res)

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host = '0.0.0.0')