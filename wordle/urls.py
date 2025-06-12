from django.urls import path
from . import views

app_name = 'wordle'

urlpatterns = [
    path('', views.home, name='home'),
    path('study/', views.study, name='study'),
    path('quiz/', views.quiz, name='quiz'),
]