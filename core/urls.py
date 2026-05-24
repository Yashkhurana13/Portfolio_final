from django.urls import path
from . import views

urlpatterns = [
    path('', views.portfolio_view, name='portfolio_home'),
    path('profile/update/', views.update_profile_view, name='update_profile'),
]
