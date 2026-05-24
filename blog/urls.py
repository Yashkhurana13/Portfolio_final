from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_view, name='blog_home'),
    path('<slug:slug>/', views.blog_detail_view, name='blog_detail'),
]
