from django.urls import path
from main.views import *
urlpatterns = [
     path('',CustomeRegisterView.as_view(),name="register"),
    path('register/',CustomeRegisterView.as_view(),name="register"),
    path('car/',cars.as_view(),name="car"),
   
]