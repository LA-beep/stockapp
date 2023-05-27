import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import redirect, render
import yfinance
from stocks.static.arima import get_arima_prediction
from stocks.static.hotlwinters import get_holt_winters_prediction
from .models import Account
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import csv
from .static import *

# Create your views here.
def home(request):
    return redirect('/login/')

def user_signup(request):

    if request.method != "POST":
        return render(request,"signup.html")
    data = request.POST
    first_name =  data.get('first_name')
    last_name = data.get('last_name')
    username = data.get('username')
    password = data.get('password')

    user = User.objects.filter(username = username)
    if user.exists():
        messages.info(request,'Username already taken')
        return redirect('/signup/')
    
    user = User.objects.create(        
        first_name = first_name,
        last_name  = last_name,
        username   = username,
            )
            
    user.set_password(password)
    user.save()
    messages.info(request,'Account Created succesfully')
    return redirect('/signup/')

def user_login(request):
    if request.method != "POST":
        return render(request,"login.html")
    data = request.POST
    username = data.get('username')
    password = data.get('password')

    if User.objects.filter(username = username).exists():
        user = authenticate(username = username , password = password)
        if user is None:
            messages.info(request,'Invalid Password')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/pred/')

    messages.info(request,'Invalid Username')
    return redirect('/login/')

def user_logout(request ):
    logout(request)
    return redirect('/login/')

def resetpwd(request):
    if request.method != "POST":
        return render(request,"pwd-reset.html")
    data = request.POST
    username = data.get('username')
    password = data.get('password')

    if  User.objects.filter(username = username).exists():
        user = User.objects.get(username = username)
        user.set_password(password)
        user.save()
        messages.info(request,'Password reset succesfully')
        return redirect('/password-reset/')
    
    messages.info(request,'Invalid Username')
    return redirect('/password-reset/')

    

@login_required(login_url="/login/")
def pred(request):
    if request.method != "POST":
        queryset = Account.objects.filter(user= request.user)
        context = {'table_data':queryset}
        return render(request,"predinput.html",context)
    market = request.POST.get('market')
    ticker = request.POST.get('ticker')
    algorithm = request.POST.get('algorithm')

    timestamp=datetime.datetime.now()
    result =0
    if algorithm != 'Arima':
        result = get_holt_winters_prediction(ticker)
    else:
        result = get_arima_prediction(ticker)

    # Plot the time series and the predicted value
    data = yfinance.download(ticker, period='5y', interval='1d')
    dates = data.index
    close_prices = data['Close']

    plt.figure(figsize=(10, 6))
    plt.plot(dates, close_prices, label='Actual')
    plt.plot(dates[-1], result, marker='o', markersize=8, label='Prediction')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.title(f"{ticker} Stock Price Prediction")
    plt.legend()

    # Convert the plot to a base64-encoded image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')

    
    context = {
            'market': market,
            'ticker': ticker,
            'algorithm': algorithm,
            'result':result,
            'timestamp':timestamp,
            'plot_data':plot_data,
        }
    
    return render(request, 'predoutput.html', context)

@login_required(login_url="/login/")
def store_result(request):
    if request.method == "POST":
        # Extract the necessary data from the request
        user=request.user
        ticker = request.POST.get('ticker')
        algorithm = request.POST.get('algorithm')
        result = request.POST.get('result')
        timestamp = request.POST.get('timestamp')
        # Create a new prediction result for the user
        Account.objects.create(
            user = user,
            ticker=ticker,
            algorithm=algorithm,
            result=result,
            timestamp =timestamp
        )
        return redirect('/pred/')
    return redirect('/pred/')
    
        