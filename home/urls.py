from django.urls import path

from . import views

app_name = "home"
urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit, name='submit'),
    path('result/', views.result, name='result'),
]