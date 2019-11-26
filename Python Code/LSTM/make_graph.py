import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#파일 읽어오기
p_data = pd.read_csv("./예측파일.csv")
t_data = pd.read_csv("./실제값.csv")
#price열 데이터 가지고 오기
p_prices = p_data['price'].values.astype(np.int64)
t_prices = t_data['price'].values.astype(np.int64)

#예측한 값 만큼만 실제 값에서 가지고 온다
predict_val = p_prices[:]
true_val = t_prices[-len(p_prices):]

#그래프 생성
fig = plt.figure(facecolor='white')
ax=fig.add_subplot(111)
ax.plot(true_val,label='True')
ax.plot(predict_val, 'red',label='Prediction')
ax.legend()
plt.show()