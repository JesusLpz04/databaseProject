from django.urls import path
from . import views

urlpatterns = [

    path('',views.home, name=""),
    path('register', views.register, name="register"),
    path('login', views.my_login, name="login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('logout', views.logout, name="logout"),
    path('create_post', views.create_post, name="create_post"),
    path('comment/<int:pk>/', views.comment, name="comment"),
    path('friends', views.friends, name="friends"),
    path('messages/<int:pk>/', views.messages, name="messages"),
]