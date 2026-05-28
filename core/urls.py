from django.urls import path
from . import views

urlpatterns = [
    path('', views.portfolio_view, name='portfolio_home'),
    path('download-resume/', views.download_resume, name='download_resume'),
]
