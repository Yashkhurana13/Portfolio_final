from django.urls import path
from . import views

urlpatterns = [
    path('', views.portfolio_view, name='portfolio_home'),
    path('download-resume/', views.download_resume, name='download_resume'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
]
