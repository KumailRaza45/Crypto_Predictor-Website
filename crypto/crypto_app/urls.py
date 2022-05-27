from django.urls import path
from . import views
urlpatterns = [
    path('home/',views.Home,name='Home_Page'),
    path('blog/',views.BlogFunc,name='Blog_Page'),
    path('about/',views.About,name='About_Page'),
    path('contact/',views.Contact,name='Contact_Page'),
    path('predictor/',views.Predictor,name='Predictor_Page'),
    path('singleblog/',views.BlogSingle,name='Single_Blog'),
    path('howto/',views.HowTo,name='How_To_Use'),
    path('history/',views.HistoryFunc,name='History_Func'),
    path('statics/',views.graph,name='Graph_Page'),
]
