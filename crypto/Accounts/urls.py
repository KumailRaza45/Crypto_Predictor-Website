from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.Login,name='login_Page'),
    path('logout/',views.Logout,name='logout'),
    path('register/',views.Register,name='Register_page'),
    path('success/',views.Success,name='Sucess_page'),
    
]
