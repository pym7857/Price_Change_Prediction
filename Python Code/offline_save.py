import tensorflow as tf
import numpy as np
from pandas.io.parsers import read_csv

#model = tf.global_variables_initializer();

data = read_csv('price_data.csv', sep=',')

xy = np.array(data, dtype=np.float32)

# 5개의 변인을 입력 (평균온도,최저온도,최고온도,강수량,습도)
x_data = xy[:, 1:6]

# 실제 가격 값을 입력
y_data = xy[:, [-1]]

 
X = tf.placeholder(tf.float32, shape=[None, 5])         # x_data 담을 placeholder
Y = tf.placeholder(tf.float32, shape=[None, 1])         # y_data 담을 placeholder
W = tf.Variable(tf.random_normal([5, 1]), name="weight") # 5x1 행렬로 W 난수 생성
b = tf.Variable(tf.random_normal([1]), name="bias")      # 5x1 행렬로 b 난수 생성

# 가설
hypothesis = tf.matmul(X, W) + b

# (손실)비용 함수
cost = tf.reduce_mean(tf.square(hypothesis - Y)) # 제곱을 함으로써 페널티 증가시킴

# 최적화 함수를 설정
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.000005)
train = optimizer.minimize(cost)

# 세션 초기화
sess = tf.Session()

# 글로벌 변수를 초기화
sess.run(tf.global_variables_initializer())

# 학습을 수행
for step in range(100001): # 학습횟수
    cost_, hypo_, _ = sess.run([cost, hypothesis, train], feed_dict={X: x_data, Y: y_data})
    if step % 5000 == 0:
        print("#", step, " 손실 비용: ", cost_)
        print("당근(예측)가격: ", hypo_[0])

# 학습된 모델을 저장
saver = tf.train.Saver()
save_path = saver.save(sess, "../Flask Web Server/model/saved.cpkt")
print('학습된 모델을 저장했습니다.')