import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import optimizers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense, Activation
from tensorflow.keras.layers import Bidirectional
from sklearn.metrics import accuracy_score

#학습 전 데이터 정규화
def normalization(x):
    result = x
    normalized_data = []

    #정규화 식 = (target / 윈도우의 첫번째 값) - 1
    #-1 ~ 1 사이의 값으로 정규화 된다
    for window in result:
        normalized_window = [((float(p) / float(window[0])) - 1) for p in window]
        normalized_data.append(normalized_window)

    return normalized_data

#학습 후 csv 파일에 저장 전에 데이터를 다시 역정규화 해준다
def denormalization(x,result):
    val = (x+1)*(result[-1,-1])
    return val

#학습
def train(prices):
    #활성함수, 손실함수, 시퀀스 길이 미리 정의
    act = 'tanh'
    loss_function = 'mse'
    seq_len = 45
    sequence_length = seq_len + 1
    result = []
    pred_val = []

    #데이터를 시퀀스 길이만큼 윈도우로 나누어 준다
    for index in range(len(prices) - sequence_length):
        result.append(prices[index: index + sequence_length])

    #데이터 정규화
    temp_result = np.array(result)
    normalized_data = normalization(result)
    result = np.array(normalized_data)

    #데이터의 90%는 train_set 10%는 test_set
    row = int(round(result.shape[0] * 0.9))

    train = result[:row, :]
    np.random.shuffle(train)

    #train,test_set 을 학습하기 적합한 구조로 reshape
    pre_train = train[:, :-1]
    pre_train = np.reshape(pre_train, (pre_train.shape[0], pre_train.shape[1], 1))
    result_train = train[:, -1:]

    pre_test = result[row:, :-1]
    pre_test = np.reshape(pre_test, (pre_test.shape[0], pre_test.shape[1], 1))
    result_test = result[row:, -1:]

    #모델구성하기
    #과적합을 방지하기 위해 중간에 Dropout 추가
    #learning rate를 0.005로 설정
    model = Sequential()
    model.add(LSTM(30, input_shape=(seq_len, 1), return_sequences=True))
    model.add(Dropout(0.25))
    model.add(LSTM(30, return_sequences=True))
    model.add(LSTM(30, return_sequences=True))
    model.add(Dropout(0.25))
    model.add(LSTM(20, return_sequences=True))
    model.add(LSTM(20, return_sequences=True))
    model.add(Dropout(0.25))
    model.add(LSTM(20, return_sequences=True))
    model.add(LSTM(20, return_sequences=True))
    model.add(Dropout(0.25))
    model.add(LSTM(30, return_sequences=False))
    model.add(Dense(1))
    model.add(Activation(act))
    adam = optimizers.Adam(lr=0.0005)
    model.compile(loss=loss_function, optimizer=adam, metrics=['accuracy'])

    #학습
    model.fit(pre_train, result_train, batch_size=256, epochs=10)

    #pred = 예측 결과
    pred = model.predict(pre_test)
    trre = np.argmax(result_test, axis=1)
    print("학습 정확도 : " + str(accuracy_score(pred.round(), trre)))

    #학습결과를 역정규화로 pred_val에 저장
    for i in range(len(pred)):
        pred_val.append(int(np.around(denormalization(pred[i], temp_result))))

    return pred_val

#실제 데이터 읽어오기
data = pd.read_csv("./결과파일.csv")
prices = data['price'].values.astype(np.int64)
#학습 진행 횟수
count = 1

for i in range(count):
    print("=========================================================")
    print('training  #' + str(i + 1) + '...')
    print("=========================================================")
    val = train(prices[i:])

    #첫번째 학습에서는 파일을 새로 작성
    #두번째 학습에서는 뒤에 붙여넣기
    if i == 0:
        pred_file = open("예측파일.csv", 'w')
        np.savetxt(pred_file, val, delimiter=",")
        pred_file.close()
    else:
        pred_file = open("예측파일.csv", 'a')
        np.savetxt(pred_file, val, delimiter=",")
        pred_file.close()

    #price 에 학습결과를 붙여넣는다.
    prices = np.append(prices, val[-1])

result_val = prices[-count:]

csv_file = open("결과파일.csv", 'a')
np.savetxt(csv_file, result_val, delimiter=",")
csv_file.close()