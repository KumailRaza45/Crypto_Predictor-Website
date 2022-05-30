from tensorflow import keras
import numpy as np
import datetime as dt
import pandas_datareader as web
from sklearn.preprocessing import MinMaxScaler

model = keras.models.load_model('BitCoin_01_day')

crypto_currency = 'BTC'
against_currency = 'USD'

prediction_days = 60

predict_start = dt.date(2022,1,31)
predict_end = dt.datetime.now()

data = web.DataReader(f'{crypto_currency}-{against_currency}','yahoo',predict_start,predict_end)
print(data.tail())
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data=scaler.fit_transform(data['Close'].values.reshape(-1,1))
real_data=[scaled_data[-60:,0]]
real_data=np.array(real_data)
real_data=np.reshape(real_data,(real_data.shape[0],real_data.shape[1],1))
prediction=model.predict(real_data)
prediction=np.reshape(prediction,(-1,1))
prediction=scaler.inverse_transform(prediction)
today_price=data['Close'].values.reshape(-1,1)[-1]
print("today: ",today_price)
print("predicted: ",prediction[-1])

