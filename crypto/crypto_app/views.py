from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tensorflow import keras
from .models import *
import numpy as np
import datetime as dt
from django.utils import timezone
import pandas_datareader as web
from sklearn.preprocessing import MinMaxScaler


# Home Page
def Home(request):
    context={'UserInfo':UserInfo(request)}
    return render(request,'home.html',context)

# How To Page
def HowTo(request):
    context={'UserInfo':UserInfo(request)}
    return render(request,'HowTo.html',context)

@login_required
# Blog Page
def BlogFunc(request):
    _Blog=Blog.objects.all()
    context={'Blog':_Blog,'UserInfo':UserInfo(request)}
    return render(request,'blog.html',context)

@login_required
# Blog Single Page
def BlogSingle(request):
    _id=request.GET.get('q','')
    _Blog=Blog.objects.get(id=_id)
    context={'blog':_Blog,'UserInfo':UserInfo(request)}
    return render(request,'single_blog.html',context)

# Home Page
def About(request):
    context={'UserInfo':UserInfo(request)}
    return render(request,'about.html',context)

# Contact Page
def Contact(request):
    context={'UserInfo':UserInfo(request)}
    return render(request,'contact.html',context)

@login_required
# Contact Page
def Predictor(request):
    if request.method == 'POST':
        PostData=request.POST.copy()
        print(PostData)
        Currency=''
        Day=''
        for data in PostData:
            if(data=="eth"):
                print("its ETH")
                Currency='ETH'
            elif(data=="lite"):
                print("its Lite")
                Currency='LTC'
            elif(data=="doge"):
                print("its Doge")
                Currency='DOGE'
            elif(data=="bit"):
                print("its bit")
                Currency='BTC'
            if(data=="01"):
                print("Day 01")
                Day='_01_'
            elif(data=="07"):
                print("Day 07")
                Day='_07_'
            elif(data=="15"):
                print("Day 15")
                Day='_15_'
        profit,value,DATA=CryptoPredict(Currency,Day)
        addHistory(request.user,"Predicted value of "+Currency+" to be "+str(value[0]))
        context={'Profit':profit,'Predicted':value[0],'Show':True,"Currency":Currency,"Day":Day[1:3],'UserInfo':UserInfo(request),'VAL':DATA['Close'],'Date':DATA.index.to_list()}
        return render(request,'predictor.html',context)
    context={'UserInfo':UserInfo(request)}
    return render(request,'predictor.html',context)


def CryptoPredict(currency,day):
        model = keras.models.load_model(currency+day+'day')
        crypto_currency = currency
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
        profit=False
        if prediction[-1]>today_price:
            profit=True
        return profit,prediction[-1],data[-30:]


def UserInfo(request):
    if request.user.is_authenticated:
        return 'logout ' #+ str(request.user)
    else:
        return 'Login'

#Add History
def addHistory(user,task):
    DB=History()
    DB.user=user
    DB.task=task
    DB.date=timezone.now()
    DB.save()


#History
@login_required
def HistoryFunc(request):
    history=History.objects.filter(user=request.user).order_by('-date') 
    context={'Data':history,'UserInfo':UserInfo(request)}
    return render(request, 'history.html',context)

#Graph
def graph(request):
    crypto_currency = 'BTC'
    against_currency = 'USD'
    predict_start = dt.date(2022,1,31)
    predict_end = dt.datetime.now()
    data = web.DataReader(f'{crypto_currency}-{against_currency}','yahoo',predict_start,predict_end)[-30:]
    crypto_currency = 'LTC'
    dataLite = web.DataReader(f'{crypto_currency}-{against_currency}','yahoo',predict_start,predict_end)[-30:]
    crypto_currency = 'ETH'
    dataETH = web.DataReader(f'{crypto_currency}-{against_currency}','yahoo',predict_start,predict_end)[-30:]
    crypto_currency = 'DOGE'
    dataDOGE = web.DataReader(f'{crypto_currency}-{against_currency}','yahoo',predict_start,predict_end)[-30:]
    context={'Date':data.index.to_list()[-30:],'Value':data['Close'],'ValLite':dataLite['Close'],'ValETH':dataETH['Close'],'ValDOGE':dataDOGE['Close'],'UserInfo':UserInfo(request)}
    return render(request,'graphs.html',context)