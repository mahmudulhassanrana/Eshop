from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name="home"),
    path('register', views.register, name = 'register'),
    path('login', views.login, name = 'login'),
    path('logout', views.logout, name = 'logout')
    
    #path('search/', views.Search, name="search"),
]
