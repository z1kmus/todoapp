from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('click/<str:pk>/', views.click, name='click'),
    path('mode/', views.mode, name='mode'),
    path('create/', views.create, name='create'),
    path('update/<str:pk>/', views.edit, name='update'),
    path('delete/<str:pk>/', views.delete, name='delete'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('signup/', views.registerPage, name='signup'),
]