from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home_page'),
    path('sentiments', views.sentiments, name='sentiments'),
    path('checkform', views.checkForm, name='checkform'),
]
