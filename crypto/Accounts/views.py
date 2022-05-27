from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .forms import LoginForm,RegisterForm
from django.contrib.auth.decorators import login_required
from .models import *
# Login function   
def Login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/crypto/home")
    Response=""
    if request.method == 'POST':
        PostData=request.POST.copy()
        print(PostData)
        user=authenticate(request,username=PostData['username'],password=PostData['pass'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/crypto/home/")
        else:
            Response="Email and Password did not match!"
    context={"LoginForm":LoginForm,"ShowResponse":Response}
    return render(request,"login.html",context)

#Logout function
def Logout(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login/")

#Register function
def Register(request):
    Message=""
    if request.method == 'POST':
        PostData=request.POST.copy()
        _username=PostData['username']
        email=PostData['email']
        password=PostData['password']
        confirmPassword=PostData['confirmpassword']
        try:
            pUser=User.objects.get(username=_username)
            Message='User Already Registered'
        except:
            if(password == confirmPassword ):
                print("password match")
                user=User.objects.create_user(_username,email,password)
                user.save()
                return HttpResponseRedirect('/accounts/success/')
            else : Message="Passwords did not match try again"
    context={"RegisterForm":RegisterForm,"Message":Message}
    return render(request,"register.html",context)

#Success Message
def Success(request):
    return render(request,"registered_successful.html")

